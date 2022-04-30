var msg_small = document.getElementById('msg-small');
var nav_status = document.getElementById('nav-status');

var accordion = document.getElementById('accordion');

var edtcodigo = document.getElementById('edtcodigo-track');
var edtdescricao = document.getElementById('edtdescricao-track');

$().ready(function() {
    search_track_pessoa(idpessoa,'W','P');
});

async function search_track_pessoa(idpessoa,status,statusbtn){
    let totped = 0;
    let totent = 0;
    let totn = 0;
    try{
        msg_small.classList.remove('alert-danger');
        msg_small.classList.remove('d-none');
        msg_small.innerHTML = '<div class="spinner-border text-warning" role="status">'+
                        '<span class="sr-only">Loading...</span></div><label class="text-warning ml-2"><strong>'+
                        'Carregando Rastreios...</strong></label>';

        url = '/get/package/track/'+idpessoa+'/'+status;
        let response = await fetch(url);

        if (response.status == 200) {
            datajson = await response.json();
            if (datajson.result){
                packs_track = datajson.data;
                if(packs_track.length>0){
                    let strcard = '';
                    packs_track.forEach((pack) => {

                        switch(pack.status) {
                            case 'P':
                                totped += 1;
                                descstatus = 'Pendente';
                                break;
                            case 'E':
                                totent += 1;
                                descstatus = 'Entregue';
                                break;
                            case 'N':
                                totn += 1;
                                descstatus = 'Não Encontrado';
                                break;
                            default:
                                totped += 1;
                                descstatus = 'Pendente';
                        }
                        if (pack.status == statusbtn){
                            strcard += '<div class="card bg-dark mb-1">';
                            strcard +='<div class="card-header bg-warning d-flex justify-content-between" id="heading_'+pack.codigo+'">';
                            strcard +='<div><h5 class="mb-0">';
                            packjson = JSON.stringify(pack);
                            console.log(packjson);
                            strcard +="<button class='btn btn-dark' onclick='btn_click_codtrack("+packjson+");' data-toggle='collapse' "+
                            "data-target='#collapse_"+pack.codigo+"'" +
                            "aria-expanded='true' aria-controls='collapse_"+pack.codigo+"'>";


                            strcard += pack.codigo + ' - '+ pack.descricao ;
                            strcard +="</button></h5><small class='text-dark'>"+descstatus+"</small></div>"+
                            "<button class='btn btn-dark' data-toggle='modal' data-target='#insert-edit-modal-track' "+
                            "onclick='alterartrack("+packjson+");'>"+
                            "<span class='glyphicon glyphicon-pencil'></span></button></div>";
                            strcard +='<div id="collapse_'+pack.codigo+'" class="collapse" '+
                            'aria-labelledby="heading_'+pack.codigo+'" data-parent="#accordion">';
                            strcard +='<div id="card-body-'+pack.codigo+'" class="card-body border border-warning">';
                            strcard +='</div></div></div>';
                        }
                    });
                    msg_small.classList.add('d-none');
                    msg_small.classList.add('alert-danger');
                    msg_small.innerHTML = '';
                    accordion.classList.remove('d-none');
                    accordion.innerHTML = strcard;
                }
                else{
                    console.log('Aqui Zerado');
                    nav_status.classList.add('d-none');
                    msg_small.classList.remove('d-none');
                    msg_small.innerHTML = '<p class="text-center text-danger">Nenhum código de rastreio cadastrado.</p>'+
                    '<p class="text-center text-danger"> Clique no botão(+) para cadastrar</p>';
                }
            }
        }
        document.getElementById('btn-track-pendentes').innerHTML = 'Pendentes'+
        ' <span class="badge badge-light">'+totped+'</span>';
        document.getElementById('btn-track-entregues').innerHTML = 'Entregues'+
        ' <span class="badge badge-ligth">'+totent+'</span>';
        document.getElementById('btn-track-nao-encontrado').innerHTML = 'Não Encontrados'+
        ' <span class="badge badge-ligth">'+totn+'</span>';

    }catch(err){

    }
}

function btn_click_codtrack(pack){
    card_body = document.getElementById('card-body-'+pack.codigo);
    capture_pack(pack,card_body);
}

async function capture_pack(pack,card_body){
    card_body.innerHTML = '<div class="spinner-border text-warning" role="status">'+
    '<span class="sr-only">Loading...</span></div><label class="text-warning ml-2"><strong>'+
    'Buscando Dados. Atualizando Informação, aguarde...</strong></label>';
    let formData = new FormData();
    formData.append('codigo',pack.codigo);
    url = '/get/tracker/correios';
    var mybody = {method:'POST', body:formData };
    let response = await fetch(url,mybody);
    if (response.status == 200) {

        let status = 'A';
        let strcard = '';
        await response.json().then(data =>{
           console.log(data);
           tot = data.tot;
           data = data.data;
           console.log(data);
            if (tot==1){
                try
                {
                    if (pack.status == 'N'){

                        status = 'A';
                        strcard +='<dl><dt><label class="text-warning">'+data[0]+'</label></dt></dl>';
                    }
                    else{
                        strcard +='<dl>';
                        for(let i=0; i<=tot-1; i++){
                            json = data[i];
                            date_tr = json[1].slice(0,10);
                            time_tr = json[1].slice(13,18);
                            city_tr = json[1].slice(22,json[1].length-1);

                            rowtwo = json[2].replace('     ',' ');

                            strcard +='<dt><label class="text-warning">' +
                            date_tr + ' - ' +
                            time_tr + ' - ' +
                            city_tr + '</label>';

                            strcard += '</dt><dd><label class="text-white">'+rowtwo+'</label>';
                            strcard +='</dd>';

                            strcard +='<hr class="solid">';

                        }
                        strcard +='</dl>';
                    }
                }
                catch(e){

                    status = 'A';
                    strcard +='<dl><dt><label class="text-warning">'+data[0]+'</label></dt></dl>';
                }
                // Não localizada ou código inválido
            }
            else{
                strcard +='<dl>';
                for(let i=0; i<=tot-1; i++){
                    json = data[i];
                    date_tr = json[1].slice(0,10);
                    time_tr = json[1].slice(13,18);
                    city_tr = json[1].slice(22,json[1].length-1);
                    rowtwo = json[2].replace('     ',' ');

                    strcard +='<dt><label class="text-warning">' +
                    date_tr + ' - ' +
                    time_tr + ' - ' +
                    city_tr + '</label>';

                    strcard += '</dt><dd><label class="text-white">'+rowtwo+'</label>';
                    strcard +='</dd>';

                    strcard +='<hr class="solid">';

                }
                strcard +='</dl>';
            }
        });
        card_body.innerHTML = strcard;

    }
}


function validabuttonactive(btns,btnclicked,nameclass){
     btns.forEach((btn) => {
        console.log(btn)
        document.getElementById(btn).classList.remove(nameclass);
     });
     btnclicked.classList.add(nameclass);

}


function search_track(btn,status){
    accordion.innerHTML = '';
    validabuttonactive(['btn-track-pendentes','btn-track-entregues','btn-track-nao-encontrado'],btn,'active');


    search_track_pessoa(idpessoa,'W',status);
}


function alterartrack(pack){
    edtcodigo.value = pack.codigo;
    edtdescricao.value = pack.descricao;
    document.getElementById('edtidpacktracker').value = pack.codigo;
}

async function gravartrack(){

    small_descricao = document.getElementById('small-descricao');
    small_codigo = document.getElementById('small-codigo');

    small_codigo.classList.add('d-none');
    small_descricao.classList.add('d-none');

    if (edtcodigo.value == ''){
        small_codigo.classList.remove('d-none');
    }
    else if(edtdescricao.value == ''){
        small_descricao.classList.remove('d-none');
    }
    else{
        form = document.getElementById('formtrack')

        let formData = new FormData(form);
        formData.append('edtstatus','A');
        url = '/post/package/track';
        alert_dadostrack = document.getElementById('alert-dadostrack');
        alert_dadostrack.classList.remove('d-none');
        alert_dadostrack.innerHTML = '<div class="spinner-border text-warning" role="status">'+
        '<span class="sr-only">Loading...</span></div><label class="text-warning ml-2"><strong>'+
        'Salvando Dados aguarde...</strong></label>';

        var mybody = {method:'POST', body:formData };
        let response = await fetch(url,mybody);
        if (response.status == 200) {
            jsondata = await response.json();
            alert_dadostrack.innerHTML = jsondata.mensagem;
            if (jsondata.result){
                alert_dadostrack.classList.add('alert-primary');
            }
            else{
                alert_dadostrack.classList.add('alert-danger');
            }
            setTimeout(function(){
                    window.location.reload(true);
            }, 3000);
        }

    }

}


// BOTÃO PESQUISA RASTREIO NO SITE DOS CORREIOS, PAGINA: layout/search_track_correios
function btn_tracker_correios(codigo){
    pack = {'codigo': codigo}
    div_tracker = document.getElementById('div-tracker-correios');
    capture_pack(pack,div_tracker);
}

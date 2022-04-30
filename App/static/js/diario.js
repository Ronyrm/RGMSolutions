var dataprev = '';
var datanext = '';
var databr = '';
var dt = '';
var dieta = [];
var foodselect = {};
var accordion_refeicoes = document.getElementById('accordion-refeicoes');
var edtdescfood = document.getElementById('edtdescfood');
var edtidrefeicao = document.getElementById('edtidrefeicao');
var edtidalimento = document.getElementById('edtidalimento');
var edtqtd = document.getElementById('edtqtd');
var divpaginationfoods = document.getElementById('div-pagination-foods');
var divfoods = document.getElementById('div-foods');
var frmgroupqtd = document.getElementById('frmgroup-qtd');
var smalldescricao = document.getElementById('smalldescricao');
var divtabledadosnutri = document.getElementById('div-table-dadosnutri');
var edtiditem = document.getElementById('edtiditem');
var bodypdf = '';
function carrega_refeicoes(refeicoes,dataatual){
    card_refeicoes = '';
    refeicoes.forEach((refeicao) => {

        if (refeicao.mostrar == 'S'){

            card_refeicoes +='<div class="card bg-warning my-1">';
            card_refeicoes +='<div class="card-header d-flex justify-content-between" id="heading'+refeicao.id+'">';
            card_refeicoes +='<button id="btnrefeicao'+refeicao.id+'" class="btn btn-dark text-warning"'+
            ' data-toggle="collapse" data-target="#collapse'+refeicao.id+
            '" aria-expanded="true" aria-controls="collapse'+refeicao.id+'">'
            +refeicao.descricao+' - '+refeicao.hora.slice(0,5)+'  <span class="glyphicon glyphicon-chevron-down"> </span>';
            card_refeicoes +='</button>';
            card_refeicoes += '<div class="d-flex justify-content-end text-center">';
            card_refeicoes += '<small id="lbl-refeicao'+refeicao.id+'" class="text-dark ml-2"></small>';
            dttemp = "'"+dataatual+"'";
            descref = "'"+refeicao.descricao+"'";

            card_refeicoes +='<small class="mr-1"><button class="btn btn-warning btn-sm text-dark ml-2"'+
            ' data-toggle="modal" data-target=".insert-edit-modal-food" '+
            'onclick="insert_edit_food('+refeicao.id+','+descref+','+dttemp+','+JSON.stringify({})+',-1);" aria-expanded="true">';
            card_refeicoes +='<span class="glyphicon glyphicon-plus"></span></button></small></div>';


            dieta_refeicao(refeicao.id,refeicao.descricao,dataatual);

            card_refeicoes +='</div>';
            card_refeicoes +='<div id="collapse'+refeicao.id+'" class="collapse" aria-labelledby="heading'+refeicao.id+
            '" data-parent="#accordion-refeicoes">';
            card_refeicoes +='<div class="card-body bg-dark" id="card-body-refeicao'+refeicao.id+'">';

            card_refeicoes +='<div class="row" id="div-itens'+refeicao.id+'">';

            card_refeicoes +='</div>';
            card_refeicoes +='</div></div></div>';
        }
    });

    accordion_refeicoes.innerHTML =  card_refeicoes;
}
// mostra itens lançado daquela refeição
async function dieta_refeicao(idrefeicao,descrefeicao,dataatual){

    url = '/dietarefeicao/'+idrefeicao+'/'+dataatual;
    console.log(url);
    let response = await fetch(url);
    if (response.ok) { // if HTTP-status is 200-299
        let json = await response.json();

        bodypdf += '<div class="row">'+
        '<div class="row"><h1 class="lbl-head"><strong>Refeicao: '+descrefeicao+ ((json.totreg==0)?"( Nenhum lançado )":"")+ '</strong></h1></div>';


        lblrefeicao = document.getElementById('lbl-refeicao'+idrefeicao);
        divitens = document.getElementById('div-itens'+idrefeicao);
        totalreg = json.totreg;
        console.log('Tot:'+totalreg);

        dttemp = '"'+dataatual+'"';
        descref = '"'+descrefeicao+'"';
        if (totalreg != 0){
            dieta =  json.data[0];
            totitens = json.totitens;
            lblrefeicao.innerHTML = '<label class="text-dark"><strong>Total de Itens: '+ json.totitens+'</strong></label>';
            itensdieta = json.dataitem;

            if (totitens > 0){

                bodypdf += '<table class="table-item"><thead class="thead-item"><tr class="tr-item">';
                bodypdf += '<th  class="th-item">Alimento</th>'+
                '<th class="th-item">Porção</th>'+
                '<th class="th-item">Kcal</th>'+
                '<th class="th-item">Proteina</th>'+
                '<th class="th-item">Carboidrato</th>'+
                '<th class="th-item">Gordura</th>';
                bodypdf +='</tr></thead>';
                bodypdf +='<tbody class="tbody-item">';


                tableitem = '<table class="table table-dark table-sm">';
                tableitem +='<thead class="text-white"><tr>'+
                '<th  class="align-middle" scope="col">Alimento</th>'+
                '<th class="align-middle" scope="col">Porção</th>'+
                '<th class="align-middle" scope="col">Kcal</th>';
                //'<th class="align-middle text-center" scope="col">Proteina</th>'+
                //'<th class="align-middle text-center" scope="col">Carboidrato</th>'+
                //'<th class="align-middle text-center" scope="col">Gordura</th>'+
                '<th class="align-middle text-center" scope="col"> Ações </th>';
                tableitem +='</tr></thead>';
                tableitem +='<tbody class="text-warning">';

                totkcal = 0;
                totcarb = 0;
                totproteina = 0;
                totfat = 0;

                itensdieta.forEach((item) => {
                    console.log(item);
                    totkcal += parseFloat(item.totalcalorias);
                    totcarb += parseFloat(item.totalcarbo);
                    totproteina += parseFloat(item.totalproteina);
                    totfat += parseFloat(item.totalgordura);

                    bodypdf += '<tr><td class="td-item">'+item.alimento.descricao+'</td>';
                    bodypdf +='<td class="td-item">'+item.quantgramas+' '+item.alimento.unalimento.sigla+'</td>';
                    bodypdf +='<td class="td-item">'+item.totalcalorias+'</td>';

                    bodypdf +='<td class="td-item">'+parseFloat(item.totalproteina).toFixed(2)+' Grs - '
                    +(parseFloat(item.totalproteina)*4).toFixed(2)+' kcal</td>';

                    bodypdf +='<td class="td-item">'+parseFloat(item.totalcarbo).toFixed(2)+' Grs - '
                    +(parseFloat(item.totalcarbo)*4).toFixed(2)+' kcal</td>';

                    bodypdf +='<td class="td-item">'+parseFloat(item.totalgordura).toFixed(2)+' Grs - '
                    +(parseFloat(item.totalgordura)*9).toFixed(2)+' Kcal</td>';


                    tableitem +='<tr><td class="align-middle"><div class="dropdown"><small>';
                    tableitem +="<button class='btn btn-link text-warning text-left' "+
                    "data-toggle='modal' data-target='.modal-info-food' "+
                    "onmouseover='mouseouverfood("+descref+","+JSON.stringify(item)+");'"+
                    "onmouseout='mouseoutfood("+item.id+");'"+
                    " onclick='infofood("+descref+","+JSON.stringify(item)+");'>"+
                    item.alimento.descricao+'</button></small>';
                    tableitem +='<div class="dropdown-content" id="dropdown-content'+item.id+'" ></div></div></td>';
                    tableitem +='<td class="align-middle text-left"><small>'+item.quantgramas+' '+item.alimento.unalimento.sigla+'</small></td>';
                    tableitem +='<td class="align-middle text-left"><small>'+item.totalcalorias+'</small></td>';

                    //tableitem +='<td class="align-middle text-center"><small>'+parseFloat(item.totalproteina).toFixed(2)+' Grs<br>'
                    //+(parseFloat(item.totalproteina)*4).toFixed(2)+' kcal</small></td>';

                    //tableitem +='<td class="align-middle text-center"><small>'+parseFloat(item.totalcarbo).toFixed(2)+' Grs<br>'
                    //+(parseFloat(item.totalcarbo)*4).toFixed(2)+' kcal</small></td>';

                    //tableitem +='<td class="align-middle text-center"><small>'+parseFloat(item.totalgordura).toFixed(2)+' Grs<br>'
                    //+(parseFloat(item.totalgordura)*9).toFixed(2)+' Kcal</small></td>';


                    tableitem +='<td class="align-middle text-center">';

                    //tableitem +="<small><button class='btn btn-warning text-dark ml-1 mb-1' "+
                    //"data-toggle='modal' data-target='.insert-edit-modal-food'"+
                    //"onclick='insert_edit_food("+idrefeicao+","+descref+","+dttemp+","+JSON.stringify(item)+","+item.id+");'>";
                    //tableitem +='<span class="glyphicon glyphicon-pencil"></span></button></small>';


                    desc = '"'+descrefeicao+'"';
                    tableitem +="<small><button class='btn btn-warning btn-sm text-dark ml-1'"+
                    "data-toggle='modal' data-target='.modal-delete-food'"+
                    "onclick='deleteitemdieta("+desc+","+JSON.stringify(item)+");' >";
                    tableitem +='<span class="glyphicon glyphicon-trash"></span></button></small></td>';



                });
                tableitem +='</tr></tbody>';

                bodypdf+= '</tr></tbody>';
                bodypdf +='<tfoot class="tfoot-item"><tr><td></td>'+
                '<th class="th-item">Total:</th>'+
                '<th class="th-item">'+totkcal.toFixed(2)+'Kcal</th>';
                '<th class="th-item">'+totproteina.toFixed(2)+'Grs - '+
                (totproteina*4).toFixed(2)+'kcal</th>'+
                '<th class="th-item">'+totcarb.toFixed(2)+'Grs - '+
                (totcarb*4).toFixed(2)+'Kcal</th>'+
                '<th class="th-item">'+totfat.toFixed(2)+'Grs - '+
                (totfat*9).toFixed(2)+'Kcal</th>';
                bodypdf +='</tr></tfoot>';
                bodypdf +='</table>';


                tableitem +='<tfoot class="text-white"><tr><td></td>'+
                '<th class="align-middle text-right" scope="col">Total:</th>'+
                '<th class="align-middle text-left" scope="col"><small>'+totkcal.toFixed(2)+' Kcal</small></th>';
                //'<th class="align-middle text-center" scope="col"><small>'+totproteina.toFixed(2)+' Grs<br>'+
                //(totproteina*4).toFixed(2)+' Kcal</small></th>'+
                //'<th class="align-middle text-center" scope="col"><small>'+totcarb.toFixed(2)+' Grs<br>'+
                //(totcarb*4).toFixed(2)+' Kcal</small></th>'+
                //'<th class="align-middle text-center" scope="col"><small>'+totfat.toFixed(2)+' Grs<br>'+
                //(totfat*9).toFixed(2)+' Kcal</small></th>';
                tableitem +='</tr></tfoot>';
                tableitem +='</table>';

                bodypdf+='</div>';
                divitens.innerHTML = tableitem;
            }
            else{

                lblrefeicao.innerHTML = '<label class="text-danger"><strong>Nenhum Item Lançado</strong></label>';
                divitens.innerHTML = '<div class="d-flex justify-content-center text-center">'+
                '<small class="text-warning">Nenhum Item Lançado para a Refeição: <strong>'+descrefeicao+
                '</strong> na data de: '+ databr + '</small></div>';
            }
        }
        else{

            lblrefeicao.innerHTML = '<label class="text-danger"><strong>Nenhum Item Lançado</strong></label>';
            divitens.innerHTML = '<div class="d-flex mx-auto justify-content-center">'+
            '<small class="text-warning">Nenhum Item Lançado para a Refeição: <strong>'+descrefeicao+
            '</strong> na data de: '+ databr + '</small></div>';
        }


    } else {
        alert("HTTP-Error: " + response.status);
    }
}
function mouseouverfood(descref,item){
    document.getElementById('dropdown-content'+item.id).innerHTML= retornadivtablefood(descref,item,true);

}
function mouseoutfood(id){

}
function zeroFill(n) {
    return ('0' + n).slice(-2);
}
function adicionarDiasData(dataat,dias){
    var hoje        = new Date(dataat);
    var datareturn    = new Date(hoje.getTime() + (dias * 24 * 60 * 60 * 1000));
    return datareturn.getFullYear() + "-" + zeroFill((datareturn.getMonth() + 1)) + "-" + zeroFill(datareturn.getDate());
}

function adicionarDiasDataBR(dataat,dias){
    var hoje        = new Date(dataat);
    var datareturn    = new Date(hoje.getTime() + (dias * 24 * 60 * 60 * 1000));
    return zeroFill(datareturn.getDate()) + "/" + zeroFill((datareturn.getMonth() + 1)) + "/" +datareturn.getFullYear();
}

function prevdatadiario(){
    window.location.href = "/sisnutri/diario?dataatual="+dataprev+"&databr="+dataprevBR;
    console.log(dataprevBR);
}
function nextdatadiario(){
    window.location.href = "/sisnutri/diario?dataatual="+datanext+"&databr="+datanextBR;

}
// modal delete item
function deleteitemdieta(descrefeicao,item){
    modalmsg = document.getElementById('modal-msg-delete');

    foodselect['id'] = item.id
    foodselect['descfood'] = item.alimento.descricao;
    foodselect['descrefeicao'] = descrefeicao;

    modalmsg.innerHTML = 'Deseja Excluir o item: <strong>'+item.alimento.descricao+'</strong> da Refeição: '+ descrefeicao+'?';
}
function confirmaexclusaofood(data){
    $.ajax({
        url: '/delete/itemdieta?',
        type: 'GET',
        data:'id='+data.id+'&descfood='+data.descfood+'&descrefeicao='+data.descrefeicao,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        result = false;
        alertmsgdelete = document.getElementById('alert-msgdelete');
        alertmsgdelete.classList.remove('d-none');

        if (data['result'] == true){
            result = true;
            alertmsgdelete.classList.add('alert-primary');
            alertmsgdelete.innerHTML = data['mensagem'];
        }
        else{
            alertmsgdelete.classList.add('alert-danger');
            alertmsgdelete.innerHTML = data['mensagem'];

        }
        setTimeout(function(){
            if (result){
                alertmsgdelete.classList.remove('alert-primary');
                window.location.reload(true);
                console.log(idrefeicao);
                document.getElementById('btnrefeicao'+idrefeicao).click();
            }
            else{
                alertmsgdelete.classList.remove('alert-danger');
            }

            alertmsgdelete.classList.add('d-none');
        }, 2000);



    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });

}

// modal insert ou edit
function insert_edit_food(idrefeicao,descrefeicao,dataatual,item,id){
    lblheadfoo = document.getElementById('lblheadfood')
    edtiditem.value = id;
    if (id == -1){
        lblheadfoo.innerHTML = 'Inserindo item na refeição: '+ descrefeicao;
    }
    else{
        lblheadfoo.innerHTML = 'Alterando o item: '+item.alimento.descricao+' na refeição: '+ descrefeicao;
    }
    edtidrefeicao.value = idrefeicao;

}

// pesquisar alimentos de acordo com o campo digitado
async function searchfood(page){
    idpessoa = document.getElementById('edtidpessoa').value;
    smalldescricao.classList.add('d-none');
    divtabledadosnutri.classList.add('d-none');
    edtidalimento.value = 0;
    smallemptydesc = document.getElementById('small-empty-desc');
    document.getElementById('small-UN').classList.add('d-none');
    food = document.getElementById('edtdescfood').value;
    if (food.length == 0 ){
        divfoods.classList.add('d-none');
        smallemptydesc.classList.remove('d-none');
    }
    else{
        smallemptydesc.classList.add('d-none');

        url = '/tabfoods.json?descricao='+food+'&page='+page+'&idpessoa='+idpessoa;
        console.log(url);
        let response = await fetch(url);
        console.log(response.ok);
        if (response.ok) { // if HTTP-status is 200-299

            let json = await response.json();
            console.log(json);
            if (json.result == true){
                divfoods.classList.remove('d-none');
                frmgroupqtd.classList.add('d-none');
                console.log(json.pagul);
                if (json.pagul != ''){
                    divpaginationfoods.classList.remove('d-none');

                    divpaginationfoods.innerHTML = json.pagul;
                    lidisabled = document.getElementsByClassName("page-item disabled");
                    for (i = 0; i < lidisabled.length; i++) {
                        try {
                            lidisabled[0].remove();
                        }
                        catch(err) {
                            console.log(err.message);
                        }

                    }
                    lispag = document.getElementsByClassName("page-link");
                    if (lispag.length > 0){
                        lispag[lispag.length-1].remove();
                    }

                    for (i = 0; i < lispag.length; i++) {
                        if (lispag[i].ariaLabel != null){
                            lispag[i].remove();
                        }

                        try {
                            lispag[i].href = "#";
                        }
                        catch(err) {
                            console.log(err.message);
                        }

                        lispag[i].addEventListener("click", function(){
                            searchfood(this.innerHTML);
                        });

                    }
                }
                btnfoods = '';
                // PRENCHE ALIMENTOS ENCONTRADOS

                json.tabfoods.forEach((food) => {
                    console.log(food);
                    vlcarbo =  parseFloat((food.carboidrato == null) ? '0' : food.carboidrato).toFixed(0);
                    vlproteina =  parseFloat((food.proteina == null) ? '0' : food.proteina).toFixed(0);
                    vlfat =  parseFloat((food.lipidios == null) ? '0' : food.lipidios).toFixed(0);
                    vlfibras =  parseFloat((food.fibras == null) ? '0' : food.fibras).toFixed(0);
                    vlsodio =  parseFloat((food.sodio == null) ? '0' : food.sodio).toFixed(0);
                    btnfoods+= "<button id='btnfood"+food.id+"' title='btnfood"+food.id+"'  onclick='selectfood("+JSON.stringify(food)+");' type='button'"+
                    " class='list-group-item list-group-item-action'><strong>"+
                    food.descricao+"</strong><br>"+
                    "<small class='text-white text-center'>UN: "+food.unalimento.descricao+", Qtd: "+parseFloat(food.qtdgramasemcima).toFixed(2)+")<br>"+
                    "Kcal: "+parseFloat(food.calorias).toFixed(2)+", Carb.: "+vlcarbo+", "+
                    "Proteina: "+vlproteina+", Gordura.: "+vlfat+" <br>"+
                    "Fibras: "+vlfibras+", Sódio.: "+vlsodio+
                    "</small></button>";
                });
                divfoods.innerHTML = btnfoods;
            }
            else{
                divfoods.classList.add('d-none');
                frmgroupqtd.classList.add('d-none');
                divpaginationfoods.classList.add('d-none');
                divpaginationfoods.innerHTML = "";
            }

        }
        else {
            alert("HTTP-Error: " + response.status);
        }
    }
}
// Clica botão Lista alimento
function selectfood(food){
    vlcarbo =  parseFloat((food.carboidrato == null) ? '0' : food.carboidrato).toFixed(2);
    vlproteina =  parseFloat((food.proteina == null) ? '0' : food.proteina).toFixed(2);
    vlfat =  parseFloat((food.lipidios == null) ? '0' : food.lipidios).toFixed(2);
    vlfibras =  parseFloat((food.fibras == null) ? '0' : food.fibras).toFixed(2);
    vlsodio =  parseFloat((food.sodio == null) ? '0' : food.sodio).toFixed(2);

    smallstr = "UN: "+food.unalimento.descricao+", "+
    "Qtd: "+parseFloat(food.qtdgramasemcima).toFixed(2)+"<br>"+
    "Kcal: "+parseFloat(food.calorias).toFixed(2)+", Carboidrato: "+vlcarbo+", "+
    "Proteina: "+vlproteina+", Gorduras: "+vlfat+", "+
    "Fibras: "+vlfibras+", Sódio.: "+vlsodio;

    document.getElementById('lblqtd').innerHTML ='Digite a quantidade de '+food.unalimento.sigla;
    document.getElementById('small-UN').innerHTML = 'Unidade Medida: '+ food.unalimento.descricao;
    document.getElementById('small-UN').classList.remove('d-none');

    smalldescricao.innerHTML = smallstr;
    smalldescricao.classList.remove('d-none');

    edtdescfood.value = food.descricao;
    edtidalimento.value = food.id;
    foodselect = food;
    console.log(foodselect);
    divpaginationfoods.classList.add('d-none');
    divfoods.classList.add('d-none');
    frmgroupqtd.classList.remove('d-none');
    divpaginationfoods.innerHTML = "";

}
// calcula valores nutricionais de acordo com a quantidade de gramas ou unidade medida mencionada
function calcula_valnutricionais(qtd,food){
    smallemptyqtd = document.getElementById('small-empty-qtd');
    if (qtd.length == 0){
        smallemptyqtd.classList.remove('d-none');
        divtabledadosnutri.classList.add('d-none');
    }
    else{

        let returnvalnutricional = function(qtdfood,vlgrfood,qtdinfo){
            return ((parseFloat(vlgrfood) * parseFloat(qtdinfo)) / parseFloat(qtdfood));
        }

        vlkcal = returnvalnutricional(food.qtdgramasemcima,food.calorias,qtd);
        vlcarbo = returnvalnutricional(food.qtdgramasemcima,food.carboidrato,qtd);
        vlproteina = returnvalnutricional(food.qtdgramasemcima,food.proteina,qtd);
        vlfat = returnvalnutricional(food.qtdgramasemcima,food.lipidios,qtd);
        vlfibras = returnvalnutricional(food.qtdgramasemcima,food.fibras,qtd);
        vlsodio = returnvalnutricional(food.qtdgramasemcima,food.sodio,qtd);


        document.getElementById('edtvalkcal').value = vlkcal;
        document.getElementById('edtvalproteina').value = vlproteina;
        document.getElementById('edtvalcarbo').value = vlcarbo;
        document.getElementById('edtvalfat').value = vlfat;
        document.getElementById('edtvalfibras').value = vlfibras;
        document.getElementById('edtvalsodio').value = vlsodio;


        console.log('Calorias:'+vlkcal);
        divtabledadosnutri.classList.remove('d-none');
        table = '<h5 class="text-center bg-warning text-white">'+
        '<strong>Informação Nutricional</strong></h5>';
        table += '<table class="table table-dark table-sm text-warning ">';
        table +='<tbody>';
        table +='<tr><th scope="row">Calorias:</th><td>'+vlkcal.toFixed(2)+' kcal</td></tr>';
        table +='<tr><th scope="row">Carboidratos:</th><td>'+vlcarbo.toFixed(2)+' grs </td></tr>';
        table +='<tr><th scope="row">Proteínas:</th><td>'+vlproteina.toFixed(2)+' grs</td></tr>';
        table +='<tr><th scope="row">Gorduras:</th><td>'+vlfat.toFixed(2)+' grs</td></tr>';
        table +='<tr><th scope="row">Fibras:</th><td>'+vlfibras.toFixed(2)+' grs </td></tr>';
        table +='<tr><th scope="row">Sódio:</th><td>'+vlsodio.toFixed(2)+'mg</td></tr>';
        table +='</tbody></table>';
        divtabledadosnutri.innerHTML = table;


    }
}
// grava item dentro do banco de dados na tabela de itemdieta

function incluiitemfood(){
    smallemptyqtd = document.getElementById('small-empty-qtd');
    smallemptyqtd.classList.add('d-none');
    smallemptydesc = document.getElementById('small-empty-qtd');
    smallemptydesc.classList.add('d-none');
    if(edtidalimento.value == '' || edtidalimento.value =='0'){
        smallemptydesc.classList.remove('d-none');
    }
    else{
        if (edtqtd.value.length == 0 || edtqtd.value<=0) {
            smallemptyqtd.classList.remove('d-none');
        }
        else{
            gravaritemDB();
        }
    }
}
function gravaritemDB(){
    idrefeicao = edtidrefeicao.value;
    form = document.getElementById('formfood');
    formData = new FormData(form);
    alertdadosfood = document.getElementById('alert-dadosfood');
    alertdadosfood.classList.remove('d-none');
    $.ajax({
        url: '/add/itemdieta',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        result = false;
        console.log(data);
        if (data['result'] == true){
            result = true;
            alertdadosfood.classList.add('alert-primary');
            alertdadosfood.innerHTML = data['mensagem'];
        }
        else{
            alertdadosfood.classList.add('alert-danger');
            alertdadosfood.innerHTML = data['mensagem'];

        }
        setTimeout(function(){
            if (result){
                alertdadosfood.classList.remove('alert-primary');
                window.location.reload(true);
                console.log(idrefeicao);
                document.getElementById('btnrefeicao'+idrefeicao).click();
            }
            else{
                alertdadosfood.classList.remove('alert-danger');
            }

            alertdadosfood.classList.add('d-none');
        }, 2000);



    }).fail( function(){

    }).always( function(){

    });
}
// calcula diferença calorica da meta menos total lançada no dia nas refeições
function calcula_preeche_valdiferenca(data_dieta, data_meta){
    console.log('-------------- data dieta -------------------');
    console.log(data_dieta);
    console.log('-------------- data meta -------------------');
    console.log(data_meta);


    vldifkcal = parseFloat(data_meta.valalvocalorico) - parseFloat(data_dieta.totalkcal)

    vldifgrproteina = parseFloat(data_meta.valgramasproteina) - parseFloat(data_dieta.totalproteina)
    vldifkcalproteina = vldifgrproteina * 4;

    vldifgrgordura = parseFloat(data_meta.valgramasgordura) - parseFloat(data_dieta.totalgordura)
    vldifkcalgordura = vldifgrgordura * 9;

    vldifgrcarbo = parseFloat(data_meta.valgramascarbo) - parseFloat(data_dieta.totalcarbo)
    vldifkcalcarbo = vldifgrcarbo * 4;

    theaddiferenca = document.getElementById('thead-diferenca');

    falta = (vldifkcal <= parseFloat(data_meta.valalvocalorico))? true : false;
    classtemp = (falta)? 'border border-primary text-primary rounded' : 'border border-danger text-danger rounded';
    msgtemp = (falta)? "Falta" : "Ultrapassou";
    trstr =  '<tr><th class="align-middle" scope="col">Valor Calórico:</th>'+
    '<th class="align-middle align-center"><label class="'+classtemp+'">'+
    msgtemp+': '+ vldifkcal.toFixed(2) +' kcal</label></th></tr> ';


    trstr += '<tr><th scope="col">Proteina:</th><td>Kcal: '+vldifkcalproteina.toFixed(0)+
    ' | Grs:' +vldifgrproteina.toFixed(2)+ '</td></tr> ';

    trstr += '<tr><th scope="col">Carboidrato:</th><td>Kcal: '+vldifkcalcarbo.toFixed(0)+
    ' | Grs:' +vldifgrcarbo.toFixed(2)+ '</td></tr> ';

    trstr += '<tr><th scope="col">Gordura:</th><td>Kcal: '+vldifkcalgordura.toFixed(0)+
    ' | Grs:' +vldifgrgordura.toFixed(2)+ '</td></tr> ';

    theaddiferenca.innerHTML = trstr;
}

async function buscaunidademedida(){
    url = '/unalimentos.json/';
    console.log(url);
    let response = await fetch(url);
    if (response.ok) { // if HTTP-status is 200-299
        let json = await response.json();
        unsfood = json.data;
        opt = '';
        unsfood.forEach((unfood) => {
            opt += '<option value="'+unfood.id+'">'+unfood.descricao+' - '+ unfood.sigla +'</option>';
        });
        document.getElementById('edtidunmedida').innerHTML = opt;
    }
}
function gravarnewfood(){

    gravar = false;
    console
    if (document.getElementById('edtqtdnew').value == '' || document.getElementById('edtqtdnew').value == '0'){
        document.getElementById('smallqtd').classList.remove('d-none');
    }
    else{
        gravar = true;
        if (document.getElementById('edtdescricao').value == '' || document.getElementById('edtdescricao').value == '0'){
            document.getElementById('smalldesc').classList.remove('d-none');
            gravar = false;
        }
    }

    if (gravar){
        savenewfood();
    }
}
function savenewfood(){
    form = document.getElementById('formnewfood');
    formData = new FormData(form);

    $.ajax({
        url: '/add/food',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        result = false;
        alertdadosfood = document.getElementById('alert-dadosnewfood');
        alertdadosfood.classList.remove('d-none');
        if (data['result'] == true){
            result = true;
            alertdadosfood.classList.add('alert-primary');
            alertdadosfood.innerHTML = data['mensagem'];

        }
        else{
            alertdadosfood.classList.add('alert-danger');
            alertdadosfood.innerHTML = data['mensagem'];

        }
        setTimeout(function(){
            if (result){
                document.getElementById('edtidalimento').value = data['data']['id'];
                document.getElementById('edtdescfood').value = data['data']['descricao'];


                setTimeout(function(){
                    $('#modal-insert-newfood').modal('hide');
                    searchfood(1);
                    document.getElementById('frmgroup-qtd').classList.remove('d-none');
                    setTimeout(function(){
                    btn= '#btnfood'+data['data']['id'];
                    console.log(btn);
                    btnfood = document.querySelector(btn);
                    btnfood.click();

                    document.getElementById('frmgroup-qtd').classList.remove('d-none');
                    setTimeout(function(){
                        document.getElementById('lblqtd').click();
                    },500);
                }, 1000);

                }, 1000);




            }
            else{
                alertdadosfood.classList.remove('alert-danger');
            }

            alertdadosfood.classList.add('d-none');
        }, 1000);



    }).fail( function(){

    }).always( function(){
    });
}

function infofood(descrefeicao,food){


    document.getElementById('card-body-infofood').innerHTML = retornadivtablefood(descrefeicao,food,true);

}
function retornadivtablefood(descrefeicao,food,mostrahead){
    document.getElementById('lbldescfood').innerHTML = 'Informações Nutricionais';
    tableitem = '';
    if (mostrahead){
        tableitem = '<div class="p-1 mb-2 bg-warning  rounded">'+
        '<div class="d-flex justify-content-center"><h5 class="text-dark"><strong>'+food.alimento.descricao+'</strong></h5></div>'+
        '<div class="d-flex justify-content-center"><p class="text-dark">Refeição: '+descrefeicao+'</p></div></div>';
    }
    tableitem += '<table class="table table-dark table-sm">';
    tableitem +='<tbody">';
    tableitem +='<tr><th class="align-middle" scope="col"><strong>Un.Medida: </strong>'+
    food.alimento.unalimento.descricao+'</strong></th>'+
    '<th class="align-middle" scope="col"><strong>Porção de: </strong>'+
    food.quantgramas+' '+food.alimento.unalimento.sigla+'</th></tr>';
    tableitem +='</tbody></table>';
    tableitem += '<table class="table table-dark table-sm"><tbody>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col"><strong>Calorias:</strong></th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalcalorias+' Kcal</th></tr>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col">Carboidrato:</th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalcarbo+' grs</th></tr>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col">Proteina:</th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalproteina+' grs</th></tr>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col">Gordura:</th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalgordura+' grs</th></tr>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col">Fibras:</th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalfibras+' grs</th></tr>';
    tableitem +='<tr><th class="align-middle text-warning" scope="col">Sódio:</th>'+
    '<th class="align-middle text-warning" scope="col">'+food.totalsodio+' grs</th></tr>';
    tableitem +='</tbody></table>';
    return tableitem;
}

function gerarpdf(){
    var style = "<style>title{font: 40px Calibri;} ";
        style += "table {width: 100%;font: 20px Calibri;}";
        style += "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
        style += "padding: 2px 3px;text-align: center;}";
        style += "</style>";
    var win = window.open('', '', 'height=700,width=700');
    win.document.write('<html><head>');
    win.document.write('<title>Diário</title>');   // <title> CABEÇALHO DO PDF.
    win.document.write(style+'</head>');
    win.document.write('<body>');
    win.document.write(bodypdf);                          // O CONTEUDO DA TABELA DENTRO DA TAG BODY
    win.document.write('</body></html>');
    win.document.close(); 	                                         // FECHA A JANELA
    win.print();

}
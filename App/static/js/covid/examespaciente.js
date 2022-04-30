var div_tab_exames = document.getElementById('div-table-exames-pacientes');
var div_menu = document.getElementById('div-menu-datas');
var div_acordion = document.getElementById('accordion');
var data_tab = [];
var pageatual = '1';
var per_page = '100';
var descsearch = '';
var tpfiltro = '0';
var datacoletatemp = '';


function return_table_exames(data){
    let tb = '<div class="d-flex justify-content-center">';
    tb += '<table class="table table-dark table-sm text-warning">';
    tb += '<thead>';
    tb += '<th scope="col" class="text-white">Exame</th>';
    tb += '<th scope="col" class="text-white">Analito</th>';
    tb += '<th scope="col" class="text-white">Resultado</th>';
    tb += '<th scope="col" class="text-white">Desc.Resultado</th>';
    tb += '<th scope="col" class="text-white">Ref. - UN.</th>';
    tb += '</thead><tbody>';
    cont = (parseInt(pageatual) * parseInt(per_page) - parseInt(per_page));
    for (const row in data){
        exame_pac = data[row];

        //item = cont + parseInt(row)+1;
        datacoleta = exame_pac.datacoleta.split("-");
        datacoleta = datacoleta[2]+'/'+datacoleta[1]+'/'+datacoleta[0];
        tb += '<td>'+exame_pac.exame.descricao+'</td>';
        tb += '<td>'+exame_pac.analito.descricao+'</td>';
        tb += '<td>'+exame_pac.valresultado+'</td>';
        tb += '<td>'+exame_pac.resultado+'</td>';
        tb += '<td>'+exame_pac.valreferencia+' - '+exame_pac.analito.unidademedida+'</td>';
        tb +='</tr>';
    }
    tb += '<tbody></table></div>';


    return tb
}

function return_div_pagination(idpaciente,datacoleta,pagination){
    totalitens = pagination.total;
    totalpage = pagination.total_pages;
    lblde = ((parseInt(pageatual) * parseInt(per_page)) - parseInt(per_page) + 1);
    lblate =(parseInt(pageatual) * parseInt(per_page));
    lblate = (lblate>parseInt(totalitens)) ? totalitens : lblate;
    nav = '<div class="d-flex justify-content-end">';
    nav +='<select id="select-search" onchange="select_search_change(this.value);" class="form-control mr-3 select-search">'+
    '<option value="0">Todos</option>'+
    '<option value="1">Por Exame</option>'+
    '<option value="2">Por Analito</option>'+
    '</select>';
    nav +='<div class="input-group mb-2">';
    nav +='<input type="text"  class="form-control" placeholder="" id="input-search-desc">';
    nav +='<div class="input-group-append">';
    nav +='<button type="button" class="btn btn-warning" onclick="filtrar_exames()">';
    nav +='<span class="glyphicon glyphicon-search"></span>';
    nav +='</button></div></div></div>';
    nav += '</div><div class="d-flex justify-content-between">';
    nav += '<div class="div-pagination-foods my-2 mr-2" id="div-pagination-foods">';
    nav += '    <nav aria-label="..."><ul class="pagination pagination-sm">';
    pages = pagination.pages;
    for (const pag in pages){

        if (pages[pag] != null){
            if (pages[pag] == pageatual){
                nav += '<li class="page-item active">';
                nav += '<a class="page-link">'+pages[pag]+'<span class="sr-only">(current)</span></a></li>';
            }else
            {
                nav += '<li class="page-item">';
                descfiltrotemp = "'"+descsearch+"'";
                descdatacoleta = "'"+datacoleta+"'";
                descid = "'"+idpaciente+"'";
                nav += '<a class="page-link" href="#" '+
                'onclick="get_exames_by_data_idpaciente('+descid+','+descdatacoleta+','+pages[pag]+');">'+pages[pag]+'</a></li>';
            }

        }
        else{
            nav += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    nav +='</div>';
    nav +='<div class="d-flex justify-content-center">';
    nav += '<label class="text-muted">De '+lblde+' até '+lblate+', Página Atual: '+pageatual+' de '+totalpage+
        ', Total de registros: '+totalitens+' </label>';
    nav += '</div>';
    nav +='</div>';

    return nav;
    select_search_change(0);

}

function return_header_data_table(paciente,pagination){
    let div = '';
    if (pagination.total > 0){
        //div = '<div class="d-flex justify-content-center"><h3 class="my-4 p-2 d-none bg-warning rounded text-dark"></h3></div>';
        div = '<br>';
    }
    else{
        strmsg = 'Nenhum Exames encontrado para o paciente:'+descsearch+' ou pacinente não encontrado';
        //div = '<div class="row my-2 d-flex justify-content-center"><h3 class="text-white">'+title+'</h3></div>';
        div +='<div class="d-flex justify-content-center">';
        div +='<div class="alert alert-warning text-center" role="alert">';
        div += '<label class="text-muted">'+strmsg+'</label></div></div>';
    }
    return div;
}


async function return_menu_groupby_data(){
    idpaciente = document.getElementById('input-id').value
    url = '/get/total/exames/paciente/data/json?desc='+idpaciente;
    let response = await fetch(url);
    if(response.status == 200){
        await response.json().then(data => {
            data_dt = data;
        });
    }
    else{
        data_dt = [];
    }
    let div = '';

    data_pac = data_dt.paciente;
    data_dt = data_dt.data;

    div +='<div class="d-flex justify-content-center">';
    div +='<div class="col-12 text-center">';
    div += '<p class="text-white text-center">Idade Paciente: '+data_pac.idade+', Sexo: '+data_pac.genero+'</p>';
    div += '<p class="text-white text-center">Local dos exames: '+data_pac.hospital+'</p>';
    div += '</div></div>';
    div += '<div class="row mt-2">';

    for (const row in data_dt){

        nameid = data_dt[row].datacoleta.dia+'_'+data_dt[row].datacoleta.mes+'_'+data_dt[row].datacoleta.ano;

        datacoleta = data_dt[row].datacoleta.dia+'/'+data_dt[row].datacoleta.mes+'/'+data_dt[row].datacoleta.ano;
        datacoletadb = data_dt[row].datacoleta.ano+'-'+data_dt[row].datacoleta.mes+'-'+data_dt[row].datacoleta.dia;
        totalreg = data_dt[row].total;
        datacoletadesc = "'"+datacoletadb+"'";
        nameiddesc = "'"+nameid+"'";
        codpac = "'"+idpaciente+"'";
        div += '<div class="divbtn col-sm"><button class="btn btn-outline-warning my-1" id="btn-data-exames-'+datacoletadb+'"'+
        ' onclick="get_exames_by_data_idpaciente('+codpac+','+datacoletadesc+');">'+
        datacoleta+' - <span class="badge badge-light">'+totalreg+'</span></button></div>';

    }
    div += '</div>';
    div_menu.innerHTML = div;
}


// Filtra exames de acordo com a data clicada.
async function get_exames_by_data_idpaciente(idpaciente,datacoleta,page=1){

    btns =  document.querySelectorAll('.divbtn > .btn');
    btns.forEach((btn,index) => {

        btn.classList.remove('active');
    });

    document.querySelector('#btn-data-exames-'+datacoleta).classList.add('active');

    idpaciente = document.getElementById('input-id').value;
    pageatual = page;
    datacoletatemp = datacoleta;
    url = '/get/covid/exames/pacientes/json?desc='+idpaciente+'&page='+page+'&per_page=50&tpfiltro=0&datacoleta='+datacoleta;
    let response = await fetch(url);
    if(response.status == 200){
        await response.json().then(data => {
            data_tab = data;
        });
    }
    else{
        data_tab = [];
    }
    if (data_tab.pagination.total > 0){
        descsearch = data_tab.desc;
        pageatual = data_tab.pagination.page;
        per_page = data_tab.pagination.per_page;
        div_tab_exames.innerHTML = return_header_data_table(data_tab.data[0].paciente,data_tab.pagination);
        div_tab_exames.innerHTML += return_div_pagination(idpaciente,datacoleta,data_tab.pagination);
        div_tab_exames.innerHTML += return_table_exames(data_tab.data);
        //return_acordion_groupby_data(idpaciente);
        select_search_change('0');
    }
    else{
        card_body.innerHTML = '<div class="alert alert-danger">'+
        'Nenhum exame encontrado para o paciente: '+data_tab.desc+'</div>';
    }

}

function select_search_change(selvalue,indesc=''){
    input_search = document.querySelector('#input-search-desc');
    input_search.value = indesc;

    campsel = document.querySelector('.select-search option[value="'+selvalue+'"]').selected=true;


    switch (parseInt(selvalue)){
        case 0:

            input_search.setAttribute('placeholder','Todos');
            input_search.disabled = true;
            break;
        case 1:
            if (indesc.length > 0){
                input_search.setAttribute('placeholder','Forneça a Descrição do Exame');
            }
            input_search.disabled = false;
            break;
        case 2:
            console.log('Analito');
            if (indesc.length > 0){
                input_search.setAttribute('placeholder','Forneça a Descrição do Análito');
            }
            input_search.disabled = false;
            break;
    }

}

function filtrar_exames(){
    sel_search = document.querySelector('.select-search').value;
    input_search = document.querySelector('#input-search-desc').value;
    var table_temp = data_tab.data.filter(function(obj_row){
    switch(parseInt(sel_search)){
        case 0:
            return (obj_row);
            break;
        case 2:

            return (obj_row.analito.descricao.toUpperCase().includes( input_search.toUpperCase()))
            //return (obj_row.analito.descricao.includes(input_search));
            break;
        case 1:
            match =  obj_row.exame.descricao.toUpperCase().match(input_search.toUpperCase());
            console.log(match);
            return (obj_row.exame.descricao.toUpperCase().includes(match));
            break;
        }
    });
    console.log(table_temp.length);
    if (table_temp.length == 0){
        alert('Nenhum registro encontrado com a descrição:'+input_search);
    }
    table_temp = (table_temp.length == 0 ) ? data_tab.data : table_temp;

    div_tab_exames.innerHTML = return_header_data_table(data_tab.data[0].paciente,data_tab.pagination);
    div_tab_exames.innerHTML += return_div_pagination(idpaciente,datacoletatemp,data_tab.pagination);
    div_tab_exames.innerHTML += return_table_exames(table_temp);
    select_search_change(sel_search,input_search);
}

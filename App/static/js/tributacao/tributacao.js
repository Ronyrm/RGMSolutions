var content_cst = document.getElementById('content-cst');
var datacst = [];
var pageatual = '1';
var per_page = '50';
var grau = '0';
var tpfiltro = '0';
var descfiltro = '';
var datancms ='';

function removeactivebtns(){
    document.getElementById('btnmostrar-csticms').classList.remove('active');
    document.getElementById('btnmostrar-cstipi').classList.remove('active');
    document.getElementById('btnmostrar-cstpiscofins').classList.remove('active');
    document.getElementById('btnmostrar-ncms').classList.remove('active');
}

async function get_cst(tpicms){
    url = '/get/tributacao/cst/'+tpicms+'/json'
    console.log(url);
    let response = await fetch(url);

    if (response.status == 200) {
        await response.json().then(data =>{
            datacst = data;
        });
    }
    else{
        return None;
    }
}

async function mostrarcst(btn,tpcst){
    removeactivebtns();
    btn.classList.add('active');
    data = await get_cst(tpcst);

    switch(tpcst) {
      case 'icms':
        content_cst.innerHTML = retorn_table_cst_icms(datacst);
        break;
      case 'ipi':
        content_cst.innerHTML = retorn_table_cst_ipi(datacst);
        break;
      case 'piscofins':
        content_cst.innerHTML = retorn_table_cst_pisconfins(datacst);
        break;
    }

}
//RETORNA TABELA CST ICMS
function retorn_table_cst_icms(data){
    stb = '<div class="my-2  p-2 text-center text-warning">';
    stb +='<h2><strong>Situação Tributária ICMS</strong></h2></div>';
    if (data.result){
        stb += '<table class="table mt-2 table-dark table-sm">';
        stb +='<thead>';
        stb +='<th scope="col" class="text-white align-middle text-center" >CST</th>';
        stb +='<th scope="col" class="text-white">Descrição</th>';
        stb +='<th scope="col" class="text-white align-middle text-center">Opt.Simples Nacional</th>';
        stb +='</thead>';
        stb +='<tbody class="text-warning">';
        data.data.forEach((cst) => {
            stb += '<tr>';
            stb += '<td class="align-middle text-center">'+cst.codcsticms+'</td>';
            stb += '<td>'+cst.descricao+'</td>';
            stb += '<td class="align-middle text-center">';
            chek = (cst.optantesimplesnacional=='S') ? 'checked': '';
            stb +='<input type="checkbox" '+chek+' name="chkativa_cstimcs'+cst.id+'" onclick="return false;" onkeydown="return false;" >';
            '</td></tr>';
        });
        stb +='</tbody></table>';
    }
    return stb;

}
//RETORNA TABELA CST IPI
function retorn_table_cst_ipi(data){
    stb = '<div class="my-2  p-2 text-center text-warning">';
    stb +='<h2><strong>Situação Tributária IPI</strong></h2></div>';
    if (data.result){
        stb += '<div class="text-center text-dark">';
        stb +='<h5 class="bg-warning rounded rounded-2"><strong>Saída</strong></h5></div>';
        stb += '<table class="table mt-2 table-dark table-sm">';
        stb +='<thead>';
        stb +='<th scope="col" class="text-white align-middle text-center" >CST</th>';
        stb +='<th scope="col" class="text-white">Descrição</th>';
        stb +='<th scope="col" class="text-white align-middle text-center">Movimentação</th>';
        stb +='</thead>';
        stb +='<tbody class="text-warning">';
        data_saida = data.data.filter(function(cst){
            return cst.tipomov=='S';
        });
        data_saida.forEach((cst) => {
            stb += '<tr>';
            stb += '<td class="align-middle text-center">'+cst.codcstipi+'</td>';
            stb += '<td>'+cst.descricao+'</td>';
            tipomov = (cst.tipomov=='E') ? 'Entrada': 'Saída';
            stb += '<td class="align-middle text-center">'+tipomov+'</td></tr>';
        });
        stb +='</tbody></table>';
        stb += '<div class="text-center text-dark">';
        stb +='<h5 class="bg-warning rounded rounded-2"><strong>Entrada</strong></h5></div>';
        stb += '<table class="table mt-2 table-dark table-sm">';
        stb +='<thead>';
        stb +='<th scope="col" class="text-white align-middle text-center" >CST</th>';
        stb +='<th scope="col" class="text-white">Descrição</th>';
        stb +='<th scope="col" class="text-white align-middle text-center">Movimentação</th>';
        stb +='</thead>';
        stb +='<tbody class="text-warning">';
        data_saida = data.data.filter(function(cst){
            return cst.tipomov=='E';
        });
        data_saida.forEach((cst) => {
            stb += '<tr>';
            stb += '<td class="align-middle text-center">'+cst.codcstipi+'</td>';
            stb += '<td>'+cst.descricao+'</td>';
            tipomov = (cst.tipomov=='E') ? 'Entrada': 'Saída';
            stb += '<td class="align-middle text-center">'+tipomov+'</td></tr>';
        });
        stb +='</tbody></table>';
    }
    return stb;
}
//RETORNA TABELA CST PIS/COFINS
function retorn_table_cst_pisconfins(data){
    stb = '<div class="my-2  p-2 text-center text-warning">';
    stb +='<h2><strong>Situação Tributária PIS/COFINS</strong></h2></div>';
    if (data.result){
        stb += '<div class="text-center text-dark">';
        stb +='<h5 class="bg-warning rounded rounded-2"><strong>Saída</strong></h5></div>';
        stb += '<table class="table mt-2 table-dark table-sm">';
        stb +='<thead>';
        stb +='<th scope="col" class="text-white align-middle text-center" >CST</th>';
        stb +='<th scope="col" class="text-white">Descrição</th>';
        stb +='<th scope="col" class="text-white align-middle text-center">Movimentação</th>';
        stb +='</thead>';
        stb +='<tbody class="text-warning">';
        data_saida = data.data.filter(function(cst){
            return cst.tipomov=='S';
        });
        data_saida.forEach((cst) => {
            stb += '<tr>';
            stb += '<td class="align-middle text-center">'+cst.codcstpiscofins+'</td>';
            stb += '<td>'+cst.descricao+'</td>';
            tipomov = (cst.tipomov=='E') ? 'Entrada': 'Saída';
            stb += '<td class="align-middle text-center">'+tipomov+'</td></tr>';
        });
        stb +='</tbody></table>';
        stb += '<div class="text-center text-dark">';
        stb +='<h5 class="bg-warning rounded rounded-2"><strong>Entrada</strong></h5></div>';
        stb += '<table class="table mt-2 table-dark table-sm">';
        stb +='<thead>';
        stb +='<th scope="col" class="text-white align-middle text-center" >CST</th>';
        stb +='<th scope="col" class="text-white">Descrição</th>';
        stb +='<th scope="col" class="text-white align-middle text-center">Movimentação</th>';
        stb +='</thead>';
        stb +='<tbody class="text-warning">';
        data_saida = data.data.filter(function(cst){
            return cst.tipomov=='E';
        });
        data_saida.forEach((cst) => {
            stb += '<tr>';
            stb += '<td class="align-middle text-center">'+cst.codcstpiscofins+'</td>';
            stb += '<td>'+cst.descricao+'</td>';
            tipomov = (cst.tipomov=='E') ? 'Entrada': 'Saída';
            stb += '<td class="align-middle text-center">'+tipomov+'</td></tr>';
        });
        stb +='</tbody></table>';
    }
    return stb;
}

// -----------------------------------NCMS-------------------------------------

// CLICA BOTÃO MENU NCMS CARREGA NCMS
async function mostrarncms(pagetemp ='0', per_pagetemp = '0', grau='0', descfiltro='', tpfiltro='0'){
    page = (pagetemp=='0') ? '1' : pagetemp;
    per_page = (per_pagetemp=='0') ? '50' : per_pagetemp;
    removeactivebtns();
    document.getElementById('btnmostrar-ncms').classList.add('active');
    url = '/get/tributacao/ncm/json?page='+page+'&per_page='+per_page+
    '&select-tpfiltro='+tpfiltro+'&select-grau='+grau+'&desc='+descfiltro;

    let response = await fetch(url);
    if (response.status == 200) {
        await response.json().then(data =>{
            datancms = data.data;
        });
    }
    else{
        return None;
    }
    return_ncms();
}
//RETORNA TABELA NCMS
function return_ncms(){
    pageatual = datancms.pagination.page;
    per_page = datancms.pagination.per_page;
    tbfiltro = datancms.tbfiltro;
    grau = datancms.grau;
    desc = datancms.desc;
    let divncms = return_div_modal_filtro_ncms();

    divncms += '<div class="my-2  p-2 text-center text-warning">';
    divncms +='<h2><strong>NCMs - Nomeclatura Comum do Mercosul</strong></h2></div>';

    // retorna nav pagination
    divncms += return_nav_link_pagination_ncms(datancms.pagination.pages,
    datancms.pagination.total_pages,datancms.pagination.total);
    //retorna table ncms
    divncms += return_table_ncms(datancms.ncms);
    content_cst.innerHTML = divncms;
}
function return_nav_link_pagination_ncms(pages,total_pages,totalitemns){

    lblde = ((parseInt(pageatual) * parseInt(per_page)) - parseInt(per_page) + 1);
    lblate =(parseInt(pageatual) * parseInt(per_page));
    lblate = (lblate>parseInt(totalitemns)) ? totalitemns : lblate;

    let nav ='<div class="d-flex justify-content-center">';
    nav += '<label class="text-white">De '+lblde+' até '+lblate+', Página Atual: '+page+', Total de registros: '+totalitemns+' </label>';
    nav += '</div>';
    nav += '<div class="d-flex justify-content-between">';
    nav += '<div class="div-pagination-foods my-2" id="div-pagination-foods">';
    nav += '<nav aria-label="..."><ul class="pagination pagination-sm">';
    for (const pag in pages){
        if (pages[pag] != null){
            if (pages[pag] == pageatual){
                nav += '<li class="page-item active">';
                nav += '<a class="page-link">'+pages[pag]+'<span class="sr-only">(current)</span></a></li>';
            }else
            {
                nav += '<li class="page-item">';
                descfiltrotemp = "'"+descfiltro+"'";
                nav += '<a class="page-link" href="#" '+
                'onclick="mostrarncms('+pages[pag]+','+per_page+','+grau+','+descfiltrotemp+','+tpfiltro+');">'+pages[pag]+'</a></li>';
            }

        }
        else{
            nav += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    nav +='</div>';
    nav +='<button class="btn btn-warning btn-sm my-auto" data-toggle="modal" data-target="#modal-filtro-ncms">Filtrar</button>';
    nav +='</div>';
    return nav;
}
// cria e retorna tabela ncms
function return_table_ncms(datancms){
    let tb = '<div class="d-flex justify-content-center">';
    tb += '<table class="table table-dark text-warning">';
    tb += '<thead>';
    tb += '<th scope="col" class="text-white" >Código</th>';
    tb += '<th scope="col" class="text-white">Descrição</th>';
    tb += '<th scope="col" class="text-white">Un.Medida</th>';
    tb += '</thead><tbody>';
    for (const row in datancms){
        ncm = datancms[row];
        tb += '<tr><td>'+ncm.codncm+'</td>';
        i = 1;
        sspc = '';
        grau = ncm.grau*2+2;
        while (i <= grau ){
            sspc += '&nbsp;';
            i+=1;
        }
        tb += '<td>'+sspc+'<strong>'+ncm.descricao+'</strong></td>';
        tb += '<td>'+ncm.unidade+'</td></tr>';

    }
    tb += '<tbody></table></div>';
    return tb
}
// retorna caixa de modal do filtro NCMS
function return_div_modal_filtro_ncms(){
    nav ='<div class="modal fade" id="modal-filtro-ncms" tabindex="1" role="dialog" '+
    'aria-labelledby="ModalLabel" aria-hidden="true">';
    nav +=  '<div class="modal-dialog" role="document">';
    nav +=      '<div class="modal-content">';
    nav +=          '<div class="modal-header">';
    nav +=              '<h5 class="modal-title" id="ModalLabel">Filtrar NCMS</h5>';
    nav +=              '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    nav +=                  '<span aria-hidden="true">&times;</span>';
    nav +=              '</button>';
    nav +=          '</div>';
    nav +=          '<div class="modal-body">';
    nav +=              '<div class="form-group">';
    nav +=                      '<label class="text-warning" id="label-select-tpfiltro" for="select-tpfiltro" >Filtrar Por</label>'
    nav +=                      '<select class="form-control" id="select-tbfiltro" name="select-tpfiltro" onchange="change_select_ncms_filtrapor(this);">';
    seltpfiltro = (tpfiltro=='0') ? ' selected' : '';
    nav +=                          '<option value="0"'+seltpfiltro+'>Descrição</option>';
    seltpfiltro = (tpfiltro=='1') ? ' selected' : '';
    nav +=                          '<option value="1"'+seltpfiltro+' >Código</option>';
    seltpfiltro = (tpfiltro=='2') ? ' selected' : '';
    nav +=                          '<option value="2"'+seltpfiltro+'>Código que Inicia com:</option>';
    nav +=                      '</select>';
    nav +=              '</div>';
    nav +=              '<div class="form-group">';
    nav +=                  '<label class="text-warning" id="label-desc-tpfiltro-ncms" for="per_page">Descrição</label>';
    nav +=                  '<input name="desc" id="desc-tpfiltro-ncms" value="'+desc+'" type="text" class="form-control">';
    nav +=              '</div>';
    nav +=              '<div class="form-row">';
    nav +=                  '<div class="form-group mr-2">';
    nav +=                      '<label class="text-warning" for="per_page">Grau</label>';
    nav +=                      '<select class="form-control" name="select-grau" id="select-grau">';
    selgrau = (grau=='0') ? ' selected' : '';
    nav +=                          '<option value="0">Todos</option>';
    selgrau = (grau=='1') ? ' selected' : '';
    nav +=                          '<option value="1"'+selgrau+'>1</option>';
    selgrau = (grau=='2') ? ' selected' : '';
    nav +=                          '<option value="2"'+selgrau+'>2</option>';
    selgrau = (grau=='3') ? ' selected' : '';
    nav +=                          '<option value="3"'+selgrau+'>3</option>';
    selgrau = (grau=='4') ? ' selected' : '';
    nav +=                          '<option value="4"'+selgrau+'>4</option>';
    selgrau = (grau=='5') ? ' selected' : '';
    nav +=                          '<option value="5"'+selgrau+'>5</option>';
    selgrau = (grau=='6') ? ' selected' : '';
    nav +=                          '<option value="6"'+selgrau+'>6</option>';
    nav +=                      '</select>';
    nav +=                  '</div>';
    nav +=                  '<div class="form-group">';
    nav +=                      '<label class="text-warning" for="per-page">Total por Página</label>';
    nav +=                      '<select class="form-control" name="per_page" id="per-page">';
    strsel = (per_page=='20')?'selected':'';
    nav +=                          '<option value="20"  '+strsel+'>20</option>';
    strsel = (per_page=='50')?'selected':'';
    nav +=                          '<option value="50"  '+strsel+'>50</option>';
    strsel = (per_page=='100')?'selected':'';
    nav +=                          '<option value="100" '+strsel+'>100</option>';
    nav +=                          '</select>';
    nav +=                  '</div>';
    nav +=              '</div>';
    nav +=          '</div>';
    nav +=          '<div class="modal-footer">';
    nav +=              '<button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>';
    nav +=              '<button type="button" class="btn btn-warning" data-dismiss="modal" onclick="filtrar_ncms();">Filtrar</button>';
    nav +=          '</div>';
    nav +=      '</div>';
    nav +=  '</div></div>';
    return nav;
}
function change_select_ncms_filtrapor(cxselect){
    label_desc = document.getElementById('label-desc-tpfiltro-ncms');
    switch(cxselect.value) {
      case '0':
        label_desc.innerHTML = 'Descrição';
        break;
      case '1':
        label_desc.innerHTML = 'Código';
        break;
      case '2':
        label_desc.innerHTML = 'Código que Inicia com';
        break;
    }
}
// clica botão filtrar
async function filtrar_ncms(){
    per_page = document.getElementById('per-page').value;
    grau = document.getElementById('select-grau').value;
    tpfiltro = document.getElementById('select-tbfiltro').value;
    descfiltro = document.getElementById('desc-tpfiltro-ncms').value;
    await mostrarncms(1,per_page,grau,descfiltro,tpfiltro);
}



// -----------------------------------SEGMENTOS CEST-------------------------------------


// CLICA BOTA SEGMENTOS CEST
async function mostrar_segmentoscest(pagetemp ='1', per_pagetemp = '20',desc=''){
    page = (pagetemp=='0') ? '1' : pagetemp;
    per_page = (per_pagetemp=='0') ? '50' : per_pagetemp;
    removeactivebtns();
    url = '/get/tributacao/segmentoscest/json?page='+page+'&per_page='+per_page+'&desc='+desc;
    let response = await fetch(url);
    if (response.status == 200) {
        await response.json().then(data =>{
           data_segmentoscest = data;
        });
    }
    else{
        return None;
    }
    return_segmentoscest(data_segmentoscest);
}
// RETORNA OS DADOS
function return_segmentoscest(data){
    pageatual = data.pagination.page;
    per_page = data.pagination.per_page;
    desc = data.desc;
    let divsegmentos = '';

    divsegmentos += '<div class="my-2  p-2 text-center text-warning">';
    divsegmentos +='<h2><strong>Segmentos CEST</strong></h2></div>';

     // retorna nav pagination
    divsegmentos += return_nav_link_pagination_segmentoscest(data.pagination.pages,
    data.pagination.total_pages,data.pagination.total,data.desc);
    //retorna table ncms
    divsegmentos += return_table_segmentoscest(data.segmentos_cest);
    content_cst.innerHTML = divsegmentos;
}
// RETORNA PAGINATION E CONSTROI CAIXA DE PESQUISA
function return_nav_link_pagination_segmentoscest(pages,total_pages,totalitemns,descsegmento){

    lblde = ((parseInt(pageatual) * parseInt(per_page)) - parseInt(per_page) + 1);
    lblate =(parseInt(pageatual) * parseInt(per_page));
    lblate = (lblate>parseInt(totalitemns)) ? totalitemns : lblate;
    let nav ='<div class="d-flex justify-content-center">';
    nav += '<label class="text-white">De '+lblde+' até '+lblate+', Página Atual: '+page+', Total de registros: '+totalitemns+' </label>';
    nav += '</div>';
    nav +='<div class="form-row mx-1">';
    nav +='<div class="form-group col-12 col-lg-9">';
    nav +=  '<label class="text-warning" for="desc-segmentocest">Filtrar por Descrição</label>';
    nav +=  '<input class="form-control" value="'+desc+'" id="desc-segmentocest" id="desc-segmentocest" type="text">';
    nav +='</div>';
    nav +='<div class="form-group col-9 col-lg-3">';
    nav +=  '<label class="text-warning" for="select-segmentoscest">Total por página</label>';
    nav +=  '<div class="input-group">';
    nav +=  '<select class="form-control" id="select-segmentoscest">';
    strselseg = (per_page=='5')? ' selected' : '';
    nav +=      '<option value="5"'+strselseg+'>5</option>';
    strselseg = (per_page=='10')? 'selected' : '';
    nav +=      '<option value="10"'+strselseg+'>10</option>';
    strselseg = (per_page=='20')? 'selected' : '';
    nav +=      '<option value="20"'+strselseg+'>20</option>';
    strselseg = (per_page=='50')? 'selected' : '';
    nav +=      '<option value="50"'+strselseg+'>50</option>';
    nav += '</select>';
    nav += '<div class="input-group-append">';
    nav += '<button class="btn btn-warning ml-2" onclick="filtrar_segmentoscest();">Filtrar</button>';
    nav +='</div></div></div>';

    nav += '</div>';
    nav += '<div class="d-flex justify-content-end">';
    nav += '<div class="div-pagination-foods my-2" id="div-pagination-foods">';
    nav += '<nav aria-label="..."><ul class="pagination pagination-sm">';
    for (const pag in pages){
        if (pages[pag] != null){
            if (pages[pag] == pageatual){
                nav += '<li class="page-item active">';
                nav += '<a class="page-link">'+pages[pag]+'<span class="sr-only">(current)</span></a></li>';
            }else
            {
                nav += '<li class="page-item">';
                descfiltrotemp = "'"+descsegmento+"'";
                nav += '<a class="page-link" href="#" '+
                'onclick="mostrar_segmentoscest('+pages[pag]+','+per_page+','+descfiltrotemp+');">'+pages[pag]+'</a></li>';
            }

        }
        else{
            nav += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    nav +='</div>';
    //nav +='<button class="btn btn-warning btn-sm my-auto" data-toggle="modal" data-target="#modal-filtro-ncms">Filtrar</button>';
    nav +='</div>';
    return nav;
}
// BOTAO FILTRAR
function filtrar_segmentoscest(){
    per_page = document.getElementById('select-segmentoscest').value;
    console.log(per_page);
    desc = document.getElementById('desc-segmentocest').value;
    mostrar_segmentoscest(1,per_page,desc);
}
// RETORNA TABLE SEGMENTOS CEST
function return_table_segmentoscest(data){
let tb = '<div class="d-flex justify-content-center">';
    tb += '<table class="table table-dark text-warning">';
    tb += '<thead>';
    tb += '<th scope="col" class="text-white" >#</th>';
    tb += '<th scope="col" class="text-white" >Código</th>';
    tb += '<th scope="col" class="text-white">Descrição</th>';
    tb += '</thead><tbody>';
    cont = (parseInt(pageatual) * parseInt(per_page) - parseInt(per_page));
    for (const row in data){
        seg_cest = data[row];
        item = cont + parseInt(row)+1;
        tb += '<tr><td class="text-muted">'+item+'</td>';
        tb += '<td>'+seg_cest.codsegmentocest+'</td>';
        tb += '<td>'+seg_cest.descricao+'</td></tr>';
    }
    tb += '<tbody></table></div>';
    return tb
}


// -----------------------------------CESTS-------------------------------------


// CLICA BOTAO CESTS
async function mostrar_cests(pagetemp ='1', per_pagetemp = '20',desc='',tpfiltro='0'){
    page = (pagetemp=='0') ? '1' : pagetemp;
    per_page = (per_pagetemp=='0') ? '50' : per_pagetemp;
    removeactivebtns();
    url = '/get/tributacao/cests/json?page='+page+'&per_page='+per_page+'&desc='+desc+'&tpfiltro='+tpfiltro;
    let response = await fetch(url);
    if (response.status == 200) {
        await response.json().then(data =>{
           data_cests = data;
        });
    }
    else{
        return None;
    }
    return_cests(data_cests);
}

// RETORNA OS DADOS
function return_cests(data){
    pageatual = data.pagination.page;
    per_page = data.pagination.per_page;
    desc = data.desc;
    tpfiltro = data.tpfiltro;
    let divcests = return_div_modal_filtro_cests();

    divcests += '<div class="my-2  p-2 text-center text-warning">';
    divcests +='<h2><strong>CESTs - Código Especificador da Substituição Tributária</strong></h2></div>';
    if (data.pagination.total>0){
        // retorna nav pagination
        divcests += return_nav_link_pagination_cests(data.pagination.pages,
        data.pagination.total_pages,data.pagination.total,data.desc);
        //retorna table ncms
        divcests += return_table_cests(data.cests);
    }
    else{
        divcests += '<div class="alert alert-warning text-center text-dark">';
        divcests +=     '<p>Nenhum registro encontrado, Clique no botão Filtrar!</p>';
        divcests +='<button class="btn btn-warning btn-sm my-auto" data-toggle="modal" data-target="#modal-filtro-cests">Filtrar</button>';
        divcests +='</div>';
    }

    content_cst.innerHTML = divcests;
}

// RETORNA PAGINATION E CONSTROI CAIXA DE PESQUISA
function return_nav_link_pagination_cests(pages,total_pages,totalitemns,desccest){

    lblde = ((parseInt(pageatual) * parseInt(per_page)) - parseInt(per_page) + 1);
    lblate =(parseInt(pageatual) * parseInt(per_page));
    lblate = (lblate>parseInt(totalitemns)) ? totalitemns : lblate;
    let nav ='<div class="d-flex justify-content-center">';
    nav += '<label class="text-white">De '+lblde+' até '+lblate+', Página Atual: '+page+', Total de registros: '+totalitemns+' </label>';
    nav += '</div>';
    //nav +='<div class="form-row mx-1">';
    //nav +='<div class="form-group col-9 col-lg-3">';
    //nav +=  '<label class="text-warning" for="select-cest">Total por página</label>';
    //nav +=  '<div class="input-group">';
    //nav += '<div class="input-group-append">';
    //nav += '<button class="btn btn-warning ml-2" onclick="filtrar_cests();">Filtrar</button>';
    //nav +='</div></div></div>';
    //nav += '</div>';
    nav += '<div class="d-flex justify-content-between">';
    nav += '<div class="div-pagination-foods my-2" id="div-pagination-foods">';
    nav += '    <nav aria-label="..."><ul class="pagination pagination-sm">';
    for (const pag in pages){
        if (pages[pag] != null){
            if (pages[pag] == pageatual){
                nav += '<li class="page-item active">';
                nav += '<a class="page-link">'+pages[pag]+'<span class="sr-only">(current)</span></a></li>';
            }else
            {
                nav += '<li class="page-item">';
                descfiltrotemp = "'"+desccest+"'";
                nav += '<a class="page-link" href="#" '+
                'onclick="mostrar_cests('+pages[pag]+','+per_page+','+descfiltrotemp+','+tpfiltro+');">'+pages[pag]+'</a></li>';
            }

        }
        else{
            nav += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    nav +='</div>';
    nav +='<button class="btn btn-warning btn-sm my-auto" data-toggle="modal" data-target="#modal-filtro-cests">Filtrar</button>';
    nav +='</div>';
    return nav;
}

// retorna caixa de modal do filtro CESTS
function return_div_modal_filtro_cests(){
    nav ='<div class="modal fade" id="modal-filtro-cests" tabindex="1" role="dialog" '+
    'aria-labelledby="ModalLabel-cests" aria-hidden="true">';
    nav +=  '<div class="modal-dialog" role="document">';
    nav +=      '<div class="modal-content">';
    nav +=          '<div class="modal-header">';
    nav +=              '<h5 class="modal-title" id="ModalLabel-cests">Filtrar CESTS</h5>';
    nav +=              '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    nav +=                  '<span aria-hidden="true">&times;</span>';
    nav +=              '</button>';
    nav +=          '</div>';
    nav +=          '<div class="modal-body">';
    nav +=              '<div class="form-group">';
    nav +=                      '<label class="text-warning" id="label-select-tpfiltro-cest" for="select-tpfiltro-cest" >Filtrar Por</label>'
    nav +=                      '<select class="form-control" id="select-tbfiltro-cest" name="select-tpfiltro-cest" onchange="change_select_ncms_filtrapor(this);">';
    seltpfiltro = (tpfiltro=='0') ? ' selected' : '';
    nav +=                          '<option value="0"'+seltpfiltro+'>Descrição CEST</option>';
    seltpfiltro = (tpfiltro=='1') ? ' selected' : '';
    nav +=                          '<option value="1"'+seltpfiltro+' >Descrição Segmento CEST</option>';
    seltpfiltro = (tpfiltro=='2') ? ' selected' : '';
    nav +=                          '<option value="2"'+seltpfiltro+' >Código Segmento CEST</option>';
    seltpfiltro = (tpfiltro=='3') ? ' selected' : '';
    nav +=                          '<option value="3"'+seltpfiltro+'>Descrição NCM</option>';
    seltpfiltro = (tpfiltro=='4') ? ' selected' : '';
    nav +=                          '<option value="4"'+seltpfiltro+'>Código NCM que inicia com</option>';
    nav +=                      '</select>';
    nav +=              '</div>';
    nav +=              '<div class="form-group">';
    nav +=                  '<label class="text-warning" for="desc-cest">Filtrar por Descrição</label>';
    nav +=                  '<input class="form-control" value="'+desc+'" id="desc-cest" id="desc-cest" type="text">';
    nav +=              '</div>';
    nav +=              '<div class="form-row">';
    nav +=                  '<div class="form-group">';
    nav +=                      '<label class="text-warning" for="per-page">Total por Página</label>';
    nav +=                      '<select class="form-control" id="select-cest">';
    strselseg = (per_page=='5')? ' selected' : '';
    nav +=                          '<option value="5"'+strselseg+'>5</option>';
    strselseg = (per_page=='10')? 'selected' : '';
    nav +=                          '<option value="10"'+strselseg+'>10</option>';
    strselseg = (per_page=='20')? 'selected' : '';
    nav +=                          '<option value="20"'+strselseg+'>20</option>';
    strselseg = (per_page=='50')? 'selected' : '';
    nav +=                          '<option value="50"'+strselseg+'>50</option>';
    nav +=                      '</select>';

    nav +=                  '</div>';
    nav +=              '</div>';
    nav +=          '</div>';
    nav +=          '<div class="modal-footer">';
    nav +=              '<button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>';
    nav +=              '<button type="button" class="btn btn-warning" data-dismiss="modal" onclick="filtrar_cests();">Filtrar</button>';
    nav +=          '</div>';
    nav +=      '</div>';
    nav +=  '</div></div>';
    return nav;
}

// BOTAO FILTRAR
function filtrar_cests(){
    per_page = document.getElementById('select-cest').value;
    console.log(per_page);
    desc = document.getElementById('desc-cest').value;
    tpfiltro = document.getElementById('select-tbfiltro-cest').value;
    mostrar_cests(1,per_page,desc,tpfiltro);
}
// MONTA <TABLE> CESTS
function return_table_cests(data){
let tb = '<div class="d-flex justify-content-center">';
    tb += '<table class="table table-dark text-warning">';
    tb += '<thead>';
    tb += '<th scope="col" class="text-white" >#</th>';
    tb += '<th scope="col" class="text-white" >Código</th>';
    tb += '<th scope="col" class="text-white">Descrição</th>';
    tb += '<th scope="col" class="text-white">Segmento</th>';
    tb += '<th scope="col" class="text-white">NCM</th>';
    tb += '</thead><tbody>';
    cont = (parseInt(pageatual) * parseInt(per_page) - parseInt(per_page));
    for (const row in data){
        cest = data[row];
        item = cont + parseInt(row)+1;
        tb += '<tr><td class="text-muted">'+item+'</td>';
        tb += '<td>'+cest.codcest+'</td>';
        tb += '<td>'+cest.descricao+'</td>';
        tb += '<td class="align-middle text-center">'+cest.segmentocest.codsegmentocest+' <br> '+cest.segmentocest.descricao+'</td>';
        tb += '<td class="align-middle text-center">'+cest.ncm.codncm+' <br> '+cest.ncm.descricao+'</td>';
        tb +='</tr>';
    }
    tb += '<tbody></table></div>';
    return tb
}




// BUSCA MEDICAMENTOS
async function get_medicamentos(page_,per_page_,desc_,tpfiltro_){

    url = '/get/anvisa/medicamentos/json?page='+page_+'&per_page='+per_page_+'&tpfiltro='+tpfiltro_+'&desc='+desc_;
    let response = await fetch(url);
    if(response.status == 200){
        await response.json().then(data => {
            data_tab = data;
        });
    }
    else{
        data_tab = [];
    }
}

// RETORNA DIV PAGINATION
function return_div_pagination(pages){
    nav = '<div class="d-flex justify-content-between">';
    nav += '<div class="div-pagination-foods my-2" id="div-pagination-foods">';
    nav += '    <nav aria-label="..."><ul class="pagination pagination-sm">';
    for (const pag in pages){
        console.log(pag);
        if (pages[pag] != null){
            if (pages[pag] == pageatual){
                nav += '<li class="page-item active">';
                nav += '<a class="page-link">'+pages[pag]+'<span class="sr-only">(current)</span></a></li>';
            }else
            {
                nav += '<li class="page-item">';
                descfiltrotemp = "'"+descsearch+"'";
                nav += '<a class="page-link" href="#" '+
                'onclick="mostrar_medicamentos('+pages[pag]+','+per_page+','+descfiltrotemp+','+tpfiltro+');">'+pages[pag]+'</a></li>';
            }

        }
        else{
            nav += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    nav +='</div>';
    nav +='<button class="btn btn-warning btn-sm my-auto" data-toggle="modal" data-target="#modal-filtro">Filtrar</button>';
    nav +='</div>';
    return nav;

}

// RETORNA <TABLE> ATRAVES DOS DADOS DA CONSULTA
function return_table_medicamentos(data){
    let tb = '<div class="d-flex justify-content-center">';
    tb += '<table class="table table-dark text-warning">';
    tb += '<thead>';
    tb += '<th scope="col" class="text-white" >#</th>';
    tb += '<th scope="col" class="text-white" >Registro</th>';
    tb += '<th scope="col" class="text-white">Descrição</th>';
    tb += '<th scope="col" class="text-white d-none d-lg-block d-xl-block">Apresentaçao</th>';
    tb += '</thead><tbody>';
    cont = (parseInt(pageatual) * parseInt(per_page) - parseInt(per_page));
    for (const row in data){
        meds = data[row];
        item = cont + parseInt(row)+1;
        tb += '<tr><td class="align-middle text-center">'+
        '<label class="text-muted mr-2">'+item+'</label></td>';
        tb += '<td>'+meds.registro+'</td>';
        tb += "<td><a href='#' onclick='mostrar_dados_medicamento("+JSON.stringify(meds)+");'"+
        "data-toggle='modal' data-target='#modal-dados-medicamento' class='text-warning'>"+
        meds.descricao+"</a></td>";
        tb += '<td class="d-none d-lg-block d-xl-block ">'+meds.apresentacao+'</td>';

        tb +='</tr>';
    }
    tb += '<tbody></table></div>';
    return tb
}

// CLICA LINK NOME DO MEDICAMENTO
async function mostrar_dados_medicamento(tb_data){
 console.log(tb_data);
 url = '/get/anvisa/medicamento/'+tb_data.id+'/tabelapreco/json';
 let tb_preco = []
 let response = await fetch(url);
 if(response.status == 200){
    await response.json().then(data => {
        tb_preco = data.data[0];
    });
 }
 else{
    data_tbpreco = [];
 }

 document.getElementById('modal-body-medicamento').innerHTML = div_colapse_data(tb_data,tb_preco);
 document.getElementById('ModalLabel-medicamento').innerHTML = 'Dados medicamentos '+tb_data.descricao;
}

// CRIA MODAL DOS DADOS DO MEDICAMENTO
function modal_dados_medicamento(){
    nav ='<div class="modal fade" id="modal-dados-medicamento" tabindex="1" role="dialog" '+
    'aria-labelledby="ModalLabel-medicamento" aria-hidden="true">';
    nav +=  '<div class="modal-dialog" role="document">';
    nav +=      '<div class="modal-content">';
    nav +=          '<div class="modal-header">';
    nav +=              '<h5 class="modal-title" id="ModalLabel-medicamento"></h5>';
    nav +=              '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    nav +=                  '<span aria-hidden="true">&times;</span>';
    nav +=              '</button>';
    nav +=          '</div>';
    nav +=          '<div class="modal-body" id="modal-body-medicamento" >';
    nav +=          '</div>';
    nav +=          '<div class="modal-footer">';
    nav +=              '<button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>';
    nav +=          '</div>';
    nav +=      '</div>';
    nav +=  '</div></div>';
    return nav;
}

// CRIA DIV COLAPSE(PAGE CONTROL) DOS DADOS GERAIS E TABELA DE PRECO
function hide_btn_dadosgerais(index_btn,data){
    console.log(data);
    let div = '';
    switch (index_btn){
        case 0:
            console.log('0');
            document.getElementById('collapse-tabpreco').classList.add('d-none');
            document.getElementById('collapse-dadosgerais').classList.remove('d-none');
            div += '<div class="card card-body bg-primary">';
            div +=      '<div class="d-flex justify-content-center"><h3>Dados Gerais</h3></div>'
            div += '</div>';
            document.getElementById('collapse-dadosgerais').innerHTML = div;
            break;
        case 1:
            console.log('1');
            document.getElementById('collapse-dadosgerais').classList.add('d-none');
            document.getElementById('collapse-tabpreco').classList.remove('d-none');
            div += '<div class="card card-body bg-primary">';
            div +=      '<div class="d-flex justify-content-center"><h3>Tabela de Preços</h3></div>'
            div += '</div>';
            document.getElementById('collapse-tabpreco').innerHTML = div;
            break;
    }
}
function div_colapse_data(tb_data,tb_preco){

    div = "<div><button class='btn btn-warning mr-1' type='button'"+
          " onclick='hide_btn_dadosgerais(0,"+JSON.stringify(tb_data)+");'>Dados Gerais</button>";
    div +="<button class='btn btn-warning ml-1' type='button'"+
          " onclick='hide_btn_dadosgerais(1,"+JSON.stringify(tb_preco)+");' >Tabela de Preços</button></div>";
    div +='<div class="d-none" id="collapse-dadosgerais">';
    div +='</div>';
    div +='<div class="d-none" id="collapse-tabpreco">';
    div +='</div>';
    return div;
}

// RETORNA HTML DIV MODAL DA TELA DE FILTRO
function return_div_modal_filtro(){
    nav ='<div class="modal fade" id="modal-filtro" tabindex="1" role="dialog" '+
    'aria-labelledby="ModalLabel" aria-hidden="true">';
    nav +=  '<div class="modal-dialog modal-lg">';
    nav +=      '<div class="modal-content">';
    nav +=          '<div class="modal-header">';
    nav +=              '<h5 class="modal-title" id="ModalLabel">Filtrar Medicamentos</h5>';
    nav +=              '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    nav +=                  '<span aria-hidden="true">&times;</span>';
    nav +=              '</button>';
    nav +=          '</div>';
    nav +=          '<div class="modal-body">';
    nav +=              '<div class="form-group">';
    nav +=                      '<label class="text-warning" id="label-desc-tpfiltro" for="select-tpfiltro" >Filtrar Por</label>'
    nav +=                      '<select class="form-control" id="select-tpfiltro" name="select-tpfiltro" onchange="change_select_filtrapor(this);">';

    seltpfiltro = (tpfiltro=='0') ? ' selected' : '';
    nav +=                          '<option value="0"'+seltpfiltro+'>Medicamento</option>';

    seltpfiltro = (tpfiltro=='2') ? ' selected' : '';
    nav +=                          '<option value="2"'+seltpfiltro+' >Substância</option>';

    seltpfiltro = (tpfiltro=='3') ? ' selected' : '';
    nav +=                          '<option value="3"'+seltpfiltro+'>Classe Terapeutica</option>';

    seltpfiltro = (tpfiltro=='4') ? ' selected' : '';
    nav +=                          '<option value="4"'+seltpfiltro+' >Laboratório</option>';

    seltpfiltro = (tpfiltro=='5') ? ' selected' : '';
    nav +=                          '<option value="5"'+seltpfiltro+'>Tipo de Medicamento</option>';

    seltpfiltro = (tpfiltro=='6') ? ' selected' : '';
    nav +=                          '<option value="6"'+seltpfiltro+'>Tipo de Tarja</option>';

    nav +=                      '</select>';
    nav +=              '</div>';
    nav +=              '<div class="form-group">';
    nav +=                  '<label class="text-warning" for="desc-input" id="label-desc-input">Medicamento</label>';
    nav +=                  '<input class="form-control" value="'+descsearch+'" id="desc-input" type="text">';
    nav +=              '</div>';
    nav +=              '<div class="form-row">';
    nav +=                  '<div class="form-group">';
    nav +=                      '<label class="text-warning" for="per-page">Total por Página</label>';
    nav +=                      '<select class="form-control" id="select-perpage-filtro">';
    strselseg = (per_page=='20')? ' selected' : '';
    nav +=                          '<option value="20"'+strselseg+'>20</option>';
    strselseg = (per_page=='50')? 'selected' : '';
    nav +=                          '<option value="50"'+strselseg+'>50</option>';
    strselseg = (per_page=='100')? 'selected' : '';
    nav +=                          '<option value="100"'+strselseg+'>100</option>';
    strselseg = (per_page=='150')? 'selected' : '';
    nav +=                          '<option value="150"'+strselseg+'>150</option>';
    nav +=                      '</select>';

    nav +=                  '</div>';
    nav +=              '</div>';
    nav +=          '</div>';
    nav +=          '<div class="modal-footer">';
    nav +=              '<button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>';
    nav +=              '<button type="button" class="btn btn-warning" data-dismiss="modal" onclick="filtrar_medicamentos();">Filtrar</button>';
    nav +=          '</div>';
    nav +=      '</div>';
    nav +=  '</div></div>';
    return nav;
}

// CHANGE DO TIPO DO FILTRO ESCOLHIDO
function change_select_filtrapor(selectfil){
    label_desc = document.getElementById('label-desc-input');
    switch(selectfil.value) {
      case '0':
        label_desc.innerHTML = 'Medicamento';
        break;
      case '2':
        label_desc.innerHTML = 'Substância';
        break;
      case '3':
        label_desc.innerHTML = 'Classe Terapeutica';
        break;
      case '4':
        label_desc.innerHTML = 'Laboratório';
        console.log(label_desc.innerHTML);
        break;
      case '5':
        label_desc.innerHTML = 'Tipo de Medicamento';
        break;
      case '6':
        label_desc.innerHTML = 'Tipo de Tarja';
        break;

    }
}

//CLICA NO BOTÃO FILTRAR DA TELA DE MODAL DE FILTRO
function filtrar_medicamentos(){
    sel_filtro = document.getElementById('select-tpfiltro').value;
    desc_input = document.getElementById('desc-input').value;
    per_page_filtro = document.getElementById('select-perpage-filtro').value;
    mostrar_medicamentos(1,per_page_filtro,desc_input,sel_filtro);
}

// CLICA NO BTÃO MEDICAMENTO OU CLICA NO NUMERO DO PAGINATION OU DE ACORDO COM O FILTRO E ESPERA O RESULTADO DA CONSULTA
async function mostrar_medicamentos(page_,per_page_,desc_,tpfiltro_){
    loading_hold('medicamentos');
    removeactivebtns();
    document.getElementById('btn_medicamentos').classList.add('active');
    await get_medicamentos(page_,per_page_,desc_,tpfiltro_);

    update_var(data_tab);
    divs = return_div_modal_filtro();
    divs += modal_dados_medicamento();
    divs += return_header_data_table(data_tab.pagination,'Medicamentos');
    divs += return_div_pagination(data_tab.pagination.pages, descsearch);

    divs += (data_tab.pagination.total > 0) ? return_table_medicamentos(data_tab.data) : '';
    content_anvisa.innerHTML = divs;
}





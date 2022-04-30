var content_anvisa = document.getElementById('content-anvisa');
var data_tab = [];
var pageatual = '1';
var per_page = '50';
var descsearch = '';
var tpfiltro = '0';

function removeactivebtns(){
    document.getElementById('btn_laboratorios').classList.remove('active');
    document.getElementById('btn_substancias').classList.remove('active');
    document.getElementById('btn_classes_terapeuticas').classList.remove('active');
    document.getElementById('btn_tipos_medicamentos').classList.remove('active');
    document.getElementById('btn_medicamentos').classList.remove('active');
}
function loading_hold(table){
    str = '<div class="spinner-border text-warning p-2" role="status">'+
    '<span class="sr-only">aguarde...</span></div>'+
    '<label class="text-warning ml-2"> Aguarde... Carregando '+ table +' </label>';
     content_anvisa.innerHTML = str;
}

function return_header_data_table(pagination,title){
    let div = '';
    if (pagination.total > 0){
        totalitens = pagination.total;
        totalpage = pagination.total_pages;
        lblde = ((parseInt(pageatual) * parseInt(per_page)) - parseInt(per_page) + 1);
        lblate =(parseInt(pageatual) * parseInt(per_page));
        lblate = (lblate>parseInt(totalitens)) ? totalitens : lblate;
        div = '<div class="row mt-2 d-flex justify-content-center"><h3 class="text-white">'+title+'</h3></div>';
        div +='<div class="d-flex justify-content-center">';
        div += '<label class="text-muted">De '+lblde+' até '+lblate+', Página Atual: '+pageatual+' de '+totalpage+
        ', Total de registros: '+totalitens+' </label>';
        div += '</div>';
    }
    else{
        switch (tpfiltro){
            case '0':
                desctpfiltro = ' o medicamento: ';
                break;
            case '1':
                desctpfiltro = ' a apresentação: ';
                break;
            case '2':
                desctpfiltro = ' a substância: ';
                break;
            case '3':
                desctpfiltro = ' a classe terapeutica: ';
                break;
            case '4':
                desctpfiltro = ' o laboratório: ';
                break;
            case '5':
                desctpfiltro = ' o tipo de medicamento: ';
                break;
            case '6':
                desctpfiltro = ' a tarja: ';
                break;
        }

        strmsg = (descsearch != '') ? 'Nenhum medicamento encontrado com '+desctpfiltro+descsearch : 'Nenhum medicamento encontrado';
        div = '<div class="row my-2 d-flex justify-content-center"><h3 class="text-white">'+title+'</h3></div>';
        div +='<div class="d-flex justify-content-center">';
        div +='<div class="alert alert-warning text-center" role="alert">';
        div += '<label class="text-muted">'+strmsg+'</label></div></div>';
    }
    return div;
}
function update_var(data){
    console.log(data);
    pageatual = data.pagination.page;
    per_page =  data.pagination.per_page;
    descsearch = data.desc;
    tpfiltro = data.tpfiltro;

}
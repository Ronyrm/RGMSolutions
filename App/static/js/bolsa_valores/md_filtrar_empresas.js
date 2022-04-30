var array_setores = [];
var array_subsetores = [];
var optionsSetores = '';
var arrayopt = {};

var optionsSubSetores = '';
var idsSetores = [];
var stridSetores = '';
var idSetorSelected = 0;
var nameSetorSelected = '';
var aidsetor = [];

function return_ModalFiltrar(){

    selectOptOne = (tipo_filtro == 0) ? 'selected' : '';
    selectOptTwo = (tipo_filtro == 1) ? 'selected' : '';
    selectOptTree = (tipo_filtro == 2) ? 'selected' : '';
    selectOptFour = (tipo_filtro == 3) ? 'selected' : '';
    selectOptFive = (tipo_filtro == 4) ? 'selected' : '';
    selectOptSix = (tipo_filtro == 5) ? 'selected' : '';

    selectedEmpAtv = '';
    selectedEmpNoAtv = '';
    selectedEmpAll = '';
    switch (empAtiva_filtro){
        case 'S':
            selectedEmpAtv = 'selected';
            break;
        case 'N':
            selectedEmpNoAtv = 'selected';
            break;
        default:
            selectedEmpAll = 'selected';
            break;
    }


    div =
    '<div class="form-group text-warning">'+
        '<label for="select-tipo">Filtro Prontos</label>'+
        '<select class="form-control" id="select-tipo" onchange="changeSelectFiltro(this.value);">'+
            '<option value=0 '+selectOptOne+'>Todos</option>'+
            '<option value=1 '+selectOptTwo+'>Que Contenha cotações</option>'+
            '<option value=2 '+selectOptTree+'>Que não Contenha cotações</option>'+
            '<option value=3 '+selectOptFour+'>Que contenha pagamentos de dividendos nos últimos 5 anos</option>'+
            '<option value=4 '+selectOptFive+'>Que apresentam maior percentual dividendos yield atualmente</option>'+
            '<option value=5 '+selectOptSix+'>Personalizar</option>'+
        '</select>'+
    '</div>'+
    /*DIV PERSONALIZAR*/
    '<div class="form-group text-warning d-none" id="div-personalite">'+
        '<div class="form-row">'+
            '<div class="col mx-1 p-2">'+
                '<div class="form-check" >';
    checked_Dividendos = (aFilterDividends.length > 0) ? 'checked' : '';
    valDividendosDe= 0;
    valDividendosAte= 0;
    if (checked_Dividendos == 'checked'){

        valDividendosDe= aFilterDividends[0];
        valDividendosAte= aFilterDividends[1];

    }
    div +=
                    '<input class="form-check-input" type="checkbox" '+checked_Dividendos+' onchange="change_chkDividends(this);" id="chk-dividends">'+
                    '<label class´="form-check-label text-warning" for="chk-dividends">Dividendos yield</label>'+
                '</div>'+
            '</div>'+
            '<div class="col-7 d-none" id="div-val-dividends">'+
                '<div class="row d-flex justify-content-start">'+
                    '<label>De:</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valDividendosDe+'" id="input-dividends-de">'+
                    '</div>'+
                    '<label>a</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valDividendosAte+'" id="input-dividends-ate">'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<small class="text-danger d-none" id="small-dividends"></small>'+
        '<hr class="solid"></hr>'+


        /* P/L */
        '<div class="form-row">'+
            '<div class="col mx-1 p-2">'+
                '<div class="form-check" >';
    checked_PL = (aFilterPL.length > 0) ? 'checked' : '';
    valPLDe= 0;
    valPLAte= 0;
    if (checked_PL == 'checked'){
        valPLDe= aFilterPL[0];
        valPLAte= aFilterPL[1];
    }
    div +=
                    '<input class="form-check-input" '+checked_PL+' type="checkbox" onchange="change_chkpl(this);" id="chk-pl">'+
                    '<label class´="form-check-label text-warning" for="chk-pl">P/L</label>'+
                '</div>'+
            '</div>'+
            '<div class="col-7 d-none" id="div-val-pl">'+
                '<div class="row d-flex justify-content-start">'+
                    '<label>De:</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valPLDe+'" id="input-pl-de">'+
                    '</div>'+
                    '<label>a</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valPLAte+'" id="input-pl-ate">'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<small class="text-danger d-none" id="small-pls"></small>'+
        '<hr class="solid"></hr>'+


        /* P/VPA */
        '<div class="form-row">'+
            '<div class="col mx-1 p-2">'+
                '<div class="form-check" >';
    checked_PVPA = (aFilterPVPA.length > 0) ? 'checked' : '';
    valPVPADe= 0;
    valPVPAAte= 0;
    if (checked_PVPA == 'checked'){
        valPVPADe= aFilterPVPA[0];
        valPVPAAte= aFilterPVPA[1];
    }
    div +=
                    '<input class="form-check-input" '+checked_PVPA+' type="checkbox" onchange="change_chkpvpa(this);" id="chk-pvpa">'+
                    '<label class´="form-check-label text-warning" for="chk-pvpa">P/VPA</label>'+
                '</div>'+
            '</div>'+
            '<div class="col-7 d-none" id="div-val-pvpa">'+
                '<div class="row d-flex justify-content-start">'+
                    '<label>De:</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valPVPADe+'" id="input-pvpa-de">'+
                    '</div>'+
                    '<label>a</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valPVPAAte+'" id="input-pvpa-ate">'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<small class="text-danger d-none" id="small-pvpas"></small>'+
        '<hr class="solid"></hr>'+


        /* Valor da Cotacao */
        '<div class="form-row">'+
            '<div class="col mx-1 p-2">'+
                '<div class="form-check" >';
    checked_ValCotacao = (aFilterValCotacao.length > 0) ? 'checked' : '';
    valCotacaoDe= 0;
    valCotacaoAte= 0;
    if (checked_ValCotacao == 'checked'){
        valCotacaoDe= aFilterValCotacao[0];
        valCotacaoAte= aFilterValCotacao[1];
    }
    div +=
                    '<input class="form-check-input" '+checked_ValCotacao+' type="checkbox" onchange="change_chkvalcotacao(this);" id="chk-valcotacao">'+
                    '<label class´="form-check-label text-warning" for="chk-valcotacao">Valor da Cotação</label>'+
                '</div>'+
            '</div>'+
            '<div class="col-7 d-none" id="div-val-cotacao">'+
                '<div class="row d-flex justify-content-start">'+
                    '<label>De:</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valCotacaoDe+'" id="input-valcotacao-de">'+
                    '</div>'+
                    '<label>a</label>'+
                    '<div class="col">'+
                        '<input type="number"  class="form-control" value="'+valCotacaoAte+'" id="input-valcotacao-ate">'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<small class="text-danger d-none" id="small-valcotacao"></small>'+
        '<hr class="solid"></hr>'+
        /* SETORES */
        '<div class="form-row">'+
            '<div class="col mx-1 p-2">'+
                '<div class="form-check" >';
    checked_Setores = (aFilterSetores.length > 0) ? 'checked' : '';
    if (checked_Setores != 'checked'){
        idsSetores = [];
    }
    div +=
                    '<input class="form-check-input" '+checked_Setores+' type="checkbox" onchange="change_chksetores(this);" id="chk-Setores">'+
                    '<label class´="form-check-label text-warning" for="chk-Setores">Setores</label>'+
                '</div>'+
            '</div>'+
            '<div class="col-9 d-none" id="div-setores">'+
                '<div class="input-group">'+
                        ' <input list="brownser-setores"  placeholder="Escolha aqui o Setor"'+
                        ' class="form-control form-control-sm" id="edtnomesetor"'+
                        ' oninput="changeBrownserSetores(this.value);">'+
                        '<datalist id="brownser-setores" data-model-name="brownser-setores">';

            div += fillOptionSetores();
            div +=
                        '</datalist>'+
                        '<input type="hidden" id="edtdescsetor">'+
                        '<input type="hidden" id="edtidsetores">'+
                    '<div class="input-group-append">'+
                        '<button class="btn btn-warning btn-sm" id="btnAddRemoveSetor" onclick="addremoveSetores();"><span class="glyphicon glyphicon-check"></span></butoon>'+
                    '</div>'+
                '</div>'+
                '<small class="text-danger d-none" id="small-setor"> Forneça ao menos um Setor</small>'+
            '</div>'+
        '</div>'+
    '</div>'+
    '<div class="form-row text-warning" id="div-limit-ativa">'+
        /*DIV LIMITE*/
        '<div class="col text-warning d-none" id="div-limit">'+
            '<label for="input-limit">Limite de Registro:</label>'+
            '<input class="form-control" value="'+limit_filtro+'" type="number" id="input-limit">'+
            '<small id="small-limit" class="d-none text-danger">Forneça um Limite  maior ou igual a 10</small>'+
        '</div>'+
        /*DIV ATIVAS OU NAO*/
        '<div class="col text-warning" id="div-ativa">'+
            '<label for="select-ativa">Ativa</label>'+
            '<select class="form-control" id="select-ativa">';
        div +=
                '<option value="S" '+selectedEmpAtv+'>Sim</option>'+
                '<option value="N" '+selectedEmpNoAtv+'>Não</option>'+
                '<option value="W" '+selectedEmpAll+'>Todas</option>'+
            '</select>'+
        '</div>'+
    '</div>'+
    /*DIV ORDER BY*/
    '<div class="form-row text-warning" id="div-orderby">'+
        '<div class="col">'+
            '<label for="select-orderby">Ordenar Por:</label>'+
            '<select class="form-control" id="select-orderby" onchange="changeOrderBY(this.value,0);">';
    selectOptOne = (orderby_filtro == 0) ? 'selected' : '';
    selectOptTwo = (orderby_filtro == 1) ? 'selected' : '';
    selectOptTree = (orderby_filtro == 2) ? 'selected' : '';
    selectOptFour = (orderby_filtro == 3) ? 'selected' : '';
    selectOptFive = (orderby_filtro == 4) ? 'selected' : '';
    selectOptSix = (orderby_filtro == 5) ? 'selected' : '';
    div +=
                '<option value="0" '+selectOptOne+'>Nome Empresa</option>'+
                '<option value="1" '+selectOptTwo+'>Valor Cotação</option>'+
                '<option value="2" '+selectOptTree+'>Valor Dividendos</option>'+
                '<option value="3" '+selectOptFour+'>Valor P/L</option>'+
                '<option value="4" '+selectOptFive+'>Variação Cotação</option>'+
                '<option value="5" '+selectOptSix+'>Variação P/VPA</option>'+
            '</select>'+
        '</div>'+
        '<div class="col">'+
            '<label for="select-tipo-order">Tipo Ordenamento</label>'+
            '<select class="form-control" id="select-tipo-order">';
    selectOptOne = (tipoorder_filtro == 'ASC') ? 'selected' : '';
    selectOptTwo = (tipoorder_filtro == 'DESC') ? 'selected' : '';
    div +=
                '<option value="ASC" '+selectOptOne+'>Crescente</option>'+
                '<option value="DESC" '+selectOptTwo+'>Descrescente</option>'+
            '</select>'+
        '</div>'+
    '</div>';
    return div;
}

async function loadingFieldModalFilter(){
    document.getElementById('modal-body-filtrar-empresas').innerHTML = await return_ModalFiltrar();
    changeSelectFiltro(document.getElementById("select-tipo").value);
    changeOrderBY(orderby_filtro,tipoorder_filtro);
    change_chkDividends(document.getElementById("chk-dividends"));
    change_chkpl(document.getElementById("chk-pl"));
    change_chkpvpa(document.getElementById("chk-pvpa"));
    change_chkvalcotacao(document.getElementById("chk-valcotacao"));
    change_chksetores(document.getElementById("chk-Setores"));
    verifySetoresSelected();
}

function changeOrderBY(valSelect,tporder){
    sel_TPOrder = document.getElementById('select-tipo-order');
    optTP = '';
    selected_ASC = (tporder == 'ASC') ? 'selected' : '';
    selected_DESC = (tporder == 'DESC') ? 'selected' : '';

    switch (parseInt(valSelect)){
        case 0:
            optTP = '<option value="ASC" '+selected_ASC+'>de A a Z</option>'+
                    '<option value="DESC" '+selected_DESC+'>de Z a A </option>';
            break;
        case 1:
            optTP = '<option value="ASC" '+selected_ASC+'>Maior Valor</option>'+
                    '<option value="DESC" '+selected_DESC+'>Menor Valor</option>';
            break;
        case 2:
            optTP = '<option value="ASC" '+selected_ASC+'>Menores Dividendos</option>'+
                    '<option value="DESC" '+selected_DESC+'>Maiores Dividendos</option>';
            break;
        case 3:
            optTP = '<option value="ASC" '+selected_ASC+'>Menores P/L</option>'+
                    '<option value="DESC" '+selected_DESC+'>Maiores P/L</option>';
            break;
        case 4:
            optTP = '<option value="ASC" '+selected_ASC+'>Maiores Baixas</option>'+
                    '<option value="DESC" '+selected_DESC+'>Maiores Altas</option>';
            break;
        case 5:
            optTP = '<option value="ASC" '+selected_ASC+'>Menores P/VPA</option>'+
                    '<option value="DESC" '+selected_DESC+'>Maiores P/VPA</option>';
            break;

    }
    sel_TPOrder.innerHTML = optTP;
}



/*Captura dados Setores */
function fillOptionSetores(){
    opt = '';
    arrayopt.forEach(setor =>{
        index = aFilterSetores.find(el => el == setor.id)
        if (index){
            idsSetores.push([setor.id,setor.name]);
        }

        opt +=
        '<option value="'+setor.name+'" '+
        ' data-value="'+setor.id+'">';
    });
    return opt;
}
// BUSCA TABELA DE SETORES E RETORNA JSON ARRAY
async function fillArraySetores(){
    url = '/get/setores/all/bolsavalores';

    const arraysetores = await fetch(url)
            .then(response => response.json())
            .then(data => data.data)
            .then(setores => {
                return setores});
    return arraysetores;


}

/*Change Selecao Setores*/
function changeBrownserSetores(idSetor){
    btnAddRemoveSetor = document.getElementById("btnAddRemoveSetor");
    optionSelected = document.querySelector('option[value="'+idSetor+'"]');
    if (optionSelected){
        idSetorSelected = parseInt(optionSelected.getAttribute('data-value'));
        nameSetorSelected = optionSelected.getAttribute('value');
        aidsetor =  idsSetores.find(setor => setor[0]==idSetorSelected);
        if (aidsetor){
            btnAddRemoveSetor.innerHTML = '<span class="glyphicon glyphicon-remove">';
        }
        else{
            btnAddRemoveSetor.innerHTML = '<span class="glyphicon glyphicon-check">';
        }
    }
}

/*Adiciona ou Remove setor da pesquisa*/
function addremoveSetores(){
    if(aidsetor){
        NewidsSetores = idsSetores.filter(setor => setor[0]!=idSetorSelected);
        idsSetores = NewidsSetores;
    }
    else{

        if (idSetorSelected != 0) {
            console.log(nameSetorSelected);
            idsSetores.push([idSetorSelected,nameSetorSelected]);

        }
    }
    idSetorSelected = 0;
    nameSetorSelected = '';
    document.querySelector('#edtnomesetor').value='';
    verifySetoresSelected();

}
function verifySetoresSelected(){
    small_setor = document.getElementById('small-setor');
    small_setor.classList.add('d-none');
    console.log(idsSetores);
    if(idsSetores.length > 0){
        small_setor.classList.remove('d-none');
        str = '';
        stridSetores = '';
        idsSetores.forEach((setor) =>{
            stridSetores += setor[0]+',';
            str += setor[1]+',';
        });
        stridSetores = stridSetores.substr(0,stridSetores.length-1);
        small_setor.innerHTML = str.substr(0,str.length-1);
    }
}


/*Change tipo de filtro*/
async function changeSelectFiltro(selectValue){
    div_limit = document.getElementById('div-limit');
    div_personalite = document.getElementById('div-personalite');

    switch (parseInt(selectValue)) {
        case 0:
            div_limit.classList.add('d-none');
            break;
        case 3:
        case 4:
            div_limit.classList.remove('d-none');
            break;
        case 5:
            div_personalite.classList.remove('d-none');
            url = '/get/setores/all/bolsavalores';


            div_limit.classList.remove('d-none');
            break;
        default:
            div_personalite.classList.add('d-none');
            break;
    }


}

/*Change Dividendos*/
function change_chkDividends(check){
    div_dividends = document.getElementById('div-val-dividends');
    div_dividends.classList.add('d-none');
    if(check.checked){
        div_dividends.classList.remove('d-none');
    }
}


function change_chksetores(check){
    div_setores = document.getElementById('div-setores');
    div_setores.classList.add('d-none');
    if(check.checked){
        div_setores.classList.remove('d-none');
    }
}
function change_chkpl(check){
    div_PL = document.getElementById('div-val-pl');
    div_PL.classList.add('d-none');
    if(check.checked){
        div_PL.classList.remove('d-none');
    }
}
function change_chkpvpa(check){
    div_PVPA = document.getElementById('div-val-pvpa');
    div_PVPA.classList.add('d-none');
    if(check.checked){
        div_PVPA.classList.remove('d-none');
    }
}
function change_chkvalcotacao(check){
    div_valcotacao = document.getElementById('div-val-cotacao');
    div_valcotacao.classList.add('d-none');
    if(check.checked){
        div_valcotacao.classList.remove('d-none');
    }
}

function clickFilltrarEmpresas(){''
    select_tipo = parseInt(document.getElementById('select-tipo').value);
    select_ativa = document.getElementById('select-ativa');
    input_limit = document.getElementById('input-limit');
    document.getElementById('small-limit').classList.add('d-none');
    document.getElementById('small-setor').classList.add('d-none');

    filterValPL = '';
    filterValDividends = '';
    filterValcotacao = '';
    filterSetores = '';
    filterValPVPA = '';
    tipo_order = '0';
    orderby = 'ASC';

    filtrar = true;
    urlfilter = '';
    console.log(select_tipo);
    switch (select_tipo){
        case 3:
        case 4:
            if (input_limit.value < 10 ){
                document.getElementById('small-limit').classList.remove('d-none');
                filtrar = false;
            }
            else{
                urlfilter = 'tipo='+select_tipo+'&limit='+input_limit.value;
            }
            break;
        default:
            urlfilter = 'tipo='+select_tipo;
            break;
    }

    if(select_tipo == 5){
        small_pls = document.querySelector('#small-pls');
        small_pls.classList.add('d-none');
        small_dividends = document.querySelector('#small-dividends');
        small_dividends.classList.add('d-none');
        small_valcotacao = document.querySelector('#small-valcotacao');
        small_valcotacao.classList.add('d-none');

        ValPL = '';
        ValDividens = '';
        ValCotacao = '';
        filterPL = 'N';

        chk_dividends = document.querySelector('#chk-dividends');

        vdividends_de =  parseFloat(document.querySelector('#input-dividends-de').value);
        vdividends_ate = parseFloat(document.querySelector('#input-dividends-ate').value);

        let msg = '';
        /* Comparar DIVIDENDOS*/
        if ((chk_dividends.checked) && (vdividends_de<= 0) && (vdividends_ate<=0)){
            msg += (vdividends_de <= 0 )? 'Forneça o valor Dividendos que começa.' : '';
            msg += (vdividends_ate <= 0 )? 'Forneça o valor Dividendos que termina.' : '';
            filtrar = false;

        }
        else{
            if ((chk_dividends.checked) && (vdividends_de >= vdividends_ate)){
                msg += 'O valor inicial de Divindedos não pode ser maior que o valor final.';
                filtrar = false;
            }
        }
        if (msg != ''){
            small_dividends.innerHTML = msg;
            small_dividends.classList.remove('d-none');
        }
        /*Comparar PL*/
        else{
            chk_pl = document.querySelector('#chk-pl');
            vpl_de = parseFloat(document.querySelector('#input-pl-de').value);
            vpl_ate = parseFloat(document.querySelector('#input-pl-ate').value);

            msg = '';
            if ((chk_pl.checked) && (vpl_de<= 0) && (vpl_ate<=0)){
                msg += (vpl_de <= 0 )? 'Forneça o valor PL que começa.' : '';
                msg += (vpl_ate <= 0 )? 'Forneça o valor PL que termina.' : '';
                filtrar = false;
            }
            else{
                if ((chk_pl.checked) && (vpl_de >= vpl_ate)){
                    msg += 'O valor inicial de P/L não pode ser maior que o valor final.';
                    filtrar = false;
                }
            }
        }
        if (msg != ''){
            small_pls.innerHTML = msg;
            small_pls.classList.remove('d-none');
        }
        /*Comparar P/VPA*/
        else{
            chk_pvpa = document.querySelector('#chk-pvpa');
            vpvpa_de = parseFloat(document.querySelector('#input-pvpa-de').value);
            vpvpa_ate = parseFloat(document.querySelector('#input-pvpa-ate').value);

            msg = '';
            if ((chk_pvpa.checked) && (vpvpa_de<= 0) && (vpvpa_ate<=0)){
                msg += (vpvpa_de <= 0 )? 'Forneça o valor P/VPA que começa.' : '';
                msg += (vpvpa_ate <= 0 )? 'Forneça o valor P/VPA que termina.' : '';
                filtrar = false;
            }
            else{
                if ((chk_pvpa.checked) && (vpvpa_de >= vpvpa_ate)){
                    msg += 'O valor inicial de P/VPA não pode ser maior que o valor final.';
                    filtrar = false;
                }
            }
        }

        if (msg != ''){
            small_pvpas.innerHTML = msg;
            small_pvpas.classList.remove('d-none');
        }
        /*Comparar Valor da Cotação*/
        else{
            chk_valcotacao = document.querySelector('#chk-valcotacao');
            vcotacao_de = parseFloat(document.querySelector('#input-valcotacao-de').value);
            vcotacao_ate = parseFloat(document.querySelector('#input-valcotacao-ate').value);

            msg = '';
            if ((chk_valcotacao.checked) && (vcotacao_de<= 0) && (vcotacao_ate<=0)){
                msg += (vcotacao_de <= 0 )? 'Forneça o Valor da Cotação que começa.' : '';
                msg += (vcotacao_ate <= 0 )? 'Forneça o Valor da Cotação que termina.' : '';
                filtrar = false;
            }
            else{
                if ((chk_valcotacao.checked) && (vcotacao_de >= vcotacao_ate)){
                    msg += 'O valor inicial de Valor da Cotação não pode ser maior que o valor final.';
                    filtrar = false;
                }
            }
        }
        if (msg != ''){
            small_valcotacao.innerHTML = msg;
            small_valcotacao.classList.remove('d-none');
        }
        /*Comparar Setores*/
        else{
            chk_Setores = document.getElementById('chk-Setores');
            filterSetores = (chk_Setores.checked) ? 'S' : 'N' ;

            if (chk_Setores.checked && idsSetores.length == 0){
                msg += 'sim';
                document.getElementById('small-setor').classList.remove('d-none');
                filtrar = false;
            }

        }

        /*TODAS ETAPAS VALORES SEM ERROS */
        if (msg == ''){
            if (input_limit.value < 10 ){
                document.getElementById('small-limit').classList.remove('d-none');
                filtrar = false;
            }
            else{
                urlfilter = 'tipo='+select_tipo+'&limit='+input_limit.value;
                filterValPL = ( chk_pl.checked) ? parseFloat(vpl_de)+','+ parseFloat(vpl_ate) : '';
                filterValPVPA = ( chk_pvpa.checked) ? parseFloat(vpvpa_de)+','+ parseFloat(vpvpa_ate) : '';
                filterValDividends = (chk_dividends.checked) ? vdividends_de+','+vdividends_ate : '';
                filterValcotacao = (chk_valcotacao.checked) ? vcotacao_de+','+vcotacao_ate : '';
                if (filterSetores == 'S'){
                    filterSetores = (idsSetores.length > 0) ? stridSetores : '';
                }
                else{
                    filterSetores = '';
                }
                filtrar = true;
            }
        }
    }
    if (filtrar){
        tipo_order = document.getElementById('select-tipo-order').value;
        orderby = document.getElementById('select-orderby').value;
        window.location.href = '/bolsavalores/empresas/main?'+urlfilter+'&ativa='+select_ativa.value+
        '&filterpl='+filterValPL+'&filterpvpa='+filterValPVPA+'&filterdividends='+filterValDividends+'&filtersetor='+filterSetores+
        '&filtervalcotacao='+filterValcotacao+'&tipoorder='+tipo_order+'&orderby='+orderby;


    }
}


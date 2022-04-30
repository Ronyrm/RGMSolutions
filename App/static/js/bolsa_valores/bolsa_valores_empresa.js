var updateEmpresa = false;
var orderField = 0;
var empresa_selected = {};
var month_extenso = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
var content_bolsa_valores = document.getElementById('content-bolsa-valores');
var content_detail_empresa = document.getElementById('content-detail-empresa');
var array_prices = [];
var array_prices_month = [];
var simbol_papel = '';
var ID_papel = '';
var lbltot = document.getElementById('lbltot');
lbltot.innerHTML = 'Atualizado:  0 de '+totalempresas;
var hoje        = new Date();
var datareturn    = new Date(hoje.getTime());
var smes = zeroFill((datareturn.getMonth()+1));
var sano = parseInt(datareturn.getFullYear());

var select_ano = document.getElementById('select-ano');
var select_ano_div_ini = document.getElementById('select-ano-ini-dividendos');
var select_ano_div_fim = document.getElementById('select-ano-fim-dividendos');
let opt_ano = '';
for (var i = 2000; i<=sano; i++){
    opt_ano += '<option value="'+i+'">'+i+'</option>';
}
select_ano.innerHTML = opt_ano;
select_ano_div_ini.innerHTML = opt_ano;
select_ano_div_fim.innerHTML = opt_ano;

document.querySelector('#mes-fim option[value="'+smes+'"]').selected = true;
document.querySelector('#select-ano option[value="'+sano+'"]').selected = true;

document.querySelector('#select-ano-ini-dividendos option[value="2000"]').selected = true;
document.querySelector('#select-ano-fim-dividendos option[value="'+sano+'"]').selected = true;


var datahoje_BR = zeroFill(datareturn.getDate()) + "/" + zeroFill((datareturn.getMonth() + 1)) + "/" +datareturn.getFullYear();
diahoje = datareturn.getDate();
var datahoje_JS_fim = datareturn.getFullYear() + "-" + zeroFill((datareturn.getMonth() + 1)) + "-" +zeroFill(datareturn.getDate());
datareturn.setDate(datareturn.getDate()-30.5);
var datahoje_JS_ini = datareturn.getFullYear() + "-" + zeroFill((datareturn.getMonth() + 1)) + "-"+zeroFill(diahoje);
document.getElementById('dt-ini').value = datahoje_JS_ini;
document.getElementById('dt-fim').value = datahoje_JS_fim;

var date = new Date();
var DiaInicialMes = new Date(date.getFullYear(), date.getMonth(), 1);
var DiaFinalMes = new Date(date.getFullYear(), date.getMonth() + 1, 0);
DiaInicialMes = DiaInicialMes.getFullYear() + "-" + zeroFill((DiaInicialMes.getMonth() + 1)) + "-" +zeroFill(DiaInicialMes.getDate());
DiaFinalMes = DiaFinalMes.getFullYear() + "-" + zeroFill((DiaFinalMes.getMonth() + 1)) + "-" +zeroFill(DiaFinalMes.getDate());
document.getElementById('dt-ini-grafic').value = datahoje_JS_ini;
document.getElementById('dt-fim-grafic').value = datahoje_JS_fim;
document.getElementById('dt-ini-individuale').value = datahoje_JS_ini;
document.getElementById('dt-fim-individuale').value = datahoje_JS_fim;
var table_empresas = document.getElementById('table-empresas');


function format_valorBRL(valor,decimal,sifrao,fixed=-1){
    if(valor == null || valor == '') return 0;
    if (sifrao) return valor.toLocaleString('pt-br',{style: 'currency', currency: 'BRL',minimumFractionDigits: decimal});
    if (!sifrao) return valor.toLocaleString('pt-br', {minimumFractionDigits: decimal});

};
function format_dateBR(dt){
    if (dt == null){ return ''}
    if (dt.length > 0){
        dtult_cotacao = new Date(dt);
        return zeroFill(dtult_cotacao.getDate()) + "/" + zeroFill((dtult_cotacao.getMonth() + 1)) + "/" +dtult_cotacao.getFullYear();
    }
    else{ return ''}
}

function zeroFill(n) {
    return ('0' + n).slice(-2);
}

function arredonda(valor,decimal){
    if (valor == null || valor == ''){
        return 0.00;
    }
    else{
        return valor.toFixed(decimal);
    }
}


// BOTAO DE ATUALIZAR VALORES DE ACORDO COM A DATA ESPECIFICADA, BUSCA DADOS YAHOO FINANCE
async function click_btn_update_empresas(btn){
    updateEmpresa = true;
    btn.disabled = true;
    lbltot.classList.remove('d-none');
    dtini  = document.getElementById('dt-ini').value;
    dtfim = document.getElementById('dt-fim').value;


    let contador = 0;
    var data = [];
    tabempresas.data.forEach( async (empresa) => {

        url = '/update/papel/bolsa/valores/'+empresa.id+'/'+empresa.papel+'/'+dtini+'/'+dtfim;
        let tdemp = 'tdempresa_'+empresa.id;
        document.getElementById(tdemp).innerHTML = '<div class="spinner-border text-warning mr-1" role="status">'+
                        '<span class="sr-only">Loading...</span></div>Atualizando '+empresa.papel;

        let response = await fetch(url);
        if(response.status == 200){
            response.json().then(async data => {
                data = await data;

                let att = '';
                contador += 1;
                if (data.atualizado){
                    att =  'SIM, total de dividendos encontrados:'+data.totdiv;
                }
                else{
                     att = 'NÃO, Empresa sem dados suficientes';
                }
                lbltot.innerHTML = 'Atualizado: '+contador+ ' de '+totalempresas;

                if(contador == totalempresas){
                    btn.disabled = false;
                    lbltot.innerHTML = 'Atualização Concluida, Aguarde, atualizando a página.';
                    setTimeout(function(){
                        document.location.reload(true);
                    }, 2000);


                }

                document.getElementById(tdemp).innerHTML = '<label class="mx-auto bg-danger">Atualizado:'+att+' </label>';
            });
        }
        else{
            data = [];
        }
    });

}

// CLICA EM CIMA DA EMPRESA(SIMBOLO) PARA ABRIR OS GRAFICOS, AUTOMATICAMENTE VAI PARA PRECOS DE COTAÇÃO
async function generate_grafic_prices_cotacao_dividendos(idpapel,papel,nameempresa){
    ID_papel = idpapel;
    empresa_selected = tabempresas.data.find(emp => emp.id==ID_papel);
    findindex = tabempresas.data.findIndex(emp => emp.id==ID_papel);

    console.log(tabempresas.data[findindex]);
    loading_data_empresa(empresa_selected);

    dtini  = document.getElementById('dt-ini').value;
    dtfim = document.getElementById('dt-fim').value;
    document.getElementById('lbl-name-empresa').innerHTML = papel + ' - '+ nameempresa;
    simbol_papel = papel;
    dt = new Date(dtini);
    dt.setDate(dt.getDate()+1)
    dtini = zeroFill(dt.getDate()) + "-"+ zeroFill((dt.getMonth() + 1)) + "-" + dt.getFullYear();
    dt = new Date(dtfim);
    dt.setDate(dt.getDate()+1);
    dtfim = zeroFill(dt.getDate()) + "-"+ zeroFill((dt.getMonth() + 1)) + "-" + dt.getFullYear();

    await generate_grafic_prices_cotacao_diary(papel,dtini,dtfim);
    await generate_grafic_prices_cotacao_month(papel,dtini,dtfim);
    await generate_grafic_dividendos_month(papel,dtini,dtfim);
    content_bolsa_valores.classList.add('d-none');
    content_detail_empresa.classList.remove('d-none');


}


//----------------------------------------- COTACOES --------------------------------------



// CLICA NO BOTÃO GERAR DENTRO DO CONTENT PRECOS DE COTAÇÃO
async function btn_click_gera_grafic_prices_cotacao_diary(){
    dtini  = document.getElementById('dt-ini-grafic').value;
    dtfim = document.getElementById('dt-fim-grafic').value;
    dt = new Date(dtini);
    dt.setDate(dt.getDate()+1)
    dtini = zeroFill(dt.getDate()) + "-"+ zeroFill((dt.getMonth() + 1)) + "-" + dt.getFullYear();
    dt = new Date(dtfim);
    dt.setDate(dt.getDate()+1);
    dtfim = zeroFill(dt.getDate()) + "-"+ zeroFill((dt.getMonth() + 1)) + "-" + dt.getFullYear();

    await generate_grafic_prices_cotacao_diary(simbol_papel,dtini,dtfim);
    //await btn_click_gera_grafic_prices_cotacao_diary();


}

// PROCEDIMENTO PARA BUSCAR OS DADOS  DE PRECOS DA COTAÇÃO DIARIAMENTE NO BANCO DE ACORDO COM A DATA INFORMADA,
async function generate_grafic_prices_cotacao_diary(papel,dtini,dtfim){
    url = '/get/prices/cotacao/history/'+papel+'/'+dtini+'/'+dtfim+'?fields=dt_cotacao,val_fechamento';

    let response = await fetch(url);
    if(response.status == 200){
        response.json().then(async data => {
            data = await data.data;

            view_grafic_prices_cotacao_diary(papel,data);
        });
    }
}

// GERAR O GRAFICO DIARIO PRECO COTACAO.
function view_grafic_prices_cotacao_diary(papel,data){
    array_prices = [];
    array_prices[0] = ['Data','Valor'];
    i = 1;
    if (data.length > 0){
        data.forEach((pricescot) => {
            dt_cotacao = new Date(pricescot['dt_cotacao']);
            dt_cotacao.setDate(dt_cotacao.getDate()+1);
            dt_cotacao = zeroFill(dt_cotacao.getDate()) + "/" + zeroFill((dt_cotacao.getMonth()+1)) + "/" +dt_cotacao.getFullYear();
            array_prices[i] =[dt_cotacao,pricescot['val_fechamento']];
            i+=1;
        });
    }
    else{
        array_prices = [];
        array_prices[0] = ['Data','Valor'];
        array_prices[1] = ['0','0'];
    }
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(array_prices);
        var options = {
            title: 'Histórico de Preços Cotação Diário ' + papel,
            curveType: 'function',
            //backgroundColor: '#ffc107',
            is3D: true,
            legend: { position: 'bottom' }
        };
        var chart = new google.visualization.LineChart(document.getElementById('chart-prices-cotacao-diary'));
        chart.draw(data, options);
    });
    content_bolsa_valores.classList.add('d-none');
    content_detail_empresa.classList.remove('d-none');
}

// CLICA NO BOTAO GERAR, PREÇOS DE COTAÇÃO MENSAL
async function btn_click_gera_grafic_prices_cotacao_month(){
    mes_ini = document.querySelector('#mes-ini').value;
    mes_fim = document.querySelector('#mes-fim').value;
    ano = document.querySelector('#select-ano').value;
    dt_ini = '01-'+mes_ini+'-'+ano;
    dt_fim = new Date(parseInt(ano),parseInt(mes_fim),0);
    dt_fim = zeroFill(dt_fim.getDate()) + "-"+ zeroFill((dt_fim.getMonth()+1)) + "-" + dt_fim.getFullYear();

    await generate_grafic_prices_cotacao_month(simbol_papel,dt_ini,dt_fim);

}

// PROCEDIMENTO PARA BUSCAR OS DADOS  DE PRECOS DA COTAÇÃO MENSALMENTE NO BANCO DE ACORDO COM A MES INICIAL E FINAL E ANO INFORMADO,
async function generate_grafic_prices_cotacao_month(papel,dtini,dtfim){
    url = '/get/prices/cotacao/history/mensal/'+papel+'/'+dtini+'/'+dtfim;

    let response = await fetch(url);
    if(response.status == 200){
        response.json().then(async data => {
            data = await data.data;
            view_grafic_prices_cotacao_month(papel,data);
        });
    }
}

// GERAR O GRAFICO MENSAL PRECOS COTAÇÃO.
function view_grafic_prices_cotacao_month(papel,data){
    array_prices_month = [];
    array_prices_month[0] = ['Data','Valor',{ role: "style" }];
    i = 1;
    if (data.length > 0){
        data.forEach((pricescot) => {
            mes = month_extenso[parseInt(pricescot[0].substr(0,2))-1];
            array_prices_month[i] =[mes,pricescot[1],'#d39e00'];
            i+=1;
        });
    }
    else{
        array_prices_month = [];
        array_prices_month[0] = ['Data','Valor',{ role: "style" }];
        array_prices_month[1] = ['0','0','#d39e00'];
    }
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(array_prices_month);
        var options = {
            title: 'Histórico de Preços Cotação(Média) Mensal ' + papel + ', ano: '+ document.getElementById('select-ano').value,
            //curveType: 'function',
            //backgroundColor: '#212121',
            height: 500,
            bar: {groupWidth: "95%"},
            legend: { position: "none" },

        };

        var view = new google.visualization.DataView(data);
        view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

        var chart = new google.visualization.ColumnChart(document.getElementById('chart-prices-cotacao-month'));

        chart.draw(view, options);
    });
}



//----------------------------------------- DIVIDENDOS --------------------------------------
async function btn_click_gera_grafic_dividendos_month(){
    ano_ini = document.querySelector('#select-ano-ini-dividendos').value;
    ano_fim = document.querySelector('#select-ano-fim-dividendos').value;
    dt_ini = '01-01-'+ano_ini;
    dt_fim = '31-12-'+ano_fim;
    await generate_grafic_dividendos_month(simbol_papel,dt_ini,dt_fim);
}
async function generate_grafic_dividendos_month(papel,dtini,dtfim){
    select_tpdate = document.getElementById('select-tpdate').value;
    console.log('teste');
    url = '/get/dividendos/empresa/interval/mensal/'+papel+'/'+dtini+'/'+dtfim+'?tpdate='+select_tpdate;
    let response = await fetch(url);
    if(response.status == 200){
        response.json().then(async data => {
            data = await data.data;
            console.log(data);
            view_grafic_dividendos_month(papel,data);
        });
    }
}
function view_grafic_dividendos_month(papel,data){
    let totaldiv = 0;
    array_prices_month = [];

    array_prices_month[0] = ['Data','Valor',{ role: "style" }];
    i = 1;
    if (data.length > 0){
        data.forEach((pricescot) => {
            totaldiv = totaldiv + pricescot[1];
            array_prices_month[i] =[pricescot[0],pricescot[1],'#d39e00'];
            i+=1;
        });
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(function (){
            var data = google.visualization.arrayToDataTable(array_prices_month);
            var options = {
                title: 'Histórico de Dividendos Mensal ' + papel + ' Total geral: '+ totaldiv.toFixed(3),
                curveType: 'function',
                legend: { position: 'none' ,}
            };

            var view = new google.visualization.DataView(data);
            view.setColumns([0, 1,
                        { calc: "stringify",
                             type: "string",
                             sourceColumn: 1,
                             role: "annotation" },
                           2]);

            var chart = new google.visualization.ColumnChart(document.getElementById('chart-dividendos-month'));

            chart.draw(view, options);
        });
    }
    else{
        document.getElementById('chart-dividendos-month').innerHTML = '<div class="alert alert-warning mx-1">'+
        'Nenhum Dividendo/proventos encontrado no determinado período</div>';
        array_prices_month[1]= ['Nenhum Valor',0,'#d39e00'];
    }

}

// BOTÃO VOLTAR
function btn_voltar_lista_empresas(btn){
    btn.href = '#td-codpapel-empresa-'+ID_papel;
    content_bolsa_valores.classList.remove('d-none');
    content_detail_empresa.classList.add('d-none');
}

// CLICA BOTAO MENU.
function btn_mostrar_detail_prices_cotacao(tipomenu,btn){
     btns = document.querySelectorAll('.btn-menu')
     btns.forEach(function(rbtn){
        rbtn.classList.remove('active');
     });

    divcontents = document.querySelectorAll('.div-content');
    divcontents.forEach(function(rdiv){
        rdiv.classList.add('d-none');
    });

    div_prices = document.getElementById('div-content-prices-cotacao');
    div_dividendos = document.getElementById('div-content-dividendos');
    div_detalhes = document.getElementById('div-content-detalhes');


    btn.classList.add('active');
    switch (tipomenu) {
      case 'detalhes':
        div_detalhes.classList.remove('d-none');
        break;
      case 'cotacao':
        div_prices.classList.remove('d-none');
        document.getElementById('lbl-name-grafic').innerHTML = 'Gráficos referente a Valores de Cotações';
        break;
      case 'dividendos':
        div_dividendos.classList.remove('d-none');
        document.getElementById('lbl-name-grafic').innerHTML = 'Gráficos referente a Valores de Dividendos';
        break;

    }

}

async function click_btn_update_empresa(){
    small_emp = document.getElementById('small-info-up-emp');
    dtini  = document.getElementById('dt-ini-individuale').value;
    dtfim = document.getElementById('dt-fim-individuale').value;

    btn_update_empresa = document.getElementById('btn-update-empresa');
    sinner_temp = btn_update_empresa.innerHTML;
    btn_update_empresa.innerHTML = '<div class="spinner-border text-warning mr-1" role="status">'+
                        '<span class="sr-only">Loading...</span></div>Atualizando '+simbol_papel;
    url = '/update/papel/bolsa/valores/'+ID_papel+'/'+simbol_papel+'/'+dtini+'/'+dtfim;
    console.log(url);
    let response = await fetch(url);
    if(response.status == 200){
        response.json().then(async data => {
            data = await data;
            let att = '';
            if (data.atualizado){
                att =  'Atualização Concluida';
            }
            else{
                att = 'Falha ao atualizar';
            }
            small_emp.classList.remove('d-none');
            small_emp.innerHTML = att;
            btn_update_empresa.innerHTML = sinner_temp;

            setTimeout(function(){
                small_emp.classList.add('d-none');
            }, 3000);
        });

    }
}
// CARREGA ARRAY LIST DAS EMPRESAS E PREENCHE <TABLE> > <TBODY>
async function loading_fill_table(array_tbempresas){
    tbody_empresas = document.getElementById('tbody-empresas');
    bodyTemp = '';
    contador = [];
    await array_tbempresas.data.forEach(rowEmpresa => {
        contador.push(1);
        bodyTemp +='<tr id="tr-empresa-'+rowEmpresa['id']+'">';
        bodyTemp +=return_tr_table_empresa(contador.length,rowEmpresa);
        bodyTemp +='</tr>';
    });
    tbody_empresas.innerHTML = bodyTemp;
}

// RETORNA LINHA DE ACORDO COM UMA EMPRESA ESPECIFICA
function return_tr_table_empresa(contador,rowEmpresa){
    vpapel = "'"+rowEmpresa['papel']+"'";
    vdescPapel = "'"+rowEmpresa['name']+"'";
    vdescEmpresa = "'"+rowEmpresa['desc_empresa']+"'";
    vSetorSub = rowEmpresa['setor']['name']+" - "+rowEmpresa['subsetor']['name'];
    bodyTemp = '';
    bodyTemp += '<td class="align-middle text-center p-2">'+
                            '<div class="form-check">'+
                                '<input onchange="click_selectpapel(this);" class="form-check-input" name="chk-identificador" '+
                                'type="checkbox" value="'+rowEmpresa['id']+'"'+
                                ' id="chk-identificador-'+rowEmpresa['id']+'">'+
                                '<label class="form-check-label" for="chk-identificador-'+rowEmpresa['id']+'">'+contador+'</label>'+
                            '</div>'+
                        '</td>'+
                        '<td class="text-center align-center">'+
                            '<div class="d-flex justify-content-center">'+
                                '<a title="Identificador: '+rowEmpresa['id']+'" class="text-warning" href="#"'+
                                ' id="td-codpapel-empresa-'+rowEmpresa['id']+'"'+
                                ' onclick="generate_grafic_prices_cotacao_dividendos('+rowEmpresa['id']+','+vpapel+','+vdescPapel+');">'+
                                    rowEmpresa['papel']+'</a>'+
                            '</div>'+
                            '<div class="d-flex justify-content-center div-btn-'+contador+'">'+
                                '<button class="btn-update-empresa" onclick="update_info_empresa('+rowEmpresa['id']+','+vpapel+','+contador+',this);">'+
                                '<i class="fas fa-sync-alt" </i></button>'+
                            '</div>'+

                        '</td>';
        bodyTemp +='<td title="'+vdescEmpresa+'">'+rowEmpresa['name']+'</td>';
        bodyTemp +='<td>'+vSetorSub+'</td>';
        bodyTemp +='<td>'+format_dateBR(rowEmpresa['dt_ult_cotacao'])+'</td>';
        //preço cotacao
        color_tpPercDiferenceCot =  (rowEmpresa['perc_dif_cotacao'] >=0 ) ? 'text-primary' : 'text-danger';

        bodyTemp +='<td class="align-middle text-center">'+
                        '<div class="row d-flex justify-content-center">'+
                            format_valorBRL(rowEmpresa['val_cotacao'],2,true)+
                        '</div>'+
                        '<div class="row d-flex justify-content-center">'+
                            '<small class="'+color_tpPercDiferenceCot+'"><strong>'+format_valorBRL(rowEmpresa['val_dif_cotacao'],2,false)+
                            '('+format_valorBRL(rowEmpresa['perc_dif_cotacao'],2,false)+' %)</strong></small>'+
                        '</div>'+
                    '</td>';
        if (rowEmpresa['perc_divyield'] != null || rowEmpresa['perc_divyield'] != ''){
            bodyTemp +='<td>'+ arredonda(rowEmpresa['perc_divyield'],2)+'% - '+
            format_valorBRL(rowEmpresa['val_divyield'],2,true)+'</td>';
        }
        else{
            bodyTemp +='<td></td>';
        }
        bodyTemp +='<td>'+format_dateBR(rowEmpresa['ex_date_dividend'])+'</td>';
        if (tipo_filtro == 4 || tipo_filtro == 5){
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_patr_liq'],2,true)+'</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_roe'],2,false)+'%</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_luc_liq_atual'],0,true,0)+'</td>';
            bodyTemp +='<td>'+parseInt(rowEmpresa['num_acoes']).toLocaleString()+'</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_lpa'],2,false)+'</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_p_l'],2,false)+'</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_vpa'],2,false)+'</td>';
            bodyTemp +='<td>'+format_valorBRL(rowEmpresa['val_p_vp'],2,false)+'</td>';
        }
        bodyTemp +='<td id="tdempresa_'+rowEmpresa['id']+'"></td>';
        return bodyTemp;
}

// ATUALIZA DADOS DA EMPRESA, COTACAO... E MUDA LINHA TR
async function update_info_empresa(idpapel,papel,numitem,btn){
    trEmpresa = document.getElementById('tr-empresa-'+idpapel);
    indexof  = tabempresas.data.findIndex(emp => emp.id==idpapel);
    div_btn = document.querySelector('.div-btn-'+numitem);
    innerTemp = div_btn.innerHTML;
    div_btn.innerHTML = '<div class="loader"></div><small class="text-warning ml-2">&nbsp;Atualizando</small>';
    url = '/update/papel/bolsa/info/'+idpapel+'/'+papel;
    let response = await fetch(url);
    if(response.status == 200){
        response.json().then(async data => {
        data = await data;
        if (data.result){
            trEmpresa.innerHTML = return_tr_table_empresa(numitem,data.data[0]);
            tabempresas.data[indexof] = data.data[0];
        }
        else{
            div_btn.innerHTML = '<small class="text-danger">Nenhuma Informação</small>';
            setTimeout(function(){
                div_btn.innerHTML = innerTemp;
            },  3000);
        }
        });
    }

}

// CARREGA OS DADOS DETAIL DA EMPRESA E PREENCHE CAMPOS DIV DETAIL
function loading_data_empresa(array_empresa){
    div_data_emp = document.getElementById('div-data-empresa');
    color_tpPercDiferenceCot =  (array_empresa['perc_dif_cotacao'] >=0 ) ? 'text-primary' : 'text-danger';
    div ='<div class="row">'+
            '<div class="col-sm-12 col-lg-3">'+
                '<div class="d-flex justify-content-center">'+
                    '<div class="form-group-cotacao text-center"'+
                        '<h3>Valor da Cotação</h3>'+
                        '<h5>'+format_valorBRL(array_empresa['val_cotacao'],2,true)+''+
                        '<small class="'+color_tpPercDiferenceCot+'">&nbsp;'+format_valorBRL(array_empresa['val_dif_cotacao'],2,false)+
                        '('+format_valorBRL(array_empresa['perc_dif_cotacao'],2,false)+' %)</small></h5>'+
                        '<h6 class="text-secondary">Data: '+format_dateBR(array_empresa['dt_ult_cotacao'])+'</h6>'+
                    '</div>'+
                '</div>'+
            '</div>'+
            '<div class="col-sm-12 col-lg-9 d-flex justify-content-start">'+
                '<div class="row">'+
                    '<div class="col-sm text-center">'+
                        '<label class="lbl-title">Valor Mercado</label><br>'+
                        '<label class="lbl-value">'+format_valorBRL(array_empresa['val_mercado'],2,true)+'</label>'+
                    '</div>'+
                    '<div class="col-sm text-center">'+
                        '<label class="lbl-title">Valor Firma</label><br>'+
                        '<label class="lbl-value">'+format_valorBRL(array_empresa['val_firma'],2,true)+'</label>'+
                    '</div>'+
                    '<div class="col-sm text-center">'+
                        '<label class="lbl-title">Total de Ações</label><br>'+
                        '<label class="lbl-value">'+format_valorBRL(array_empresa['num_acoes'],2,true)+'</label>'+
                    '</div>'+
                    '<div class="col-sm text-center">'+
                        '<label class="lbl-title">Último Balanço</label><br>'+
                        '<label class="lbl-value">'+format_dateBR(array_empresa['dt_ult_balanco'],2,true)+'</label>'+
                    '</div>'+
                '</div>'+
            '</div>'+
         '</div>';
    div_data_emp.innerHTML = div;
}

function click_selectpapel(selectinput){
    if (selectinput.checked){
        console.log(selectinput.value+' selecionado');
    }
    else{
        console.log(selectinput.value+' não selecionado');
    }
    aselected = verify_empresas_selected();
    console.log(aselected);
    document.getElementById('btn-comparar-papeis').classList.add('d-none');
    if(aselected.result.length > 1){
        document.getElementById('btn-comparar-papeis').classList.remove('d-none');
    }
}

function verify_empresas_selected(){
    result = [];
    strsel = '';
    achks = document.querySelectorAll('input[name="chk-identificador"]:checked');
    achks.forEach(function(rchk){
        result.push(tabempresas.data.find(emp => emp.id==rchk.value));
        strsel += rchk.value +',';
    });
    return {'result': result,'strsel':strsel.substr(0,strsel.length-1)} ;

}




function sorted_tabempresas_value(field){
    switch (orderField){
        case 0:
            tabempresas.data.sort(function(a,b){
                if (a[field] == ''){
                    a[field] = 0;
                }
                if (b[field] == ''){
                    b[field] = 0;
                }
                if (( (a[field].length == 0)? 0 : a[field]) < ( (b[field].length == 0)? 0 : b[field]) ) return -1;
                if (((a[field].length == 0)? 0 : a[field]) > ( (b[field].length == 0)? 0 : b[field]) ) return 1;
                return 0;
            });
            orderField = 1;
            break;
        case 1:
            tabempresas.data.sort(function(a,b){
                if (a[field] > b[field]) return -1;
                if (a[field] < b[field]) return 1;
                return 0;
            });
            orderField = 0;
            break;
    }

    console.log(tabempresas.data);
    loading_fill_table(tabempresas);

}

function sorted_tabempresas_date(field){
    switch (orderField){
        case 0:
            tabempresas.data.sort(function(a,b){
                if (a[field] == '' || b[field] == ''){
                    console.log('Sim');
                    return -1;
                }
                if (new Date(a[field]) < new Date(b[field])) return -1;
                if (new Date(a[field]) > new Date(b[field])) return 1;
                return 0;
            });
            orderField = 1;
            break;
        case 1:
            tabempresas.data.sort(function(a,b){
                if (a[field] == '' || b[field] == ''){
                    console.log('Sim');
                    return -1;
                }
                if (new Date(a[field]) > new Date(b[field])) return -1;
                if (new Date(a[field]) < new Date(b[field])) return 1;
                return 0;
            });
            orderField = 0;
            break;
    }

    console.log(tabempresas.data);
    loading_fill_table(tabempresas);

}

async function loadingDataIbovespa(){
    if (!updateEmpresa){
        div_ibovespa = document.getElementById('div-data-ibovespa');
        div_ibovespa.innerHTML =
        '<div class="form-row d-flex justify-content-center">'+
             '<h3 class="text-white"><strong>IBOVESPA(^BVSP)</strong></h3>'+
             '<div class="ml-2 my-auto">'+
                '<button class="btn btn-warning btn-sm" data-toggle="modal" onclick="click_btn_data_ibov();" data-target="#modal-data-ibov"><span class="glyphicon glyphicon-new-window"></span></button>'+
            '</div>'+
        '</div>'+
        '<div class="spinner-border text-warning mr-1" role="status">'+
                            '<span class="sr-only">Loading...</span></div>Atualizando valores Ibovespa';
        fetch('/get/info/ibovespa')
        .then(await function(response){
            return response.json();
        })
        .then(function(resultJson){
            if (resultJson.result){
                data = resultJson.data[0];
                colorsmall = (parseFloat(data.val_dif_cotacao) < 0) ? 'text-danger' : 'text-primary';
                operadoDay = (parseFloat(data.val_dif_cotacao) < 0) ? '' : '+';
                valDifCotacao = format_valorBRL(data.val_dif_cotacao,2,false);
                percDifCotacao = format_valorBRL(data.perc_dif_cotacao,2,false);
                let div =
                '<div class="form-row d-flex justify-content-center">'+
                    '<h3 class="text-white"><strong>IBOVESPA(^BVSP)</strong></h3>'+
                    '<div class="ml-2 my-auto">'+
                        '<button class="btn btn-warning btn-sm" data-toggle="modal" data-target="#modal-data-ibov"><span class="glyphicon glyphicon-new-window"></span></button>'+
                    '</div>'+
                '</div>'+
                '<div class="form-row d-flex justify-content-center">'+
                    '<label class="text-warning mr-2"><strong>'+data.val_cotacao.toLocaleString()+'</strong</label>'+
                    '<small class="'+colorsmall+' ml-2">'+operadoDay+valDifCotacao+' ('+operadoDay+percDifCotacao+'%)</strong</label>'+
                '</div>';


                div_ibovespa.innerHTML = div;
            }
        });
    }
}
function click_btn_data_ibov(){


}

$().ready(async function() {
    loadingDataIbovespa();
    arrayopt = await fillArraySetores();
    loading_fill_table(tabempresas);
    temporizador();
    loadingFieldModalFilter();


});

function temporizador() {
	setInterval (function() {
        urlMain = window.location.href;
    	var hora = new Date().toLocaleTimeString();
        console.log(hora);
        loadingDataIbovespa();

  	}, 60000);
}

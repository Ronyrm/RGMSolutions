var smallIbov = document.querySelector('#small-msg-ibov');
var divDataIbov = document.querySelector('#div-data-ibov');
var divTpDatas = document.querySelector('#div-tp-datas');
function click_btn_dados(){
    $('#collapseGrafico').collapse('hide');
    document.querySelector('#dt-ini-ibov-dados').value = datahoje_JS_ini;
    document.querySelector('#dt-fim-ibov-dados').value = datahoje_JS_fim;
}

function click_btn_grafico(){
    $('#collapseDados').collapse('hide');
    change_tp_data(0);
    
}

async function click_btn_update_ibov(){
    let btnUp = document.querySelector('#btn-update-ibov');
    innerBtn = btnUp.innerHTML;
    btnUp.innerHTML = '<div class="spinner-border text-warning mr-1" role="status">'+
    '<span class="sr-only">Loading...</span></div>Atualizando Valores...';  
    let dataIni = new Date(document.querySelector('#dt-ini-ibov-dados').value);
    dtIndex = new Date(dataIni.setDate(dataIni.getDate()+1));
    
    let dataFim = new Date(document.querySelector('#dt-fim-ibov-dados').value);
    dataFim = new Date(dataFim.setDate(dataFim.getDate() + 1));

    while (dtIndex <= dataFim){
        let stopped = false;
        
        dataini = zeroFill(dtIndex.getDate()) + '-' + zeroFill(dtIndex.getMonth()+1) + '-' + dtIndex.getFullYear();
        datafim = dtIndex;
        datafim = datafim.setDate(datafim.getDate()+1);    
        datafim = new Date(datafim);
        datafim = zeroFill(datafim.getDate()) + '-' + zeroFill(datafim.getMonth()+1) + '-' + datafim.getFullYear();
        
        //let fds = (dtIndex.getDay() == 5 || dtIndex.getDay() == 6) ? true : false;
        //if (!fds){
            while (!stopped){ 
                await fetch('/update/prices/ibovespa/'+dataini+'/'+datafim)
                .then(await function(respose){
                    return respose.json();  
                })
                .then(await function(resultJson){
                    if (resultJson.result){
                        smallIbov.innerHTML = dataini + ', situação:'+resultJson.msg;         
                    } 
                    else{
                        smallIbov.innerHTML = 'Erro: '+dataini; 
                    }
                    stopped = true;  
                });

            }
        //}
        //else{
        //    smallIbov.innerHTML = dataini + ', final de semana';         
        //}
        console.log(dtIndex);
        newDt = dtIndex.setDate(dtIndex.getDate());       
        dtIndex = new Date(newDt);
    }    
    btnUp.innerHTML = innerBtn;
    smallIbov.innerHTML = '';
}

async function click_btn_mostrar_ibov(){
    let alertDataIbov = document.querySelector('#alert-data-Ibov');
    let tableDataIbov = document.querySelector('#table-data-Ibov'); 
    let btnMostrar = document.querySelector('#btn-mostrar-ibov');
    innerBtn = btnMostrar.innerHTML;
    btnMostrar.innerHTML = '<div class="spinner-border text-warning mr-1" role="status">'+
    '<span class="sr-only">Loading...</span></div>Buscando Valores...';  
    
    let dataIni = new Date(document.querySelector('#dt-ini-ibov-dados').value);
    dataIni = new Date(dataIni.setDate(dataIni.getDate()+1));
    dataIni = zeroFill(dataIni.getDate()) + '-' + zeroFill(dataIni.getMonth()+1) + '-' + dataIni.getFullYear();

    let dataFim = new Date(document.querySelector('#dt-fim-ibov-dados').value);
    dataFim = new Date(dataFim.setDate(dataFim.getDate()+1));
    dataFim = zeroFill(dataFim.getDate()) + '-' + zeroFill(dataFim.getMonth()+1) + '-' + dataFim.getFullYear();
    
    await fetch('/get/prices/cotacao/history/^BVSP/'+dataIni+'/'+dataFim)
    .then(await function(response){
        return response.json();          
    })
    .then(await function(resultJson){
        if (resultJson.result){
            alertDataIbov.classList.add('d-none');
            tableDataIbov.classList.remove('d-none');
            dataIbov = resultJson.data;
            fillTableDataIbov(dataIbov);
        }
        else{
            alertDataIbov.classList.remove('d-none');
            alertDataIbov.innerHTML = 'Nenhum valor foi encontrado com as datas informadas. Verifique';
            tableDataIbov.classList.add('d-none');
        }
        
    })
    .catch(function(error) {
        alertDataIbov.classList.remove('d-none');
        alertDataIbov.innerHTML = 'Houve um Erro ao tentar fazer a consulta. Erro:'+error;
        tableDataIbov.classList.add('d-none');
    });
    btnMostrar.innerHTML = innerBtn;
    smallIbov.innerHTML = '';

}

function fillTableDataIbov(dataIbov){
    
    let bodyIbov = document.querySelector('#body-table-ibov');
    let tr = ''; 
    dataIbov.forEach(cotacao => {
        dtcotacao ="'"+cotacao.dt_cotacao+"'";
        tr += 
        '<tr>'+
            '<td>'+format_dateBR(dtcotacao)+'</td>'+
            '<td>'+cotacao.volume.toLocaleString()+'</td>'+
            '<td>'+cotacao.val_abertura.toLocaleString()+'</td>'+
            '<td>'+cotacao.val_maior.toLocaleString()+'</td>'+
            '<td>'+cotacao.val_menor.toLocaleString()+'</td>'+
            '<td>'+cotacao.val_fechamento.toLocaleString()+'</td>'+
        '</tr>';
    });
    bodyIbov.innerHTML = tr;
}


function change_tp_data(selectTp){
    divTpDatas.classList.remove('d-none');
    div = '<div class="form-row mb-2">';
    let optsMeses = ''; 
    
    for (let i = 0; i < month_extenso.length; i++) {
        mes = i+1;
        optsMeses += '<option value="'+mes+'">'+month_extenso[i]+'</option>';
    }
    
    let optsAnos = ''; 
    for ( i = 2000; i <= sano; i ++) {
        optsAnos += '<option value="'+i+'">'+i+'</option>';
    }
    
    divBtn = 
        '<div class="form-row d-flex justify-content-center">'+
            '<button id="btn-gerar-grafico" class="btn btn-warning" onclick="click_btn_GerarGraficoIbov();">Gerar Gráfico</button>'+
        '<div>';

    document.getElementById('select-tp-agrupamento').value = 0;
    document.getElementById('div-agrupamento').hidden      = false;

    switch (parseInt(selectTp)){
        //Datas
        case 0:
            div += 
                '<div class="col">'+
                    '<div class="form-group">'+ 
                        '<small class="text-warning" for="dt-ini-ibov-grafico">Data Inicial</small>'+                   
                        '<input class ="form-control" type="date" id="dt-ini-ibov-grafico">'+
                    '</div>'+
                '</div>'+
                '<div class="col">'+
                    '<div class="form-group">'+ 
                        '<small class="text-warning" for="dt-fim-ibov-grafico">Data Final</small>'+                   
                        '<input class ="form-control" type="date" id="dt-fim-ibov-grafico">'+
                    '</div>'+
                '</div>';
            divTpDatas.innerHTML = div + '</div>' + divBtn;
            document.querySelector('#dt-ini-ibov-grafico').value = DiaInicialMes;
            document.querySelector('#dt-fim-ibov-grafico').value = DiaFinalMes;
            break;
        //Mensal
        case 1:
            div += 
                '<div class="col">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="mes-ini-ibov-grafico">Mês Inicial</small>'+
                        '<select id="mes-ini-ibov-grafico" class="form-control">'+ optsMeses + '</select>'+
                    '</div>'+
                    
                '</div>'+
                '<div class="col">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="mes-final-ibov-grafico">Mês Final</small>'+
                        '<select id="mes-final-ibov-grafico" class="form-control">'+ optsMeses + '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col-3">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="ano-ibov-grafico">Ano</small>'+
                        '<select id="ano-ibov-grafico" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>';
            divTpDatas.innerHTML = div + '</div>'  + divBtn;
            document.querySelector('#mes-ini-ibov-grafico').value = 1;
            document.querySelector('#mes-final-ibov-grafico').value = 12;
            document.querySelector('#ano-ibov-grafico').value = sano;
            document.getElementById('select-tp-agrupamento').value = 1;
            break;
        // Anual
        case 2:
            div += 
                '<div class="col-3">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="ano-ini-ibov-grafico">Ano Inicial</small>'+
                        '<select id="ano-ini-ibov-grafico" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                    
                '</div>'+
                '<div class="col-3">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="ano-final-ibov-grafico">Ano Final</small>'+
                        '<select id="ano-final-ibov-grafico" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>';
            divTpDatas.innerHTML = div +'</div>' + divBtn;
            document.querySelector('#ano-ini-ibov-grafico').value   = sano - 5;
            document.querySelector('#ano-final-ibov-grafico').value = sano;
            document.getElementById('select-tp-agrupamento').value  = 2;
            break;
        // Mes por anos        
        case 3:
            div += 
                '<div class="col-4">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="mes-ibov-grafico">Mês</small>'+
                        '<select id="mes-ibov-grafico" class="form-control">'+ optsMeses + '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="ano-inicial">Ano Inicial</small>'+
                        '<select id="ano-inicial" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col">'+
                    '<div class="form-group">'+
                        '<small class="text-warning" for="ano-final">Ano Final</small>'+
                        '<select id="ano-final" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>';
            divTpDatas.innerHTML = div +'</div>' + divBtn;   
            document.querySelector('#mes-ibov-grafico').value      = parseInt(smes);
            document.querySelector('#ano-inicial').value           = sano - 5;
            document.querySelector('#ano-final').value             = sano;   
            document.getElementById('select-tp-agrupamento').value  = 2; 
            
            break;
        // Pontuação
        case 4:
            div += 
                '<div class="col-6">'+
                    '<div class="form-group">'+
                        '<small class="text-warning">Pontuação</small>'+
                        '<select class="form-control" id="select-ranking-pontuacao">'+
                            '<option value="DESC">Maiores Pontuações</option>'+
                            '<option value="ASC">Menores Pontuações</option>'+
                        '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col-6">'+
                    '<div class="form-group">'+
                        '<small class="text-warning">Limite de Registro</small>'+
                        '<select class="form-control" id="select-limite-pontuacao">'+
                            '<option value="5" selected>5</option>'+
                            '<option value="10">10</option>'+
                            '<option value="20">20</option>'+
                        '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col-6">'+
                    '<div class="form-group">'+
                        '<small class="text-warning">Ano Inicial</small>'+
                        '<select id="ano-inicial" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>'+
                '<div class="col-6">'+
                    '<div class="form-group">'+
                        '<small class="text-warning">Ano Final</small>'+
                        '<select id="ano-final" class="form-control">'+ optsAnos + '</select>'+
                    '</div>'+
                '</div>';
            divTpDatas.innerHTML = div +'</div>' + divBtn;
            document.getElementById('ano-inicial').value = sano;  
            document.getElementById('ano-final').value = sano;
            document.getElementById('div-agrupamento').hidden = true;
            break;
    }
    
    
}
async function click_btn_GerarGraficoIbov(){
    let selectTpDatas = parseInt(document.getElementById('select-tp-datas').value);
    let selectTpGrupos = parseInt(document.getElementById('select-tp-agrupamento').value);

    let div_Chart = document.getElementById('div-chart-ibov');
    div_Chart.classList.remove('d-none');

    let alertDiv  = document.getElementById('alert-ibov');
    let chartIbov = document.getElementById('chart-ibov');
    chartIbov.classList.add('d-none');
    alertDiv.classList.add('d-none');

    let url = '/get/prices/cotacao/history/ibovespa?tpfiltro=' + selectTpDatas + '&tpgrupo=' +selectTpGrupos ;
    
    let TpNameOneColumn = '';

    let btnGerarGrafico = document.getElementById('btn-gerar-grafico');
    innerBtnTemp = btnGerarGrafico.innerHTML;
    btnGerarGrafico.innerHTML = '<div class="spinner-border text-warning mr-1" role="status">'+
    '<span class="sr-only">Loading...</span></div>Gerando Gráfico...';    
    
    switch (selectTpDatas) {
        // Por Periodo de Datas
        case 0:
            let dtIni = document.getElementById('dt-ini-ibov-grafico').value;
            let dtFinal = document.getElementById('dt-fim-ibov-grafico').value;
            url +='&dtini='+dtIni+'&dtfim='+dtFinal; 
            TpNameOneColumn = 'Data';
            titleChart = 'Histórico Valor Fechamento Diário Ibovespa';
            break;
        // Mensal
        case 1:
            let mesIni   = document.getElementById('mes-ini-ibov-grafico').value;
            let mesFinal = document.getElementById('mes-final-ibov-grafico').value;
            let ano      = document.getElementById('ano-ibov-grafico').value;
            url +='&mesini=' + mesIni + '&mesfim=' + mesFinal + '&ano='+ano; 
            TpNameOneColumn = 'Mês';
            titleChart = 'Histórico Valor Fechamento Mensal Ibovespa';
            break;
        // Anual    
        case 2:
            let anoIni2 = document.getElementById('ano-ini-ibov-grafico').value;
            anoFim2 = document.getElementById('ano-final-ibov-grafico').value;
            url +='&anoini=' + anoIni2 + '&anofim='+anoFim2; 
            TpNameOneColumn = 'Ano';
            titleChart = 'Histórico Valor Fechamento Anual Ibovespa';
            break;
        // Mes por intervalo de anos    
        case 3:
            let mes = document.querySelector('#mes-ibov-grafico').value;
            let anoIni3 = document.querySelector('#ano-inicial').value;
            let anoFim3 = document.querySelector('#ano-final').value;  
            url +='&mes=' + mes + '&anoini=' + anoIni3 + '&anofim=' + anoFim3; 
            TpNameOneColumn = 'Mês';
            titleChart = 'Histórico Valor Fechamento Mês: ' + month_extenso[mes-1];  
            break;
        // Por Pontuação Ranking
        case 4:
            let valRankingPnt = document.getElementById('select-ranking-pontuacao').value;
            let limitePnt     = document.getElementById('select-limite-pontuacao').value;
            let anoIni4        = document.getElementById('ano-inicial').value;
            let anoFim4        = document.getElementById('ano-final').value;
            url += '&rankingpnt=' + valRankingPnt + '&limitepnt=' + limitePnt + '&anoini='+ anoIni4 + '&anofim='+ anoFim4;
            TpNameOneColumn = 'Pontuação'; 
            
            titleChart = (valRankingPnt.value='DESC') ? 'Histórico das '+ limitePnt + ' maiores pontuações.' : 
            'Histórico das '+ limitePnt + ' menores pontuações';
            break;
    }
    let arrayPricesChart = [];
    
    await fetch(url)
    .then(await function(response){
        return response.json()   
    })
    .then(await function(resultJson){
        if (resultJson.result) {
            resultJson.data.sort();
            if (resultJson.data.length > 0){
                arrayPricesChart[0] = [TpNameOneColumn,'Valor',{ role: 'style' }];
                let i = 1;
                resultJson.data.forEach(price => {
                    arrayPricesChart[i] = [price[0],price[1],'color:#d39e00'];
                    i+=1; 
                });
                
                viewChart(arrayPricesChart,titleChart);
                alertDiv.classList.add('d-none');
                chartIbov.classList.remove('d-none');
            }
            else{
                console.log('total') ;   
                alertDiv.classList.remove('d-none')
                alertDiv.innerHTML = 'Nenhum valor encontrado com o filtro passado';
            }
        }
        else{
            alertDiv.classList.remove('d-none')
            alertDiv.innerHTML = 'Erro ao Buscar Valores';
            ;   
        }
    })
    .catch((error) => {
        alertDiv.classList.remove('d-none')
        alertDiv.innerHTML = 'Erro ao Buscar Valores: '+error;    
        
    });
    btnGerarGrafico.innerHTML = innerBtnTemp;
}
function viewChart(arrayData,stitle){
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(arrayData);
        var options = {
            title: stitle,
            curveType: 'function',
            //backgroundColor: '#ffc107',
            is3D: true,
            legend: { position: 'none' }
        };
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-ibov'));
        chart.draw(data, options);
    });

}
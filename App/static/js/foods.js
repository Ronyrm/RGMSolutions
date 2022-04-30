var tbfoods = [];
var data_calc = [];
var thporcao = document.getElementById('th-porcao');

function calcinfonutri(){
    qtdgramasemcima = tbfoods.qtdgramasemcima;
    tbfood = [];
    tbfood.proteina = ((tbfoods.proteina*thporcao.value)/qtdgramasemcima)
    tbfood.carboidrato = (tbfoods.carboidrato*thporcao.value)/qtdgramasemcima;
    tbfood.lipidios = (tbfoods.lipidios*thporcao.value)/qtdgramasemcima;
    tbfood.fibras = (tbfoods.fibras*thporcao.value)/qtdgramasemcima;
    tbfood.calorias = (tbfoods.calorias*thporcao.value)/qtdgramasemcima;
    tbfood.descricao = tbfoods.descricao;
    tbfood.id = tbfoods.id;

    data_calc = tbfood;
    calculardadosnutri(tbfood,thporcao.value);


}

function mostradadosfoods(tbfood,qtdgramas){
    tbfoods = tbfood;
    calculardadosnutri(tbfoods,qtdgramas);
}
function calculardadosnutri(tbfood,qtdgramas){
    console.log(tbfood);
    if (usuariologado){
        document.getElementById('edtidalimento').value = tbfood.id;
    }
    google.charts.load('current', {'packages':['corechart']}).then( function(){

        var data = google.visualization.arrayToDataTable([
        ['Task', 'Hours per Day'],
        ['Protéina', tbfood['proteina']],
        ['Carboidrato', tbfood['carboidrato']],
        ['Gordura', tbfood['lipidios']],
        ['Fibras', tbfood['fibras']]
        ]);

        var options = {//'title':'Informação Nutricional - Total Calorias:',
                       'backgroundColor': 'transparent',
                       'legend':{'position':'rigth'},
                       'chartArea':{'left':0,'top':30,'width':'100%','height':'80%'},
                       'is3D':true,
                       'left': 0,
                       'width':550,
                       'height':300,
                       //'pieHole': 0.4,
                       };
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);

        tablefoods = document.getElementById('table-foods');
        divdadosfood = document.getElementById('div-dadosfood');
        divdescfood = document.getElementById('div-descfood');
        thcalorias = document.getElementById('th-calorias');
        trfood = document.getElementById('tr-food');
        navpaginationfoods = document.getElementById('navpagination-foods');
        divcabfoods = document.getElementById('divcab-foods');

        divdescfood.innerHTML = '<h5>Alimento: '+ tbfood['descricao'] + '</h5>';

        proteina = tbfood['proteina'] == null ? 0 : tbfood['proteina'];

        fibras = tbfood['fibras'] == null ? 0 : tbfood['fibras'];
        carbo = tbfood['carboidrato'] == null ? 0 : tbfood['carboidrato'];
        lipidios = tbfood['lipidios'] == null ? 0 : tbfood['lipidios'];
        sodio = tbfood['sodio'] == null ? 0 : tbfood['sodio'];


        thporcao.value = qtdgramas;
        tdtemp  = '<td class="text-padrao"><small><strong>'+carbo.toFixed(2)+' gr</small></strong></td>';
        tdtemp += '<td class="text-padrao"><small><strong>'+proteina.toFixed(2)+' gr</small></strong></td>';
        tdtemp += '<td class="text-padrao"><small><strong>'+lipidios.toFixed(2)+' gr</small></strong></td>';
        tdtemp += '<td class="text-padrao"><small><strong>'+fibras.toFixed(2)+' gr</small></strong></td>';
        tdtemp += '<td class="text-padrao"><small><strong>'+fibras.toFixed(2)+' gr</small></strong></td>';

        trfood.innerHTML = tdtemp;
        thcalorias.innerHTML = tbfood['calorias'];
        tablefoods.classList.add('d-none');
        divcabfoods.classList.add('d-none');
        navpaginationfoods.classList.add('d-none');
        divdadosfood.classList.remove('d-none');

    });
}

function btnvoltarmain(){
    tablefoods = document.getElementById('table-foods');
    divdadosfood = document.getElementById('div-dadosfood');
    navpaginationfoods = document.getElementById('navpagination-foods');
    divcabfoods = document.getElementById('divcab-foods');

    tablefoods.classList.remove('d-none');
    divcabfoods.classList.remove('d-none');
    navpaginationfoods.classList.remove('d-none');
    divdadosfood.classList.add('d-none');

}


$('#orberby-foods').on('change', function(e) {
    e.preventDefault();
    console.log(pageatual);
    console.log(perpage);
    console.log(this.value);
    valinputdescricao = document.getElementById('input-descricao').value;
    var valorderby = $( "#orberby-foods option:selected" ).val();
    window.location.href = '/tabalimentos?page='+pageatual+'&totpage='+perpage+'&orderby='+valorderby+'&descricao='+valinputdescricao;

});

function click_btnrefeicao(idrefeicao){
    document.getElementById('edtidrefeicao').value = idrefeicao;
    alertmsgaddrefeicao = document.getElementById('alert-msg-addrefeicao');
    alertmsgaddrefeicao.classList.add('d-none');

}

function confirmarinsertrefeicao(){
    document.getElementById('edtqtd').value = thporcao.value;
    continuar = false;
    try{
        continuar = true;
        if (document.getElementById('edtqtd').value ==''){
            document.getElementById('edtqtd').value = '0';
        }

        if (parseFloat(document.getElementById('edtqtd').value) <= 0){
            continuar = false;
        }

        if (document.getElementById('edtidrefeicao').value == '' ||
            document.getElementById('edtidrefeicao').value =='0'){
            continuar = false;
            alertmsgaddrefeicao = document.getElementById('alert-msg-addrefeicao');
            alertmsgaddrefeicao.classList.remove('d-none');
            alertmsgaddrefeicao.classList.add('alert-danger');
            alertmsgaddrefeicao.innerHTML = 'Clique em uma das refeições para continuar';
            setTimeout(function(){
                alertmsgaddrefeicao.classList.add('d-none');
        }, 2000);

        }
    }
    catch{
        continuar = false;
    }
    if (continuar){
        calcinfonutri();

        document.getElementById('edtdescfood').value = data_calc.descricao;
        document.getElementById('edtvalcarbo').value = parseFloat(data_calc.carboidrato).toFixed(2);
        document.getElementById('edtvalproteina').value = parseFloat(data_calc.proteina).toFixed(2);
        document.getElementById('edtvalfat').value = parseFloat(data_calc.lipidios).toFixed(2);
        document.getElementById('edtvalsodio').value = parseFloat(data_calc.sodio).toFixed(2);
        document.getElementById('edtvalfibras').value = parseFloat(data_calc.fibras).toFixed(2);
        document.getElementById('edtvalkcal').value = parseFloat(data_calc.calorias).toFixed(2);
        document.getElementById('edtidalimento').value = data_calc.id;
        addfoodinrefeicao();
    }

}

function addfoodinrefeicao(){
    form = document.getElementById('formrefeicao');
    formData = new FormData(form);
    alertmsgaddrefeicao = document.getElementById('alert-msg-addrefeicao');
    alertmsgaddrefeicao.classList.remove('d-none');
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
            alertmsgaddrefeicao.classList.add('alert-primary');
            alertmsgaddrefeicao.innerHTML = data['mensagem'];
        }
        else{
            alertmsgaddrefeicao.classList.add('alert-danger');
            alertmsgaddrefeicao.innerHTML = data['mensagem'];

        }
        setTimeout(function(){
            if (result){
                alertmsgaddrefeicao.classList.remove('alert-primary');
                window.location.reload(true);
            }
            else{
                alertmsgaddrefeicao.classList.remove('alert-danger');
            }

            alertmsgaddrefeicao.classList.add('d-none');
        }, 2000);
    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });
}

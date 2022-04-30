var formlogin = document.getElementById("form-login");

var imgportifolio = document.getElementById("img-portifolio");
var divsimulator = document.getElementById("div-simulator");
var btnmenu = document.getElementById("btn-menu");
var edtcaloriasexercises = document.getElementById('edt-caloriasexercises');
var edtcaloriasmeta = document.getElementById('edt-caloriasmeta');
var msgfinal = '';
var curRadio = 'ganho';
var vlalvo = 0;
var vlcalmoreless = 0;
var vlcalexerc = 0;
var vlmetakgdia_tp = 0;

var vlkcalproteina = 0;
var vlpercproteina = 0;
var vlgramasproteina = 0;
var vlgrporkgproteina = 0;

var vlkcalcarbo = 0;
var vlperccarbo = 0;
var vlgramascarbo = 0;
var vlgrporkgcarbo = 0;

var vlkcalgordura = 0;
var vlpercgordura = 0;
var vlgramasgordura = 0;
var vlgrporkggordura = 0;

var pesoinicialmetaatleta = 0;

verifydadosgerais();

document.getElementById("edtdateniver").value = retornadata(new Date(),'-');
verificametaselect(0);
divsimulator.classList.add('d-none');

// clica no botão de LOGIN
$('#login-form-link').on('click', function(e) {
    e.preventDefault();
    divsimulator.classList.add('d-none');
    formregistrar = document.getElementById("form-registrar");
    formregistrar.classList.add('d-none');
    formlogin.classList.remove('d-none');
    $('#form-registrar').fadeOut();
    $('#img-portifolio').fadeOut();
    $('#form-login').fadeIn();


    document.getElementById('register-form-link').classList.remove('active');
    document.getElementById('login-form-link').classList.add('active');
    document.getElementById('btnsimulator').classList.remove('active');
});

// clica no botão de REGISTRAR
$('#register-form-link').on('click', function(e) {
    e.preventDefault();
    divsimulator.classList.add('d-none');
    formregistrar = document.getElementById("form-registrar");
    formregistrar.classList.remove('d-none');
    formlogin.classList.add('d-none');

    $('#img-portifolio').fadeOut();
    $('#form-login').fadeOut();
    $('#form-registrar').fadeIn();


    document.getElementById('register-form-link').classList.add('active');
    document.getElementById('login-form-link').classList.remove('active');
    document.getElementById('btnsimulator').classList.remove('active');
});

// clica no botão SIMULADOR
$('#btnsimulator').on('click', function(e) {

    e.preventDefault();

    document.getElementById('btnsimulator').classList.add('active');
    document.getElementById('register-form-link').classList.remove('active');
    document.getElementById('login-form-link').classList.remove('active');
    $('#img-portifolio').fadeOut();
    formregistrar = document.getElementById("form-registrar");
    formregistrar.classList.add('d-none');
    formlogin.classList.add('d-none');

    divsimulator.classList.remove('d-none');
    $('#div-simulator').fadeIn();
});


//#############           FUNCOES PRIMEIRA ETAPA SIMULADOR           #############

// verificar se % gordura esta vazio ao entrar no campo
document.getElementById('edtpercfat').addEventListener("focus", function(){
    verifycampopercfat(this.value);
});
// verificar se % gordura esta vazio ao sair do campo
document.getElementById('edtpercfat').addEventListener("blur", function(){
    verifycampopercfat(this.value);
});

function verifycampopercfat(valor){
    if(valor == ''){
        document.getElementById('lbl-msgdadosgerais').innerHTML =  'Caso não souber o % de Gordura, deixar em branco';
    }
    else{
        document.getElementById('lbl-msgdadosgerais').innerHTML = '';
    }
}

// verifica se o campo peso da com valor maior que zero ou não
$('#edtpeso').on('blur',function(e){
    if ($(this).val()=='0' || $(this).val()==''){
        document.getElementById('msg-peso').innerHTML = 'Forneça o Peso para continuar';
    }
    else{
        document.getElementById('msg-peso').innerHTML = '';
    }
    verifydadosgerais();
});

// verifica se o campo altura da com valor maior que zero ou não
$('#edtaltura').on('blur',function(e){
    if ($(this).val()=='0' || $(this).val()==''){
        document.getElementById('msg-altura').innerHTML = 'Forneça a Altura para continuar';
    }
    else{
        document.getElementById('msg-altura').innerHTML = '';
    }
    verifydadosgerais();
});

// habilita  ou não botão PROXIMO primeira etapa
function verifydadosgerais(){
    document.getElementById('btnprimeiraetapa').disabled = true;
    if (document.getElementById('edtpeso').value.length > 0 && document.getElementById('edtaltura').value.length > 0) {
        document.getElementById('btnprimeiraetapa').disabled = false;
    }
}

// Botão Proximo Primeira tela simulador = Dados pessoais
$('#btnprimeiraetapa').on('click', function(e) {
    e.preventDefault();

    valpeso = document.getElementById('edtpeso').value;
    valaltura = document.getElementById('edtaltura').value;

    valpercfat = document.getElementById('edtpercfat').value;
    valgenero = $( "#selectgenero option:selected" ).val();

    document.getElementById('msg-altura').innerHTML = '';
    document.getElementById('msg-peso').innerHTML = '';

    if ((valaltura=='0')||(valaltura=='')){
        document.getElementById('msg-altura').innerHTML = 'Forneça a Altura(em CM) para continuar';
        document.getElementById('edtaltura').focus();
    }
    else
    {
        if ((valpeso=='0')||(valpeso=='')){
            document.getElementById('msg-peso').innerHTML = 'Forneça o Peso para continuar';
            document.getElementById('edtpeso').focus();
        }
        else
        {
            formsimuladortwoetap = document.getElementById('form-simulador-twoetap');
            formsimuladoroneetap = document.getElementById('form-simulador-oneetap');
            formsimuladoroneetap.classList.add('d-none');
            formsimuladortwoetap.classList.remove('d-none');

        }
    }

});

//#############           FUNCOES SEGUNDA ETAPA SIMULADOR           #############

// clica botão voltar presente na SEGUNDA ETAPA DO SIMULADOR
$('#btnvoltarsegundaetapa').on('click', function(e) {
    e.preventDefault();
    formsimuladortwoetap = document.getElementById('form-simulador-twoetap');
    formsimuladoroneetap = document.getElementById('form-simulador-oneetap');
    formsimuladoroneetap.classList.remove('d-none');
    formsimuladortwoetap.classList.add('d-none');
});

//retorna linhas tabela formulas TMB
function retornrowsformula(valna,valgenero,valpeso,valaltura,valpercfat,idade,logado){

    trbody = '';
    //calcula  Harris-Benedict (original)
    valharris_original = harris_original(valgenero,valpeso,valaltura,idade);
    valtdde = valharris_original*valna;

    trbody = '<tr>';
    trbody += '<th  scope="row">Harris-Benedict (original) </th>';
    titleformula = "'Fórmula Herris-Benedict Original'";
    trbody += '<td class="align-middle text-center"><a class="text-warning" data-toggle="modal" data-target="#modal-info" onclick="chamamodalinfo('+titleformula+',msginfo.formula_harris_benedict);" ><span class="glyphicon glyphicon-info-sign"></span></a></td>';
    trbody += '<td class="align-middle text-center">'+valharris_original.toFixed(0)+'</td>';
    trbody += '<td class="align-middle text-center">'+valtdde.toFixed(0)+'</td>';
    if (!logado){
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk" onclick="checkedbmr();"></td>';
    }else{
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk-meta" onclick="checkedbmr_meta();"></td>';
    }
    trbody += '</tr>';

    //calcula  Harris-Benedict (revisada)
    valharris_revisada = harris_revisada(valgenero,valpeso,valaltura,idade);
    valtdde = valharris_revisada*valna;
    trbody += '<tr>';
    trbody += '<th  scope="row">Harris-Benedict (Revisada)</th>';
    titleformula = "'Fórmula Herris-Benedict Revisada'";
    trbody += '<td class="align-middle text-center"><a class="text-warning" data-toggle="modal" data-target="#modal-info" onclick="chamamodalinfo('+titleformula+',msginfo.formula_harris_benedict_revisada);" ><span class="glyphicon glyphicon-info-sign"></span></a></td>';
    trbody += '<td class="align-middle text-center">'+valharris_revisada.toFixed(0)+'</td>';
    trbody += '<td class="align-middle text-center">'+valtdde.toFixed(0)+'</td>';
    if (!logado){
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk" onclick="checkedbmr();"></td>';
    }else{
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk-meta" onclick="checkedbmr_meta();"></td>';
    }
    trbody += '</tr>';

    //calcula  Mifflin St Jeor
    valmiflin = mifflin(valgenero,valpeso,valaltura,idade)
    valtdde = valmiflin*valna;
    trbody += '<tr>';
    trbody += '<th scope="row">Mifflin St Jeor</th>';
    titleformula = "'Fórmula Mifflin St Jeor'";
    trbody += '<td class="align-middle text-center"><a class="text-warning" data-toggle="modal" data-target="#modal-info" onclick="chamamodalinfo('+titleformula+',msginfo.formula_mifflin);" ><span class="glyphicon glyphicon-info-sign"></span></a></td>';
    trbody += '<td class="align-middle text-center">'+valmiflin.toFixed(0)+'</td>';
    trbody += '<td class="align-middle text-center">'+valtdde.toFixed(0)+'</td>';
    if (!logado){
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk" onclick="checkedbmr();"></td>';
    }else{
        trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk-meta" onclick="checkedbmr_meta();"></td>';
    }
    trbody += '</tr>';

    //calcula  Katch-McArdle
    if (valpercfat == ''){
        valpercfat = '0';
    }
    if (parseFloat(valpercfat) > 0){
        valkatchmcardle = katchmcardle(valpeso,valpercfat);
        valtdde = valkatchmcardle*valna;
        trbody += '<tr>';
        trbody += '<th scope="row">Katch-McArdle</th>';
        titleformula = "'Fórmula Katch-McArdle'";
        trbody += '<td class="align-middle text-center"><a class="text-warning" data-toggle="modal" data-target="#modal-info" onclick="chamamodalinfo('+titleformula+',msginfo.formula_katchmcardle);" ><span class="glyphicon glyphicon-info-sign"></span></a></td>';
        trbody += '<td class="align-middle text-center">'+valkatchmcardle.toFixed(0)+'</td>';
        trbody += '<td class="align-middle text-center">'+valtdde.toFixed(0)+'</td>';

        if (!logado){
            trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk" onclick="checkedbmr();"></td>';
        }else{
            trbody += '<td class="align-middle text-center"><input type="checkbox" name="chk-meta" onclick="checkedbmr_meta();"></td>';
        }
        trbody += '</tr>';
    }

    return trbody;
}

// clica no item nivel de atividade selecionado
function btnnivelatv(valna){

    valdtnascimento = document.getElementById('edtdateniver').value;
    valpeso = document.getElementById('edtpeso').value;
    valaltura = document.getElementById('edtaltura').value;
    valpercfat = document.getElementById('edtpercfat').value;
    valgenero = $( "#selectgenero option:selected" ).val();

    idade = retornaidade(valdtnascimento);


    bodyBMR = document.getElementById('body-BMR');
    bodyBMR.innerHTML = retornrowsformula(valna,valgenero,valpeso,valaltura,valpercfat,idade,false);

    formsimuladortwoetap = document.getElementById('form-simulador-twoetap');
    formsimuladorthreeetap =document.getElementById('form-simulador-threeetap');
    formsimuladortwoetap.classList.add('d-none');
    formsimuladorthreeetap.classList.remove('d-none');
    document.getElementById('btnproximoformula').disabled = true;
}

function btnnivelatv_meta(valna){
    document.getElementById('btnavancarformula').disabled = true;
    edtmediabmr = document.getElementById('edtmediabmr-meta');
    edtmediatdee = document.getElementById('edtmediatdee-meta');

    edtmediatdee.innerHTML = 0;
    edtmediabmr.innerHTML = 0;
    document.getElementById('edtnameta').value = valna;
    valpeso = document.getElementById('edtpesoinicialmetaatleta').value;
    valaltura = document.getElementById('edtalturaatleta').value;
    valpercfat = document.getElementById('edtpercfatinicialmetaatleta').value;
    valgenero = document.getElementById('selectgeneroatleta').value;
    valdtnascimento = document.getElementById('edtdtbirthatleta').value;
    console.log(valdtnascimento);

    idade =  retornaidade(valdtnascimento);


    bodyBMR = document.getElementById('body-BMR-meta');
    bodyBMR.innerHTML = retornrowsformula(valna,valgenero,valpeso,valaltura,valpercfat,idade,true);
}


//#############           FUNCOES TERCEIRA ETAPA SIMULADOR           #############

// clica botão voltar presente na TERCEIRA ETAPA DO SIMULADOR
$('#btnvoltarna').on('click', function(e) {
    e.preventDefault();
    formsimuladortwoetap = document.getElementById('form-simulador-twoetap');
    formsimuladorthreeetap = document.getElementById('form-simulador-threeetap');
    formsimuladortwoetap.classList.remove('d-none');
    formsimuladorthreeetap.classList.add('d-none');
    edtmediabmr = document.getElementById('edtmediabmr');
    edtmediatdee = document.getElementById('edtmediatdee');
    edtmediabmr.innerHTML = '0';
    edtmediatdee.innerHTML = '0';
});

// CHECK BOX, Seleciona quais os valores das formulas irão fazer parte da média
function checkedbmr(){
    checkboxs = document.getElementsByName('chk');
    //checkboxs = Array.from(checkboxs);
    tabbmr = document.getElementById('tab-bmr');

    valortotbmr = 0;
    valortottdee = 0;
    contchk = 0;
    for (i = 1; i < tabbmr.rows.length-1; i++) {
        objCells = tabbmr.rows.item(i).cells;
        if(checkboxs[i-1]['checked'] == true){
            valortotbmr = valortotbmr + parseFloat(objCells.item(2).innerHTML);
            valortottdee = valortottdee +  parseFloat(objCells.item(3).innerHTML);
            contchk = contchk +1;
        }


        //for (var j = 0; j < objCells.length; j++) {
        //console.log('Posição J: '+i+' - '+objCells.item(j).innerHTML);
        //}
    }
    valmediabmr = 0;
    valmediatdee = 0;
    if (contchk != 0){
        valmediabmr = valortotbmr / contchk;
        valmediatdee = valortottdee / contchk;
    }
    edtmediabmr = document.getElementById('edtmediabmr');
    edtmediatdee = document.getElementById('edtmediatdee');

    edtmediabmr.innerHTML = valmediabmr.toFixed(0);
    edtmediatdee.innerHTML = valmediatdee.toFixed(0);

    document.getElementById('btnproximoformula').disabled = false;
    if (document.querySelectorAll('input[name="chk"]:checked').length == 0) {
        document.getElementById('btnproximoformula').disabled = true;
    }


}

function checkedbmr_meta(){
    checkboxs = document.getElementsByName('chk-meta');
    //checkboxs = Array.from(checkboxs);
    tabbmr = document.getElementById('tab-bmr-meta');

    edtfrmharrisoriginal = document.getElementById('edtfrmharrisoriginal');
    edtfrmharrisoriginal.value = 'N';
    edtfrmharrisrevisada = document.getElementById('edtfrmharrisrevisada');
    edtfrmharrisrevisada.value = 'N';
    edtfrmmiffin = document.getElementById('edtfrmmiffin');
    edtfrmmiffin.value = 'N';
    edtfrmkatch = document.getElementById('edtfrmkatch');
    edtfrmkatch.value = 'N';

    valortotbmr = 0;
    valortottdee = 0;
    contchk = 0;
    for (i = 1; i < tabbmr.rows.length-1; i++) {
        objCells = tabbmr.rows.item(i).cells;
        console.log(i+' - '+objCells.item(0).innerHTML);
        if(checkboxs[i-1]['checked'] == true){
            switch(i) {
                case 1:
                    edtfrmharrisoriginal.value = 'S';
                    break;
                case 2:
                    edtfrmharrisrevisada.value = 'S';
                    break;
                case 3:
                    edtfrmmiffin.value = 'S';
                    break;
                case 4:
                    edtfrmkatch.value = 'S';
                    break;
            }
            valortotbmr = valortotbmr + parseFloat(objCells.item(2).innerHTML);
            valortottdee = valortottdee +  parseFloat(objCells.item(3).innerHTML);
            contchk = contchk +1;
        }


        //for (var j = 0; j < objCells.length; j++) {
        //console.log('Posição J: '+i+' - '+objCells.item(j).innerHTML);
        //}
    }
    valmediabmr = 0;
    valmediatdee = 0;
    if (contchk != 0){
        valmediabmr = valortotbmr / contchk;
        valmediatdee = valortottdee / contchk;
    }
    edtmediabmr = document.getElementById('edtmediabmr-meta');
    edtmediatdee = document.getElementById('edtmediatdee-meta');

    edtmediabmr.innerHTML = valmediabmr.toFixed(0);
    edtmediatdee.innerHTML = valmediatdee.toFixed(0);

    document.getElementById('btnavancarformula').disabled = true;
    if (valmediabmr > 0) {
        document.getElementById('btnavancarformula').disabled = false;
    }

}

// clica botão proxima tela = Escolha da meta
$('#btnproximoformula').on('click', function(e) {
    e.preventDefault();
    formsimuladorthreeetap = document.getElementById('form-simulador-threeetap');
    formsimuladorfouretap = document.getElementById('form-simulador-fouretap');
    formsimuladorfouretap.classList.remove('d-none');
    formsimuladorthreeetap.classList.add('d-none');

    // Meta média final BMR
    lblmymetabmr =  document.getElementById('lbl-mymeta-bmr');
    edtmediabmr = document.getElementById('edtmediabmr');
    lblmymetabmr.innerHTML = 'TMB: '+ edtmediabmr.innerHTML;
    //Meta média final TDEE
    lblmymetatdee =  document.getElementById('lbl-mymeta-tdee');
    edtmediatdee = document.getElementById('edtmediatdee');
    lblmymetatdee.innerHTML = 'GCD: '+ edtmediatdee.innerHTML;


    validacamposmeta();

});


//#############           FUNCOES QUARTA ETAPA SIMULADOR           #############

// clica botão voltar presente na QUARTA ETAPA DO SIMULADOR
$('#btnvoltarformula').on('click', function(e) {
    e.preventDefault();
    formsimuladorthreeetap = document.getElementById('form-simulador-threeetap');
    formsimuladorfouretap = document.getElementById('form-simulador-fouretap');
    formsimuladorthreeetap.classList.remove('d-none');
    formsimuladorfouretap.classList.add('d-none');

});
function checkmeta(){
    curRadio = document.querySelector('input[name="radiometa"]:checked').value;
    verificametaselect((curRadio=='ganho')?0:1);
    validacamposmeta();
}

function verificametaselect(valor){

    lbltipometa = document.getElementById('label-tipometa');
    lbltipometa.innerHTML = (valor == 0) ? 'Excedente Calórico Diário <a class="text-warning a-info" href="#"><span class="glyphicon glyphicon-info-sign"></span></a>' : 'Defícit Calórico Diário <a class="text-warning a-info" href="#"><span class="glyphicon glyphicon-info-sign"></span></a>';
}

function checkmeta_atleta(){
    curRadio = document.querySelector('input[name="radiometaatleta"]:checked').value;
    verificametaatletaselect((curRadio=='ganho')?0:1);

}

function verificametaatletaselect(valor){
    document.getElementById('edtobjetivometa').value = (valor == 1) ? 'P' : 'G';
    document.getElementById('lbltipometaatleta').innerHTML = (valor == 0) ? 'Excedente Calórico Diário <a class="text-warning a-info" href="#"><span class="glyphicon glyphicon-info-sign"></span></a>' : 'Defícit Calórico Diário <a class="text-warning a-info" href="#"><span class="glyphicon glyphicon-info-sign"></span></a>';
}

//#############           FUNCOES Quinta ETAPA SIMULADOR           #############

// verificar campo calorias excedente/deficit se ta vazio ou zero - na entrada
edtcaloriasmeta.addEventListener("focus", function(){

    if(edtcaloriasmeta.value == '0'){
        edtcaloriasmeta.value = '';
    }
    curRadio = document.querySelector('input[name="radiometa"]:checked').value;
    tipo = (curRadio=='ganho')? 'excedente' : 'defícit';
    tipo = 'Forneça as Calorias '+tipo;
    validacamposmeta();

});
// verificar campo calorias excedente/deficit  se ta vazio ou zero - na saida
edtcaloriasmeta.addEventListener("blur", function(){
    curRadio = document.querySelector('input[name="radiometa"]:checked').value;
    tipo = (curRadio=='ganho')? 'excedente' : 'defícit';
    tipo = 'Forneça as Calorias '+tipo;
    validacamposmeta();
});

// verificar campo calorias dos exercicios se ta vazio ou zero - na entrada
edtcaloriasexercises.addEventListener("focus", function(){
    if(edtcaloriasexercises.value == '0'){
        edtcaloriasexercises.value = '';
    }

    validacamposmeta();
});
// verificar campo calorias excedente/deficit  se ta vazio ou zero - na saida
edtcaloriasexercises.addEventListener("blur", function(){
    validacamposmeta();
});



function validacamposmeta(){
    vlalvo = 0;
    vlcalmoreless = (edtcaloriasmeta.value=='') ? 0 : parseFloat(edtcaloriasmeta.value);
    vlcalexerc = (edtcaloriasexercises.value=='') ? 0 : parseFloat(edtcaloriasexercises.value);

    curRadio = document.querySelector('input[name="radiometa"]:checked').value;
    if (curRadio == 'ganho'){
        vlalvo = parseFloat(edtmediatdee.innerHTML) + vlcalmoreless + vlcalexerc;
    }
    else{
        vlalvo = parseFloat(edtmediatdee.innerHTML) + vlcalexerc;
        vlalvo = vlalvo - vlcalmoreless;
    }


    document.getElementById('lbl-alvocaloricodia').innerHTML = 'Alvo de Calorias Diária: <strong>'+ vlalvo + '</strong>' ;
    document.getElementById('btn-result').disabled = false;
    //}
}
document.getElementById('btnvoltarmeta').addEventListener("click", function(e){
    e.preventDefault();
    formsimuladorfouretap = document.getElementById('form-simulador-fouretap');
    formsimuladorfiveetap = document.getElementById('form-simulador-fiveetap');
    formsimuladorfiveetap.classList.add('d-none');
    formsimuladorfouretap.classList.remove('d-none');
});
document.getElementById('btn-result').addEventListener("click", function(e){
    e.preventDefault();
    formsimuladorfouretap = document.getElementById('form-simulador-fouretap');
    formsimuladorfiveetap = document.getElementById('form-simulador-fiveetap');
    formsimuladorfiveetap.classList.remove('d-none');
    formsimuladorfouretap.classList.add('d-none');

    calcularesultfinal();

});

document.getElementById('btnvoltarfouretapa').addEventListener("click", function(e){
    e.preventDefault();
    formsimuladorfouretap = document.getElementById('form-simulador-fouretap');
    formsimuladorthreeetap = document.getElementById('form-simulador-threeetap');

    formsimuladorfouretap.classList.add('d-none');
    formsimuladorthreeetap.classList.remove('d-none');

});

function verifycampokgfatempty(){
    kcalkgfat = document.getElementById('edt-kcalkgfat').value;
    if (kcalkgfat == '' | kcalkgfat == '0'){
        kcalkgfat = 3500;
        document.getElementById('edt-kcalkgfat').value = 3500;
    }
    return kcalkgfat;
}

//  calcula e preenche os campos referente a quantidade de kilograma que ira ganhar ou perder de acordo com dia, semana, mes, ano
function calcmetakg(vlmetakaldia,vlkcalkgfat){

    vlmetakgdia = (vlmetakaldia/vlkcalkgfat);
    vlmetakgdia = vlmetakgdia * 0.4536;

    // KG por dia
    if (vlmetakgdia < 1){
        document.getElementById('lblpesodia').innerHTML = ' gr';
        vlmetakgdia_tp = vlmetakgdia*1000;
        document.getElementById('edtpesodia').value = (vlmetakgdia_tp).toFixed(0);
    }
    else{
        document.getElementById('lblpesodia').innerHTML = ' kg';
        document.getElementById('edtpesodia').value = (vlmetakgdia_tp).toFixed(3);
    }


    //KG por semana
    vlmetakgsemana = vlmetakgdia * 7;
    if (vlmetakgsemana < 1){
        document.getElementById('lblpesosemanal').innerHTML = ' gr';
        vlmetakgsemana = vlmetakgsemana * 1000;
        document.getElementById('edtpesosemanal').value = vlmetakgsemana.toFixed(0);
    }
    else{
        document.getElementById('lblpesosemanal').innerHTML = ' kg';
        document.getElementById('edtpesosemanal').value = vlmetakgsemana.toFixed(3);
    }



    //KG por mes
    vlmetakgmensal = vlmetakgdia * 30.5;
    if (vlmetakgmensal < 1){
        document.getElementById('lblpesomensal').innerHTML = ' gr';
        vlmetakgmensal = vlmetakgmensal * 1000;
        document.getElementById('edtpesomensal').value = vlmetakgmensal.toFixed(0);
    }
    else{
        document.getElementById('lblpesomensal').innerHTML = ' kg';
        document.getElementById('edtpesomensal').value = vlmetakgmensal.toFixed(3);
    }
    //KG por ano
    vlmetakganual = vlmetakgdia * 365;

    if(vlmetakganual < 1){
        document.getElementById('lblpesoanual').innerHTML = ' gr';
        vlmetakganual = vlmetakganual * 1000;
        document.getElementById('edtpesoanual').value = vlmetakganual.toFixed(0);
    }
    else{
        document.getElementById('lblpesoanual').innerHTML = ' kg';
        document.getElementById('edtpesoanual').value = vlmetakganual.toFixed(3);
    }

}

//  calcula e preenche os campos referente a quantidade de kcal que ira ganhar ou perder de acordo com dia, semana, mes, ano
function calcmetakcal(vlmetakaldia){
    document.getElementById('edtmetakaldia').value = vlmetakaldia;
    document.getElementById('edtmetakalsemanal').value = (vlmetakaldia * 7).toFixed(0) ;
    document.getElementById('edtmetakalmensal').value =  (vlmetakaldia * 30.5).toFixed(0);
    document.getElementById('edtmetakalanual').value = (vlmetakaldia * 365).toFixed(0);
}

//preeche campos da linha calorias dos exercicios: dia, semana, mes e ano
function preenchedadoskcalexec(vlkcalexecdia){
    document.getElementById('edtKcalExecsemanal').value = (vlkcalexecdia * 7).toFixed(0);
    document.getElementById('edtKcalExecmensal').value = (vlkcalexecdia * 30.5).toFixed(0);
    document.getElementById('edtKcalExecanual').value = (vlkcalexecdia * 365).toFixed(0);

}
//preeche campos da linha calorias alvo: dia, semana, mes e ano
function preenchedadadoskcalalvo(vlkcalalvodia){
    document.getElementById('edtalvokcalsemanal').value = (vlkcalalvodia * 7).toFixed(0);
    document.getElementById('edtalvokcalmensal').value = (vlkcalalvodia * 30.5).toFixed(0);
    document.getElementById('edtalvokcalanual').value = (vlkcalalvodia * 365).toFixed(0);
}

//preeche campos da linha calorias TMB: dia, semana, mes e ano
function preenchedadadoskcalbmr(vlkcalbmr){
    document.getElementById('edtbmrsemanal').value = (vlkcalbmr * 7).toFixed(0);
    document.getElementById('edtbmrmensal').value = (vlkcalbmr * 30.5).toFixed(0);
    document.getElementById('edtbmranual').value = (vlkcalbmr * 365).toFixed(0);
}

//preeche campos da linha calorias TMB: dia, semana, mes e ano
function preenchedadadoskcalgcd(vlkcalgcddia){
    document.getElementById('edtgcdsemanal').value = (vlkcalgcddia * 7).toFixed(0);
    document.getElementById('edtgcdmensal').value = (vlkcalgcddia * 30.5).toFixed(0);
    document.getElementById('edtgcdanual').value = (vlkcalgcddia * 365).toFixed(0);
}
// on change Campo input "Kcal excedente ou perda  tela de Resultado Final
document.getElementById('edtmetakaldia').addEventListener("change", function(e){
    e.preventDefault();
    edtcaloriasmeta.value = this.value;
    if (edtcaloriasmeta.value == ''){
        edtcaloriasmeta.value = '0';
        this.value = '0';
    }
    calcularesultfinal();

});
// CHANGE INPUT kcal meta semanal
document.getElementById('edtmetakalsemanal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'S');
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();
});
// CHANGE INPUT kcal meta mensal
document.getElementById('edtmetakalmensal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'M');
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();
});
// CHANGE INPUT kcal meta anual
document.getElementById('edtmetakalanual').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'A');
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();
});


// on change Campo input "Kcal dos exercicios tela de Resultado Final
document.getElementById('edtKcalExecdia').addEventListener("change", function(e){
    e.preventDefault();
    edtcaloriasexercises.value = this.value;
    if (edtcaloriasexercises.value == ''){
        edtcaloriasexercises.value = '0';
        this.value = '0';
    }
    calcularesultfinal();
});

// CHANGE INPUT kcal exercicios semanal
document.getElementById('edtKcalExecsemanal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'S');
    document.getElementById('edtKcalExecdia').value = result;
    edtcaloriasexercises.value = result;

    calcularesultfinal();
});


// CHANGE INPUT kcal exercicios mensal
document.getElementById('edtKcalExecmensal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'M');
    document.getElementById('edtKcalExecdia').value = result;
    edtcaloriasexercises.value = result;

    calcularesultfinal();
});

// CHANGE INPUT kcal exercicios anual
document.getElementById('edtKcalExecanual').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }

    result = calc_kcal_weekmonthyear((this.value=='')?'0':this.value,'A');
    document.getElementById('edtKcalExecdia').value = result;
    edtcaloriasexercises.value = result;

    calcularesultfinal();
});
// change Ganho ou perda de Peso
document.getElementById('edtpesodia').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }
    result = calccalporkg(this.value/1000).toFixed(0);
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();

});

document.getElementById('edtpesosemanal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }


    result = calccalporkg((this.value/1000)/7).toFixed(0);
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();

});

document.getElementById('edtpesomensal').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }


    result = calccalporkg((this.value/30.5)).toFixed(0);
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();

});

document.getElementById('edtpesoanual').addEventListener("change", function(e){
    e.preventDefault();
    if (this.value < -1) {
        this.value = 0;
    }


    result = calccalporkg((this.value/365)).toFixed(0);
    document.getElementById('edtmetakaldia').value = result;
    edtcaloriasmeta.value = result;

    calcularesultfinal();

});



function calccalporkg(valorkgdia){
    return  ((valorkgdia / 0.453592) * verifycampokgfatempty());
}
// CALCULA RESULTADO FINAL E PREECHE VALORES
function calcularesultfinal(){
    validacamposmeta();

    //curRadio = document.querySelector('input[name="radiometa"]:checked').value;
    if (curRadio=='ganho'){
        document.getElementById('lbl-tipometa').innerHTML = '<strong>Ganho</strong>';
        document.getElementById('lbl-desctipometa').innerHTML = '<strong>Excedente Calórico</strong>';
    }
    if (curRadio=='perda'){
        document.getElementById('lbl-tipometa').innerHTML = '<strong>Perda</strong>';
        document.getElementById('lbl-desctipometa').innerHTML = '<strong>Defícit Calórico</strong>';
    }

    edtmediabmr = document.getElementById('edtmediabmr');
    edtmediatdee = document.getElementById('edtmediatdee');


    document.getElementById('edtmetakaldia').value = vlcalmoreless;
    document.getElementById('edtbmrdia').value = edtmediabmr.innerHTML;
    document.getElementById('edtgcddia').value = edtmediatdee.innerHTML;
    document.getElementById('edtKcalExecdia').value = vlcalexerc;
    document.getElementById('edtalvokcaldia').value = vlalvo;


    vlkcalkgfat = verifycampokgfatempty();
    calcmetakg(vlcalmoreless,vlkcalkgfat);
    calcmetakcal(vlcalmoreless);

    preenchedadoskcalexec(vlcalexerc);

    preenchedadadoskcalalvo(vlalvo);
    preenchedadadoskcalbmr(edtmediabmr.innerHTML);
    preenchedadadoskcalgcd(edtmediatdee.innerHTML);


}

function calc_kcal_weekmonthyear(valor,tipo){
    result = 0;
    if (valor != '0'){
        switch(tipo) {
            case "S":
                result = (valor/7).toFixed(0);
                break;
            case "M":
                result = (valor/30.5).toFixed(0);
                break;
            case "A":
                result = (valor/365).toFixed(0);
                break;
        }
    }
    return result;
}
function chamamodalinfo(title,msg){
    document.getElementById('modal-infotitle').innerHTML = title;
    document.getElementById('modal-infobody').innerHTML = msg;

}

function buscarefeicaoatleta(){
    if (idatleta != '0' && idatleta != ''){
        //console.log('Atleta:'+idatleta);
        $.ajax({
            url: '/get/refeicao/atleta',
            type: 'GET',
            data: 'idatleta='+idatleta,
            dataType: 'json',
            cache: false,
            async: true,
            success:function(data) {
                        if(data.result == true){
                            document.getElementById('span-total-ref').innerHTML = data.total;
                            data_refeicao = data.data;

                            setTimeout(function(){
                                //console.log(data['data']);
                            }, 3000);
                        }
            }
        })
        .always(
        )
        .fail(function() {
            console.log('Erro');
            // Caso falhe solicite outro id
        });
    }
}
async function teste(){
    let response = await fetch('/get/refeicao/atleta?idatleta='+idatleta);
    let data = await response.json();
    return data;
    console.log('Aqui --------');
    console.log(data);
    console.log('Aqui --------');
}
// Botão Menu Refeições.
function mostrarrefeicoes(){
    btnmostrarefeicoes = document.getElementById('btnmostrarefeicoes')
    teste().then((value) => {
        console.log("Entrei Aqui");
        console.log(value);
    });
    btnmostrarefeicoes.classList.add('active');

    divrefatleta = document.getElementById('divrefatleta');
    divrefatleta.classList.remove('d-none');
    document.getElementById('btndadosatleta').classList.remove('active');

    divdadosatleta =document.getElementById('div-dados-atleta');
    divdadosatleta.classList.add('d-none');
    //buscarefeicaoatleta();
    //$.each(data_refeicao, function(chave,valor){
        //console.log(chave + ' - '+valor);
    //    console.log(valor['descricao']);
    //});

    document.getElementById('div-meta-atleta').classList.add('d-none');
    document.getElementById('btnmostrarmeta').classList.remove('active');

}

// Botão Voltar da tela de Refeição
function btnvoltarref(){
    divrefatleta = document.getElementById('divrefatleta');
    divrefatleta.classList.add('d-none');
    document.getElementById('btnmostrarefeicoes').classList.remove('active');
}

// Botão Editar Refeição
function editrefeicao(refeicao){

    document.getElementById('lblidrefeicao').innerHTML = 'Alterando a Refeição: '+refeicao.descricao;
    document.getElementById('edtdescricao').value = refeicao.descricao;
    document.getElementById('edthora').value = refeicao.hora;
    document.getElementById('edtidrefeicao').value = refeicao.id;
    document.getElementById('edtidpessoa-refeicao').value = refeicao.pessoa;

    chkmostrar = document.getElementById('edtmostrar');
    if (refeicao.mostrar == 'S') {
        chkmostrar.checked = true;
    }
    else{
        chkmostrar.checked = false;

    }

}

// Botão Inserir Refeição
function btninsertrefeicao(idpessoa){
    console.log('Pessoa:'+idpessoa);
    document.getElementById('lblidrefeicao').innerHTML = 'Inserindo Refeição';
    document.getElementById('edtdescricao').value = '';
    document.getElementById('edthora').value = '00:00';
    document.getElementById('edtidrefeicao').value = '-1';
    console.log(idpessoa);
    document.getElementById('edtidpessoa-refeicao').value = idpessoa;
    chkmostrar = document.getElementById('chkativa');
    divdadosatleta = document.getElementById('div-dados-atleta');
    divdadosatleta.classList.add('d-none');

}

// Botão Gravar Modal Inserir e Editar Refeição
function gravarrefeicao(){

    form = document.getElementById('formrefeicao');
    formData = new FormData(form);
    $.ajax({
        url: '/post/refeicao',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        alert_dadosrefeicao = document.getElementById('alert-dadosrefeicao');
        if (data.result == true) {

            alert_dadosrefeicao.classList.add("alert-primary");
            alert_dadosrefeicao.innerHTML = '<strong>Sucesso</strong> <br> '+data['mensagem'];
            alert_dadosrefeicao.classList.remove('d-none');

            setTimeout(function(){
                $('#insert-edit-modal-refeicao').modal('hide');
                alert_dadosrefeicao.classList.remove('alert-primary');
                alert_dadosrefeicao.classList.add('d-none');

                //window.location.href = '/sisnutri';
                tbodyrefeicoes = document.getElementById('tbody-refeicoes');
                tab = '';
                refeicoes = data['data'];
                totalreg = refeicoes.length;
                refeicoes.forEach((refeicao) => {

                    tab += '<tr id="tr-refeicao'+refeicao.id+'" title="tr-reifeicao'+refeicao.id+'">';
                    tab += '<td class="align-middle"><label class="text-warning">'+refeicao.descricao+'</label></td>';
                    tab += '<td class="align-middle text-center"><label class="text-warning">'+refeicao.hora.substr(0, 5)+'</label></td>';
                    tab += '<td class="align-middle text-center">';
                    if (refeicao.mostrar == 'S'){
                        tab += '<input type="checkbox" checked name="chkativa'+refeicao.id+'" onclick="return false;" onkeydown="return false;" >';
                    }
                    else{
                        tab += '<input type="checkbox"  name="chkativa'+refeicao.id+'" onclick="return false;" onkeydown="return false;" >';
                    }
                    tab += '</td>';
                    tab += '<td class="text-center">';
                    tab += '<button class="btn btn-sm btn-warning mx-1 my-1"';
                    tab += ' title="Editar '+refeicao.descricao+'"';
                    tab += ' data-toggle="modal" data-target=".insert-edit-modal-refeicao"';

                    descricao = '"'+refeicao.descricao+'"';
                    hora = '"'+refeicao.hora+'"';
                    mostrar = "'"+refeicao.mostrar+"'";

                    tab += " onclick='editrefeicao("+JSON.stringify(refeicao)+");'>";
                    //tab += ' onclick="editrefeicao('+refeicao.id+','+descricao+','+hora+','+mostrar);">';
                    tab += ' <span class="glyphicon glyphicon-pencil"></span>';
                    tab += '</button> ';
                    tab += '<button class="btn btn-sm btn-danger mx-1 my-1"';
                    tab += ' data-toggle="modal" data-target=".modal-delete-refeicao"';
                    tab += ' title="Excluir '+refeicao.descricao+'"';
                    tab += " onclick='deleterefeicao("+refeicao.id+","+descricao+");'>";
                    tab += ' <span class="glyphicon glyphicon-trash"></span>';
                    tab += '</button> ';
                    tab += '</td></tr>';
                });

                tbodyrefeicoes.innerHTML = tab;
                verifica_table_refeicao_empty(totalreg);

            }, 2000);

        }
        else{
            alert_dadosrefeicao.classList.add('alert-danger');
            alert_dadosrefeicao.innerHTML = '<strong>Erro</strong> <br> '+data['mensagem'];
            alert_dadosrefeicao.classList.remove('d-none');
            setTimeout(function(){
                alert_dadosrefeicao.classList.remove('alert-danger');
                alert_dadosrefeicao.classList.add('d-none');

            }, 2000);
        }

    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });
}

//Excluir Refeicao
function deleterefeicao(id,descricao){
    document.getElementById('edtiddelete').value = id;
    document.getElementById('modal-msg-delete').innerHTML = 'Deseja excluir a Refeição:<strong> '+descricao+'?</strong>';
}
//Confirma Exclusão
function confirmaexclusaorefeicao(){
    id = document.getElementById('edtiddelete').value;
    rowrefeicao = document.getElementById('tr-refeicao'+id);

    $.ajax({
        url: '/del/refeicao/atleta/'+id,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        alertmsg = document.getElementById('alert-msgdelete');
        if (data.result == true) {
            alertmsg.classList.add("alert-primary");
            alertmsg.innerHTML = '<strong>Sucesso</strong> <br> '+data['mensagem'];
            alertmsg.classList.remove('d-none');

            setTimeout(function(){
                $('#modal-delete-refeicao').modal('hide');
                alertmsg.classList.remove('alert-primary');
                alertmsg.classList.add('d-none');
                rowrefeicao.remove();
                verifica_table_refeicao_empty(data.total);
                if (data.total == 0){
                    window.location.href = '/';
                }
            }, 2000);

        }
        else{
            alertmsg.classList.add('alert-danger');
            alertmsg.innerHTML = '<strong>Erro</strong> <br> '+data['mensagem'];
            alertmsg.classList.remove('d-none');
            setTimeout(function(){
                alertmsg.classList.remove('alert-danger');
                alertmsg.classList.add('d-none');

            }, 2000);
        }

    }).fail( function(){

    }).always( function(){

    });
}

// Verifica Se tabela refeicao esta vazia
function verifica_table_refeicao_empty(totalreg){
    //divrefatleta = document.getElementById('divrefatleta');
    //divrefatleta.classList.remove('d-none');
    document.getElementById('span-total-ref').innerHTML = totalreg;


    if (totalreg == 0){
        document.getElementById('head-telarefeicao').innerHTML = '<p class="text-danger"><strong>'+
        'Nenhuma Refeição Cadastrada, clique no botão inserir</strong></p>';
    }
    else{
        document.getElementById('head-telarefeicao').innerHTML = '<h5  class=""><strong>Minhas Refeições</strong></h5>';
    }
}

// Botão Menu Dados Atleta
function dadosatleta(){
    //document.getElementById('div-dados-empty').classList.add('d-none');
    document.getElementById('btndadosatleta').classList.add('active');
    divdadosatleta = document.getElementById('div-dados-atleta');
    divdadosatleta.classList.remove('d-none');
    document.getElementById('div-meta-atleta').classList.add('d-none');
    document.getElementById('btnmostrarmeta').classList.remove('active');
    btnvoltarref();
}
//Salva dados atleta
function salvardadosatleta(){

    edtname = document.getElementById('edtnomeatleta');

    edtusername = document.getElementById('edtusernameatleta');
    edtemail = document.getElementById('edtemailatleta');
    dtnasc = document.getElementById('edtdtbirthatleta');
    selectgenero = document.getElementById('selectgeneroatleta');
    edtaltura = document.getElementById('edtalturaatleta');
    edtpeso = document.getElementById('edtpesoatleta');

    document.getElementById('alert-nome-atleta').classList.add('d-none');
    document.getElementById('alert-username-atleta').classList.add('d-none');
    document.getElementById('alert-email-atleta').classList.add('d-none');
    document.getElementById('alert-dtnasc-atleta').classList.add('d-none');
    document.getElementById('alert-genero-atleta').classList.add('d-none');
    document.getElementById('alert-peso-atleta').classList.add('d-none');
    document.getElementById('alert-altura-atleta').classList.add('d-none');

    gravar = true;
    //valida campo nome
    if (edtname.value.length == 0) {
        document.getElementById('alert-nome-atleta').classList.remove('d-none');
    }
    //valida campo UserName
    if (edtusername.value.length == 0) {
        document.getElementById('alert-username-atleta').classList.remove('d-none');
        gravar = false;
    }
    //valida campo email
    if (edtemail.value.length == 0) {
        document.getElementById('alert-email-atleta').classList.remove('d-none');
        gravar = false;
    }

    //valida campo datanascimento
    if (dtnasc.value.length == 0) {
        document.getElementById('alert-dtnasc-atleta').classList.remove('d-none');
        gravar = false;
    }
    //valida campo genero
    if (selectgenero.value.length == 0) {
        document.getElementById('alert-genero-atleta').classList.remove('d-none');
        gravar = false;
    }

    //valida campo peso
    if (edtpeso.value.length == 0){
        document.getElementById('alert-peso-atleta').classList.remove('d-none');
        gravar = false;
    }
    else{
        if(parseFloat(edtpeso.value) <= 0){
            document.getElementById('alert-peso-atleta').classList.remove('d-none');
            gravar = false;
        }
    }
    //valida campo altura
    if (edtaltura.value.length == 0){
        document.getElementById('alert-altura-atleta').classList.remove('d-none');
        gravar = false;
    }
    else{
        if (parseFloat(edtaltura.value) <= 0){
            document.getElementById('alert-altura-atleta').classList.remove('d-none');
            gravar = false;
        }
    }


    if(gravar){
        form = document.getElementById('formdadosatleta');
        formData = new FormData(form);
        updatedadosatleta(formData,this);

    }


}

function updatedadosatleta(formData,btn){
    htmlbtn = btn.innerHTML;
    msgdadosatleta = document.getElementById('msg-dados-atleta');
    $.ajax({
        url: '/sisnutri/update/atleta',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        beforesend: function(e){
            e.preventDefault();
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Atualizando...';

        }
    }).done( function(data){
        if(data.result == true){
            divdadosempty = document.getElementById('div-dados-empty');
            if (divdadosempty != null){
                if (!divdadosempty.classList.contains('d-none')){
                    divdadosempty.classList.add('d-none');
                }
            }
            msgdadosatleta.classList.add("alert-primary");
            msgdadosatleta.innerHTML = '<strong>Sucesso</strong> <br> '+data.mensagem;
            msgdadosatleta.classList.remove('d-none');

            setTimeout(function(){
                msgdadosatleta.classList.remove('alert-primary');
                msgdadosatleta.classList.add('d-none');
                btn.innerHTML = htmlbtn;
                dadoscompletoatleta = true;
                window.location.href = '/';
            }, 2000);

        }
        else{
            msgdadosatleta.classList.add("alert-danger");
            msgdadosatleta.innerHTML = '<strong>Erro</strong> <br> '+data.mensagem;
            msgdadosatleta.classList.remove('d-none');

            setTimeout(function(){
                msgdadosatleta.classList.remove('alert-primary');
                msgdadosatleta.classList.add('d-none');
                btn.innerHTML = htmlbtn;
            }, 2000);
        }
    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });
}

function avancarmain(){
    alertmetaatleta = document.getElementById('alertmetaatleta');
    pesoinicial = document.getElementById('edtpesoinicialmetaatleta');
    pesofinal = document.getElementById('edtpesofinalmetaatleta');

    msgtemp = 'Forneça os seguinte campos: ';
    passar = false;

    if (pesoinicial.value != '' && pesoinicial.value !='0'){
        passar = true;
    }else{
        msgtemp = msgtemp + ' <strong>"Peso Inicial"</strong>';

    }
    if (pesofinal.value != '' && pesofinal.value !='0'){
        passar = true;

    }else{
        passar = false;
        msgtemp = msgtemp + ' <strong>"Meta de Peso"</strong>';
    }

    if (passar){
        $('#collapseOne').collapse('show');

    }
    else{
        alertmetaatleta.innerHTML = msgtemp;
    }

}

function exitpesofinalmetaatleta(input){
    edtpesoinicial = document.getElementById('edtpesoinicialmetaatleta');

    if(input.value < edtpesoinicial.value){
        document.getElementById('radiometalessatleta').checked = true;
    }
    else{
        document.getElementById('radiometamoreatleta').checked = true;
    }
    checkmeta_atleta();
}

function validacamposmetaatleta(){
    vlalvo = 0;
    edtcaloriasexercises = document.getElementById('edtkcalexercatleta');
    edtcaloriasmeta = document.getElementById('edtkcalmetaatleta');

    edtmediatdee = document.getElementById('edtmediatdee-meta');
    edtmediabmr = document.getElementById('edtmediabmr-meta');

    vlcalmoreless = (edtcaloriasmeta.value=='') ? 0 : parseFloat(edtcaloriasmeta.value);
    vlcalexerc = (edtcaloriasexercises.value=='') ? 0 : parseFloat(edtcaloriasexercises.value);

    curRadio = document.querySelector('input[name="radiometaatleta"]:checked').value;
    if (curRadio == 'ganho'){
        document.getElementById('lbl-tipometa-atleta').innerHTML = '<strong>Ganho</strong>';
        document.getElementById('lbl-desctipometaatleta').innerHTML = '<strong>Excedente Calórico</strong>';
        vlalvo = parseFloat(edtmediatdee.innerHTML) + vlcalmoreless + vlcalexerc;
    }
    else{
        document.getElementById('lbl-tipometa-atleta').innerHTML = '<strong>Perda</strong>';
        document.getElementById('lbl-desctipometaatleta').innerHTML = '<strong>Defícit Calórico</strong>';
        vlalvo = parseFloat(edtmediatdee.innerHTML) + vlcalexerc;
        vlalvo = vlalvo - vlcalmoreless;
    }
}
function calcularesultfinal_metaatleta(){
    validacamposmetaatleta();
    // TMB
    document.getElementById('edtbmrdiametaatleta').value = edtmediabmr.innerHTML;
    document.getElementById('edttmb').value = document.getElementById('edtbmrdiametaatleta').value;

    // GCD
    document.getElementById('edtgcddiametaatleta').value = edtmediatdee.innerHTML;
    document.getElementById('edtgcd').value = document.getElementById('edtgcddiametaatleta').value;

    // total kcal excedentes ou deficit
    document.getElementById('edtmetakaldiametaatleta').value  = vlcalmoreless;
    // kcal gastas em exercicios
    document.getElementById('edtKcalExecdiametaatleta').value = vlcalexerc;
    // KCAL ALVO
    document.getElementById('edtalvokcaldiametaatleta').value = vlalvo;
    document.getElementById('edtkcalalvo').value = vlalvo;
    vlkcalkgfat = verifycampokgfatempty_metaatleta();


    calcmetaatleta_kg(vlcalmoreless,vlkcalkgfat);
    preenchedadadoskcalalvo_metaatleta(vlalvo);
    preenchedadadoskcalbmr_metaatleta();
    preenchedadadoskcalgcd_metaatleta();
    preechemetakcal_metaatleta();
    preenchedadoskcalexec_metaatleta();

}

//  calcula e preenche os campos referente a quantidade de kilograma que ira ganhar ou perder de acordo com dia, semana, mes, ano
function calcmetaatleta_kg(vlmetakaldia,vlkcalkgfat){

    vlmetakgdia = (vlmetakaldia/vlkcalkgfat);
    vlmetakgdia = vlmetakgdia * 0.4536;

    // KG por dia
    if (vlmetakgdia < 1){
        document.getElementById('lblpesodiametaatleta').innerHTML = ' gr';
        vlmetakgdia_tp = vlmetakgdia*1000;
        document.getElementById('edtpesodiametaatleta').value = (vlmetakgdia_tp).toFixed(0);
    }
    else{
        document.getElementById('lblpesodiametaatleta').innerHTML = ' kg';
        document.getElementById('edtpesodiametaatleta').value = (vlmetakgdia_tp).toFixed(3);
    }


    //KG por semana
    vlmetakgsemana = vlmetakgdia * 7;
    if (vlmetakgsemana < 1){
        document.getElementById('lblpesosemanalmetaatleta').innerHTML = ' gr';
        vlmetakgsemana = vlmetakgsemana * 1000;
        document.getElementById('edtpesosemanalmetaatleta').value = vlmetakgsemana.toFixed(0);
    }
    else{
        document.getElementById('lblpesosemanalmetaatleta').innerHTML = ' kg';
        document.getElementById('edtpesosemanalmetaatleta').value = vlmetakgsemana.toFixed(3);
    }



    //KG por mes
    vlmetakgmensal = vlmetakgdia * 30.5;
    if (vlmetakgmensal < 1){
        document.getElementById('lblpesomensalmetaatleta').innerHTML = ' gr';
        vlmetakgmensal = vlmetakgmensal * 1000;
        document.getElementById('edtpesomensalmetaatleta').value = vlmetakgmensal.toFixed(0);
    }
    else{
        document.getElementById('lblpesomensalmetaatleta').innerHTML = ' kg';
        document.getElementById('edtpesomensalmetaatleta').value = vlmetakgmensal.toFixed(3);
    }
    //KG por ano
    vlmetakganual = vlmetakgdia * 365;

    if(vlmetakganual < 1){
        document.getElementById('lblpesoanualmetaatleta').innerHTML = ' gr';
        vlmetakganual = vlmetakganual * 1000;
        document.getElementById('edtpesoanualmetaatleta').value = vlmetakganual.toFixed(0);
    }
    else{
        document.getElementById('lblpesoanualmetaatleta').innerHTML = ' kg';
        document.getElementById('edtpesoanualmetaatleta').value = vlmetakganual.toFixed(3);
    }

}


// verifica se campo calorias gordura por kilo se esta vazio ou não
function verifycampokgfatempty_metaatleta(){
    kcalkgfat = document.getElementById('edtkcalkgfatmetaatleta').value;
    if (kcalkgfat == '' | kcalkgfat == '0'){
        kcalkgfat = 3500;
        document.getElementById('edt-kcalkgfat').value = 3500;
    }
    return kcalkgfat;
}

function calccalporkg_metaatleta(valorkgdia){
    result1 = (valorkgdia / 0.453592);
    console.log('Res1:'+result1);
    result2 = verifycampokgfatempty_metaatleta();
    console.log('Res2:'+result2);

    return  (result1 * result2);
}

// preeche campos input alvos meta atleta
function preenchedadadoskcalalvo_metaatleta(vlkcalalvodia){
    document.getElementById('edtalvokcalsemanalmetaatleta').value = (vlkcalalvodia * 7).toFixed(0);
    document.getElementById('edtalvokcalmensalmetaatleta').value = (vlkcalalvodia * 30.5).toFixed(0);
    document.getElementById('edtalvokcalanualmetaatleta').value = (vlkcalalvodia * 365).toFixed(0);

    document.getElementById('lbl-resultadofinal').innerHTML = 'Sua meta de gasto calórico diário é: <strong>'+vlkcalalvodia+'</strong>';

    pesoinicialmeta = document.getElementById('edtpesoinicialmetaatleta').value;
    pesometa = document.getElementById('edtpesofinalmetaatleta').value;
    tipometa = document.getElementById('edtobjetivometa').value;
    tipometadesc = ((tipometa=='G')?'Ganho':'Perda');
    tipokcalmeta = ((tipometa=='G')?'Excedente':'Defícit');
    na = document.getElementById('edtnameta').value;

    pesoganharperderdia = document.getElementById('edtpesodiametaatleta').value;



    pesoinicialmeta = parseFloat(pesoinicialmeta);
    pesometa = parseFloat(pesometa);

    diferencapeso = pesoinicialmeta - pesometa;
    console.log('Diferença de peso:'+diferencapeso);
    if (diferencapeso < 0){
        diferencapeso = diferencapeso * -1;
    }

    pesoganharperderdia = pesoganharperderdia / 1000;
    resultdias = diferencapeso / pesoganharperderdia;

    msgfinal  = '<p class="text-warning text-center">';
    msgfinal += 'Com base no seu peso inicial: <strong>'+pesoinicialmeta+'</strong> e sua Meta de Peso: <strong>'+pesometa;
    msgfinal +='</strong> e de acordo com o objetivo escolhido: <strong>"'+tipometadesc+' Peso"</strong>';
    msgfinal +=', o nível de atividade: <strong>"'+ na +'"</strong>, o <strong>'+tipokcalmeta+'</strong> calórico de: <strong>"';
    msgfinal +=vlcalmoreless+'"</strong> e o total de calorias gasta aproximadamente no exercício de: <strong>"'+vlcalexerc+'"</strong>, ';
    msgfinal +=' e com a(s) fórmula(s) escolhida(s). Seu Gasto Calorico Diário é de: <strong>"'+vlalvo+'"</strong></small>';
    msgfinal +='</p><p class="text-warning text-center">Total de dias aproximadamente para atingir a Meta de Peso é: <strong>'+Math.round(resultdias)+'</strong></p>';
    document.getElementById('modal-body-confirmameta').innerHTML = msgfinal;

    document.getElementById('edtdiasprevisto').value = Math.round(resultdias);
}
//  calcula e preenche os campos referente a quantidade de kcal que ira ganhar ou perder de acordo com dia, semana, mes, ano
function preechemetakcal_metaatleta(){
    vlmetakaldia = document.getElementById('edtmetakaldiametaatleta').value;
    document.getElementById('edtmetakalsemanalmetaatleta').value = (vlmetakaldia * 7).toFixed(0) ;
    document.getElementById('edtmetakalmensalmetaatleta').value =  (vlmetakaldia * 30.5).toFixed(0);
    document.getElementById('edtmetakalanualmetaatleta').value = (vlmetakaldia * 365).toFixed(0);
}
//preeche campos da linha calorias dos exercicios: dia, semana, mes e ano
function preenchedadoskcalexec_metaatleta(){
    vlkcalexecdia = document.getElementById('edtKcalExecdiametaatleta').value;
    document.getElementById('edtKcalExecsemanalmetaatleta').value = (vlkcalexecdia * 7).toFixed(0);
    document.getElementById('edtKcalExecmensalmetaatleta').value = (vlkcalexecdia * 30.5).toFixed(0);
    document.getElementById('edtKcalExecanualmetaatleta').value = (vlkcalexecdia * 365).toFixed(0);

}
//preeche campos da linha calorias TMB: dia, semana, mes e ano
function preenchedadadoskcalgcd_metaatleta(){
    vlkcalgcddia = document.getElementById('edtgcddiametaatleta').value;
    document.getElementById('edtgcdsemanalmetaatleta').value = (vlkcalgcddia * 7).toFixed(0);
    document.getElementById('edtgcdmensalmetaatleta').value = (vlkcalgcddia * 30.5).toFixed(0);
    document.getElementById('edtgcdanualmetaatleta').value = (vlkcalgcddia * 365).toFixed(0);
}
//preeche campos da linha calorias TMB: dia, semana, mes e ano
function preenchedadadoskcalbmr_metaatleta(){
    vlkcalbmr = document.getElementById('edtbmrdiametaatleta').value;
    document.getElementById('edtbmrsemanalmetaatleta').value = (vlkcalbmr * 7).toFixed(0);
    document.getElementById('edtbmrmensalmetaatleta').value = (vlkcalbmr * 30.5).toFixed(0);
    document.getElementById('edtbmranualmetaatleta').value = (vlkcalbmr * 365).toFixed(0);
}


function calckcalmetaatleta(input){
    edtcaloriasmeta.value = input.value;
    if (edtcaloriasmeta.value == ''){
        edtcaloriasmeta.value = '0';
        this.value = '0';
    }
    calcularesultfinal_metaatleta();
}
// onchange campo calorias gastas no exercicios
function calckcalexercmetaatleta(input){
    edtcaloriasexercises.value = input.value;
    if (edtcaloriasexercises.value == ''){
        edtcaloriasexercises.value = '0';
        this.value = '0';
    }
    calcularesultfinal_metaatleta();
}

// onchange campo resultado final em kgs por dia KG/GR
function calcpesodia_metaatleta(input) {
    if (input.value < -1) {
        input.value = 0;
    }
    console.log(input.value);
    result = calccalporkg_metaatleta(input.value/1000).toFixed(0);
    console.log(result);
    document.getElementById('edtmetakaldiametaatleta').value = result;
    edtcaloriasmeta.value = result;
    calckcalmetaatleta(edtcaloriasmeta);
    calcularesultfinal_metaatleta();

}

function avancarformula(){
    validacamposmetaatleta();
    calcularesultfinal_metaatleta();
}
// Mostrar Meta Ativa
function mostrarmeta(btn){
    if (dadoscompletoatleta){
        btn.classList.add('active');
        console.log('Meta ativa:'+ metaativa);
        document.getElementById('msg-meta-atleta').classList.add('d-none');
        document.getElementById('div-meta-atleta').classList.remove('d-none');
        if (metaativa == 'N'){
            document.getElementById('formmetaatleta').classList.remove('d-none');
            document.getElementById('div-meta-atleta-ativa').classList.add('d-none');
        }
        else{
            document.getElementById('formmetaatleta').classList.add('d-none');
            document.getElementById('div-meta-atleta-ativa').classList.remove('d-none');
            geragraficomacronutriente();
        }

        document.getElementById('divrefatleta').classList.add('d-none');
        document.getElementById('div-dados-atleta').classList.add('d-none');
    }else{
        dadosatleta();
    }


}
function geragraficomacronutriente(){
    console.log(data_meta);
    google.charts.load('current', {'packages':['corechart']}).then( function(){

        var data = google.visualization.arrayToDataTable([
        ['Task', 'Hours per Day'],
        ['Protéinas: '+data_meta.valgramasproteina+'gr', data_meta.valkcalproteina],
        ['Carboidratos: '+data_meta.valgramascarbo+'gr', data_meta.valkcalcarb],
        ['Gorduras: '+data_meta.valgramasgordura+'gr', data_meta.valkcalfat]]);

        var options = {//'title':'Informação Nutricional - Total Calorias:',
                       'backgroundColor': 'transparent',
                       'legend':{'position':'rigth'},
                       'chartArea':{'left':0, 'right':10,'top':30,'width':'100%','height':'80%'},
                       'is3D':true,
                       'left': 0,
                       'width':350,
                       'height':200,
                       //'pieHole': 0.4,
                       };
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    });

}
// clica botão avançar tela de resultado para a tela de contagem de macromutrientes
function avancarresultado(){
    vlpercproteina = document.getElementById('edtpercproteina');
    vlgramasproteina = document.getElementById('edtgramasproteina');
    vlkcalproteina = document.getElementById('edtkcalproteina');
    vlgrporkgproteina = document.getElementById('edtgrporkgproteina');

    vlperccarbo = document.getElementById('edtperccarbo');
    vlgramascarbo = document.getElementById('edtgramascarbo');
    vlkcalcarbo = document.getElementById('edtkcalcarbo');
    vlgrporkgcarbo = document.getElementById('edtgrporkgcarbo');


    vlpercgordura = document.getElementById('edtpercgordura');
    vlgramasgordura = document.getElementById('edtgramasgordura');
    vlkcalgordura = document.getElementById('edtkcalgordura');
    vlgrporkggordura = document.getElementById('edtgrporkggordura');

    pesoinicialmetaatleta = parseFloat(document.getElementById('edtpesoinicialmetaatleta').value);

    // calcula kcal macros
    calcpercproteina(vlpercproteina);
    calckcalproteina(vlkcalproteina);
    calcgramasproteina(vlgramasproteina);

    calcperccarbo(vlperccarbo);
    calckcalcarbo(vlkcalcarbo);
    calcgramascarbo(vlgramascarbo);


    calcvaluesgordura();
    document.getElementById('div-titulo-macronutriente').innerHTML = '<strong>Gasto Calórico Diário: '+vlalvo+'</strong>';
}
function calcvaluesgordura(){
    if (vlkcalproteina.value > 0 && vlkcalcarbo.value > 0){
        valorkcal = vlalvo - ( parseFloat(vlkcalproteina.value) + parseFloat(vlkcalcarbo.value));
        vlkcalgordura.value = valorkcal;

        vlgramasgordura.value = (vlkcalgordura.value / 9).toFixed(0);
        percfat = ((vlkcalgordura.value * 100) / vlalvo).toFixed(0);
        vlpercgordura.value = percfat;
        vlgrporkggordura.value = (vlgramasgordura.value / pesoinicialmetaatleta).toFixed(2);
    }
    calctotalmacronutrient();

}
function calctotalmacronutrient(){
    totperc = parseFloat(vlpercproteina.value) + parseFloat(vlperccarbo.value) + parseFloat(vlpercgordura.value);
    totkcal = parseFloat(vlkcalproteina.value) + parseFloat(vlkcalcarbo.value) + parseFloat(vlkcalgordura.value);
    totgrama= parseFloat(vlgramasproteina.value) + parseFloat(vlgramascarbo.value) + parseFloat(vlkcalgordura.value);
    console.log('Percentual:'+ totperc);
    document.getElementById('lbl-total-perc').innerHTML = '<strong>'+totperc+' %</strong>';
    document.getElementById('lbl-total-calorias').innerHTML = '<strong>'+totkcal+' kcal</strong>';
    document.getElementById('lbl-total-gramas').innerHTML = '<strong>'+totgrama+' gr</strong>';

}

function calcgrporkgproteina(input){
    if (input.value > 0){
        vlkcalproteina.value = (pesoinicialmetaatleta * parseFloat(input.value)*4);

    }
    calckcalproteina(vlkcalproteina);
    calcvaluesgordura();

}

// calcula total calorias de Proteina de acordo com total de calorias alvo
function calckcalproteina(input){
    if (input.value > 0){
        vlpercproteina.value = ((input.value * 100) / vlalvo).toFixed(0);
        vlgramasproteina.value = (input.value / 4).toFixed(0);
        vlgrporkgproteina.value = (vlgramasproteina.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}
// calcula Percentual de Proteina de acordo com total de calorias alvo
function calcpercproteina(input){
    if (input.value > 0){
        vlkcalproteina.value = (vlalvo * (input.value/100)).toFixed(0);
        vlgramasproteina.value = (vlkcalproteina.value / 4).toFixed(0);
        vlgrporkgproteina.value = (vlgramasproteina.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}
// calcula total gramas de Proteinas de acordo com total de calorias alvo
function calcgramasproteina(input){
    if (input.value > 0){
        vlkcalproteina.value = (input.value * 4).toFixed(0);
        vlpercproteina.value = ((vlkcalproteina.value * 100) / vlalvo).toFixed(0);
        vlgrporkgproteina.value = (input.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}

function calcgrkgporcarbo(input){

    if (input.value > 0){
        vlkcalcarbo.value = (pesoinicialmetaatleta * parseFloat(input.value)*4);
    }
    calckcalcarbo(vlkcalcarbo);
    calcvaluesgordura();

}

// calcula total caloria de carboidratos de acordo com total de calorias alvo
function calckcalcarbo(input){
    if (input.value > 0){
        vlperccarbo.value = ((input.value * 100) / vlalvo).toFixed(0);
        vlgramascarbo.value = (input.value / 4).toFixed(0);
        vlgrporkgcarbo.value = (vlgramascarbo.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}
// calcula percentual de carboidratos de acordo com total de calorias alvo
function calcperccarbo(input){
    if (input.value > 0){
        vlkcalcarbo.value = (vlalvo * (input.value/100)).toFixed(0);
        vlgramascarbo.value = (vlkcalcarbo.value / 4).toFixed(0);
        vlgrporkgcarbo.value = (vlgramascarbo.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}
// calcula total gramas de carboidratos de acordo com total de calorias alvo
function calcgramascarbo(input){
    if (input.value > 0){
        vlkcalcarbo.value = (input.value * 4).toFixed(0);
        vlperccarbo.value = ((vlkcalcarbo.value * 100) / vlalvo).toFixed(0);
        vlgrporkgcarbo.value = (input.value / pesoinicialmetaatleta).toFixed(2);
        calcvaluesgordura();
    }
}

function salvarmeta(){
    document.getElementById('modal-body-confirmameta').innerHTML = msgfinal;
}
function confirmameta(){

form = document.getElementById('formmetaatleta');
    formData = new FormData(form);
    $.ajax({
        url: '/post/metaatleta',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        alert_confirmameta = document.getElementById('alert-confirmameta');

        if (data.result == true) {
            alert_confirmameta.classList.add('alert-primary');
            alert_confirmameta.classList.remove('d-none');
            alert_confirmameta.innerHTML = data.mensagem;
            setTimeout(function(){

                alert_confirmameta.classList.add('d-none');
                window.location.href = '/';


            }, 2000);

        }
        else{
            alert_confirmameta.classList.add('alert-danger');
            alert_confirmameta.classList.remove('d-none');
            alert_confirmameta.innerHTML = data.mensagem;
            setTimeout(function(){
                alert_confirmameta.add('d-none');
                window.location.href = '/';
            }, 2000);
        }

    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });

}

function finalizameta(id, descricao){
    document.getElementById('edtidmetaatleta').value=id;

}

async function confirmafinalizacaometa(){
    gravar = false;
    console.log('Id:'+document.getElementById('edtpesofinal').value);
    if (document.getElementById('edtpesofinal').value == ''){
        document.getElementById('edtpesofinal').value = '0';
    }
    if (parseFloat(document.getElementById('edtpesofinal').value)<=0){
        document.getElementById('small-pesofinal').classList.remove('d-none');
    }
    else{
        gravar = true;
    }

    if(gravar){

        form = document.getElementById('form-finalizameta');
        let formData = new FormData(form);
        url = '/sisnutri/finaliza/meta/atleta';
        var mybody = {method:'POST', body:formData };

        let response = await fetch(url,mybody);
        if (response.ok) {
            alertmsgfinalizameta = document.getElementById('alert-msgfinalizameta');
            alertmsgfinalizameta.classList.remove('d-none');
            alertmsgfinalizameta.innerHTML = 'Aguarde...';
            let json = await response.json();
            if (json.result){
                alertmsgfinalizameta.classList.add('alert-primary');
            }
            else{
                alertmsgfinalizameta.classList.add('alert-danger');
            }
            alertmsgfinalizameta.innerHTML = json.mensagem+'<br> Aguarde, Atualizando informações!';

            setTimeout(function(){
                window.location.reload(true);
            },2000)
        }
        else{
            alert(response.status);
        }
    }

}

function btn_click_forgoutitpwd(email){
    window.location.href = '/sisnutri/forgoutit/pwd?email='+email;

}

// CAPTURA DADOS DO CLIMA de acordo com a função geolocaltion_clima, abaixo()
async function dados_clima(position){
    div_clima = document.querySelector('#div-clima');
    div_clima.classList.remove('d-none');
    div_clima.innerHTML = str_div_loading+" Aguarde, buscando informações...<br>";
    lat = position.coords.latitude.toString().substring(0, 8);
    lon = position.coords.longitude.toString().substring(0, 8);

    response = await fetch('/get/clima/latlon/'+lat+'/'+lon);

    result_json = await response.json();

    // função transale_text : static/js/funcoes/js
    strtempnow = await translate_text(result_json["weather"][0]["description"]);

    temp_now = result_json["main"]["temp"].toString().substring(0,2)+' ºC';;
    temp_max = result_json["main"]["temp_max"].toString().substring(0,2)+' ºC';
    temp_min = result_json["main"]["temp_min"].toString().substring(0,2)+' ºC';

    // valor pressão atmosfetica em paschol e polegas por mercurio
    vl_pressure_hPa = result_json['main']["pressure"];
    vl_pressure_polHg = ((vl_pressure_hPa * 29.92126)/1013.25).toFixed(2);

    sessionstemper ='<div class="text-white text-center"><h5 class="text-warning">Informações Climáticas</h5></div>'+
    '<div class="d-flex justify-content-center  my-1">'+
        '<div class="div-info-clima p-3">'+
            '<p class="text-white"><strong>Tempo Agora: </strong>'+strtempnow+'</p>'+
            '<p><strong> Temperatura </strong></p>'+
            '<p>Atual: '+temp_now+'</p>'+
            '<p>Máxima: '+temp_max+
            ', mínima: '+temp_min+'</p></small>'+
        '</div>'+
    '</div>'+
    '<div class="d-flex justify-content-center my-1">'+
        '<div class="div-info-clima p-3"><small>'+
            '<p>Latitude: '+lat+
            ', longitude: '+lon+'</p>'+
            '<p>Atm hPa: '+vl_pressure_hPa+
            ', Atm polHg: '+vl_pressure_polHg+'</p>'+
            '</small>'+
        '</div>'+
    '</div>';
    //'</div>';

    div_clima.innerHTML = sessionstemper;
}

// BUSCA DADOS CLIMATICOS, DE ACORDO COM A LOCALIZAÇÃO DO DISPOSITIVO, QUE RETORNA LATITUDE E LONGITUDE
// E BUSCA OS VALORES. REFERENTE A FUNÇÃO ACIMA: dados_clina
function geolocation_clima(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(dados_clima);
    } else {
        console.loh( "Geolocation is not supported by this browser.");
    }
}

// CAPTURA COTAÇÃO
async function dados_moeda_BR(){
    div_moedaBR = document.querySelector('#div-moedaBR');
    div_moedaBR.classList.remove('d-none');
    div_moedaBR.innerHTML = str_div_loading+" Aguarde, buscando informações...<br>";
    result_json = await search_moeda_conversion_BRL();

    USDBRL_json = await result_json["USDBRL"]; // DOLAR->REAL
    EURBRL_json = await result_json["EURBRL"]; //EURO->REAL
    BTCBRL_json = await result_json["BTCBRL"]; //BITCOION->REAL


    dataUSD = retornadataBR(new Date(USDBRL_json["create_date"]));
    horaUSD = retornahoraBR(new Date(USDBRL_json["create_date"]));
    dataEUR = retornadataBR(new Date(EURBRL_json["create_date"]));
    horaEUR = retornahoraBR(new Date(EURBRL_json["create_date"]));
    dataBTC = retornadataBR(new Date(BTCBRL_json["create_date"]));
    horaBTC = retornahoraBR(new Date(BTCBRL_json["create_date"]));
    div_moedaBR.innerHTML ='<div class="text-warning text-center"><h5>Cotação Moeda</h5></div>';
    div_moedaBR.innerHTML +='<div id="demo" class="carousel slide" data-ride="carousel">'+
    '<div class="carousel-inner">'+
    // DOLAR > BRL
    ' <div class="carousel-item active">'+
    '<div class="row text-white d-flex justify-content-center">'+
    '<div class="div-info-cotacoes p-4">'+
    '<div class="row text-warning d-flex mx-2 justify-content-center"><label>Cotação Dólar para Real </label></div> '+
    '<small><table class="table  text-white  table-sm">'+
    '<thead><tr><th>Compra</th><td>'+parseFloat(USDBRL_json["bid"]).toFixed(2)+' R$</td></tr></thead>'+
    '<thead><tr><th>Venda</th><th>'+parseFloat(USDBRL_json["ask"]).toFixed(2)+' R$</th></tr></thead>'+
    '</table>'+
    '<p> Variação: '+parseFloat(USDBRL_json["varBid"]).toFixed(2)+'</p>'+
    '<p> Maior: '+parseFloat(USDBRL_json["high"]).toFixed(2)+
    ', Menor:'+parseFloat(USDBRL_json["low"]).toFixed(2)+'</p>'+
    '<p> Data: '+dataUSD+', '+horaUSD+' </p></small></div>'+

    '</div></div>'+
  // EURO > BRL
  '<div class="carousel-item">'+
    '<div class="row text-white d-flex justify-content-center">'+
    '<div class="div-info-cotacoes p-4">'+
    '<div class="row text-warning d-flex mx-2 justify-content-center"><label>Cotação Euro para Real </label></div> '+
    '<small><table class="table  text-white  table-sm">'+
    '<thead><tr><th>Compra</th><td>'+parseFloat(EURBRL_json["bid"]).toFixed(2)+' R$</td></tr></thead>'+
    '<thead><tr><th>Venda</th><th>'+parseFloat(EURBRL_json["ask"]).toFixed(2)+' R$</th></tr></thead>'+
    '</table>'+
    '<p> Variação: '+parseFloat(EURBRL_json["varBid"]).toFixed(2)+'</p>'+
    '<p> Maior: '+parseFloat(EURBRL_json["high"]).toFixed(2)+
    ', Menor:'+parseFloat(EURBRL_json["low"]).toFixed(2)+'</p>'+
    '<p> Data: '+dataEUR+', '+horaEUR+' </p></small></div></div></div>'+
  // BITCOIN > BRL
  '<div class="carousel-item">'+
    '<div class="row text-white d-flex justify-content-center">'+
    '<div class="div-info-cotacoes p-4">'+
    '<div class="row text-warning d-flex mx-2 justify-content-center"><label> Bitcoin para Real </label></div> '+
    '<small><table class="table text-white  table-sm">'+
    '<thead><tr><th>Compra</th><td>'+parseFloat(BTCBRL_json["bid"]).toFixed(2)+' R$</td></tr></thead>'+
    '<thead><tr><th>Venda</th><th>'+parseFloat(BTCBRL_json["ask"]).toFixed(2)+' R$</th></tr></thead>'+
    '</table>'+
    '<p> Variação: '+parseFloat(BTCBRL_json["varBid"]).toFixed(2)+'</p>'+
    '<p> Maior: '+parseFloat(BTCBRL_json["high"]).toFixed(2)+
    ', Menor:'+parseFloat(BTCBRL_json["low"]).toFixed(2)+'</p>'+
    '<p> Data: '+dataBTC+', '+horaBTC+' </p></small></div></div></div>'+
  '</div>'+
  '<a class="carousel-control-prev" href="#demo" data-slide="prev">'+
  '  <span class="carousel-control-prev-icon"></span>'+
  '</a>'+
  '<a class="carousel-control-next" href="#demo" data-slide="next">'+
  '  <span class="carousel-control-next-icon"></span></a></div>';
}

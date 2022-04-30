var div_ft_especificar = document.getElementById('div-filtros-especificar');
var div_ft_prontos = document.getElementById('div-filtros-prontos');
var div_sexo_idade = document.getElementById('div-sexo-idade');
var select_ft = document.getElementById('select-filtro');
var select_hospital = document.getElementById('select-hospital');
var brownser_exames = document.getElementById('brownser-exames');
var edtidexame = document.getElementById('edtidexame');
var brownser_analitos = document.getElementById('brownser-analitos');
var edtidanalito = document.getElementById('edtidanalito');

function select_filtro_change(val){
    divs_filtro = document.querySelectorAll('.div-filtros');
    divs_filtro.forEach((divft,index) => {
        divft.classList.add('d-none');
    });

    switch (parseInt(val)){
        case 0:
            div_sexo_idade.classList.remove('d-none');
            break;
        case 1:
            div_ft_prontos.classList.remove('d-none');
            break;
        case 2:
            div_ft_especificar.classList.remove('d-none');
            break;
    }

}

function select_op_idade_change(val){
    document.getElementById('div-idade-one').classList.remove('d-none');
    document.getElementById('div-idade-two').classList.add('d-none');

    if (parseInt(val) == 5){
        document.getElementById('div-idade-one').classList.add('d-none');
        document.getElementById('div-idade-two').classList.remove('d-none');
    }

}

async function filtrar_pacientes(){
    sel_filtro = document.getElementById('select-filtro').value;
    sel_hospital = document.getElementById('select-hospital').value;
    sel_op_resultado = document.getElementById('select-operador-resultado').value;
    input_resultado = document.getElementById('input-valresultado').value;
    sel_op_idade = document.getElementById('select-operador-idade').value;
    input_idade = document.getElementById('input-idade').value;
    sel_sexo = document.getElementById('select-sexo').value;
    let url =  '';
    let idade_de = null;
    let idade_ate = null;
    if (parseInt(sel_op_idade) == 5){
        idade_de = document.getElementById('input-idade-de').value;
        idade_ate = document.getElementById('input-idade-ate').value;
    }

    // VERIFICA SEXO INFORMADO
    sexo = '';
    console.log('Sexo:'+sel_sexo);
    switch (parseInt(sel_sexo)){
        case 1:
            sexo = 'M'
            break;
        case 2:
            sexo = 'F'
            break;
        case 3:
            sexo = 'W'
            break;
    }
    switch (parseInt(sel_filtro)){
        case 0:
            console.log('Entrei Aqui: '+ sexo + ' - '+ sel_op_idade + ' - '+input_idade);
            url = '/sishealth/get/pacientes/main?page=1&per_page=20&sexo='+sexo+'&tpoperadoridade='+sel_op_idade+'&idade='+input_idade+
            '&idadede='+idade_de+'&idadeate='+idade_ate;
            window.location.href = url ;
            break;
        case 1:
            url = '/sishealth/get/pacientes/main?page=1&per_page=20&tpfiltro=1,sexo='+sexo+'&tpoperadoridade='+sel_op_idade+'&idade='+input_idade;
            window.location.href(url);
            break;
    }

}


async function search_hospitais(idhospital=''){
    let small_hosp = document.getElementById('small-hospital');
    small_hosp.innerHTML = 'Aguarde busca dados'+str_div_loading;
    small_hosp.classList.remove('d-none');
    url = '/get/covid/hospitais/json';
    let response = await fetch(url);
    if(response.status == 200){
        await response.json().then(data => {
            data_hospitais = data.data;
        });
    }
    else{
        data_hospitais = [];
    }

    const option = document.createElement('option');
    option.setAttribute('value','0');
    option.textContent = 'Todos';
    select_hospital.appendChild(option);
    if (idhospital.length == 0){
        option.setAttribute('selected',true);
    }
    data_hospitais.map(hospital =>{
        const option = document.createElement('option');
        option.setAttribute('value',hospital.id);
        if (idhospital != ''){
            if (idhospital == hospital.id){
                option.setAttribute('selected',true);
            }
        }
        console.log(hospital);
        console.log(hospital.name);
        option.textContent = hospital.name;
        select_hospital.appendChild(option);
    });
    small_hosp.classList.add('d-none');
}

function click_btn_filtro(){
    search_hospitais();
    search_exames();
}

// FUNCAO BUSCA TODOS EXAMES BANCO DE DADOS
async function search_exames(idexames=''){
    let small_exames = document.getElementById('small-exames');
    small_exames.innerHTML = 'Aguarde busca exames...'+str_div_loading;
    small_exames.classList.remove('d-none');

    url = '/get/covid/exames/json';
    let response = await fetch(url);
    let data_exames = [];
    if(response.status == 200){
        await response.json().then(data => {
            data_exames = data.data;
        });
    }
    data_exames.map(exame =>{
        const option = document.createElement('option');
        option.setAttribute('value',exame.descricao);
        option.setAttribute('data-value',exame.id);
        brownser_exames.appendChild(option);
    });
    small_exames.classList.add('d-none');
}
// CHANGE INPUT EXAME, PARA DETECTAR O ID
function btn_brownser_exame_change(value){
    option_selector = document.querySelector('#brownser-exames > option[value="'+value+'"]');
    edtidexame.value = '0';
    if (option_selector){
        edtidexame.value = option_selector.getAttribute('data-value');
    }


}
function btn_brownser_exame_blur(){
    search_analitos('',edtidexame.value);
}
// FUNCAO BUSCA TODOS ANALITOS BANCO DE DADOS
async function search_analitos(idanalito='',idexame=''){
    let small_analitos = document.getElementById('small-analitos');
    small_analitos.innerHTML = 'Aguarde busca analitos...'+str_div_loading;
    small_analitos.classList.remove('d-none');

    url = '/get/covid/analitos/json?idexame='+idexame;
    let response = await fetch(url);
    let data_analitos = [];
    if(response.status == 200){
        await response.json().then(data => {
            data_analitos = data.data;
        });
    }
    data_analitos.map(analito =>{
        const option = document.createElement('option');
        option.setAttribute('value',analito.descricao);
        option.setAttribute('data-value',analito.id);
        if (idanalito == analito.id){
            option.setAttribute('selected',true);
        }
        brownser_analitos.appendChild(option);
    });
    small_analitos.classList.add('d-none');
}
// CHANGE INPUT Analito, PARA DETECTAR O ID
function btn_brownser_analito_change(value){
    option_selector = document.querySelector('#brownser-analitos > option[value="'+value+'"]');
    edtidanalito.value = '0';
    if (option_selector){
        edtidanalito.value = option_selector.getAttribute('data-value');
    }
}

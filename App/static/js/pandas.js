var ckb_datanascimento = document.getElementById('ckb-datanascimento');
var ckb_phone = document.getElementById('ckb-phone');
var ckb_nome = document.getElementById('ckb-nome');
var edtnome = document.getElementById('edtnome');
var vper_page = document.getElementById('per_page');
var ckb_localidade = document.getElementById('ckb-localidade');
var ckb_nolocalidade = document.getElementById('ckb-nolocalidade');
var selectUF = document.getElementById('selectUF');

function click_ckbnome(){
    edtnome.classList.add('d-none');
    if (ckb_nome.checked){
        edtnome.classList.remove('d-none');
     }
}


function click_ckbnolocalidade(){
    div_check_localidade = document.getElementById('div-check-localidade');
    div_check_nolocalidade = document.getElementById('div-check-nolocalidade');

    div_check_localidade.classList.remove('d-none');
    if (ckb_nolocalidade.checked){
        div_check_localidade.classList.add('d-none');
    }

}
function click_ckblocalidade(uf){
    console.log('UF>'+uf);
    div_localidade = document.getElementById('div-localidade');
    div_localidade.classList.add('d-none');
    if (ckb_localidade.checked){
        div_localidade.classList.remove('d-none');
        populate_uf(uf,selectUF);
    }
}


function click_btn_filtrar(){
    ckb_dt = (ckb_datanascimento.checked) ? 'S' : 'N';
    ckb_phone = (ckb_phone.checked) ? 'S' : 'N';
    ckb_nome = (ckb_nome.checked) ? 'S' : 'N';
    per_page = vper_page.value;
    ckb_localidade = (ckb_localidade.checked) ? 'S' : 'N';
    ckb_nolocalidade = (ckb_nolocalidade.checked) ? 'S' : 'N';

    if (ckb_nome == 'S' && edtnome.value==''){

    }
    else if (ckb_localidade == 'S' && selectUF.value == '0'){

    }
    else{
        if (ckb_nolocalidade=='S'){
            ckb_localidade = 'N';
            selectUF.value = '0';
            edtidcidade.value = '0';
        }
        url = '/pandas/get/schedules?per_page='+per_page+'&page=1&ckb_dt='+ckb_dt+
        '&ckb_phone='+ckb_phone+'&ckb_nome='+ckb_nome+'&edtnome='+edtnome.value+
        '&ckb_localidade='+ckb_localidade+'&uf='+selectUF.value+'&ckb_nolocalidade='+ckb_nolocalidade+
        '&idcidade='+edtidcidade.value+'&gerarcsv=N';
        console.log(url);
        window.location.href = url;
    }
}

function click_btn_modalfiltro(uf){
    console.log(uf.length);
    if (uf.length == 2){
        onchange_input_uf(uf);
    }
}
function click_gerarcsv(){
    url = location.href+'&gerarcsv=S';
    window.location.href = url;
}

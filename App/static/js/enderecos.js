function loading_var() {
    var edtcep = document.getElementById('edtcep');
    var edtlogradouro = document.getElementById('edtlogradouro');
    var edtbairro = document.getElementById('edtbairro');
    var edtcomplemento = document.getElementById('edtcomplemento');
    var edtidcidade = document.getElementById('edtidcidade');
    var edtnomecidade = document.getElementById('edtnomecidade');
    var edtidendereco = document.getElementById('edtidendereco');
    var edtsiglauf = document.getElementById('edtsiglauf');
    var edtidpessoa = document.getElementById('edtidpessoa');
    var chkprincipal = document.getElementById('chkprincipal');
    var edtpadrao = document.getElementById('edtpadrao');
    var edtlocalidade = document.getElementById('edtlocalidade');

}

// CLICA BOTÃO INSERIR
function btn_click_add_endereco(){
    loading_var();

    edtidendereco.value='-1';
    edtidcidade.value='0';
    populate_uf('',document.getElementById('selectUF'));
    array_inputs = ["edtlogradouro","edtbairro","edtcomplemento","edtnomecidade","selectUF","edtcep","edtnumero"];
    verify_campempty(array_inputs,'limpar');
}

// Clica botão Delete endereco
function btn_click_delete_endereco(endereco){
    console.log(endereco);
    document.querySelector('#edtidendereco-delete').value = endereco.id;
    modal_msg = document.querySelector('#modal-msg-delete-endereco');
    modal_msg.innerHTML = 'Deseja Excluir o Endereço: '+endereco.logradouro+', '+endereco.numero+
    ', '+endereco.bairro+', '+endereco.cidade.nome+' - '+endereco.cidade.microregiao.mesoregiao.uf.sigla+
    ', Cep: '+endereco.cep+' ?';
}

// Confirmar exclusao
function confirmar_exclusao_endereco(idpessoa,idendereco){
    alert_msg = document.querySelector('#alert-msgdelete-endereco');
    alert_msg.classList.remove('d-none');
    console.log(idendereco);
    url = '/delete/endereco/'+idendereco+'/'+idpessoa;
    fetch(url)
    .then( res => res.json())
    .then(data => {
        result = data;
        classalert = (result) ? 'alert-primary' : 'alert-danger';
        alert_msg.classList.add(classalert);
        alert_msg.innerHTML = result.mensagem;
        setTimeout(function(){
                alert_msg.classList.add('d-none');
                alert_msg.classList.remove(classalert);
                $('#modal-delete-endereco').modal('hide');
                enderecosatleta(result.idpessoa);
            },3000)
    });
}


function btn_click_alterar_endereco(endereco){
    loading_var();

    edtcep.value = mCEP(endereco.cep.replace(/\D/g,""));
    edtlogradouro.value = endereco.logradouro;
    edtbairro.value = endereco.bairro;
    edtcomplemento.value = endereco.complemento;
    edtidcidade.value = endereco.cidade.id;
    edtnomecidade.value = endereco.cidade.nome;
    uf = endereco.cidade.microregiao.mesoregiao.uf.sigla;
    console.log(uf);
    edtsiglauf.value = uf;
    populate_uf(uf,document.getElementById('selectUF'));
    edtidendereco.value = endereco.id;
    edtnumero.value = endereco.numero;
    
}



// BUSCA ENDERECOS E PREENCHE, CONSTROI TABELA
async function enderecosatleta(idpessoa){
    console.log(idpessoa);

    alert_enderecos = document.getElementById('alert-msg-table-enderecos');
    table_enderecos = document.getElementById('table-enderecos');
    tbody_enderecos = document.getElementById('tbody-enderecos');
    try{
        url = '/get/enderecos/pessoa/'+idpessoa;
        let response = await fetch(url);
        let tr_endereco = '';
        if (response.ok) {
            alert_enderecos.classList.remove('d-none');
            alert_enderecos.classList.remove('alert-dark');
            alert_enderecos.innerHTML = '<div class="spinner-border text-primary" role="status">'+
            '<span class="sr-only">Loading...</span></div>>Aguarde! Buscando Endereços';
            let response_json = await response.json();
            console.log(response_json);
            if (response_json.tot > 0){
                tab_enderecos = response_json.data;
                tab_enderecos.forEach((endereco) => {
                    desctipo = '';
                    switch(endereco.tipo) {
                        case 0:
                            desctipo = 'Comercial'
                            break;
                        case 1:
                            desctipo = 'Entrega'
                            break;
                        case 2:
                            desctipo = 'Cobrança'
                            break;
                        case 3:
                            desctipo = 'Residencial'
                            break;
                        case 4:
                            desctipo = 'Rural'
                            break;
                    }
                    tr_endereco += '<td>'+desctipo+': '+endereco.logradouro+', Nº: '+endereco.numero+', '+endereco.bairro+
                    ', '+endereco.cidade.nome+' - '+endereco.cidade.microregiao.mesoregiao.uf.nome+', '+
                    'Cep: '+endereco.cep+'</td>';
                    tr_endereco +='<td class="align-middle text-center">'+((endereco.padrao=='S') ? 'Sim' : 'Não')+'</td>';

                    enderecojson = JSON.stringify(endereco);
                    tr_endereco +="<td class='align-middle text-center'>"+
                    "<button class='btn btn-warning btn-sm mb-1' "+
                    "data-toggle='modal' data-target='#insert-edit-modal-endereco' "+
                    "onclick='btn_click_alterar_endereco("+enderecojson+");'>"+
                    "<span class='glyphicon glyphicon-pencil'></span></button>"+
                    "<button class='btn btn-warning btn-sm' "+
                    "data-toggle='modal' data-target='#modal-delete-endereco' "+
                    "onclick='btn_click_delete_endereco("+enderecojson+");'>"+
                    "<span class='glyphicon glyphicon-trash'></span></button>"+
                    "</td></tr>";

                });
                alert_enderecos.classList.add('d-none');
                table_enderecos.classList.remove('d-none');
                tbody_enderecos.innerHTML = tr_endereco;
            }
            else{
                alert_enderecos.classList.remove('d-none');
                table_enderecos.classList.add('d-none');
                alert_enderecos.classList.add('alert-warning');
                alert_enderecos.innerHTML = '<label class="text-dark"><strong>'+
                'Nenhum Endereço Lançando para esse usuário</strong></label>';
            }
        }

    }
    catch(err){

    }

}


// SELECIONA A UF ESCOLHIDA NO COMBOBOX DE UF
function selectedUF(siglauf){
    optionufselect = document.querySelector('div.selectoruf option[value='+siglauf+']');
    optionufselect.selected = true;

}

// BUSCA DADOS ENDERECO POR CEP DIGITADO
async function search_cidade_by_cep(vlcep){
    cep = vlcep.replace(/\D/g,"");
    small_cep = document.getElementById('small-cep');
    small_cep.classList.remove('d-none');
    if(cep.length < 8){
        small_cep.innerHTML =  'Forneça um CEP válido';
    }
    else{
        small_cep.innerHTML='Aguarde Buscando dados...';
        let response = await fetch('/get/cep/'+cep);
        if(response.ok){
            let json = await response.json();
            let erro = false;
            try{
                erro = json.erro;
            }
            catch{
                erro = false;
            }
            if (!erro){
                edtcep.value = mCEP(json.cep.replace(/\D/g,""));
                edtlogradouro.value = json.logradouro;
                edtbairro.value = json.bairro;
                edtcomplemento.value = json.complemento;
                edtidcidade.value = json.ibge;
                edtnomecidade.value = json.localidade;
                edtsiglauf.value = json.uf;

                selectedUF(json.uf);

                array_inputs = ["edtnomecidade","selectUF"];
                verify_campempty(array_inputs,'disabled');
                small_cep.classList.add('d-none');
            }
            else{
                array_inputs = ["edtlogradouro","edtbairro","edtcomplemento","edtnomecidade","selectUF"];
                verify_campempty(array_inputs,'limpar');
                verify_campempty(array_inputs,'disabled');

                optionufselect = document.querySelector('div.selectoruf option[value="0"]');
                optionufselect.selected = true;

                small_cep.classList.remove('d-none');
                small_cep.innerHTML = 'CEP informado não encontrado';
            }
        }
    }
}


// ATRIBUIR DISABLED OU LIMPAR CAMPOS
function verify_campempty(inputs,acao){
    for(index in inputs){
        console.log(inputs[index]);
        if(acao == 'disabled'){
            document.getElementById(inputs[index]).readOnly = false;
            document.getElementById(inputs[index]).style.backgroundColor = '';

            if (document.getElementById(inputs[index]).value.length > 0){
                document.getElementById(inputs[index]).readOnly = true;
                document.getElementById(inputs[index]).style.backgroundColor = '#dcdcdc';

            }
            else{

            }

        }else if(acao=='limpar'){
            document.getElementById(inputs[index]).value = '';
        }
    }
}



// PREENCHE UF
function populate_uf(ufselected='',selectUF){

    let option = document.createElement('option');
    option.setAttribute('value',0);
    option.textContent = 'Forneça o Estado';
    selectUF.appendChild(option);


    fetch('/get/uf/0?dataonly=id,nome,sigla')
    .then(res => res.json())
    .then(data => {
        ufs = data.data;

        ufs.map(uf =>{
            const option = document.createElement('option');
            option.setAttribute('value',uf.sigla);
            if (ufselected ==uf.sigla){
                option.setAttribute('selected',true);
            }
            option.textContent = uf.nome;
            selectUF.appendChild(option);
        });
    })
}


// PREENCHE CIDADE DE ACORDO COM A UF ESCOLHIDA
function onchange_input_uf(uf){
    edtsiglauf.value = uf;
    small_selectuf = document.querySelector('#small-selectuf');
    small_selectuf.classList.remove('d-none');

    var brownser_cidades = document.querySelector('#brownser-cidades');

    fetch('/get/cidade/UF/'+uf+'?dataonly=id,nome')
    .then(res => res.json())
    .then(data =>{
        cidades = data.data;
        cidades.map(cidade =>{
            const option = document.createElement('option');
            option.setAttribute('value',cidade.nome);
            option.setAttribute('data-value',cidade.id);
            brownser_cidades.appendChild(option);
        });

        small_selectuf.classList.add('d-none');
    })
}


// INPUT NOMECIDADE, QUANDO DIGITA, BUSCA CIDADE COM O NOME DIGITADO
function btn_brownser_change(inputcidade){
    option_selector = document.querySelector('option[value="'+inputcidade+'"]');
    edtidcidade.value = '0';
    if (option_selector){
        edtidcidade.value = option_selector.getAttribute('data-value');
    }
    console.log(edtidcidade.value);


}


// GRAVAR ENDERECO NO BANCO DE DADOS
function gravarendereco(){
    edtlocalidade.value = edtnomecidade.value;
    let idpessoatemp = edtidpessoa.value;
    console.log(edtlogradouro.value);
    edtpadrao.value = (chkprincipal.checked) ? 'S' : 'N';
    small_selectuf = document.querySelector('#small-selectuf');
    small_cidade = document.querySelector('#small-cidade');
    small_cep = document.querySelector('#small-cep');
    small_logradouro = document.querySelector('#small-logradouro');
    small_bairro = document.querySelector('#small-bairro');

    small_selectuf.classList.add('d-none');
    small_cidade.classList.add('d-none');
    small_cep.classList.add('d-none');
    var gravar = false;
    if (edtcep.value.length==0){ // cep
        small_cep.innerHTML = 'Forneça o CEP para continuar';
        small_cep.classList.remove('d-none');
    }else if(edtlogradouro.value.length == 0){
        small_logradouro.innerHTML = 'Forneça o Logradouro para continuar';
        small_logradouro.classList.remove('d-none');
    }else if(edtbairro.value.length == 0){
        small_bairro.innerHTML = 'Forneça o Bairro para continuar';
        small_bairro.classList.remove('d-none');
    }else if (edtsiglauf.value == '' || edtsiglauf.value == '0'){ // UF
        small_selectuf.innerHTML = 'Forneça o Estado para continuar';
        small_selectuf.classList.remove('d-none');
    } else if (edtidcidade.value == '0' || edtidcidade.value == ''){ // Cidade
        small_cidade.innerHTML = 'Forneça a Cidade para continuar';
        small_cidade.classList.remove('d-none');
    }else{
        gravar = true;
    }

    if (gravar){
        alert_dados = document.querySelector('#alert-dadosendereco');

        alert_dados.innerHTML = (edtidendereco.value =='-1')? 'Inserindo':'Alterando' + ' endereço. Aguarde';
        alert_dados.classList.remove('d-none');
        url = '/post/endereco/pessoa';
        form_endereco = document.querySelector('#formendereco');
        formData = new FormData(form_endereco);
        mybody = { method:'POST', body:formData };
        fetch(url,mybody)
        .then(res => res.json())
        .then(data => {
            res = data;
            alert_dados.innerHTML = res.mensagem;
            classalert = (res.result) ? 'alert-primary' : 'alter-danger';
            alert_dados.classList.add(classalert);
            setTimeout(function(){
                alert_dados.classList.add('d-none');
                alert_dados.classList.remove(classalert);
                $('#insert-edit-modal-endereco').modal('hide');
                enderecosatleta(res.idpessoa);
            },3000)
        });
    }
}
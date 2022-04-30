var btn_enviar = document.getElementById('btnenviar');
var msg_small = document.getElementById('msg-small');
var contentforgoutit = document.getElementById('contentforgoutit');
var contentnewpwd  = document.getElementById('contentnewpwd');
var contentkeyacess = document.getElementById('contentkeyacess');
var small_key = document.getElementById('small-key');

document.getElementById('contentnewpwd').classList.add('d-none');

function btn_click_envia(){
    msg_small.classList.add('d-none');
    small_email = document.getElementById('small-email');
    email = document.getElementById('edtemail').value;
    if (email != ''){
        small_email.classList.add('d-none');
        verificaemail(email);
    }
    else{
        small_email.classList.remove('d-none');

    }

}

async function verificaemail(email){
    let response = await fetch('/sisnutri/getemail?email='+email);
    if (response.ok) {
        btn_enviar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"'+
        'aria-hidden="true"></span> Enviando ...';
        btn_enviar.disabled = true;
        let data = await response.json();
        if (data.result){
            atleta = data.data;
            enviaremail(atleta.email,atleta.name,atleta.id);

        }
        else{
            btn_enviar.disabled = false;
            btn_enviar.innerHTML = 'Enviar';
            msg_small.classList.add('alert-danger');
            msg_small.classList.remove('d-none');
            msg_small.innerHTML = 'Email não foi encontrado na base de dados';

        }
    }
    else{

    }
}
async function enviaremail(email,nome,id){

    try{
        let formData = new FormData();
        formData.append('email',email);
        formData.append('nome',nome);
        formData.append('id',id);
        msg_small.classList.add('d-none');
        url = '/sisnutri/sendemail/verifykey';
        var mybody = {method:'POST', body:formData };
        let response = await fetch(url,mybody);
        if (response.status == 200) {
            let resultjson = await response.json();
            msg_small.classList.remove('alert-danger');
            if(resultjson){
                msg_small.classList.add('alert-primary');
                msg_small.innerHTML = '<p>Email Enviado com Sucesso '+ nome +', Verique sua caixa de entrada.</p>'+
                '<p>E digite abaixo o código de validação que foi enviado</p>';

                contentkeyacess.classList.remove('d-none');
                contentforgoutit.classList.add('d-none');
                document.getElementById('edtidatleta').value = id;
            }
            else{
                contentforgoutit.classList.remove('d-none');
                contentkeyacess.classList.add('d-none');
                contentnewpwd.classList.add('d-none');
                msg_small.classList.add('alert-danger');
                msg_small.innerHTML = 'Erro ao enviar o email!, Tente novamente mais tarde!';
            }
            msg_small.classList.remove('d-none');
            btn_enviar.disabled = false;
            btn_enviar.innerHTML = 'Enviar';
        }
        else{
            msg_small.classList.remove('d-none');
            msg_small.classList.innerHTML = '<p>Error ao tentar enviar e-mail, Atualiza a pagina e tente novamente.</p>'+
            '<p>Erro: '+response.status+'</p>';
        }
    }
    catch(err) {
        msg_small.classList.remove('d-none');
        msg_small.classList.innerHTML = '<p>Error ao tentar enviar e-mail, Atualiza a pagina e tente novamente.</p>'+
        '<p>Erro: '+err+'</p>';
    }
}

async function btn_valida_key(){
    if (document.getElementById('edtkeyacess').value != ''){
        small_key.classList.add('d-none');
        try{
            form = document.getElementById('form-keyacess');
            let formData = new FormData(form);
            url = '/sisnutri/atleta/verifykeyacess';
            var mybody = {method:'POST', body:formData };
            let response = await fetch(url,mybody);
            if (response.ok) { // if HTTP-status is 200-299
                let resultjson = await response.json();
                if (resultjson.result){
                    document.getElementById('edtidatletapwd').value = resultjson.idatleta;
                    msg_small.classList.remove('d-none');
                    msg_small.classList.remove('alert-primary');
                    msg_small.classList.add('alert-primary');
                    msg_small.innerHTML = 'Código Validado com Sucesso! Digite Abaixo sua nova senha.';
                    contentforgoutit.classList.add('d-none');
                    contentkeyacess.classList.add('d-none');
                    contentnewpwd.classList.remove('d-none');
                }else{
                    msg_small.classList.add('alert-danger');
                    msg_small.innerHTML = 'Código não corresponde com o enviado para o email! Verifique!';
                    contentforgoutit.classList.add('d-none');
                    contentkeyacess.classList.remove('d-none');
                    contentnewpwd.classList.add('d-none');
                }
            }
        }
        catch(err){
            msg_small.classList.add('alert-danger');
            msg_small.classList.remove('d-none');
            msg_small.classList.innerHTML = '<p>Error ao tentar verificar a chave de acesso, Atualiza a pagina e tente novamente.</p>'+
            '<p>Erro: '+err+'</p>';
        }
    }
    else{
        small_key.classList.remove('d-none');
        small_key.innerHTML = 'Código de Acesso em Branco!';
    }
}

function btn_confimar_newpwd(){
    vlpwd = document.getElementById('edtpwd');
    vlpwd_conf = document.getElementById('edtpwdconf');
    small_pwd = document.getElementById('small-pwd');
    small_pwd.classList.add('d-none');
    small_pwd_conf = document.getElementById('small-pwd-conf');
    small_pwd_conf.classList.add('d-none');
    msg_small.classList.add('alert-danger');
    msg_small.classList.add('d-none');
    msg_small.classList.remove('alert-primary');

    if (vlpwd.value.length<8){
        small_pwd.classList.remove('d-none');
    }
    else if(vlpwd_conf.value.length<8){
            small_pwd_conf.classList.remove('d-none');
    }
    else{
        if (vlpwd.value == vlpwd_conf.value){
            msg_small.classList.add('d-none');
            save_pwd();
            console.log('Salvar Senha');
        }
        else{
            msg_small.classList.add('alert-danger');
            msg_small.innerHTML = '<Label class="text-danger"><strong>Senhas não conferem. Verifique!</strong></label>';
            msg_small.classList.remove('d-none');
            vlpwd_conf.focus();
        }

    }
}
async function save_pwd(){
    try{
        form = document.getElementById('form-newpdw');
        let formData = new FormData(form);
        url = '/sisnutri/atleta/update/newpwd';
        var mybody = {method:'POST', body:formData };
        let response = await fetch(url,mybody);
        if (response.status == 200) { // if HTTP-status is 200-299
            msg_small.classList.remove('alert-danger');
            msg_small.classList.remove('alert-primary');

            btnconfirmar = document.getElementById('btnconfirmar');
            btnconfirmar.disabled = true;
            btnconfirmar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"'+
            'aria-hidden="true"></span>Redirecionando para a tela de Login...';

            let resultjson = await response.json();
            if (resultjson.result){
                msg_small.classList.add('alert-primary');
            }

            else{
                msg_small.classList.add('alert-danger');
            }
            console.log("Ate Aqui");
            msg_small.classList.remove('d-none');
            msg_small.classList.innerHTML = resultjson.mensagem;
            setTimeout(function(){
                edtid = document.getElementById('edtidatletapwd').value;
                window.location.href = '/redirect/telalogin/atleta/'+edtid+'/'+resultjson.mensagem;
                btnconfirmar.disabled = false;
            },3000);

        }
    }
    catch(err){
        msg_small.classList.add('alert-danger');
        msg_small.classList.remove('d-none');
        msg_small.classList.innerHTML = '<p>Erro interno ao tentar enviar a nova senha, Atualiza a pagina e tente novamente.</p>'+
        '<p>Erro: '+err+'</p>';
    }
}
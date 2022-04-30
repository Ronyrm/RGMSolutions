function editvendedor(tbvendedor){
    document.getElementById('lblidvendedor').innerHTML = 'Editando vendedor id: '+ tbvendedor.id;
    document.getElementById('edtid').value = tbvendedor.id;
    document.getElementById('edtnome').value = tbvendedor.pessoa.nome;
    document.getElementById('edtrazaosocial').value = tbvendedor.pessoa.razaosocial;
    document.getElementById('edtusername').value = tbvendedor.pessoa.username;
    document.getElementById('edtemail').value = tbvendedor.pessoa.email;
    document.getElementById('edtcpfcnpj').value = tbvendedor.cpfcnpj;
    document.getElementById('edtcomissao').value = tbvendedor.comissao;
    document.getElementById('edtusername').focus();
}
function btninserirvendedor(){
    document.getElementById('lblidvendedor').innerHTML = 'Inserindo Vendedpr';
    document.getElementById('edtnome').value = '';
    document.getElementById('edtrazaosocial').value = '';
    document.getElementById('edtusername').value = '';
    document.getElementById('edtemail').value = '';
    document.getElementById('edtcpfcnpj').value = '';
    document.getElementById('edtcomissao').value = '';
    document.getElementById('edtusername').focus();
    document.getElementById('edtid').value = '-1';
}

function changeorderby(token,pageatual,per_page){
    pageatual = (pageatual == '') ? '1' : pageatual;
    per_page = (per_page=='') ? '15' : per_page;

    orderby = $( "#orberby-vendedor option:selected" ).val();
    window.location.href = '/allvendedoresmain/'+pageatual+'/'+per_page+'/'+orderby+'?token='+token;

}

$('#formvendedor').submit( function(e){
    e.preventDefault();
    var myForm = document.getElementById('formvendedor');
    formData = new FormData(myForm);
    var token = document.getElementById('edttoken').value;
    var pageatual = document.getElementById('edtpageatual').value;
    var per_page = document.getElementById('edtper_page').value;
    var orderby = document.getElementById('edtorder').value;

    formData = new FormData($('#formvendedor')[0]);

    pageatual = (pageatual == '') ? '1' : pageatual;
    per_page = (per_page=='') ? '15' : per_page;
    orderby = (orderby=='') ? '1' : orderby;

    url = '';
    if (document.getElementById('edtid').value == '-1'){
        url = '/add/vendedor/'+pageatual+'/'+per_page+'/?token='+token;
    }
    else{
        url = '/edit/vendedor/'+pageatual+'/'+per_page+'/?token='+token;
    }

    confirmvendedor(formData,token,pageatual,per_page,orderby,url);
});

function confirmvendedor(formData,token,pageatual,per_page,orderby,urlacao){
    $.ajax({
        url: urlacao,
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false

    }).done( function(data){
        alert_dadosvendedor = document.getElementById('alert-dadosvendedor');
        if (data['result'] == true) {

            alert_dadosvendedor.classList.add("alert-primary");
            alert_dadosvendedor.innerHTML = '<strong>Sucesso</strong> <br> '+data['mensagem'];
            alert_dadosvendedor.classList.remove('d-none');

            setTimeout(function(){
                orderby = (orderby == '') ? '0' : orderby;

                $('#insert-edit-modal-vendedor').modal('hide');
                alert_dadosvendedor.classList.remove('alert-primary');
                alert_dadosvendedor.classList.add('d-none');
                window.location.href = '/allvendedoresmain/'+pageatual+'/'+per_page+'/'+orderby+'?token='+token;
            }, 3000);

        }
        else{
            alert_dadosvendedor.classList.add('alert-danger');
            alert_dadosvendedor.innerHTML = '<strong>Erro</strong> <br> '+data['mensagem'];
            alert_dadosvendedor.classList.remove('d-none');
            setTimeout(function(){
                alert_dadosvendedor.classList.remove('alert-danger');
                alert_dadosvendedor.classList.add('d-none');

            }, 3000);
        }

    }).fail( function(){

    }).always( function(){
        //var imgload = document.getElementById('imgcarregamento');
        //imgload.style.display = 'none';
    });
}




function add_rowtablevendedor(){
    var table_vendedor = document.getElementById('table-vendedores');
    var tr = document.createElement('tr');
    var tdid = tr.appendChild(document.createElement('td'));
    var tdcpfcnpj = tr.appendChild(document.createElement('td'));
    var tdnome = tr.appendChild(document.createElement('td'));
    var tdacoes = tr.appendChild(document.createElement('td'));

    tdid.innerHTML = data['data']['id'];

    tdnome.innerHTML = data['data']['pessoa']['nome'];

    table_vendedor.appendChild(tr);
}

function deletevendedor(idvendedor,nome,token){
    document.getElementById('edtiddelete').value = idvendedor;
    document.getElementById('modal-msg-delete').innerHTML = '<h5> Deseja excluir o Vendedor: '+idvendedor+' - '+nome+'?</h3>';
}

function confirmaexclusao(token,pageatual,per_page,orderby){
    idvendedor = document.getElementById('edtiddelete').value;

    if (idvendedor != ''){
        $.ajax({
            url: '/delete/vendedor',
            type: 'GET',
            data: 'idvendedor='+idvendedor,
            dataType: 'json'
        })
        .always(function(data) {

            console.log(data);
            alertmsg =  document.getElementById('alert-msgdelete');
            if(data['result'] == true){

                alertmsg.classList.add("alert-primary");
                alertmsg.innerHTML = '<strong>Sucesso</strong> <br> '+data['mensagem'];
                alertmsg.classList.remove('d-none');

                setTimeout(function(){
                    if (orderby == ''){
                        orderby = '0';
                    }
                    $('#modal-delete').modal('hide');
                    alertmsg.classList.remove('alert-primary');
                    alertmsg.classList.add('d-none');
                    window.location.href = '/allvendedoresmain/'+pageatual+'/'+per_page+'/'+orderby+'?token='+token;
                }, 3000);

            }
            else{
                alertmsg.classList.add('alert-danger');
                alertmsg.innerHTML = '<strong>Erro</strong> <br> '+data['mensagem'];
                alertmsg.classList.remove('d-none');
                setTimeout(function(){
                    alertmsg.classList.remove('alert-danger');
                    alertmsg.classList.add('d-none');
                    $('#modal-delete').modal('hide');
                }, 3000);

            }

        })
        .fail(function() {
            console.log('Erro');
            // Caso falhe solicite outro id
        });
    }


}


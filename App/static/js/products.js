function readURL(input) {
    console.log('entrou');
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#imgprod')
        .attr('src', e.target.result)
        .width(100)
        .height(100);
    };
    reader.readAsDataURL(input.files[0]);
  }
}
function editprod(product,caminhoimg,acao){

    cam = "";
    if (acao == 'A'){
        console.log(product['produto_grupo']);
        if (product['produto_grupo'] != null){
            document.getElementById('edtdescgrupoproduto').value = product['produto_grupo']['descricao'];
        }
        else {
            document.getElementById('edtdescgrupoproduto').value = ''
        }
        searchdalist_grupoprodutos(document.getElementById('edtdescgrupoproduto').value);

        document.getElementById('edtid').value = product['id'];
        document.getElementById('edtdescricao').value = product['descricao'];
        document.getElementById('edtsubdescricao').value = product['subdescricao'];
        document.getElementById('edtprecocusto').value = product['precocusto'];
        document.getElementById('edtmargemlucro').value = product['margemlucro'];
        document.getElementById('edtprecovenda').value = product['precovenda'];
        document.getElementById('edtestoqminimo').value = product['estoquemin'];
        document.getElementById('edtestoqatual').value = product['estoqueatual'];
        document.getElementById('lblidprod').innerHTML = 'Edição Produto. Código: '+product['id'];
        cam = caminhoimg + "\\"+product['caminhoimg'];
    }
    if (acao == 'I'){

        document.getElementById('edtid').value = '-1';
        document.getElementById('edtdescricao').value = '';
        document.getElementById('edtsubdescricao').value = '';
        document.getElementById('edtprecocusto').value = '';
        document.getElementById('edtmargemlucro').value = '';
        document.getElementById('edtprecovenda').value = '';
        document.getElementById('edtestoqminimo').value = '';
        document.getElementById('edtestoqatual').value = '';
        document.getElementById('lblidprod').innerHTML = 'Inserir novo Produto';
        cam ="nophoto.png";
    }

    if(product['caminhoimg'] != ''){
            console.log(cam);
            elimg = document.getElementById('imgprod');
            console.log('Acao:'+ acao);
            if (acao == 'A')
            {

                elimg.src = document.getElementById('imgprod_'+product['id']).src;
            }
            if (acao == 'I')
            {
                $('#imgprod')
                    .attr('src', document.getElementById('imgprod_semfoto').src)
                    .width(100)
                    .height(100);

                console.log('INserir');

            }

    }
    $('#collapse-dadosgerais').addClass('show');



}
function deleteprod(id,descricao,token){
    console.log('Codigo:'+id);

    document.getElementById('edtiddelete').value = id;

    document.getElementById('modal-msg-delete').innerHTML = '<p> Deseja excluir o Produto: '+id+' - '+descricao+'?</p>';
}

function exclusaoclick(token,page,qtdporpag){
    id = document.getElementById('edtiddelete').value;
    console.log('Id:'+document.getElementById('edtiddelete').value);
    $.ajax({
        url: '/del/produto/'+page+'/'+qtdporpag,
        type: 'GET',
        data: 'token='+token+'&id='+id,
        dataType: 'json'
    }).always(function(data) {
        console.log('Deletar:'+data['delete']);
        console.log(data['mensagem']);
        if(data['delete']){
            $('#msgdel').removeClass('d-none');
            $('#msgdel').addClass('alert alert-primary show');
            document.getElementById('msgdel').innerHTML = '<strong>Mensagem</strong>'+data['mensagem']+
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
            '<span aria-hidden="true">&times;</span></button>';
            $('#tr-prod'+id).remove();
        }
        else{
            console.log('Não Deletou')
        }

        setTimeout(function () {
		    $('#msgdel').hide();

	    }, 3000);


    })
    .fail(function() {
        console.log('Erro')
        // Caso falhe solicite outro id
    });

}
function btnqtdpag(token,page,qtdporpag,urlroot){
    console.log(token);
    console.log(page);
    console.log(qtdporpag);
    console.log(urlroot);
    window.location.assign(urlroot+'allprodutos/'+page+'/'+qtdporpag+'?current_user={}&token='+token);


}

function datalist_grupoprod(){
    $.ajax({
        url: '/all/grupoprodutos/',
        type: 'GET',
        dataType: 'json'
    }).always(function(data) {
        console.log(data);
        option_brownser = "";

        $.each(data['data'], function(chave,valor){
            option_brownser += '<option data-value="'+valor["id"]+'" value="'+valor["descricao"]+'">';
        });

        document.getElementById('browsers').innerHTML = option_brownser;

    })
    .fail(function() {
        console.log('Erro')
        // Caso falhe solicite outro id
    });
}
function searchdalist_grupoprodutos(descgrupo){

    value  = (descgrupo == '') ? document.getElementById("edtdescgrupoproduto").value : descgrupo;
    console.log(value);


    var idgrupoproduto = "0";
    try {
        idgrupoproduto = $('#browsers [value="' + value + '"]').data('value');
        idgrupoproduto = (typeof(idgrupoproduto) == "undefined") ? "0" : idgrupoproduto;
    }
    catch(err) {
        idgrupoproduto = "0";
    }
    document.getElementById("edtidgrupoproduto").value = idgrupoproduto;

    console.log("Valor " + idgrupoproduto);


}


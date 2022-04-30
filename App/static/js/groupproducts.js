function btnconfirmargrupo(){
    console.log('btnconfirmargrupo');
    edtdesc = document.getElementById("edtdescgrupo").value;
    edtid = document.getElementById("edtidgrupo").value;
    console.log('Desricao Prod:'+edtdesc);
    paginaatual = document.getElementById("edtpagatual").value;

    if (edtdesc != ''){

        $.ajax({
            url: '/post/grupoprodutos/',
            type: 'GET',
            data: 'idgrupo='+edtid+'&descgrupo='+edtdesc,
            dataType: 'json'
        })
        .always(function(data) {

            console.log(data);
            if(data['resultado'] == true){
                cxmsg = document.getElementById("cxmsg-grupo");
                cxmsg.classList.remove("d-none");
                cxmsg.classList.add("alert-primary");
                cxmsg.classList.remove("alert-danger");
                msgbox = '<strong>Mensagem</strong><br>'+data['mensagem'];
                msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
                msgbox += '<span aria-hidden="true">&times;</span></button>';
                cxmsg.innerHTML = msgbox;

                setTimeout(function () {
                    try {
                        seltopag = document.getElementById("seltotpag").value;
                    }
                    catch(err) {
                        seltopag = 5;
                    }
                    seltopag = (typeof(seltopag) == "undefined") ? "0" : seltopag;
		            btngrupoprod(paginaatual,seltopag);
                    modalgrid = document.getElementById("modal-grid-grupoprod");
                    modaldados = document.getElementById("modal-dados-grupoprod");
                    modaldados.classList.add("d-none");
                    modalgrid.classList.remove("d-none");

	            }, 2000);


            }
            else{
                cxmsg = document.getElementById("cxmsg-grupo");
                cxmsg.classList.remove("d-none");
                cxmsg.classList.remove("alert-primary");
                cxmsg.classList.add("alert-danger");
                msgbox = '<strong>Erro</strong><br> '+ data['mensagem'];
                msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
                msgbox += '<span aria-hidden="true">&times;</span></button>';
                cxmsg.innerHTML = msgbox;

            }

        })
        .fail(function() {
            console.log('Erro');
            // Caso falhe solicite outro id
        });
    }
    else{
        cxmsg = document.getElementById("cxmsg-grupo");
        cxmsg.classList.remove("d-none");
        cxmsg.classList.remove("alert-primary");
        cxmsg.classList.add("alert-danger");
        msgbox = '<strong>Error</strong><br> Forneça a Descrição do Grupo de Produtos para continuar';
        msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
        msgbox += '<span aria-hidden="true">&times;</span></button>';
        cxmsg.innerHTML = msgbox;


    }



}
function btnconfirmarexclusaogrupo(){
    edtid = document.getElementById("edtidgrupo").value;
    if (edtid != ''){

        $.ajax({
            url: '/delete/grupoprodutos/',
            type: 'GET',
            data: 'idgrupo='+edtid,
            dataType: 'json'
        })
        .always(function(data) {

            console.log(data);
            if(data['resultado'] == true){
                cxmsg = document.getElementById("cxmsgdelete-grupo");
                cxmsg.classList.remove("d-none");
                cxmsg.classList.add("alert-primary");
                cxmsg.classList.remove("alert-danger");
                msgbox = '<strong>Mensagem</strong><br>'+data['mensagem'];
                msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
                msgbox += '<span aria-hidden="true">&times;</span></button>';
                cxmsg.innerHTML = msgbox;

                setTimeout(function () {
		            btngrupoprod(1,5);
                    modalgrid = document.getElementById("modal-grid-grupoprod");
                    modaldados = document.getElementById("modal-dados-grupoprod");
                    modaldelete = document.getElementById("modal-delete-grupoprod");
                    modaldados.classList.add("d-none");
                    modaldelete.classList.add("d-none");
                    modalgrid.classList.remove("d-none");
	            }, 2000);


            }
            else{
                cxmsg = document.getElementById("cxmsgdelete-grupo");
                cxmsg.classList.remove("d-none");
                cxmsg.classList.remove("alert-primary");
                cxmsg.classList.add("alert-danger");
                msgbox = '<strong>Erro</strong><br> '+ data['mensagem'];
                msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
                msgbox += '<span aria-hidden="true">&times;</span></button>';
                cxmsg.innerHTML = msgbox;

            }

        })
        .fail(function() {
            console.log('Erro');
            // Caso falhe solicite outro id
        });
    }
    else{
        cxmsg = document.getElementById("cxmsgdelete-grupo");
        cxmsg.classList.remove("d-none");
        cxmsg.classList.remove("alert-primary");
        cxmsg.classList.add("alert-danger");
        msgbox = '<strong>Erro</strong><br> Id do Grupo de Produtos não carregado. Verifique!';
        msgbox += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
        msgbox += '<span aria-hidden="true">&times;</span></button>';
        cxmsg.innerHTML = msgbox;
        setTimeout(function () {
		    modalgrid = document.getElementById("modal-grid-grupoprod");
            modaldados = document.getElementById("modal-dados-grupoprod");
            modaldelete = document.getElementById("modal-delete-grupoprod");
            modaldados.classList.add("d-none");
            modaldelete.classList.add("d-none");
            modalgrid.classList.remove("d-none");
	    }, 2000);

    }

}
function btndeletegrupo(id,desc){
    console.log('Id: '+id+" - Descricao:"+desc);
    modalgrid = document.getElementById("modal-grid-grupoprod");
    modaldelete = document.getElementById("modal-delete-grupoprod");
    modaldados = document.getElementById("modal-dados-grupoprod");

    modaldelete.classList.remove("d-none");
    modalgrid.classList.add("d-none");
    modaldados.classList.add("d-none");
    document.getElementById("edtdescgrupo").value = desc;
    document.getElementById("edtidgrupo").value = id;

    document.getElementById("paragraf-msg-del").innerHTML = 'Deseja excluir o Grupo de Produtos: '+ id + ' - '+desc;
    cxmsg = document.getElementById("cxmsgdelete-grupo");
    cxmsg.classList.add("d-none");

}
function btneditgrupo(id,desc){
    console.log('Id: '+id+" - Descricao:"+desc);
    modalgrid = document.getElementById("modal-grid-grupoprod");
    modaldados = document.getElementById("modal-dados-grupoprod");
    modaldelete = document.getElementById("modal-delete-grupoprod");

    modaldados.classList.remove("d-none");
    modalgrid.classList.add("d-none");
    modaldelete.classList.add("d-none");
    document.getElementById("edtdescgrupo").value = desc;
    document.getElementById("edtidgrupo").value = id;

    document.getElementById("modal-title-dados-grupo").innerHTML = 'Editando Produto: '+ id + ' - '+desc;
    cxmsg = document.getElementById("cxmsg-grupo");
    cxmsg.classList.add("d-none");



}
function btncancelargrupo(){

    modalgrid = document.getElementById("modal-grid-grupoprod");
    modaldados = document.getElementById("modal-dados-grupoprod");

    modaldados.classList.add("d-none");
    modalgrid.classList.remove("d-none");

}
function btngrupoprod(page=1,totporpag=10){
    document.getElementById('edtpagatual').value = page;
    desc = 'None';
    console.log('to aqui');
    $.ajax({
        url: '/grupoprodutos/desc/'+page+'/'+totporpag,
        type: 'GET',
        data:'descricao='+desc,
        dataType: 'json'
    })
    .always(function(data) {
        console.log(data);
        divbtnins ='<div><button class="btn btn-sm btn-success mx-2 my-2"';
        vardesc = "''";
        divbtnins +=' onclick="btneditgrupo(-1,'+vardesc+')">';
        divbtnins +=' <span class="glyphicon glyphicon-plus"></span> Inserir';
        divbtnins +=' </button></div>';
        tab = '';
        pagination = '';

        if (data['achou'] == true) {
            tab += '<table class="table table-striped table-light ">';
            tab += '<thead class="bg-success">';
            tab += '<tr>';
            tab += '<th scope="col">Id</th>';
            tab += '<th scope="col">Descrição</th>';
            tab += '<th scope="col">Ações</th>';
            tab += '</tr> </thead>';
            tab += '<tbody class="border border-success border-2">';
            $.each(data['data'], function(chave,valor){
                console.log(chave + ' - '+valor);
                console.log(valor['descricao']);

                tab += '<tr id="tr-grupprod'+valor['id']+'" title="tr-grupoprod'+valor['id']+'">';
                tab += '<th scope="row">'+valor['id']+'</th>';
                tab += '<td>'+valor['descricao']+'</td>';
                tab +='<td><div>';
                tab +='<button class="btn btn-sm btn-success mx-2 my-2"';
                vardesc = "'"+valor['descricao']+"'";
                tab +=' onclick="btneditgrupo('+valor['id']+','+vardesc+')">';
                tab +=' <span class="glyphicon glyphicon-pencil"></span> Editar';
                tab +=' </button>';
                tab +='<button class="btn btn-sm btn-danger mx-2 my-2"';
                tab +=' onclick="btndeletegrupo('+valor['id']+','+vardesc+');"> ';
                tab +='<span class="glyphicon glyphicon-trash"></span> Excluir';
                tab +='</button></div></td></tr>';
            });
            tab += '</tbody> </table>';
            datapag = data['datapag'];

            pagination += '<nav class="" aria-label="Page navigation example">';
            pagination +='  <div class="row justify-content-center my-2">';
            pagination +='    <ul class="pagination bg-primary mx-2 my-2">';

            var disable = (datapag['prevpag'] == 'False') ? 'disabled' : '';


            pagination +='<li class="page-item '+disable+' ">';
            pagat = parseInt(datapag['pageatual']);

            ant = pagat-1;
            pagination +='<a class="page-link" onclick="btngrupoprod('+ant+','+datapag['per_page']+');">';
            pagination +='Anterior</a></li>';

            for (let number = 1; number <= parseInt(datapag['totpage']); number++) {
                disableli = (number == parseInt(datapag['pageatual'])) ? 'active' : '';
                pagination +='<li  class="page-item bg-success text-warning '+disableli+'">';
                npag = number;

                pagination +='    <a class="page-link" onclick="btngrupoprod('+npag+','+datapag['per_page']+');">';

                    pagination += number.toString()+'</a></li>';
            }

            disable = (datapag['nextpag'] == 'False') ? 'disabled' : '';

            pagination +='<li class="page-item '+disable+'">';
            pagat = parseInt(datapag['pageatual'])+1;

            pagination +='<a class="page-link" onclick="btngrupoprod('+pagat+','+datapag['per_page']+');">';
            pagination +='Próximo </a></li></ul>';
            pagination +='<div class="form-group text-center mx-2 my-2">';
            pagination +='<div class="row "><div class="d-inline text-center "><label class="text-center mx-2" for="seltotpag">Itens por Página:</label></div>';
            pagination +='<div class="d-inline"><select class="form-control" id="seltotpag" onchange="changetotpag(1);" >';
            pagination +='<option value="5" '+ ((parseInt(datapag['per_page']) == 5)? 'selected' : '') +'>5</option>';
            pagination +='<option value="15" '+ ((parseInt(datapag['per_page']) == 15)? 'selected' : '') +'>15</option>';
            pagination +='<option value="30" '+ ((parseInt(datapag['per_page']) == 30)? 'selected' : '') +'>30</option>';
            pagination +='<option value="60" '+ ((parseInt(datapag['per_page']) == 60)? 'selected' : '') +'>60</option>';

            pagination +='</select></div></div></div></div></nav>';

        }
        else{
            console.log()
            divbtnins +='<div class="alert alert-warning" role="alert">';
            divbtnins += data['mensagem'] + '</div>';
        }

        document.getElementById('modal-gridprod').innerHTML = divbtnins + tab + pagination;
        modalgrid = document.getElementById("modal-grid-grupoprod");
        modaldados = document.getElementById("modal-dados-grupoprod");
        modaldelete = document.getElementById("modal-delete-grupoprod");
        modaldelete.classList.add("d-none");
        modalgrid.classList.remove("d-none");
        modaldados.classList.add("d-none");
    })
    .fail(function() {
        console.log('Erro');
        // Caso falhe solicite outro id
    });

}
function changetotpag(pagat){
    valcampsel = document.getElementById("seltotpag").value;
    console.log(valcampsel);
    btngrupoprod(pagat,valcampsel);

}
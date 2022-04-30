var datancms = [];
var edtdesc = document.getElementById('input-descricao');
function select_filtro_change(vlsel){
    switch(parseInt(vlsel)) {
      case 0:
        edtdesc.setAttribute("placeholder","Digite aqui a Descricao");
        break;
      case 1:
        edtdesc.setAttribute("placeholder","Digite aqui o Código");
        break;
      case 2:
        edtdesc.setAttribute("placeholder","Digite aqui o Código");
        break;
    }
}
select_filtro_change("0");
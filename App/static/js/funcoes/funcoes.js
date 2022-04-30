var data_clima = {};
const str_div_loading = '<div class="spinner-border text-warning" role="status">'+
                        '<span class="sr-only">Loading...</span></div>';
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.loh( "Geolocation is not supported by this browser.");
  }
}
function showPosition(position) {
    lat = position.coords.latitude.toString();
    lon = position.coords.longitude.toString();
    data_clima =  {'lat':lat.substring(0, 8),
    'lon':lon.substring(0, 8)};
    return data_clima;
}


// TRADUZ TEXTOS PORTUGUES EM INGLES OU VICE-VERSA AUTOMATICAMENTE
async function translate_text(text){
    url = '/post/translate';
    let formData = new FormData();
    formData.append('texttranslate',text);
    var mybody = {method:'POST', body:formData };
    let response = await fetch(url,mybody);
    if (response.status == 200) {
        jsondata = await response.json();
        return jsondata.traducao;
    }
    else{
        return '';
    }
}

async function search_moeda_conversion_BRL(){
      url = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL';
      response = await fetch(url);
      if (response.status==200){
        result = await response.json();
        return result;
      }
      else{
        return {};
      }

}
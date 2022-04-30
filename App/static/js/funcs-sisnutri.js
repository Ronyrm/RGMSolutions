//retorna idade pela data de nascimento Ex: "1988-08-06"
function retornaidade(birthday){
    dtnv = +new Date(birthday);
    return  ~~((Date.now() - dtnv) / (31557600000));
}

// retorna o valor calorico TBM harris_original
function harris_original(genero,valpeso,valaltura,idade){
    //Homens: (13.7516 * W) + (5.0033 * H) - (6.755 * A) + 66.473
    //Mulheres: (9.5634 * W) + ( 1,8496 * H) - (4,6756 * A) + 655,0955
    //Variáveis: W = peso em quilogramas, H = altura em centímetros, A = idade em anos

    if (genero == 'M'){
        return  (13.7516 * valpeso) + (5.0033 * valaltura) - (6.755 * idade) + 66.473;
    } else{
        return  (9.5634 * valpeso) + ( 1.8496 * valaltura) - (4.6756 * idade) + 655.0955;
    }
}

// retorna o valor calorico TBM harris Revisada
function harris_revisada(genero,valpeso,valaltura,idade){
    //Homens: (13,397 * W) + (4,799 * H) - (5,677 * A) + 88,362
    //Mulheres: (9,247 * W) + (3,098 * H) - (4,330 * A) + 447,593
    //Variáveis: W = peso em quilogramas, H = altura em centímetros, A = idade em anos
    if(genero=='M'){
        return (13.397 * valpeso) + (4.799 * valaltura) - (5.677 * idade) + 88.362;
    }
    else{
        return (9.247 * valpeso) + (3.098 * valaltura) - (4.330 * idade) + 447.593
    }
}

// retorna o valor calorico TBM Mifflin St Jeor
function mifflin(genero,valpeso,valaltura,idade){
    //Homens: (10 * W) + (6,25 * H) - (5 * A) + 5
    //Mulheres: (10 * W) + (6,25 * H) - (5 * A) - 161
    //Variáveis: W = peso em quilogramas, H = altura em centímetros,
    if (genero == 'M'){
        return (10 * valpeso) + (6.25 * valaltura) - (5 * idade) + 5;
    }
    else{
        return (10 * valpeso) + (6.25 * valaltura) - (5 * idade) - 161;
    }
}

// retorna o valor calorico TBM Katch-McCardle
function katchmcardle(valpeso,percfat){
    //Fórmula:
    //370 + (21,6 * (W * (1 - P)))
    //Variáveis: W = peso em quilogramas, P = porcentagem de gordura corporal
    return 370 + (21.6 * ((valpeso * (100 - percfat)/100)));

}

function retornadata(data,separator){
    dia = data.getDate();
    mes = data.getMonth();
    mes += 1;
    if (dia<=9){
        dia = '0'+dia;
    }
    if (mes<=9){
        mes = '0'+mes;
    }
    ano = data.getFullYear();

    return ano+separator+mes+separator+dia;
}

function retornadataBR(data){
    dia = data.getDate();
    mes = data.getMonth();
    mes += 1;
    if (dia<=9){
        dia = '0'+dia;
    }
    if (mes<=9){
        mes = '0'+mes;
    }
    ano = data.getFullYear();

    return dia+'/'+mes+'/'+ano;
}

function retornahoraBR(data){
    hora = data.getHours();
    min = data.getMinutes();
    seg = data.getSeconds();


    return hora+':'+min+':'+seg;

}

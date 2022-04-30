def calcmacronutriente(qtdmacro,qtdgramastotal,qtdgramasinfo):
    valor = qtdmacro * qtdgramasinfo
    return  round(valor/qtdgramastotal,2)
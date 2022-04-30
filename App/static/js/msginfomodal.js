const msginfo = {
    calkgfat : "<small><p class='align-center'><strong>Perda / ganho (peso):</strong></p> "+
    "<p>Você pode escolher entre calcular a perda de peso selecionando o botão 'Perda de Peso' ou o ganho de peso selecionando o botão 'Ganho de Peso'"+
    " na tela anterior.<br>Se você alterar a meta de peso para qualquer coluna (dia, semana, mês ou ano), todos os déficits calóricos (ou excedentes) e metas"+
    " de ingestão serão atualizados automaticamente. Seu déficit / superávit calórico é calculado pegando o peso correspondente (em KG)"+
    " e multiplicando-o por um valor padrão (de 3.500).</p><p>"+
    "<p>Este é um número geralmente usado para representar as calorias necessárias para perder meio quilo de gordura corporal."+
    "<br>Se desejar usar algo diferente de 3.500, você pode editar o valor ao lado.</p></small>",

    bmr:"<small>É (aproximadamente) a taxa de energia em calorias que você usa em um período de 24 horas quando está completamente em repouso e sem se mover."+
    "É o que seu corpo precisa para sobreviver em um estado confortável, mas em coma, mantendo o peso atual. Muitas coisas podem entrar no cálculo de uma verdadeira TMB, "+
    "como genética, ambiente (incluindo temperatura), estado emocional, doença, relação músculo / gordura, etc. "+
    "<br>É por isso que qualquer fórmula que não leve todos esses fatores em consideração deve ser apenas usado para calcular um valor 'geral'. "+
    "Outros valores que estão intimamente relacionados à TMB são a Taxa Metabólica de Repouso (TMR) e o Gasto Energético Diário de Repouso (GEDR). "+
    "<br>Para obter mais informações, consulte a referência da <a href='https://pt.wikipedia.org/wiki/Metabolismo_basal#:~:text=Metabolismo%20basal%20ou%20Taxa%20metab%C3%B3lica,sem%20prejudicar%20o%20funcionamento%20dos' target='_blank'>Wikipedia</a>."+
    "<br><br>Uma TMB para cada método individual é refletida nesta coluna, enquanto a TMB média para todos os métodos selecionados (em: 'Incluir' e 'Média(final)') é exibida na linha inferior e ao lado.</small>",

    tdee:"<small>É (aproximadamente) a taxa de energia (em calorias) que você normalmente usaria, em média, em um período de 24 horas."+
    "<brAo iniciar uma nova dieta, este é o número inicial que as pessoas parecem dar mais ênfase. "+
    "Como um cálculo direto, o GCD é o sua TMB(metabolismo basal) multiplicado pelo seu fator de nível de atividade(escolhido na etapa anterior)."+
    " O que obviamente significa que obter um bom TMB e travar o nível de atividade mais preciso é fundamental, mas antes que você gaste uma quantidade infinita de tempo e energia obcecado por esse valor, "+
    "deixe-me puxá-lo de volta ... não se preocupe! Não é TÃO importante. Lembre-se de que este é apenas um ponto de partida e muitas coisas podem alterar sua TMB e seu nível de atividade.<br>"+
    "Se você está começando um novo estilo de vida, é bem provável que inclua algum tipo de aumento nos exercícios. Por esta razão, muitas pessoas acham que é melhor escolher um 'Nível de atividade' baixo, como 'Sedentário' e, em seguida, "+
    "controlar todas as calorias extras que podem queimar com exercícios (e outras atividades) usando um dos incontáveis registros / diários facilmente encontrados na internet.<br>"+
    "Isso permite que você 'coma de volta' as calorias gastas durante as atividades. Essa pode ser uma ótima maneira de se motivar ... sabendo que você pode continuar 'aumentando' seu GCD, permitindo-se comer mais (ou perder mais peso). "+
    "Então, ao calcular seu GCD inicial, basta escolher as configurações que você acha que são 'VERDADEIRAS' e com as quais você pode viver. Por que você iria querer atrapalhar sua motivação selecionando um GCD tão baixo que você se sentiria constrangido? "+
    "Você vai se descobrir ajustando esse valor à medida que avança. Quando você finalmente obtiver uma boa configuração de atividade e metodologia (fórmula TMB), poderá usá-la em cálculos futuros ... lembre-se, cada vez que perder alguns quilos, "+
    "você precisará calcular seu TDEE novamente.<br>"+
    "Um GCD para cada método individual é refletido nesta coluna enquanto a média para todos os métodos selecionados (por: 'Incluir' e 'Média (Final)') é exibida na linha inferior.</small>",

    formula_harris_benedict:"<small><p>Este é  o mais antigo conjunto de equações, originalmente publicado em 1919. Ele ilustra o quanto surgiu a diferença entre a utilização de energia por homens e mulheres ao longo dos anos."+
    " Em nossos dias modernos é muito pouca usada.<br>"+
    "Parte disso se deve às diferenças nas porcentagens de gordura corporal, mas também pode ser atribuído às percepções dominadas pelos homens da época. Já vi pessoas ainda usando essa fórmula mais antiga, embora ela tenha sido atualizada em 1984."+
    "</p><p class='align-center'><strong>Fórmulas:</strong></p>"+
    "<p><strong>Homens:</strong> (13.7516 * peso) + (5.0033 * altura) - (6.755 * idade) + 66.473</p>"+
    "<p><strong>Mulheres:</strong> (9.5634 * peso) + ( 1,8496 * altura) - (4,6756 * idade) + 655,0955</p>"+
    "Referência: <a href='https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation' target='_blank'>Wikipedia</a>.</small>",

    formula_harris_benedict_revisada:"<small><p>Mesmo que as equações tenham sido atualizadas em 1984 por Roza e Shizgal, elas ainda são consideradas desatualizadas."+
    "Muito parecido com o primeiro conjunto de fórmulas, publicado originalmente em 1919, as diferenças entre homens e mulheres são consideradas por alguns como ainda muito grandes.</p>"+
    "<p>Além disso, o gasto de energia dos humanos modernos, na maioria das opiniões, diminuiu consideravelmente."+
    " Mesmo assim, ainda existem sites que usam essas e as equações mais antigas nas calculadoras da web BMR / TDEE modernas.</p>"+
    "</p><p class='align-center'><strong>Fórmulas:</strong></p>"+
    "<p><strong>Homens:</strong> (13,397 * peso) + (4,799 * altura) - (5,677 * idade) + 88,362</p>"+
    "<p><strong>Mulheres:</strong> (9,247 * peso) + (3,098 * altura) - (4,330 * idade) + 447,593</p>"+
    "Referência: <a href='https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation' target='_blank'>Wikipedia</a>.<small>",

    formula_mifflin : "<small><p>Publicado em fevereiro de 1990, Mifflin-St Jeor é amplamente considerado como a fórmula mais precisa para calcular o gasto energético(calórico) diário em repouso(GCD -> RDEE(sigla em inglês))"+
    " e recebeu o endosso da American Dietetic Association e do American Journal of Nutrition. A maior diferença entre as fórmulas Mifflin-St Jeor e Harris-Benedict é que homens e mulheres são considerados iguais (quase). "+
    "Se você olhar as equações, verá que a única diferença é uma constante de 166 calorias. O que significa que um homem que tem a mesma altura, peso e idade que uma mulher pode supostamente comer exatamente 166 calorias a mais do que sua contraparte feminina..."+
    " se ambos estiverem tentando manter o mesmo peso corporal.</p>"+
    "<p>Você verá esse método usado na Internet na maioria das calculadoras TMB(taxa Metabólica Basal) e GCDT( Gasto Energético( calórico) Diário Total). Um grande motivo é que todas as medidas (idade, peso, altura e sexo) estão prontamente disponíveis para os usuários da Internet. "+
    "Limitações entram em jogo para idosos e certos grupos étnicos, além disso, há alguns na indústria do fitness que sentem que as fórmulas que não levam em consideração o percentual de gordura corporal são menos precisas"+
    "(veja a 'Katch-McArdle' se na primeira etapa você forneceu seu percentual(%) de gordura</p>"+
    "</p><p class='align-center'><strong>Fórmulas:</strong></p>"+
    "<p><strong>Homens:</strong> (10 * W) + (6,25 * H) - (5 * A) + 5</p>"+
    "<p><strong>Mulheres:</strong> (10 * W) + (6,25 * H) - (5 * A) - 161</p>"+
    "Referência: <a href='https://academic.oup.com/ajcn/article-abstract/51/2/241/4695104' target='_blank'>The American Journal of Clinical Nutrition</a>.<small>",

    formula_katchmcardle:"<small><p>Eles lançaram algumas publicações, incluindo o Livro: 'Essentials of Exercise Physiology', que foi publicado em 2010. Sua fórmula é considerada o mais preciso de todos os métodos por indivíduos que tem uma sólida experiência em fitness."+
    " A saber, porque leva em consideração a Massa Corporal Enxuta (MMC). As duas únicas medidas necessárias são o seu peso e a porcentagem de gordura corporal. A ciência aqui é que idade, altura e sexo não são necessários porque sua massa corporal magra "+
    "já leva isso em consideração (ou seja, as mulheres carregam naturalmente mais gordura corporal do que os homens, perdemos massa magra à medida que envelhecemos, etc.). O único problema, porém, é que a massa gorda não é contabilizada; isso pode ser devido"+
    " à crença de que o músculo consome até 30 vezes mais calorias do que a gordura.</p><p>"+
    "Leia a informação sobre '% de gordura corporal' na primeira etapa para obter mais informações.</p>"+
    "<p><strong>Fórmula:</strong>370 + (21,6 * (peso * (1 - % de gordura)))</p></small>"
}
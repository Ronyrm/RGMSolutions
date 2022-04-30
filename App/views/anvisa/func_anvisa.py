import re
from App.views.anvisa.substancias_anvisa import get_substancia_anvisa,add_substancia_anvisa
from App.views.anvisa.laboratorios_anvisa import get_laboratorio, add_laboratorio
from App.views.anvisa.classe_terapeurica_anvisa import get_classe_terapeutica, add_classe_terapeurica
from App.views.anvisa.tipos_medicamentos_anvisa import get_tipo_medicamento,add_tipo_medicamento
from App.views.anvisa.medicamentos_anvisa import get_medicamento_by_desc_and_apresentacao,add_medicamento
from App.views.anvisa.tabpreco_medicamento_anvisa import get_tabpreco_by_idmedicamento,add_tabpreco_medicamento
import pandas as pd

def verify_cp_white(campo):
    if pd.isna(campo):
        return None
    else:
        vl = re.sub('\W', '', campo)
        vl = vl.strip()
        return vl if len(vl) > 0 else None

def verify_float_none(campo):
    if pd.isna(campo):
        return None
    else:
        return  campo


def verify_cp_piscofins(campo):
    if campo == 'Positiva':
        return 'P'
    elif campo == 'Negativa':
        return 'N'
    elif campo == 'Neutra':
        return 'B'



def add_arq_csv_in_db(rowmed):

    result = True
    while result:
        # VERIFICA A SUBSTANCIA
        idsubstancia = None
        if len(rowmed[1]) > 0:
            substancia = get_substancia_anvisa(rowmed[1])
            if not substancia:
                data_result = add_substancia_anvisa(rowmed[1])
                result = data_result['result']
                if result:
                    idsubstancia = data_result['data']['id']
            else:
                idsubstancia = substancia.id

        # VERIFICA O LABORATORIOS
        idlaboratorio = None
        if len(rowmed[2]) > 0:
            laboratorio = get_laboratorio(rowmed[2],1)
            if not laboratorio:
                data_result = add_laboratorio(rowmed[3],rowmed[2])
                result = data_result['result']
                if result:
                    idlaboratorio = data_result['data']['id']
            else:
                idlaboratorio = laboratorio.id

        # VERIFICA A CLASSE TERAPEUTICA
        idclasseterapeutica = None
        if len(rowmed[11]) > 0:
            classe = get_classe_terapeutica(rowmed[11])
            if not classe:
                data_result = add_classe_terapeurica(rowmed[11])
                result = data_result['result']
                if result:
                    idclasseterapeutica = data_result['data']['id']
            else:
                idclasseterapeutica = classe.id

        #VERIFICA TIPO DE MEDICAMENTO
        idtipomedicamento = None
        if len(rowmed[12]) > 0:
            tpmed = get_tipo_medicamento(rowmed[12])
            if not tpmed:
                data_result = add_tipo_medicamento(rowmed[12])
                result = data_result['result']
                if result:
                    idtipomedicamento = data_result['data']['id']
            else:
                idtipomedicamento = tpmed.id

        #VERIFICA MEDICAMENTO
        idmedicamento = None
        if len(rowmed[9]) > 0 and len(rowmed[10]) > 0:
            medicamento = get_medicamento_by_desc_and_apresentacao(rowmed[9],rowmed[10])
            if not medicamento:
                datamed = {'descricao': rowmed[9],
                           'apresentacao': rowmed[10],
                           'idsubstancia': idsubstancia,
                           'idlaboratorio': idlaboratorio,
                           'idtipomedicamento': idtipomedicamento,
                           'idclasseterapeurica': idclasseterapeutica,
                           'ean1': verify_cp_white(rowmed[6]),
                           'ean2': verify_cp_white(rowmed[7]),
                           'ean3': verify_cp_white(rowmed[8]),
                           'codggrem': rowmed[4],
                           'registro': rowmed[5],
                           'tarja':rowmed[40]
                           }
                data_result = add_medicamento(datamed)
                result = data_result['result']
                if result:
                    idmedicamento = data_result['data']['id']
            else:
                idmedicamento = medicamento.id

        #VERIFICA TABELA DE PREÇOS
        idtabelapreco = None
        if idmedicamento:
            tabpreco = get_tabpreco_by_idmedicamento(idmedicamento)
            if not tabpreco:
                data_tabpreco = {'idmedicamento': idmedicamento,
                                 'cap': 'S' if rowmed[34] == 'Sim' else 'N',
                                 'icms0': 'S' if rowmed[36] == 'Sim' else 'N',
                                 'analise_recursal': verify_cp_white(rowmed[37]),
                                 'comercializacao2019': 'S' if rowmed[39] == 'Sim' else 'N',
                                 'confaz87': 'S' if rowmed[35] == 'Sim' else 'N',
                                 'list_piscofins': verify_cp_piscofins(rowmed[38]),
                                 'regime_preco': 'R' if rowmed[13] == 'Regulado' else 'L',
                                 'restr_hospitalar': 'S' if rowmed[33] == 'Sim' else 'N',
                                 'vl_pf0': verify_float_none(rowmed[15]),
                                 'vl_pf12': verify_float_none(rowmed[16]),
                                 'vl_pf17': verify_float_none(rowmed[17]),
                                 'vl_pf17alc': verify_float_none(rowmed[18]),
                                 'vl_pf18': verify_float_none(rowmed[21]),
                                 'vl_pf18alc': verify_float_none(rowmed[22]),
                                 'vl_pf20': verify_float_none(rowmed[23]),
                                 'vl_pf175': verify_float_none(rowmed[19]),
                                 'vl_pf175alc': verify_float_none(rowmed[20]),
                                 'vl_pfsemimposto': verify_float_none(rowmed[14]),
                                 'vl_pmc0': verify_float_none(rowmed[24]),
                                 'vl_pmc12': verify_float_none(rowmed[25]),
                                 'vl_pmc17': verify_float_none(rowmed[26]),
                                 'vl_pmc17alc': verify_float_none(rowmed[27]),
                                 'vl_pmc18': verify_float_none(rowmed[30]),
                                 'vl_pmc18alc': verify_float_none(rowmed[31]),
                                 'vl_pmc20': verify_float_none(rowmed[32]),
                                 'vl_pmc175': verify_float_none(rowmed[28]),
                                 'vl_pmc175alc': verify_float_none(rowmed[29])
                                }
                data_result = add_tabpreco_medicamento(data_tabpreco)
                result = data_result['result']
                if result:
                    idtabelapreco = data_result['data']['id']
                    print('Inserindo:'+str(idtabelapreco))
                    result = False
            else:
                result = False
        else:
            result = False
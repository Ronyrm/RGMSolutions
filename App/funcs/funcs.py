import datetime
import math
import json
import re
import decimal
import pandas as pd
# Gera chave aleatoria
def gera_keyacess(qtd=20):
    import string
    import random
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    return ''.join(random.choice(random_str) for i in range(qtd))

def gera_keyacess_pdw(qtd=6):
    import string
    import random
    random_str = string.digits
    restemp = ''.join(random.choice(random_str) for i in range(100))
    return ''.join(random.choice(restemp) for i in range(qtd))


# Funcao Retorna Idade
def retorna_idade(ano,mes,dia):
    d1 = datetime.datetime(ano,mes,dia)
    d2 = datetime.datetime.now()
    diff = d2-d1
    idade = diff.days/365
    return math.trunc(idade)


def verificexistscampjson(camp,Numeric=True):
    try:
        return camp
    except:
        if Numeric:
            return '0'
        return ''


def dt_parser(dt):
    if isinstance(dt, type(datetime)):
        return dt.isoformat()


def formatdatetime_parser(dt):
    return dt.isoformat()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def returnPagination(pagination):
    datapag = '{"nextpag":"'+str(pagination.has_next)+'","prevpag":"'+str(pagination.has_prev)+'",'
    datapag +='"nextnum": "'+str(pagination.next_num if pagination.next_num!=None else 0) +'",'
    datapag +='"pageatual": "'+str(pagination.page if pagination.page!=None else 0)+'",'
    datapag += '"totpage": "'+str(pagination.pages if pagination.pages!=None else 0)+'",'

    if pagination.per_page != None:
        datapag +='"per_page": "'+ str(pagination.per_page)+'",'
    else:
        datapag += '"per_page": "' + str(0) + '",'

    if pagination.prev_num != None:
        datapag +='"prev_num": "'+ str(pagination.prev_num)+'"}'
    else:
        datapag += '"prev_num": "' + str(0) + '"}'

    return json.loads(datapag)


def format_date_yyyymmaa(sdate):
    if len(sdate) == 10:
        dia =  sdate[0:2]
        mes = sdate[3:5]
        ano = sdate[6:10]
        return ano+'-'+mes+'-'+dia
    return None
def convert_date_int_timestamp_in_date(inttimestamp,tpcaracter):
    if tpcaracter == '-':
        return datetime.datetime.fromtimestamp(inttimestamp).strftime('%Y-%m-%d')
    elif tpcaracter == '/':
        return  datetime.datetime.fromtimestamp(inttimestamp).strftime('%d-%m-%Y')


def capture_float_in_string(str):
    return re.findall(r"[-+]?\d*\.\d+|\d+",str)

def FormatStrToFloat(sValue):
    try:    
        if sValue != None:
            return float(sValue.replace('.','').replace(',','.'))
        else:
            return None
    except:
        return None


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)
    


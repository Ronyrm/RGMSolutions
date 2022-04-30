from App import db,app
from flask import request
from App.model.tributacao.cests import Cests,SchemaCests
from App.model.tributacao.segmentos_cest import SegmentosCest
from App.model.tributacao.ncms import NCMS
from flask_paginate import get_page_args
from App.funcs.getpagination import get_pagination
import simplejson
from werkzeug.utils import secure_filename
import os
def get_SegmentosCest():
     try:
        if request.method == 'GET':
            desc= request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'


            segmentoscest = SegmentosCest.query. \
                with_entities(SegmentosCest.id,SegmentosCest.codsegmentocest,SegmentosCest.descricao).\
                filter(SegmentosCest.descricao.like('%{}%'.format(desc))).\
                paginate(page=int(page),per_page=int(per_page),error_out=False)
            if segmentoscest:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=segmentoscest.total,
                    record_name="segmentos_cest"
                )
                #segmentoscest_list = list(segmentoscest.items)
                # transforma lista em stringjson
                result = simplejson.dumps(segmentoscest.items)
                # transforma string em json
                resultjson = simplejson.loads(result)

                pages = {}
                if type(pagination.pages) is list:
                    pages = pagination.pages
                elif type(pagination.pages) is range:
                    for num in pagination.pages:
                        pages.update({num: num})

                return {'segmentos_cest': resultjson,
                        'pagination': {
                            'links': pagination.links,
                            'page': pagination.page,
                            'per_page': pagination.per_page,
                            'info': pagination.info,
                            'pages': pages,
                            'total_pages': pagination.total_pages,
                            'total': pagination.total},
                        'result': True,
                        'mensagem': 'Sucesso',
                        'desc': desc}
     except:
         pass
     return {'segmentos_cest': [], 'pagination': [], 'result': False,
             'mensagem': 'Erro ao abrir tabela de NCMS', 'desc': ''}


def get_Cests():
    try:
        if request.method == 'GET':
            desc= request.args.get('desc') if request.args.get('desc') != None else ''
            page = request.args.get('page') if request.args.get('page') != None else '1'
            per_page = request.args.get('per_page') if request.args.get('per_page') != None else '50'
            tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'
            filtercests = ''
            if tpfiltro == '0':
                filtercests = Cests.descricao.like('%'+desc+'%')
            elif tpfiltro == '1':
                filtercests = SegmentosCest.descricao.like('%' + desc + '%')
            elif tpfiltro == '2':
                filtercests = SegmentosCest.codsegmentocest==desc
            elif tpfiltro == '3':
                filtercests = NCMS.descricao.like('%'+desc + '%')
            elif tpfiltro == '4':
                filtercests = NCMS.codncm.like(desc + '%')

            cests = Cests.query.\
                join(SegmentosCest,Cests.idsegmentocest==SegmentosCest.id).\
                join(NCMS,Cests.idncm==NCMS.id).\
                filter(filtercests).\
                paginate(page=int(page),per_page=int(per_page),error_out=False)
            if cests:
                page, per_page, offset = get_page_args()
                pagination = get_pagination(
                    page=page,
                    per_page=per_page,
                    total=cests.total,
                    record_name="cests"
                )

                pages = {}
                if type(pagination.pages) is list:
                    pages = pagination.pages
                elif type(pagination.pages) is range:
                    for num in pagination.pages:
                        pages.update({num: num})

                schemacests = SchemaCests()
                tabcests = schemacests.dump(cests.items,many=True)
                return {'cests': tabcests,
                        'pagination': {
                        'links': pagination.links,
                        'page': pagination.page,
                        'per_page': pagination.per_page,
                        'info': pagination.info,
                        'pages': pages,
                        'total_pages': pagination.total_pages,
                        'total': pagination.total},
                        'result': True,
                        'mensagem': 'Sucesso',
                        'desc': desc,
                        'tpfiltro':tpfiltro}

    except:
        pass
        return {'cests': [], 'pagination': [], 'result': False,
                'mensagem': 'Erro ao abrir tabela de NCMS', 'desc': ''}


def insert_into_sql(table):

    if request.method == 'POST':
        if 'file_sql' in request.files:
            file_sql = request.files['file_sql']
            #file_sql = file_sql.split('\n')

        if file_sql:
            try:
                filename = secure_filename(file_sql.filename)
                localesave = app.config['UPLOAD_FOLDER']

                spath = os.path.join(localesave, filename)

                if os.path.exists(spath):
                    os.remove(spath)

                file_sql.save(spath)
            except:
                return {'mensagem':f'Erro ao tentar salvar o arquivo {filename} no servidor',
                        'result':False,
                        'data':{}}

            tb = table.query.all()
            if not tb:
                try:
                    from App.funcs.migrate_sql import insert_data_script_sql
                    insert_data_script_sql(spath)
                    os.remove(spath)
                except:
                    return {'mensagem': f'Erro ao inserir sql no banco de dados',
                            'result': True,
                            'data':{}}

                db.session.commit()
                tb = table.query.all()


                # transforma lista em stringjson
                result = simplejson.dumps(tb)
                # transforma string em json
                resultjson = simplejson.loads(result)
                return {'mensagem': f'Dados Inseridos com sucesso',
                        'result': True,
                        'data': result}

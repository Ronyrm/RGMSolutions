from App import db,app
from App.model.tributacao.cst_icms import CST_Icms,SchemaCSTICMS
from flask import request,render_template,jsonify
from werkzeug.utils import secure_filename
import os
def get_cst_icms():
    try:
        desc = ''
        tpfiltro = '0'

        if request.method == 'GET':
            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'

        filtro = CST_Icms.descricao.like('%' + desc + '%')
        if tpfiltro == '1':
            filtro = CST_Icms.codcsticms == desc

        result = CST_Icms.query.filter(filtro).all()
        return result

    except:
        return None
        #return render_template('layouts/tributacao/csticms/main.html',csticms=[],result=False)

def insert_into():
    if request.method == 'POST':
        if 'file_sql' in request.files:
            file_sql = request.files['file_sql']

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

            csticms = get_cst_icms()

            if not csticms:
                try:
                    from App.funcs.migrate_sql import insert_data_script_sql
                    insert_data_script_sql(spath)
                    os.remove(spath)
                except:
                    return {'mensagem': f'Erro ao inserir sql no banco de dados',
                            'result': True,
                            'data':{}}

                db.session.commit()
                csticms = get_cst_icms()
                schemacsticms = SchemaCSTICMS()


                return {'mensagem': f'Dados Inseridos com sucesso',
                        'result': True,
                        'data': schemacsticms.dump(csticms,many=True)}
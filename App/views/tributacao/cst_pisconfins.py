from App import db, app
from App.model.tributacao.cst_piscofins import CST_PisCofins, SchemaCSTPisCofins
from flask import request, render_template, jsonify
from werkzeug.utils import secure_filename
import os


def get_cst_piscofins():
    try:
        desc = ''
        tpfiltro = '0'

        if request.method == 'GET':
            desc = request.args.get('desc') if request.args.get('desc') != None else ''
            tpfiltro = request.args.get('tpfiltro') if request.args.get('tpfiltro') != None else '0'

        filtro = CST_PisCofins.descricao.like('%' + desc + '%')
        if tpfiltro == '1':
            filtro = CST_PisCofins.codcstipi == desc

        result = CST_PisCofins.query.filter(filtro).all()
        return result

    except:
        return None


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
                return {'mensagem': f'Erro ao tentar salvar o arquivo {filename} no servidor',
                        'result': False,
                        'data': {}}

            cstpiscofins = get_cst_piscofins()

            if not cstpiscofins:
                try:
                    from App.funcs.migrate_sql import insert_data_script_sql
                    insert_data_script_sql(spath)
                    os.remove(spath)
                except:
                    return {'mensagem': f'Erro ao inserir sql no banco de dados',
                            'result': True,
                            'data': {}}

                db.session.commit()
                cstipi = get_cst_piscofins()
                schemacstpiscofins = SchemaCSTPisCofins()

                return {'mensagem': f'Dados Inseridos com sucesso',
                        'result': True,
                        'data': schemacstpiscofins.dump(cstipi, many=True)}
from App import db,app
from App.model.packagetrack import PackageTrack
from flask import request,render_template,jsonify,redirect,url_for
from App.schema.schema import PackageTrackSchema
from flask_login import LoginManager,current_user
from App.model.atleta import Atleta

login_manager = LoginManager()
#login_manager.login_view = 'routesatleta.get_mainatleta'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Atleta.query.get(int(user_id))


def get_main_package_track(pessoa):
    print(current_user)
    if current_user.is_authenticated:
        return render_template('layouts/pessoas/package_tracker/main.html', idpessoa=current_user.idpessoa)
    else:
        return redirect(url_for('routesatleta.get_mainatleta'))


def get_package_track_pessoa(idpessoa,status):
    try:
        from sqlalchemy import and_
        if status.upper() !='W':
            packs = PackageTrack.query.filter(and_(PackageTrack.idpessoa == idpessoa,PackageTrack.status==status))
        else:
            packs = PackageTrack.query.filter(PackageTrack.idpessoa == idpessoa)
        from App.views.several import search_tracker_correios

        #ATUALIZA STATUS DO RASTREIO
        for pack in packs:
            if pack.status != 'E':
                search_tracker_correios(pack.codigo)
        return packs
    except:
        return None

def get_package_track_codigo(codigo):
    try:
        pack = PackageTrack.query.filter(PackageTrack.codigo == codigo).one()
        return pack
    except:
        return None

def update_status_track(codigo,status):
    try:
        pack = get_package_track_codigo(codigo)
        if pack:
            pack.status = status
            db.session.commit()
    except:
        pass

def add_update_pack_track():
    msg='Erro, ao cadatrar código, tente novamente mais tarde!'
    if request.method == 'POST':
        data = request.form
        idpessoa = data['edtidpessoa']
        codigo = data['edtcodigo']
        descricao = data['edtdescricao']
        status = data['edtstatus']
        idpacktracker = data['edtidpacktracker']
        if idpacktracker == '-1':
            packtemp = get_package_track_codigo(codigo)
            if packtemp:
                msg = 'Código ja cadastrado no sistema com a Descrição:'+packtemp.descricao;
                return {'result': False, 'data': {}, 'mensagem': msg}

            pack = PackageTrack(idpessoa=idpessoa,codigo=codigo,
                                descricao=descricao,status=status)
            db.session.add(pack)
        else:

            pack = get_package_track_codigo(idpacktracker)
            if pack:
                pack.codigo = codigo
                pack.descricao = descricao

        db.session.commit()
        packschema = PackageTrackSchema()
        acao = ' cadastrado' if idpacktracker == '-1' else ' altertado '
        msg = 'Código: '+codigo+acao+' com sucesso!'
        result = packschema.dump(pack)
        return {'result': True, 'data': result,'mensagem':msg}
    return {'result': False, 'data': {},'mensagem':msg}
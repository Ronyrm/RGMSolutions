# atualiza banco de dados 
# flask db migrate -m "add tab fiisdatahora"
# flask db upgrade

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from googletrans import Translator
from sqlalchemy import create_engine
from flask_login import LoginManager,current_user

db = SQLAlchemy()
migrate = Migrate()
translator = Translator()
login_manager = LoginManager()

def create_app():
    print('entrei')
    app = Flask(__name__)
    
    # Configuração do banco
    app.config.from_object('config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    login_manager.init_app(app)
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Conexão bruta opcional
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # Importa models
    from App.model.atleta import Atleta
    
    # Registra blueprints
    register_blueprints(app)

    # Cria tabelas caso não existam
    with app.app_context():
        db.create_all()

        # Atualiza triggers
        #from App.funcs.migrate_sql import migrate_trigger
        #migrate_trigger()

    return app


def register_blueprints(app):
    from App.routes.main import main
    app.register_blueprint(main)

    from App.routes.auth import auth
    app.register_blueprint(auth)

    from App.routes.routestabalimentos import routestabalimentos
    app.register_blueprint(routestabalimentos)

    from App.routes.routesrefeicao import routesrefeicao
    app.register_blueprint(routesrefeicao)

    from App.routes.routesdieta import routesdieta
    app.register_blueprint(routesdieta)

    from App.routes.routescliente import routesclientes
    app.register_blueprint(routesclientes)

    from App.routes.routesitemdieta import routesitemdieta
    app.register_blueprint(routesitemdieta)

    from App.routes.produtos.routesproduct import routesproduct
    app.register_blueprint(routesproduct)

    from App.routes.produtos.routesgroupproducts import routesgroupproducts
    app.register_blueprint(routesgroupproducts)

    from App.routes.routespessoa import routespessoa
    app.register_blueprint(routespessoa)

    from App.routes.routesvendedor import routesvendedores
    app.register_blueprint(routesvendedores)

    from App.routes.routesusers import routes
    app.register_blueprint(routes)

    from App.routes.routesunalimento import routesunalimentos
    app.register_blueprint(routesunalimentos)

    from App.routes.routesmetaatleta import routesmetaatleta
    app.register_blueprint(routesmetaatleta)

    from App.routes.routesmagazine import routesmagazine
    app.register_blueprint(routesmagazine)

    from App.routes.routesatleta import routesatleta
    app.register_blueprint(routesatleta)

    from App.routes.routesmensagewhatsapp import routesmensagewhatsapp
    app.register_blueprint(routesmensagewhatsapp)

    from App.routes.routesseveral import routesseveral
    app.register_blueprint(routesseveral)

    from App.routes.routespackagetrack import routespackagetrack
    app.register_blueprint(routespackagetrack)

    from App.routes.localidades.routesregiao import routesregiao
    app.register_blueprint(routesregiao)

    from App.routes.localidades.routesuf import routesuf
    app.register_blueprint(routesuf)

    from App.routes.localidades.routesmesoregiao import routesmesoregiao
    app.register_blueprint(routesmesoregiao)

    from App.routes.localidades.routesmicroregiao import routesmicroregiao
    app.register_blueprint(routesmicroregiao)

    from App.routes.localidades.routes_add_update_IBGE import routesIBGE
    app.register_blueprint(routesIBGE)

    from App.routes.localidades.routescidades import routescidades
    app.register_blueprint(routescidades)

    from App.routes.routesenderecos import routesenderecos
    app.register_blueprint(routesenderecos)

    from App.routes.pandas.routespandas import routespandas
    app.register_blueprint(routespandas)

    from App.routes.pandas.routeschedules import routesschedules
    app.register_blueprint(routesschedules)

    from App.routes.tributacao.routesncms import routesncms
    app.register_blueprint(routesncms)

    from App.routes.tributacao.routescst import routescst
    app.register_blueprint(routescst)

    from App.routes.tributacao.routescests import routescests
    app.register_blueprint(routescests)

    from App.routes.tributacao.routescfops import routescfops
    app.register_blueprint(routescfops)

    from App.routes.tributacao.routesreinfs import routesreinfs
    app.register_blueprint(routesreinfs)

    from App.routes.anvisa.routesanvisa import routesanvisa
    app.register_blueprint(routesanvisa)

    from App.routes.covid.routescovid import routescovid
    app.register_blueprint(routescovid)

    from App.routes.bolsavalores.routessubsetorbolsa import routessubsetorbolsa
    app.register_blueprint(routessubsetorbolsa)

    from App.routes.bolsavalores.routessetorbolsa import routessetorbolsa
    app.register_blueprint(routessetorbolsa)

    from App.routes.bolsavalores.routesempresabolsa import routesempresabolsa
    app.register_blueprint(routesempresabolsa)

    from App.routes.bolsavalores.routescotacoesbolsa import routescotacoesbolsa
    app.register_blueprint(routescotacoesbolsa)

    from App.routes.bolsavalores.routesdividendosbolsa import routesdividendosbolsa
    app.register_blueprint(routesdividendosbolsa)

    from App.routes.bolsavalores.routespricescotacaobolsa import routespricescotacaobolsa
    app.register_blueprint(routespricescotacaobolsa)

    from App.routes.bolsavalores.routesbalancopatrimonial import routesbalancopatrimonial
    app.register_blueprint(routesbalancopatrimonial)

    from App.routes.bolsavalores.routesbalancofinancas import routesbalancofinancas
    app.register_blueprint(routesbalancofinancas)

    from App.routes.mercadopago.mercadopago import routemercadopago
    app.register_blueprint(routemercadopago)

    from App.routes.bolsavalores.routesfiis import routesfiis
    app.register_blueprint(routesfiis)


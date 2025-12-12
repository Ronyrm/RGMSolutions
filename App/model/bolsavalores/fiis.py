from App import db
from sqlalchemy import Column, String, Float, Integer,Date,Time
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#from App.model.users import SchemaUser

class Fiis(db.Model):
    __tablename__ = 'fiis'
    ticker = Column(String(20), primary_key=True)
    preco = Column(Float)
    ultimo_dividendo = Column(Float)
    dy = Column(Float)
    valor_patrimonial_cota = Column(Float)
    p_vp = Column(Float)
    liquidez_media_diaria = Column(Float)
    percentual_caixa = Column(Float)
    cagr_dividendos_3a = Column(Float)
    cagr_valor_cota_3a = Column(Float)
    patrimonio = Column(Float)
    n_cotistas = Column(Integer)
    gestao = Column(String(20))
    n_cotas = Column(Integer)

class ShemaFiis(SQLAlchemyAutoSchema):
    class Meta:
        model = Fiis

# ----------------------- FIIS DATA E HORA ATUAL ARMAZENA VALORES ATRAVES DO GET DA PAGINA STATUS INVEST
class FiisDataHora(db.Model):
   __tablename__ = 'fiisdatahora' 
   ticker = Column(String(20),db.ForeignKey('fiis.ticker'), primary_key=True,nullable=False) 
   data_movimentacao = Column(Date,primary_key=True,nullable=False)
   hora_movimentacao = Column(Time,primary_key=True,nullable=False)
   valor_cotacao = Column(Float)
   fii = db.relationship('Fiis')

class SchemaFiisDataHora(SQLAlchemyAutoSchema):
    class Meta:
        model = FiisDataHora
    fii = fields.Nested("ShemaFiis")

# --------------- CARTEIRA DE FIIS DO USUÁRIO -----------
from App.model.users import Users

class SchemaUserFiis(SQLAlchemyAutoSchema):
    class Meta:
        model = Users



class CarteiraFiis(db.Model):
    __tablename__ = 'carteirafiis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20),db.ForeignKey('fiis.ticker'), nullable=False) 
    iduser = Column(Integer,db.ForeignKey('users.id')      ,nullable=False) 
    fii = db.relationship('Fiis')
    user = db.relationship('Users')
    
class SchemaCarteiraFiis(SQLAlchemyAutoSchema):
    class Meta:
        model = CarteiraFiis 
    fii = fields.Nested("ShemaFiis")
    user = fields.Nested("SchemaUserFiis")



class ComprasFiis(db.Model):
    __tablename__ = 'comprasfiis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idcarteirafiis = Column(Integer,db.ForeignKey('carteirafiis.id'),nullable=False) 
    data = Column(Date,nullable=False)
    valorcota = Column(Float)
    quantidade = Column(Integer)
    total = Column(Float)
    carteirafiis = db.relationship('CarteiraFiis')



class SchemaComprasFiis(SQLAlchemyAutoSchema):
    class Meta:
        model = ComprasFiis
    carteirafiis = fields.Nested("SchemaCarteiraFiis")
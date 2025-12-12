from App import db
import datetime

class Metaatleta(db.Model):
    __tablename__ = 'metaatleta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    pesoinicial = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    pesofinal = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    percentual_gordura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    nivelatividade = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    # 0-Harris Benedict Original 1-Harris Benedict Revisada 2-Mifflin St Jeor 3-Katch-McArdle
    frmharrisbenedictoriginal = db.Column(db.String(1), nullable=False)
    frmharrisbenedictrevisada = db.Column(db.String(1), nullable=False)
    frmmifflin = db.Column(db.String(1), nullable=False)
    frmkatch = db.Column(db.String(1), nullable=False)
    valtmb = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=0))
    valgcd = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=0))
    # P-perda de peso G-ganho de peso
    tipometa = db.Column(db.String(1), nullable=False)
    valtotkclmeta = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=0))
    valtotkclexercicio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=0))
    valalvocalorico = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=0))

    # Proteina
    percproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valkcalproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgramasproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgrkgproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    # Carboidrato
    perccarb = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valkcalcarb = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgramascarbo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgrkgcarbo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    # Gordura
    percfat = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valkcalfat = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgramasgordura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    valgrkggordura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    # A-Aberto F-Fechada
    status = db.Column(db.String(1), nullable=False)
    idatleta = db.Column(db.Integer, db.ForeignKey('atleta.id',ondelete='CASCADE'))
    atleta = db.relationship("Atleta", back_populates="metaatleta")
    totaldiasprevisto = db.Column(db.Integer)
    dataprevisaofinal = db.Column(db.DateTime)
    datafinalizada = db.Column(db.DateTime)
    pesofinalizado = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#from App.model.atleta import SchemaAtletas

#class SchemaMetaAtletas(SQLAlchemyAutoSchema):
    #class Meta:
        #model = Metaatleta
    #atleta = fields.Nested(SchemaAtletas)

from App import db
from flask_login import UserMixin
import datetime

class Atleta(UserMixin,db.Model):
    __tablename__ = 'atleta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    dtnascimento = db.Column(db.DateTime, nullable=True)
    peso = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    altura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))
    genero = db.Column(db.String(1), nullable=True)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id',ondelete='CASCADE'))
    pessoa = db.relationship("Pessoa", back_populates="atleta")
    metaatleta = db.relationship('Metaatleta',back_populates="atleta")
    bloqueado = db.Column(db.String(1), nullable=True)
    keyacess = db.Column(db.String(100), nullable=True)

    percfat = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=2))

    phone = db.Column(db.String(20))
    profilenamephone = db.Column(db.String(20))

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#from App.model.pessoas.pessoa import SchemaPessoas
#class SchemaAtletas(SQLAlchemyAutoSchema):
    #class Meta:
        #model = Atleta
    #pessoa = fields.Nested(SchemaPessoas)
    #metaatleta = fields.Nested(SchemaMetaAtletas)


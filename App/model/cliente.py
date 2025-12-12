from App import db
import datetime


class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rg = db.Column(db.String(20))
    titulo = db.Column(db.String(20))
    orgaoemissor = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    datacadastro = db.Column(db.DateTime, default=datetime.datetime.now())
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
    pessoa = db.relationship("Pessoa", back_populates="cliente")

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#from App.model.pessoas.pessoa import SchemaPessoas
#class SchemaClientes(SQLAlchemyAutoSchema):
    #class Meta:
     #   model = Cliente
    #pessoa = fields.Nested("SchemaPessoas")

#from App.model.pessoas.pessoa import Pessoa
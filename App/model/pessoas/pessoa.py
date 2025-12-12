from App import db
import datetime


class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30))
    nome = db.Column(db.String(70))
    razaosocial = db.Column(db.String(70))
    tipopessoa = db.Column(db.String(2), nullable=False)
    password = db.Column(db.String(200))
    email = db.Column(db.String(60))

    refeicao = db.relationship('Refeicao', back_populates="pessoa")
    cliente = db.relationship("Cliente", back_populates="pessoa")
    atleta = db.relationship("Atleta", back_populates="pessoa")
    #mensagewhatsapp = db.relationship("MensageWhatsApp", back_populates="pessoa")
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    phone = db.Column(db.String(20))
    profilenamephone = db.Column(db.String(20))


#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#from App.model.refeicao import SchemaRefeicao
#class SchemaPessoas(SQLAlchemyAutoSchema):
    #class Meta:
        #model = Pessoa
    #refeicao = fields.Nested("SchemaRefeicao")
    #cliente = fields.Nested("SchemaClientes")
    #atleta = fields.Nested("SchemaAtletas")
    

#pessoa_schema = SchemaPessoas()
#pessoas_schema = SchemaPessoas(many=True)
#from App.model.cliente import Cliente


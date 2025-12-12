from App import db


class Refeicao(db.Model):
    __tablename__ = 'refeicao'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.Time)
    mostrar = db.Column(db.String(1))
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id',ondelete='CASCADE'))
    pessoa = db.relationship("Pessoa", back_populates="refeicao")

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields

#class SchemaRefeicao(SQLAlchemyAutoSchema):
    #class Meta:
        #model = Refeicao
    #pessoa = fields.Nested('SchemaPessoas')




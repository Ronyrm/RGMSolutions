from App import db
from marshmallow_sqlalchemy import ModelSchema

class TiposMedicamentos_anvisa(db.Model):
    __tablename__ = 'tiposmedicamentos_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(500), nullable=False)

class SchemaTiposMedicamentos_anvisa(ModelSchema):
    class Meta:
        model = TiposMedicamentos_anvisa

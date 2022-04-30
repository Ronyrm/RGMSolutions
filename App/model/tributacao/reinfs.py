from App import db
from marshmallow_sqlalchemy import ModelSchema

class REINFs(db.Model):
    __tablename__ = 'reinfs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codreinf = db.Column(db.String(9))
    descricao = db.Column(db.String(100), nullable=False)

class SchemaREINFs(ModelSchema):
    class Meta:
        model = REINFs
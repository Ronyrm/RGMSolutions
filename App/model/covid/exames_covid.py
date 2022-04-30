from App import db
from marshmallow_sqlalchemy import ModelSchema


class Exames_covid(db.Model):
    __tablename__ = 'exames_covid'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)


class SchemaExames(ModelSchema):
    class Meta:
        model = Exames_covid
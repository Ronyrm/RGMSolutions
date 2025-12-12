from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class CST_Icms(db.Model):
    __tablename__ = 'cst_icms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codcsticms = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    optantesimplesnacional =  db.Column(db.String(1))

class SchemaCSTICMS(SQLAlchemyAutoSchema):
    class Meta:
        model = CST_Icms
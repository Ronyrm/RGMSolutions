from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class CST_Ipi(db.Model):
    __tablename__ = 'cst_ipi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codcstipi = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    tipomov =  db.Column(db.String(1))

class SchemaCSTIpi(SQLAlchemyAutoSchema):
    class Meta:
        model = CST_Ipi
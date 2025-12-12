from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class CST_PisCofins(db.Model):
    __tablename__ = 'cst_piscofins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codcstpiscofins = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    tipomov =  db.Column(db.String(1))

class SchemaCSTPisCofins(SQLAlchemyAutoSchema):
    class Meta:
        model = CST_PisCofins
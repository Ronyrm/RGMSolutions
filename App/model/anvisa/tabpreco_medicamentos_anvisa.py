from App import db
from marshmallow_sqlalchemy import ModelSchema,fields
from App.model.anvisa.medicamentos_anvisa import SchemaMedicamentos_anvisa

class TabPrecoMedicamentos_anvisa(db.Model):
    __tablename__ = 'tabpreco_medicamentos_anvisa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    regime_preco = db.Column(db.String(1)) # R - Regulado | L - Liberado
    vl_pfsemimposto = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf0 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf12 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf17 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf17alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf175 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf175alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf18 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf18alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pf20 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc0 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc12 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc17 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc17alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc175 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc175alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc18 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc18alc = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vl_pmc20 = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    restr_hospitalar = db.Column(db.String(1)) # S - Sim | N -Na0
    cap = db.Column(db.String(1)) # S - Sim | N -Na0
    confaz87 = db.Column(db.String(1)) # S - Sim | N -Na0
    icms0 = db.Column(db.String(1)) # S - Sim | N -Na0
    analise_recursal = db.Column(db.String(5))
    list_piscofins = db.Column(db.String(1)) # P - Positiva | N - Negativa
    comercializacao2019 = db.Column(db.String(1)) # S - Sim | N -Na0

    idmedicamento = db.Column(db.Integer, db.ForeignKey('medicamentos_anvisa.id'))
    medicamento = db.relationship("Medicamentos_anvisa")

class SchemaTabPrecoMedicamentos_anvisa(ModelSchema):
    class Meta:
        model = TabPrecoMedicamentos_anvisa

    medicamento = fields.Nested(SchemaMedicamentos_anvisa)

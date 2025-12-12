from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


from App.model.localidades.regiao import Regiao
class RegiaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Regiao

from App.model.localidades.uf import UF
class UfSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UF
    regiao = fields.Nested(RegiaoSchema)


from App.model.localidades.mesoregiao import MesoRegiao
class MesoRegiaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MesoRegiao
    uf = fields.Nested(UfSchema)

from App.model.localidades.microregiao import MicroRegiao
class MicroRegiaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicroRegiao
    mesoregiao = fields.Nested(MesoRegiaoSchema)


from App.model.localidades.cidades import Cidades
class CidadesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cidades
    microregiao = fields.Nested(MicroRegiaoSchema)
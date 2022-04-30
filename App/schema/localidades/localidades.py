from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


from App.model.localidades.regiao import Regiao
class RegiaoSchema(ModelSchema):
    class Meta:
        model = Regiao

from App.model.localidades.uf import UF
class UfSchema(ModelSchema):
    class Meta:
        model = UF
    regiao = fields.Nested(RegiaoSchema)


from App.model.localidades.mesoregiao import MesoRegiao
class MesoRegiaoSchema(ModelSchema):
    class Meta:
        model = MesoRegiao
    uf = fields.Nested(UfSchema)

from App.model.localidades.microregiao import MicroRegiao
class MicroRegiaoSchema(ModelSchema):
    class Meta:
        model = MicroRegiao
    mesoregiao = fields.Nested(MesoRegiaoSchema)


from App.model.localidades.cidades import Cidades
class CidadesSchema(ModelSchema):
    class Meta:
        model = Cidades
    microregiao = fields.Nested(MicroRegiaoSchema)
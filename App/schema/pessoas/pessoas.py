from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from App.schema.localidades.localidades import CidadesSchema
# Esquema Endereço
from App.model.pessoas.enderecos import Enderecos
class EnderecosSchema(ModelSchema):
    class Meta:
        model = Enderecos
    cidade = fields.Nested(CidadesSchema)

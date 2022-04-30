from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from App.model.pandas.schedules import Schedules
from App.schema.localidades.localidades import CidadesSchema
class SchedulesSchema(ModelSchema):
    class Meta:
        model = Schedules
    cidade = fields.Nested(CidadesSchema)
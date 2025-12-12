from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.model.pandas.schedules import Schedules
from App.schema.localidades.localidades import CidadesSchema
class SchedulesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Schedules
    cidade = fields.Nested(CidadesSchema)
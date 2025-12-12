from App import db
from App.model.bolsavalores.fiis import ComprasFiis,CarteiraFiis,SchemaComprasFiis
from App.model.users import Users

def GetComprasFiisByCarteira(vIdCarteira):
    comprasfii =   ComprasFiis.query.filter_by(idcarteirafiis=vIdCarteira).all()
    schema = SchemaComprasFiis()
    return {"comprasfii":schema.dump(comprasfii,many=True)}

def GetComprasFiisByUser(vIdUser):
    compras = (
        db.session.query(ComprasFiis)
        .join(CarteiraFiis,ComprasFiis.idcarteirafiis == CarteiraFiis.id)
        .join(Users,CarteiraFiis.iduser==Users.id)
        .filter(Users.id==vIdUser).all()
    )
    schema = SchemaComprasFiis()
    return {"comprasfii":schema.dump(compras,many=True)}



from App.model.bolsavalores.fiis import CarteiraFiis,SchemaCarteiraFiis

def GetCarteiraFiisByuser(vIdUser):
    carteira =   CarteiraFiis.query.filter_by(iduser=vIdUser).all()
    schema = SchemaCarteiraFiis(
        only= ("fii.ticker",
               "fii.preco",
               "fii.dy"

        )
    )
    return {"carteirafiis":schema.dump(carteira,many=True)}
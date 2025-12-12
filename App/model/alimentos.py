from App import db


class Alimentos(db.Model):
    __tablename__ = 'alimentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)
    umidades = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    calorias = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    joule = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    proteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    lipidios = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    colesterol = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    carboidrato = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    fibras = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    cinzas = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    calcio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    magnesio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    manganes = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    fosforo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    ferro = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    sodio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    potasio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    cobre = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    zinco = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    retinol = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    re = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    rae = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    tiamina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    riboflavina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    piridoxina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    niacina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    vitaminac = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    qtdgramasemcima = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id',ondelete='CASCADE'))
    pessoa = db.relationship("Pessoa")
    idunalimento = db.Column(db.Integer, db.ForeignKey('unidademedidaalimento.id'))
    unalimento = db.relationship("Unalimento")


    def __init__(self, descricao, umidades, calorias, joule, proteina, lipidios, colesterol, carboidrato, fibras,
                 cinzas, calcio, magnesio, manganes, fosforo, ferro, sodio, potasio, cobre, zinco, retinol,re,
                 rae, tiamina, riboflavina, piridoxina, niacina, vitaminac, qtdgramasemcima,idpessoa,idunalimento):

        self.descricao = descricao
        self.umidades = umidades
        self.calorias = calorias
        self.joule = joule
        self.proteina = proteina
        self.lipidios = lipidios
        self.colesterol = colesterol
        self.carboidrato = carboidrato
        self.fibras = fibras
        self.cinzas = cinzas
        self.calcio = calcio
        self.magnesio = magnesio
        self.manganes = manganes
        self.fosforo = fosforo
        self.ferro = ferro
        self.sodio = sodio
        self.potasio = potasio
        self.cobre = cobre
        self.zinco = zinco
        self.retinol = retinol
        self.re = re
        self.rae = rae
        self.tiamina = tiamina
        self.riboflavina = riboflavina
        self.piridoxina = piridoxina
        self.niacina = niacina
        self.vitaminac = vitaminac
        self.qtdgramasemcima = qtdgramasemcima
        self.idpessoa = idpessoa
        self.idunalimento=idunalimento

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
#class SchemaAlimentos(SQLAlchemyAutoSchema):
#    class Meta:
#        model = Alimentos
    #unalimento = fields.Nested('SchemaUnAlimentos')
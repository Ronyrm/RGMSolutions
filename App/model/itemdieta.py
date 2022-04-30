from App import db

class ItemDieta(db.Model):
    __tablename__ = 'itemdieta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantgramas = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalcarbo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalgordura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalsodio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalfibras = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalcalorias = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    iddieta = db.Column(db.Integer, db.ForeignKey('dieta.id',onupdate='CASCADE',ondelete="CASCADE"))
    idalimento = db.Column(db.Integer, db.ForeignKey('alimentos.id',onupdate='CASCADE',ondelete="CASCADE"))
    dieta =  db.relationship('Dieta')
    alimento = db.relationship('Alimentos')
from App import db
import datetime


class Dieta(db.Model):
    __tablename__ = 'dieta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False, unique=True)
    data = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    mesano = db.Column(db.String(8), nullable=False)
    totalcarbo = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalproteina = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalgordura = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalfibras = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalsodio = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    totalcalorias = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    idrefeicao = db.Column(db.Integer, db.ForeignKey('refeicao.id'))
    idmetaatleta = db.Column(db.Integer, db.ForeignKey('metaatleta.id'))
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    dieta_refeicao = db.relationship('Refeicao')
    metaatleta = db.relationship('Metaatleta')
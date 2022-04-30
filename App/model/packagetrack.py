from App import db
from flask_login import UserMixin
import datetime

class PackageTrack(UserMixin,db.Model):
    __tablename__ = 'packagetrack'

    codigo = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    descricao = db.Column(db.String(50), nullable=True)
    date_lanc = db.Column(db.Date, default=datetime.datetime.now())
    status = db.Column(db.String(1), nullable=False)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id', ondelete='CASCADE'))
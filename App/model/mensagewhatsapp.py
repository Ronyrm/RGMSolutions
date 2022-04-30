from App import db
import datetime
class MensageWhatsApp(db.Model):
    __tablename__ = 'mensagewhatsapp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pergunta = db.Column(db.String(500), nullable=False)
    proceed = db.Column(db.String(1), default='N')
    resposta = db.Column(db.String(500), nullable=False)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id', ondelete='CASCADE'))
    data = db.Column(db.DateTime,default=datetime.datetime.now())
    etapa = db.Column(db.Integer)
    menu = db.Column(db.Integer, default=0)
    submenu = db.Column(db.Integer, default=0)
    etapamenu = db.Column(db.String(50))
    #pessoa = db.relationship("Pessoa", back_populates="mensagewhatsapp")
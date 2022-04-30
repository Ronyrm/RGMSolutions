from App import db
import datetime


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False, unique=False)
    subdescricao = db.Column(db.String(50), nullable=False, unique=False)
    create_on = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    estoquemin = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    estoqueatual = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    precocusto = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    margemlucro = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    precovenda = db.Column(db.NUMERIC(precision=8, asdecimal=False, scale=3))
    caminhoimg = db.Column(db.String(50), nullable=False, unique=False)
    idgrupoproduto = db.Column(db.Integer, db.ForeignKey('grupoprodutos.id'))
    idtribestadual = db.Column(db.Integer)
    produto_grupo = db.relationship('GroupProducts')

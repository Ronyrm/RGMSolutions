from App import db

class Enderecos(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.Integer)  # 0 - Comercial, 1 - Entrega, 2 - Cobrança, 3 - Residencial, 4 - Rural
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id', ondelete='CASCADE'))
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(100))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    numero = db.Column(db.String(5))
    localidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    padrao = db.Column(db.String(1), default='N') # Endereço Principal S-Sim ou N-Nao

    idcidade = db.Column(db.Integer, db.ForeignKey('cidades.id'))
    cidade = db.relationship("Cidades")


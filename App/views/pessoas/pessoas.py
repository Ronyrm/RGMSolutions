from App.model.pessoas.pessoa import  Pessoa
from App.schema.schema import PessoaClienteRefeicoesSchema


def get_byemailpessoa(email,tipopessoa):
    try:
        from sqlalchemy import and_
        pessoa = Pessoa.query.filter(and_(Pessoa.email == email,Pessoa.tipopessoa==tipopessoa)).all()
        return pessoa
    except:
        return None



def get_byusernamepessoa(username):
    try:
        pessoa = Pessoa.query.filter(Pessoa.username == username).one()
        return pessoa
    except:
        return None

def get_byid(id):
    pessoaschema = PessoaClienteRefeicoesSchema()
    pessoa = Pessoa.query.get(id)
    result = pessoaschema.dump(pessoa)
    return result

def get_pessoa_by_phone(phone):
    phone2 = phone[2:len(phone)-1]
    try:
        from sqlalchemy import  or_
        return  Pessoa.query.filter(or_(Pessoa.phone==phone,Pessoa.phone==phone2)).one()
    except:
        return None


from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


from App.model.pessoas.pessoa import Pessoa
from App.model.cliente import Cliente
from App.model.refeicao import Refeicao
from App.model.dieta import Dieta
from App.model.itemdieta import ItemDieta
from App.model.produtos.products import Product
from App.model.produtos.groupproducts import GroupProducts
from App.model.vendedor import Vendedor
from App.model.users import Users
from App.model.alimentos import Alimentos
from App.model.atleta import Atleta
from App.model.metaatleta import Metaatleta
from App.model.unalimento import Unalimento
from App.model.mensagewhatsapp import MensageWhatsApp
from App.model.packagetrack import PackageTrack

class GroupProductsSchema(ModelSchema):
    class Meta:
        model = GroupProducts


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
    produto_grupo = fields.Nested(GroupProductsSchema)



class PessoaSchema(ModelSchema):
    class Meta:
        model = Pessoa

class ClienteSchema(ModelSchema):
    class Meta:
        model = Cliente
    pessoa = fields.Nested("PessoaSchema")


class VendedorSchema(ModelSchema):
    class Meta:
        model = Vendedor
    pessoa = fields.Nested("PessoaSchema")

class UsersSchema(ModelSchema):
    class Meta:
        model = Users


class RefeicaoSchema(ModelSchema):
    class Meta:
        model = Refeicao
    #pessoa = fields.Nested(PessoaSchema)

class UnAlimentoSchema(ModelSchema):
    class Meta:
        model = Unalimento

class AlimentoSchema(ModelSchema):
    class Meta:
        model = Alimentos

    unalimento = fields.Nested(UnAlimentoSchema)

class ItemDietaSchema(ModelSchema):
    class Meta:
        model = ItemDieta
    #dieta = fields.Nested('DietaSchema',only=('id','descricao','data',))
    alimento = fields.Nested('AlimentoSchema',only=('id','descricao','unalimento'))


class PessoaSchema(ModelSchema):
    class Meta:
        model = Pessoa
    cliente = fields.Nested(ClienteSchema,many=True)
    refeicao =fields.Nested(RefeicaoSchema,many=True)

class PessoaClienteRefeicoesSchema(ModelSchema):
    class Meta:
        model = Pessoa

    refeicao = fields.Nested(RefeicaoSchema(many=True),exclude=('pessoa',),dump_only=True)
    cliente  = fields.Nested(ClienteSchema(many=True),exclude=('pessoa',),dump_only=True)


class ClienteFoodsschema(ModelSchema):
    class Meta:
       model = Cliente

class ClientePessoaschema(ModelSchema):
    class Meta:
        model = Pessoa
    cliente = fields.Nested(ClienteFoodsschema,many=True,only=('id','cpf'))


class UnFoodsSchema(ModelSchema):
    class Meta:
        model = Unalimento


class FoodsSchema(ModelSchema):
    class Meta:
        model = Alimentos

    pessoa = fields.Nested(ClientePessoaschema)
    unalimento = fields.Nested(UnFoodsSchema)

class Atletaschema(ModelSchema):
    class Meta:
        model = Atleta

class MetaAtletaschema(ModelSchema):
    class Meta:
        model = Metaatleta

    exclude = ('atleta',)



class DietaSchema(ModelSchema):
    class Meta:
        model = Dieta

    dieta_refeicao = fields.Nested(RefeicaoSchema)
    metaatleta = fields.Nested(MetaAtletaschema)


class MensageWhatsAppSchema(ModelSchema):
    class Meta:
        model = MensageWhatsApp

    pessoa = fields.Nested(PessoaSchema)


class PackageTrackSchema(ModelSchema):
    class Meta:
        model = PackageTrack

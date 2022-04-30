from flask import Blueprint,jsonify,render_template
from App.views.tributacao import cst_icms,cst_ipi,cst_pisconfins
from App.model.tributacao.cst_icms import SchemaCSTICMS
from App.model.tributacao.cst_ipi import SchemaCSTIpi
from App.model.tributacao.cst_piscofins import SchemaCSTPisCofins

routescst = Blueprint('routescst',__name__)

# Mostra Dados CST ICMS
@routescst.route('/tributacao/cst/main')
def get_cst_main():
    return render_template('layouts/tributacao/cst/main.html')


"""----------------------- CODIGO SITUAÇÃO TRIBUTÁRIA ICMS ----------------------------"""


# Mostra Dados CST ICMS
@routescst.route('/tributacao/cst/icms/main',methods=['GET'])
def get_cst_icms_main():
    pass

# Mostra Dados CST em Json
@routescst.route('/get/tributacao/cst/icms/json',methods=['GET'])
def get_cst_icms_json():
    csticms = cst_icms.get_cst_icms()
    if csticms:
        schemacsticms = SchemaCSTICMS()
        return jsonify({'data':schemacsticms.dump(csticms,many=True),'result':True})
    else:
        return jsonify({'data': {}, 'result': False})

@routescst.route('/tributacao/cst/icms/insertinto', methods=['POST'])
def insert_into_cst_icms():
    return jsonify(cst_icms.insert_into())


"""----------------------- CODIGO SITUAÇÃO TRIBUTÁRIA IPI ----------------------------"""


# Mostra Dados CST IPI
@routescst.route('/tributacao/cst/ipi/main',methods=['GET'])
def get_cst_ipi_main():
    pass

# Mostra Dados CST IPI em Json
@routescst.route('/get/tributacao/cst/ipi/json',methods=['GET'])
def get_cst_ipi_json():
    cstipi = cst_ipi.get_cst_ipi()
    if cstipi:
        schemacstipi = SchemaCSTIpi()
        return jsonify({'data':schemacstipi.dump(cstipi,many=True),'result':True})
    else:
        return jsonify({'data': {}, 'result': False})

@routescst.route('/tributacao/cst/ipi/insertinto', methods=['POST'])
def insert_into_cst_ipi():
    return jsonify(cst_ipi.insert_into())


"""----------------------- CODIGO SITUAÇÃO TRIBUTÁRIA PISCOFINS ----------------------------"""


# Mostra Dados CST PISCOFINS
@routescst.route('/tributacao/cst/piscofins/main',methods=['GET'])
def get_cst_piscofins_main():
    pass

# Mostra Dados CST PIS/COFINS em Json
@routescst.route('/get/tributacao/cst/piscofins/json',methods=['GET'])
def get_cst_piscofins_json():
    cstpiscofins = cst_pisconfins.get_cst_piscofins()
    if cstpiscofins:
        schemacstpiscofins = SchemaCSTPisCofins()
        return jsonify({'data':schemacstpiscofins.dump(cstpiscofins,many=True),'result':True})
    else:
        return jsonify({'data': {}, 'result': False})

@routescst.route('/tributacao/cst/piscofins/insertinto', methods=['POST'])
def insert_into_cst_pisconfins():
    return jsonify(cst_pisconfins.insert_into())
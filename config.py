import string
import random
import os
random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))
DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'mysql://221068:rony0608@mysql-rgmsolutions.alwaysdata.net/rgmsolutions_siscontrol'
#SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(USERNAME_MYSQL,PWD_MYSQL,
#                                                                HOST_MYSQL,PORT_MYSQL,DATABASE_MYSQL)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/rgmnutri?charset=utf8"


from App.conections.conns import return_db
SQLALCHEMY_DATABASE_URI ="mysql+pymysql://root:@localhost:3306/rgmnutri?charset=utf8"
#SQLALCHEMY_DATABASE_URI = return_db(0)
#SQLALCHEMY_DATABASE_URI = 'mysql://root:root@db/sisnutri' #docker criando banco mariadb(container tmb:localhost)
#SQLALCHEMY_DATABASE_URI = 'mysql://221068:rony0608@mysql-rgmsolutions.alwaysdata.net/rgmsolutions_siscontrol'
#SQLALCHEMY_DATABASE_URI = 'mysql://rony:rony@localhost:3307/sisnutri'
#SQLALCHEMY_DATABASE_URI = 'mysql://root:root@db/sisnutri'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = key
UPLOAD_FOLDER = 'App/static/img/uploads/'
DOWNLOAD_FOLDER = 'static/downloads/'
DIRECTORY_APP = os.path.abspath(os.getcwd())
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Configuração EMAIL
MAIL_SERVER = 'smtp-rgmsolutions.alwaysdata.net'
MAIL_PORT = 465
MAIL_USERNAME = 'rgmsolutions@alwaysdata.net'
MAIL_PASSWORD = 'rony0608'
MAIL_USE_TLS= False
MAIL_USE_SSL = True


TWILIO_ACCOUNT_SID = 'AC7a7e41e876b89f83259ecbfc83553377'
TWILIO_AUTH_TOKEN = 'f991d65a2ad8463258a46727cbe20048'
TWILIO_NUMBER_PHONE = '+5532984422783'

#Config Mercado Pago
PUBLIC_KEY_MERCADOPAGO = 'TEST-41b19948-fd9f-4ad8-b1eb-de01a2a5f938'
ACESS_TOKEN_MERCADOPAGO = 'TEST-7826144472079669-112923-baa2de3e52100271a60975bd01cb9ffe-50407128'

PUBLIC_KEY_MERCADOPAGO_VENDEDOR_TEST = "TEST-8e948c88-fed0-4dc4-92d7-1e13e63964d6"
ACESS_TOKEN_MERCADOPAGO_VENDEDOR_TEST = "TEST-3327606737646947-120700-faa807c0a63af4bd8546c31342f793ad-1034126701"

db_locahost = {
    'USERNAME_MYSQL' : 'root',
    'PWD_MYSQL' : '',
    'HOST_MYSQL' : 'localhost',
    'PORT_MYSQL' : '3306',
    'DATABASE_MYSQL' : 'rgmnutri'
}

db_alwaysdata = {
    'USERNAME_MYSQL' : '268760',
    'PWD_MYSQL' : 'rony0608',
    'HOST_MYSQL' : 'mysql-rgmsolutions.alwaysdata.net',
    'PORT_MYSQL' : '3306',
    'DATABASE_MYSQL' : 'rgmsolutions_rgmsolutions'
}
db_doker = {
    'USERNAME_MYSQL' : 'root',
    'PWD_MYSQL' : 'root',
    'HOST_MYSQL' : 'db',
    'DATABASE_MYSQL' : 'sisnutri'
}

db_localhost_postgres ={
    'HOST_POSTGRES' : 'localhost',
    'PORT_POSTGRES' : '5432',
    'PWD_POSTGRES': 'rony0608',
    'USERNAME_POSTGRES': 'postgres',
    'DATABASE_POSTGRES': 'sisnutri'
}

def return_db(intqual):
    if intqual == 0:
        return 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(db_locahost["USERNAME_MYSQL"],
                                               db_locahost["PWD_MYSQL"],
                                               db_locahost["HOST_MYSQL"],
                                               db_locahost["PORT_MYSQL"],
                                               db_locahost["DATABASE_MYSQL"])
    elif intqual == 1:
        return 'mysql://{}:{}@{}/{}?charset=utf8'.format(db_alwaysdata["USERNAME_MYSQL"],
                                               db_alwaysdata["PWD_MYSQL"],
                                               db_alwaysdata["HOST_MYSQL"],
                                               db_alwaysdata["DATABASE_MYSQL"])
    elif intqual == 2:
        return 'mysql://{}:{}@{}/{}?charset=utf8'.format(db_doker["USERNAME_MYSQL"],
                                            db_doker["PWD_MYSQL"],
                                            db_doker["HOST_MYSQL"],
                                            db_doker["DATABASE_MYSQL"])
    elif intqual == 3:
        return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_localhost_postgres['USERNAME_POSTGRES'],
                                                                     pw=db_localhost_postgres['PWD_POSTGRES'],
                                                                     url=db_localhost_postgres['HOST_POSTGRES']+':'+
                                                                         db_localhost_postgres['PORT_POSTGRES'],
                                                                     db=db_localhost_postgres['DATABASE_POSTGRES'])



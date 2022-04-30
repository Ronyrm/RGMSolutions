from App import engine
from sqlalchemy import text
from App.sql.migrate_triggers import sql_array

# Atualiza as trigger criadas
def migrate_trigger():
    with engine.connect() as conn:
        for row in sql_array:
            try:
                sql = text(sql_array[row])
                conn.execute(sql)
            except:
                pass


def insert_data_script_sql(spath):
    sql = open(spath,'r',encoding="utf8").read()
    with engine.connect() as conn:
        conn.execute(text(sql))

#sql = open('App\sql\Triggers_sisnutri.sql','r').read()
#db.session.execute(text(sql).execution_options(autocommit=True))

#dbmysql = MySQLdb.connect(user="rony",passwd="rony",host="localhost",db="sisnutri",port=3307)
#cursor = dbmysql.cursor()
#cursor.execute('SELECT * FROM atleta')
#data = cursor.fetchall()
#print(data)
#dbmysql.close()

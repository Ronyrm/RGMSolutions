from App import db,engine
from sqlalchemy.sql import text
def execute_procedure_db(nameproc,parameter):
    result = False
    try:
        result = True
        conn = engine.raw_connection()
        cursor = conn.cursor()

        cursor.callproc(nameproc,parameter)
        conn.commit()

        return result

    finally:
        conn.close()


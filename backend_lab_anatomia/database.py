import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost:3307",
        user="lab_user",
        password="lab_pass",
        database="laboratorio_anatomia"
    )



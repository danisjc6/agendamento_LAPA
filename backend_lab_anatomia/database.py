import mysql.connector
import os

def get_db():
    return mysql.connector.connect(
        host="mysql",
        port=3306,
        user="lab_user",
        password="lab_pass",
        database="laboratorio_anatomia"
    )


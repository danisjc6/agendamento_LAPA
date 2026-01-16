import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="daniela",
        password="daniela123",
        database="laboratorio_anatomia"
    )


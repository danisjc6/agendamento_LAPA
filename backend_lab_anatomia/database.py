import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="mysql",
        port=3306,
        user="lab_user",
        password="lab_pass",
        database="laboratorio_anatomia",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )

    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8mb4;")
    cursor.close()

    return conn


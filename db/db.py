import mysql.connector

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="mydatabase"
    )

    return mydb
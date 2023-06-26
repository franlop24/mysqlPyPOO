from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

mydb = get_connection()

class User:

    def __init__(self, 
                 username, 
                 password,
                 first_name = '',
                 last_name = '',
                 email = '',
                 image = '',
                 id = None):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.image = image

    def save(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                self.password = generate_password_hash(self.password)
                sql = "INSERT INTO users(username, password) VALUES(%s, %s)"
                val = (self.username, self.password)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id

    @staticmethod
    def __get__(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM users WHERE id = { id }"
            cursor.execute(sql)

            user = cursor.fetchone()

            if user:
                user = User(user["username"], #username
                            user["password"], #password
                            user["first_name"], #first_name
                            user["last_name"], #last_name
                            user["email"], #email
                            user["image"], #image
                            id)
                return user
            
            return None
    
    @staticmethod
    def get_by_password(username, password):
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT id, username, password FROM users WHERE username = %s"
            val = (username,)
            cursor.execute(sql, val)
            user = cursor.fetchone()
            
            if user != None:
                if check_password_hash(user["password"], password):
                    return User.__get__(user["id"])
            return None

    def __str__(self):
        return f"{ self.username } { self.first_name } { self.last_name }"
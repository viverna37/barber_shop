
import sqlite3
class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()


    async def add_users(self, user_id):
        with self.connect:
            return self.cursor.execute("""INSERT OR IGNORE INTO users (user_id) VALUES (?)""",
                                           [user_id])
    async def get_users(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT user_id FROM users WHERE user_id=(?)""", [user_id]).fetchone()


    async def get_products(self, categori_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE categori_id=(?)""", [categori_id]).fetchall()

    async def update_label(self, label, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET label=(?) WHERE user_id=(?)""",
                                       [label, user_id])



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

    async def get_userss(self):
        with self.connect:
            return self.cursor.execute("""SELECT user_id FROM users""").fetchall()

    async def get_filials(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM filials""").fetchall()

    async def get_info_filials(self, filials_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM filials WHERE filials_id=(?)""", [filials_id]).fetchall()


    async def update_opp(self, opp, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET opp=(?) WHERE user_id=(?)""",
                                       [opp, user_id])

    async def get_opp(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT opp FROM users WHERE user_id=(?)""", [user_id]).fetchmany()

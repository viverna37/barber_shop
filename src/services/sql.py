
import sqlite3
class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()


    async def add_users(self, user_id):
        with self.connect:
            return self.cursor.execute("""INSERT OR IGNORE INTO users (user_id) VALUES (?)""",
                                           [user_id])

    async def get_products(self, categori_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE categori_id=(?)""", [categori_id]).fetchall()

    async def products(self, product_id, categori_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE product_id=(?) AND categori_id=(?)""", [product_id, categori_id]).fetchall()

    async def update_label(self, label, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET label=(?) WHERE user_id=(?)""",
                                       [label, user_id])

    async def get_payment_status(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT bought, label FROM users WHERE user_id=(?)""",
                                       [user_id]).fetchall()

    async def update_payment_status(self, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET bought=(?) WHERE user_id=(?)""",
                                       [True, user_id])

    async def unupdate_payment_status(self, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET bought=(?) WHERE user_id=(?)""", [False, user_id])










    async def get_user_product(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE product_id=(?)""", [product_id]).fetchall()

    async def get_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM cart WHERE user_id=(?)""", [user_id]).fetchall()

    async def add_to_cart(self, count, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""UPDATE cart SET count=(?) WHERE user_id=(?) AND product_id=(?)""", [count, user_id, product_id]).fetchall()

    async def add_to_cart_mb(self, user_id, product_id, count):
        with self.connect:
            return self.cursor.execute("""INSERT INTO cart (user_id, product_id, mb) VALUES (?, ?, ?)""",
                                       [user_id, product_id, 1])

    # async def add_to_cart(self, user_id, product_id, count):
    #     with self.connect:
    #         return self.cursor.execute("""UPDATE cart SET count = (?) WHERE user_id""",
    #                                    [user_id, product_id, 1])
    async def empty_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM cart WHERE user_id=(?)""", [user_id])

    async def get_categories(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM categories""").fetchall()



    async def get_count_in_cart(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM cart WHERE user_id=(?) AND product_id=(?)""", [user_id, product_id]).fetchall()

    async def get_count_in_cart_mb(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT mb FROM cart WHERE user_id=(?) AND product_id=(?)""", [user_id, product_id]).fetchall()

    async def get_count_in_stock(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM products WHERE product_id=(?)""", [product_id]).fetchall()

    async def remowe_one_item(self, mb, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""UPDATE cart SET mb=(?) WHERE user_id=(?) AND product_id=(?)""", [mb, user_id, product_id]).fetchall()

    async def remowe_one_item_mb(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM cart WHERE user_id=(?) AND product_id=(?)""", [user_id, product_id]).fetchall()

    async def change_count(self, count, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""UPDATE cart SET count=(?) WHERE user_id=(?) AND product_id=(?)""", [count, user_id, product_id]).fetchall()

    async def change_count_mb(self, mb, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""UPDATE cart SET mb=(?) WHERE user_id=(?) AND product_id=(?)""", [mb, user_id, product_id]).fetchall()

    async def user(self):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (user_id) VALUES (?)""").fetchall()

    async def wiev_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM cart WHERE user_id=(?)""", [user_id]).fetchall()

    async def number(self, user_id, data):
        with self.connect:
            return self.cursor.execute("""INSERT OR IGNORE INTO users (user_id, number) VALUES (?,?)""",[user_id, data])

    async def adres(self, adres, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET adres = (?) WHERE user_id = (?)""",[adres, user_id])
        

    async def comment(self, comment, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET comment = (?) WHERE user_id = (?)""",[comment, user_id])


    async def wiev_num(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT number FROM users WHERE user_id=(?)""",
                                           [user_id]).fetchall()

    async def wiev_adres(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT adres FROM users WHERE user_id=(?)""",
                                           [user_id]).fetchall()
        
    async def wiev_comment(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT comment FROM users WHERE user_id=(?)""",
                                           [user_id]).fetchall()



    async def view_cart(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT product_id, count FROM cart WHERE user_id=(?)""",
                                           [user_id]).fetchall()
    async def name(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT name FROM products WHERE product_id=(?)""",
                                       [product_id]).fetchall()
    async def count(self, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM cart WHERE product_id=(?) AND user_id=(?)""",
                                       [product_id, user_id]).fetchall()
    async def price(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT price FROM products WHERE product_id=(?)""",
                                       [product_id]).fetchall()

    async def get_products(self, categori_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products WHERE categori_id=(?)""", [categori_id]).fetchall()

    async def add_cart_photo(self, name, price, count, categori_id, img, opp):
        with self.connect:
            return self.cursor.execute("""INSERT INTO products (name, price, count, categori_id, img, opp) VALUES(?,?,?,?,?,?)""",
                                       [name, price, count, categori_id, img, opp]).fetchall()

    async def update_stock(self, stock, product_id):
        with self.connect:
            return self.cursor.execute("""UPDATE products SET count=(?) WHERE product_id=(?)""",
                                       [stock, product_id]).fetchall()

    async def del_cart(self, product_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM products WHERE product_id=(?)""", [product_id]).fetchall()

    async def add_category(self, name):
        with self.connect:
            return self.cursor.execute("""INSERT INTO categories (categori_name) VALUES(?)""", [name]).fetchall()

    async def del_category(self, category_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM categories WHERE categori_id=(?)""", [category_id]).fetchall()


    async def update_categoory(self, category_name, category_id):
        with self.connect:
            return self.cursor.execute("""UPDATE categories SET categori_name=(?) WHERE categori_id=(?)""", [category_name, category_id]).fetchall()


    async def del_product(self, product_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM cart WHERE product_id=(?)""", [product_id]).fetchall()     

    async def admin(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT admin FROM users WHERE user_id=(?)""", [user_id]).fetchall()  
        


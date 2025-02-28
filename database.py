import sqlite3

class Database:
    def __init__(self, path):
        self.path = path
        self.create_tables()

    def _execute_query(self, query, params=()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def _fetchall_query(self, query, params=()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def create_tables(self):
        create_products_table = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                size TEXT,
                price TEXT,
                product_id TEXT,
                photo TEXT
            )
        '''
        self._execute_query(create_products_table)

        create_orders_table = '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                size TEXT,
                quantity INTEGER,
                phone TEXT
            )
        '''
        self._execute_query(create_orders_table)

    def add_product(self, data: dict):
        insert_product = '''
            INSERT INTO products (name, category, size, price, product_id, photo) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self._execute_query(insert_product, (
        data['name'], data['category'], data['size'], data['price'], data['product_id'], data['photo']))

    def get_products(self):
        select_products = "SELECT name, category, size, price, product_id, photo FROM products"
        return self._fetchall_query(select_products)

    def add_order(self, data: dict):
        insert_order = '''
            INSERT INTO orders (product_id, size, quantity, phone) 
            VALUES (?, ?, ?, ?)
        '''
        self._execute_query(insert_order, (data['product_id'], data['size'], data['quantity'], data['phone']))

import sqlite3
import re
from datetime import datetime

class PriceDatabase:
    def __init__(self, db_path='deals_history.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS price_history (id INTEGER PRIMARY KEY AUTOINCREMENT, asin TEXT, product_name TEXT, price REAL, timestamp DATETIME, category TEXT)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_asin ON price_history(asin)")
            conn.commit()

    def add_price(self, asin, name, price, category):
        try:
            clean_price = float(re.sub(r'[^0-9.]', '', str(price)))
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO price_history (asin, product_name, price, timestamp, category) VALUES (?, ?, ?, ?, ?)", (asin, name, clean_price, datetime.now(), category))
                conn.commit()
            return True
        except Exception as e:
            print(f'DB Error: {e}')
            return False

    def get_min_//price(self, asin):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(price) FROM price_history WHERE asin = ?", (asin,))
            result = cursor.fetchone()
            return result[0] if result else None
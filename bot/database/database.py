import sqlite3
import logging
from config import DATABASE_PATH

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self._init_database()

    def _init_database(self):
        """Initializes the database and creates tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                last_xp_update DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def get_user_level(self, user_id):
        """Gets the user's XP and level from the database"""
        self.cursor.execute("SELECT xp, level FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def update_user_xp(self, user_id, xp, level):
        """Updates user's XP and level in the database"""
        self.cursor.execute(
            "UPDATE users SET xp=?, level=?, last_xp_update=CURRENT_TIMESTAMP WHERE user_id=?", 
            (xp, level, user_id)
        )
        self.conn.commit()

    def add_new_user(self, user_id, xp=0):
        """Adds a new user to the database"""
        self.cursor.execute(
            "INSERT INTO users (user_id, xp, last_xp_update) VALUES (?, ?, CURRENT_TIMESTAMP)", 
            (user_id, xp)
        )
        self.conn.commit()

    def close(self):
        """Closes the database connection"""
        self.conn.close()

import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS organizations
                   (name TEXT, address TEXT, website TEXT, operation_hours TEXT, contacts TEXT, link TEXT)"""
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while working with SQLite: {e}")

    def insert_organization(self, **kwargs):
        columns = ', '.join(kwargs.keys())  # Column names are the keys of kwargs
        placeholders = ', '.join('?' for _ in kwargs)  # A placeholder for each value
        values = tuple(kwargs.values())  # The corresponding values

        query = f"INSERT INTO organizations ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def fetch_all_links(self):
        try:
            self.cursor.execute("SELECT link FROM organizations")
            links = self.cursor.fetchall()  # Fetch all links
            return [link[0] for link in links if link[0]]  # Return a list of non-empty links
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()

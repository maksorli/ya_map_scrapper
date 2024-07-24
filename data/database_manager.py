import sqlite3
from typing import List, Optional


class DatabaseManager:
    def __init__(self, db_path: str) -> None:
        """
        Initialize the DatabaseManager with the path to the SQLite database.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """
        Connect to the SQLite database and create the organizations table if it doesn't exist.
        """
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

    def insert_organization(self, key: Optional[str] = None, **kwargs) -> None:
        """
        Insert a new organization or update an existing one in the database.

        Args:
            key (Optional[str]): The link to identify the organization for updates.
            kwargs: Column names and their corresponding values to insert or update.
        """
        columns = ", ".join(kwargs.keys())  # Column names are the keys of kwargs
        placeholders = ", ".join("?" for _ in kwargs)  # A placeholder for each value
        values = tuple(kwargs.values())  # The corresponding values

        if key:
            # Check if a row with the specified link exists
            self.cursor.execute("SELECT 1 FROM organizations WHERE link=?", (key,))
            row = self.cursor.fetchone()
            if row is None:
                print(f"No row found with link={key}.")
                return

            set_clause = ", ".join(f"{col}=?" for col in kwargs.keys())
            query = f"UPDATE organizations SET {set_clause} WHERE link=?"
            values += (key,)
        else:
            query = f"INSERT INTO organizations ({columns}) VALUES ({placeholders})"

        # Print the full query and values
        print("SQL Query:", query)
        print("Values:", values)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Query executed and committed successfully.")

            # Verify the update
            if key:
                self.cursor.execute("SELECT * FROM organizations WHERE link=?", (key,))
                updated_row = self.cursor.fetchone()
                print("Updated row:", updated_row)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction in case of an error

    def fetch_all_links(self) -> List[str]:
        """
        Fetch all links from the organizations table.

        Returns:
            List[str]: A list of non-empty links.
        """
        try:
            self.cursor.execute("SELECT link FROM organizations")
            links = self.cursor.fetchall()  # Fetch all links
            return [
                link[0] for link in links if link[0]
            ]  # Return a list of non-empty links
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self) -> None:
        """
        Close the connection to the SQLite database.
        """
        if self.conn:
            self.conn.close()

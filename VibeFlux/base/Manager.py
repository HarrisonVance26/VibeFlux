# IMcore
import sqlite3
from sqlite3 import Error


class BaseDB:
    """
    A base class that provides fundamental database connection management.
    """

    def __init__(self, db_path: str, check_same_thread: bool = True):
        """
        Initializes the database connection with the provided path.

        Args:
            db_path (str): The path to the SQLite database file.
            check_same_thread (bool): Whether to check the same thread for connections
                                      (default is True).
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect(check_same_thread=check_same_thread)  # Establish connection

    def connect(self, check_same_thread: bool = True):
        """
        Establishes a connection to the SQLite database.

        Args:
            check_same_thread (bool): Whether to check the same thread for connections
                                      (default is True).

        Returns:
            None
        """
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=check_same_thread)
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to database: {self.db_path}")
        except Error as e:
            print(f"Failed to connect to database: {e}")

    def close(self):
        """
        Closes the database connection.

        Returns:
            None
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("Database connection closed.")

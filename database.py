import sqlite3
from config import DB_NAME


def get_db_connection():
    """
        Establishes a connection to the SQLite database with a specified timeout.

        Returns:
            sqlite3.Connection: Connection object to interact with the SQLite database.
        """
    conn = sqlite3.connect(DB_NAME, timeout=10)
    return conn


def init_db():
    """
        Initializes the SQLite database by creating the subscribers table if it doesn't exist.

        The subscribers table contains:
            - id (INTEGER PRIMARY KEY): The unique identifier for each subscriber.
        """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()


def add_subscriber(user_id):
    """
        Adds a subscriber to the subscribers table.

        If the user_id already exists, it replaces the existing entry.

        Args:
            user_id (int): The unique identifier of the subscriber to be added.
        """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('REPLACE INTO subscribers (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def remove_subscriber(user_id):
    """
        Removes a subscriber from the subscribers table based on user_id.

        Args:
            user_id (int): The unique identifier of the subscriber to be removed.
        """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM subscribers WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_subscriber():
    """
        Retrieves all subscriber IDs from the subscribers table.

        Returns:
            list: A list of subscriber IDs.
        """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM subscribers')
    subscribers = [row[0] for row in c.fetchall()]
    conn.close()
    return subscribers


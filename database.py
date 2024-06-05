import sqlite3

def init_db():
    conn = sqlite3.connect("subscribers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()


def add_subscriber(user_id):
    conn = sqlite3.connect("subscribers.db")
    c = conn.cursor()
    c.execute('INSERT INTO subscribers (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def remove_subscriber(user_id):
    conn = sqlite3.connect("subscribers.db")
    c = conn.cursor()
    c.execute('DELETE FROM subscribers WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_subscriber():
    conn = sqlite3.connect("subscribers.db")
    c = conn.cursor()
    c.execute('SELECT id FROM subscribers')
    subscribers = [row[0] for row in c.fetchall()]
    conn.close()
    return subscribers


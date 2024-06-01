# database.py
import sqlite3

def initialize_database():
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    content BLOB NOT NULL,
                    checksum TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    modified_at TEXT,
                    FOREIGN KEY(owner_id) REFERENCES users(id)
                )''')

    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

def add_artifact(owner_id, name, artifact_type, encrypted_content, checksum, timestamp):
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('''INSERT INTO artifacts (owner_id, name, type, content, checksum, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)''', (owner_id, name, artifact_type, encrypted_content, checksum, timestamp))
    conn.commit()
    conn.close()

def delete_artifact(artifact_id):
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    conn.commit()
    conn.close()


# database.py
import sqlite3

def initialize_database():
    """
    Initialize the database by creating necessary tables.
    This function is idempotent; it can be run multiple times without affecting existing data.
    """
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
                )''')

    # Create artifacts table
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
    """
    Add a new user to the database.
    This function assumes that the username is unique.
    """
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

def add_artifact(owner_id, name, artifact_type, encrypted_content, checksum, timestamp):
    """
    Add a new artifact to the database.
    The content of the artifact is stored in encrypted form.
    """
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('''INSERT INTO artifacts (owner_id, name, type, content, checksum, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)''', (owner_id, name, artifact_type, encrypted_content, checksum, timestamp))
    conn.commit()
    conn.close()

def delete_artifact(artifact_id, owner_id):
    """
    Delete an artifact from the database.
    Only the owner or an admin can delete an artifact.
    """
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('DELETE FROM artifacts WHERE id = ? AND owner_id = ?', (artifact_id, owner_id))
    conn.commit()
    conn.close()

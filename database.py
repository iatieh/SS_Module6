import sqlite3
import hashlib
from utils import generate_key, encrypt_content, get_timestamp


def generate_checksum(content):
    """
    Generate a SHA-256 checksum for the given content.
    This is used to verify the integrity of the artifact.

    Args:
    - content (bytes): The content for which to generate the checksum.

    Returns:
    - str: The SHA-256 checksum as a hexadecimal string.
    """
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()


def initialize_database():
    """
    Initialize the database by creating necessary tables.
    This function is idempotent; it can be run multiple times without affecting existing data.
    Also, it creates a default admin user if no users exist.
    """
    conn = sqlite3.connect('DB1.db')
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

    # Check if there are any users in the database
    c.execute('SELECT COUNT(*) FROM users')
    user_count = c.fetchone()[0]

    # If no users exist, create a default admin user
    if user_count == 0:
        default_admin_username = 'admin'
        default_admin_password = 'admin123'
        default_admin_role = 'admin'
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                  (default_admin_username, default_admin_password, default_admin_role))
        print(f"Default admin user created: {default_admin_username} / {default_admin_password}")

    conn.commit()
    conn.close()


def add_user(username, password, role):
    """
    Add a new user to the database.
    This function assumes that the username is unique.

    Args:
    - username (str): The username of the new user.
    - password (str): The password of the new user.
    - role (str): The role of the new user (either 'admin' or 'user').
    """
    conn = sqlite3.connect('DB1.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()


def add_artifact(owner_id, name, artifact_type, file_path):
    """
    Add a new artifact to the database.
    The content of the artifact is read from the file, encrypted, and stored.
    A checksum of the content is also calculated and stored.

    Args:
    - owner_id (int): The ID of the owner of the artifact.
    - name (str): The name of the artifact.
    - artifact_type (str): The type of the artifact (e.g., 'lyric', 'score', 'recording').
    - file_path (str): The path to the artifact file.
    """
    with open(file_path, 'rb') as file:
        content = file.read()

    key = generate_key()
    encrypted_content = encrypt_content(content, key)
    checksum = generate_checksum(content)
    timestamp = get_timestamp()

    conn = sqlite3.connect('DB1.db')
    c = conn.cursor()
    c.execute('''INSERT INTO artifacts (owner_id, name, type, content, checksum, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)''', (owner_id, name, artifact_type, encrypted_content, checksum, timestamp))
    conn.commit()
    conn.close()


def delete_artifact(artifact_id):
    """
    Delete an artifact from the database.
    Only an admin can delete any artifact.

    Args:
    - artifact_id (int): The ID of the artifact to delete.
    """
    conn = sqlite3.connect('DB1.db')
    c = conn.cursor()
    c.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    conn.commit()
    conn.close()


def modify_artifact(artifact_id, owner_id, file_path):
    """
    Modify an existing artifact. Only the owner can modify their own artifacts.

    Args:
    - artifact_id (int): The ID of the artifact to modify.
    - owner_id (int): The ID of the owner of the artifact.
    - file_path (str): The path to the new artifact file.
    """
    with open(file_path, 'rb') as file:
        content = file.read()

    key = generate_key()
    encrypted_content = encrypt_content(content, key)
    checksum = generate_checksum(content)
    timestamp = get_timestamp()

    conn = sqlite3.connect('DB1.db')
    c = conn.cursor()
    c.execute('''UPDATE artifacts SET content = ?, checksum = ?, modified_at = ?
                 WHERE id = ? AND owner_id = ?''',
              (encrypted_content, checksum, timestamp, artifact_id, owner_id))
    conn.commit()
    conn.close()

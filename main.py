# main.py
import argparse
import sqlite3
from database import initialize_database, add_user, add_artifact, delete_artifact
from utils import generate_key, encrypt_content, generate_checksum, get_timestamp

def print_logo():
    """Read and print the logo from logo.txt file."""
    with open('logo.txt', 'r') as file:
        logo = file.read()
    print(logo)

def authenticate_user():
    """
    Authenticate the user by checking the username and password.
    Returns a tuple of user_id and role if authentication is successful.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('SELECT id, role FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user
    else:
        print("Authentication failed. Please check your username and password.")
        return None

def view_artifacts(user_id, role):
    """
    View artifacts owned by the user if the user is not an admin.
    Admins can view all artifacts.
    """
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    if role == 'admin':
        c.execute('SELECT * FROM artifacts')
    else:
        c.execute('SELECT * FROM artifacts WHERE owner_id = ?', (user_id,))
    artifacts = c.fetchall()
    conn.close()
    if artifacts:
        print("Artifacts:")
        for artifact in artifacts:
            print(f"ID: {artifact[0]}, Owner ID: {artifact[1]}, Name: {artifact[2]}, Type: {artifact[3]}, Checksum: {artifact[5]}, Created At: {artifact[6]}, Modified At: {artifact[7]}")
    else:
        print("No artifacts found.")

def update_user_role(username, new_role):
    """Update the role of a user."""
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('UPDATE users SET role = ? WHERE username = ?', (new_role, username))
    conn.commit()
    conn.close()

def delete_artifact(user_id, role):
    """
    Delete an artifact if the user is the owner or if the user is an admin.
    """
    artifact_id = input("Enter artifact ID to delete: ")
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    if role == 'admin':
        c.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    else:
        c.execute('DELETE FROM artifacts WHERE id = ? AND owner_id = ?', (artifact_id, user_id))
    conn.commit()
    conn.close()
    if c.rowcount == 0:
        print("No artifact found or you don't have permission to delete this artifact.")
    else:
        print(f"Artifact {artifact_id} deleted successfully.")

def menu():
    """
    Display the main menu and process user input.
    Uses a loop to keep the menu active until the user chooses to exit.
    """
    user = authenticate_user()
    if not user:
        return
    user_id, role = user
    while True:
        print_logo()
        print("Options:")
        print("1. Add User")
        print("2. Add Artifact")
        print("3. View Artifacts")
        print("4. Delete Artifact")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1' and role == 'admin':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role_input = input("Enter role (admin/user): ")
            add_user(username, password, role_input)
            print(f"User {username} added successfully.")
        elif choice == '2':
            owner_id = user_id
            name = input("Enter artifact name: ")
            artifact_type = input("Enter artifact type (lyric/score/recording): ")
            file_path = input("Enter path to artifact file: ")
            with open(file_path, 'rb') as file:
                content = file.read()
            key = generate_key()
            encrypted_content = encrypt_content(content, key)
            checksum = generate_checksum(content)
            timestamp = get_timestamp()
            add_artifact(owner_id, name, artifact_type, encrypted_content, checksum, timestamp)
            print(f"Artifact {name} added successfully.")
        elif choice == '3':
            view_artifacts(user_id, role)
        elif choice == '4':
            delete_artifact(user_id, role)
        elif choice == '5':
            break
        else:
            print("Invalid choice or insufficient permissions. Please try again.")

if __name__ == '__main__':
    initialize_database()
    menu()

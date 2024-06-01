# main.py
import argparse
import sqlite3
from database import initialize_database, add_user, add_artifact, delete_artifact
from utils import generate_key, encrypt_content, generate_checksum, get_timestamp

def print_logo():
    logo = """
    =======================================
                     IYAD
    Secure Enclave for Music Artifacts
    =======================================
    """
    print(logo)

def view_artifacts():
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('SELECT * FROM artifacts')
    artifacts = c.fetchall()
    conn.close()
    if artifacts:
        print("Artifacts:")
        for artifact in artifacts:
            print(f"ID: {artifact[0]}, Owner ID: {artifact[1]}, Name: {artifact[2]}, Type: {artifact[3]}, Checksum: {artifact[5]}, Created At: {artifact[6]}, Modified At: {artifact[7]}")
    else:
        print("No artifacts found.")

def update_user_role(username, new_role):
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('UPDATE users SET role = ? WHERE username = ?', (new_role, username))
    conn.commit()
    conn.close()

def delete_artifact(artifact_id):
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    conn.commit()
    conn.close()

def menu():
    while True:
        print_logo()
        print("Options:")
        print("1. Add User")
        print("2. Add Artifact")
        print("3. View Artifacts")
        print("4. Delete Artifact")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (admin/user): ")
            add_user(username, password, role)
            print(f"User {username} added successfully.")
        elif choice == '2':
            owner_id = input("Enter owner ID: ")
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
            view_artifacts()
        elif choice == '4':
            artifact_id = input("Enter artifact ID to delete: ")
            delete_artifact(artifact_id)
            print(f"Artifact {artifact_id} deleted successfully.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    initialize_database()
    menu()

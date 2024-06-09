import sqlite3
import getpass
from database import initialize_database, add_user, add_artifact, delete_artifact, modify_artifact

def print_logo():
    """Read and print the logo from logo.txt file."""
    with open('logo.txt', 'r') as file:
        logo = file.read()
    print(logo)

def authenticate_user():
    """
    Authenticate the user by checking the username and password.
    Returns a tuple of user_id and role if authentication is successful.
    Uses the `getpass` module to securely handle password input.
    """
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    conn = sqlite3.connect('DB1.db')
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
    conn = sqlite3.connect('DB1.db')
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

def delete_artifact_by_id(user_id, role):
    """
    Delete an artifact if the user is an admin.
    Regular users are not allowed to delete artifacts.
    """
    if role != 'admin':
        print("Permission denied. Only admins can delete artifacts.")
        return

    artifact_id = input("Enter artifact ID to delete: ")
    delete_artifact(artifact_id)
    print(f"Artifact {artifact_id} deleted successfully.")

def modify_user_artifact(user_id):
    """
    Modify an artifact if the user is the owner of the artifact.
    """
    artifact_id = input("Enter artifact ID to modify: ")
    file_path = input("Enter path to the new artifact file: ")
    modify_artifact(artifact_id, user_id, file_path)
    print(f"Artifact {artifact_id} modified successfully.")

def menu(user_id, role):
    """
    Display the main menu and process user input.
    Uses a loop to keep the menu active until the user chooses to exit.
    """
    while True:
        print("Options:")
        print("1. Add User")
        print("2. Add Artifact")
        print("3. View Artifacts")
        print("4. Modify Artifact")
        print("5. Delete Artifact (Admin Only)")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == '1' and role == 'admin':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            role_input = input("Enter role (admin/user): ")
            add_user(username, password, role_input)
            print(f"User {username} added successfully.")
        elif choice == '2':
            name = input("Enter artifact name: ")
            artifact_type = input("Enter artifact type (lyric/score/recording): ")
            file_path = input("Enter path to artifact file: ")
            add_artifact(user_id, name, artifact_type, file_path)
            print(f"Artifact {name} added successfully.")
        elif choice == '3':
            view_artifacts(user_id, role)
        elif choice == '4':
            modify_user_artifact(user_id)
        elif choice == '5':
            delete_artifact_by_id(user_id, role)
        elif choice == '6':
            break
        else:
            print("Invalid choice or insufficient permissions. Please try again.")

if __name__ == '__main__':
    initialize_database()
    print_logo()
    user = authenticate_user()
    if user:
        user_id, role = user
        menu(user_id, role)


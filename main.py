# main.py
import argparse
from database import initialize_database, add_user, add_artifact
from utils import generate_key, encrypt_content, generate_checksum, get_timestamp

def print_logo():
    logo = """
    =======================================
                S-Wallet 
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

def main():
    print_logo()
    parser = argparse.ArgumentParser(description='Iyad - Secure Enclave for Music Artifacts')
    subparsers = parser.add_subparsers(dest='command')

    # Add user command
    parser_add_user = subparsers.add_parser('add_user', help='Add a new user')
    parser_add_user.add_argument('username', help='Username of the new user')
    parser_add_user.add_argument('password', help='Password of the new user')
    parser_add_user.add_argument('role', help='Role of the new user (admin or user)')

    # Add artifact command
    parser_add_artifact = subparsers.add_parser('add_artifact', help='Add a new artifact')
    parser_add_artifact.add_argument('owner_id', help='ID of the owner')
    parser_add_artifact.add_argument('name', help='Name of the artifact')
    parser_add_artifact.add_argument('type', help='Type of the artifact (lyric, score, recording)')
    parser_add_artifact.add_argument('file_path', help='Path to the artifact file')

    # View artifacts command
    parser_view_artifacts = subparsers.add_parser('view_artifacts', help='View all artifacts')

    # Update user role command
    parser_update_role = subparsers.add_parser('update_role', help='Update user role')
    parser_update_role.add_argument('username', help='Username of the user')
    parser_update_role.add_argument('new_role', help='New role for the user (admin or user)')

    args = parser.parse_args()

    if args.command == 'add_user':
        add_user(args.username, args.password, args.role)
        print(f"User {args.username} added successfully.")
    elif args.command == 'add_artifact':
        with open(args.file_path, 'rb') as file:
            content = file.read()
        key = generate_key()
        encrypted_content = encrypt_content(content, key)
        checksum = generate_checksum(content)
        timestamp = get_timestamp()
        add_artifact(args.owner_id, args.name, args.type, encrypted_content, checksum, timestamp)
        print(f"Artifact {args.name} added successfully.")
    elif args.command == 'view_artifacts':
        view_artifacts()
    elif args.command == 'update_role':
        update_user_role(args.username, args.new_role)
        print(f"User {args.username}'s role updated to {args.new_role}.")
    else:
        parser.print_help()

if __name__ == '__main__':
    initialize_database()
    main()

# cli.py
import argparse
from database import initialize_database, add_user, add_artifact
from utils import generate_key, encrypt_content, generate_checksum, get_timestamp

def print_logo():
    logo = """
    =======================================
                     IYAD
    Secure Enclave for Music Artifacts
    =======================================
    """
    print(logo)

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
    else:
        parser.print_help()

if __name__ == '__main__':
    initialize_database()
    main()
# view_database.py
import sqlite3

def view_users():
    conn = sqlite3.connect('iyad.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    if users:
        print("Users:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")
    else:
        print("No users found.")

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

if __name__ == '__main__':
    view_users()
    view_artifacts()
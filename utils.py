# utils.py
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet

def generate_checksum(content):
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()

def generate_key():
    return Fernet.generate_key()

def encrypt_content(content, key):
    f = Fernet(key)
    return f.encrypt(content)

def decrypt_content(encrypted_content, key):
    f = Fernet(key)
    return f.decrypt(encrypted_content)

def get_timestamp():
    return datetime.now().isoformat()
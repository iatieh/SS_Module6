# utils.py
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet


def generate_key():
    """
    Generate a new Fernet key for encryption.
    This key should be stored securely.
    """
    return Fernet.generate_key()

def encrypt_content(content, key):
    """
    Encrypt the given content using the provided Fernet key.
    """
    f = Fernet(key)
    return f.encrypt(content)

def decrypt_content(encrypted_content, key):
    """
    Decrypt the given content using the provided Fernet key.
    """
    f = Fernet(key)
    return f.decrypt(encrypted_content)

def get_timestamp():
    """
    Get the current timestamp in ISO format.
    This is used to record the creation and modification times of artifacts.
    """
    return datetime.now().isoformat()

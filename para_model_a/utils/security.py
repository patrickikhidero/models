# security.py
import hashlib
from cryptography.fernet import Fernet

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
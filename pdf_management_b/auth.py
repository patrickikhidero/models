import json
from functools import wraps

def hash_password(password):
    # Implement a simple hash (for educational purposes, use libraries like bcrypt in production)
    return password  # This is not secure, just for demonstration

def verify_password(stored_password, provided_password):
    return stored_password == provided_password  # Again, not secure

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session['role'] != 'admin':
            return 'Access denied', 403
        return f(*args, **kwargs)
    return decorated
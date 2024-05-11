import bcrypt
import hashlib
import uuid

def generate_uuid():
    return uuid.uuid4()

def hash_login(login):
    return hashlib.sha256(login.encode()).hexdigest()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def hash_email(email):
    return hashlib.md5(email.encode()).hexdigest()

def check_password(password_hash, password):
    return bcrypt.checkpw(password.encode(), password_hash)
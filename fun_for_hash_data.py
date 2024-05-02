import bcrypt
import hashlib
import uuid


class User:
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email
        self.uuid = self.generate_uuid()
        self.login_hash = self.hash_login()
        self.password_hash = self.hash_password()
        self.email_hash = self.hash_email()

    def generate_uuid(self):
        return uuid.uuid4()

    def hash_login(self):
        return hashlib.sha256(self.login.encode()).hexdigest()

    def hash_password(self):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.password.encode(), salt)

    def hash_email(self):
        return hashlib.md5(self.email.encode()).hexdigest()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash)

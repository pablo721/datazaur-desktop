

class User:
    def __init__(self, username, password_hash, salt, email=''):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.email = email



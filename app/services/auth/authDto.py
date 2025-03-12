from app.services.db.db import get_db
from werkzeug.security import generate_password_hash


class AuthDto:
    def __init__(self):
        self.db = get_db()
        self.cursor = self.db.cursor(dictionary=True)

    def register_user(self, username, password):
        self.cursor.execute(
            "INSERT INTO user (username, password) VALUES (%s, %s)",
            (username, generate_password_hash(password)),
        )
        self.db.commit()
        self.cursor.close()
        return True

    def get_user(self, username):
        self.cursor.execute(
            "SELECT id, username, password FROM user WHERE username = %s", (username,)
        )
        user = self.cursor.fetchone()
        return user

    def load_logged_user(self, id_user):
        self.cursor.execute(
            "SELECT * FROM user WHERE id = %s", (id_user,)
        )
        user = self.cursor.fetchone()
        return user

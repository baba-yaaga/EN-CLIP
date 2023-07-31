from PyQt5.QtWidgets import QMessageBox
import re, string, bcrypt
from DB import NewUserDBFuncs

class Validate:
    #def __init__(self, database):
     #   self.database = database

    def validate_username(self, username):
        # Validate username format using regular expressions
        username_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_]{1,18}[a-zA-Z0-9]$'
        # Regular expression pattern for username format
        if not re.match(username_pattern, username):
            # Display an error message if username format is invalid
            QMessageBox.critical(None, "Error", "Invalid username format. Username should contain 3-20 alphanumeric characters, and underscores can't be at the beginning or end!")
            return False
        return True

    def validate_password(self, password):
        # Validate password requirements
        if len(password) < 6 or len(password) > 64:
            QMessageBox.critical(None, "Error", "Password should be between 6 and 64 characters long, contain at least one digit and letter, and one special character!!")
            return False

        if not any(char.isdigit() for char in password):
            QMessageBox.critical(None, "Error", "Password should be between 6 and 64 characters long, contain at least one digit and letter, and one special character!!")
            return False

        if not any(char.isalpha() for char in password):
            QMessageBox.critical(None, "Error", "Password should be between 6 and 64 characters long, contain at least one digit and letter, and one special character!!")
            return False

        if not any(char in string.punctuation for char in password):
            QMessageBox.critical(None, "Error", "Password should be between 6 and 64 characters long, contain at least one digit and letter, and one special character!!")
            return False

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        return hashed_password

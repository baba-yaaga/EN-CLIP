from PyQt5.QtWidgets import QMessageBox
import re, string
class UserManager:
    def __init__(self, database):
        self.database = database

    def is_empty(self, username, password):
        # Check if username or password is empty
        if not username or not password:
            # Display an error message if username or password is empty
            QMessageBox.critical(self, "Error", "Username and password are required.")
            return

    def validate_username(self, username):
        # Validate username format using regular expressions
        username_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_]{1,18}[a-zA-Z0-9]$'
        # Regular expression pattern for username format
        if not re.match(username_pattern, username):
            # Display an error message if username format is invalid
            QMessageBox.critical(self, "Error", "Invalid username format. Username should contain 3-20 alphanumeric characters and underscores can't be at the beginning or end!")
            return

    def validate_password(self, password):
        # Validate password requirements
        if len(password) < 6 or len(password) > 64:
            QMessageBox.critical(self, "Error", "Password should be between 6 and 64 characters long.")
            return

        if not any(char.isdigit() for char in password):
            QMessageBox.critical(self, "Error", "Password should contain at least one digit.")
            return

        if not any(char.isalpha() for char in password):
            QMessageBox.critical(self, "Error", "Password should contain at least one letter.")
            return

        if not any(char in string.punctuation for char in password):
            QMessageBox.critical(self, "Error", "Password should contain at least one special character.")
            return

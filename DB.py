import sqlite3

class UserDBFuncs:
    def __init__(self, database):
        self.database = database

    def login(self, username, password):
        connection = None
        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            
            # Check if the user exists in the userAccounts table
            cursor.execute("SELECT * FROM userAccounts WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user:
                # Verify the password
                if user[2] == password:
                    print("Login successful")
                    # Perform any additional actions for a successful login
                else:
                    print("Invalid password")
            else:
                print("User does not exist")
            
        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            
        finally:
            if connection:
                connection.close()

class NewUserDBFuncs:
    def __init__(self, database):
        self.database = database

    def insert_user(self, username, hashed_password):
        connection = None
        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            
            # Insert the new user into the userAccounts table
            cursor.execute("INSERT INTO userAccounts (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            
        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            
        finally:
            if connection:
                connection.close()

    def user_exists(self, username):
        connection = None
        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            # Check if the username already exists in the userAccounts table
            cursor.execute("SELECT * FROM userAccounts WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user:
                return False 
            else:
                return True

        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            
        finally:
            if connection:
                connection.close()

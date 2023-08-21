import sqlite3, bcrypt, config

class UserDBFuncs:
    def __init__(self, database):
        self.database = database

    def login(self, username, password):
        connection = None
        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            # Retrieve the stored hashed password for the given username
            cursor.execute("SELECT password FROM userAccounts WHERE username=?", (username,))
            stored_password = cursor.fetchone()

            if stored_password:
                # Verify the entered password against the stored hashed password
                if bcrypt.checkpw(password.encode(), stored_password[0]):
                    return True
                else:
                    return False
            else:
                return False

        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])

        finally:
            if connection:
                connection.close()

    def show_credentials(self, username):
        try:
            with sqlite3.connect(self.database) as connection:
                cursor = connection.cursor()
                loggedInUser = username
                user_id = self.get_user(loggedInUser)
                if user_id:
                    # Perform the SQL query with a join between Credentials and userAccounts tables
                    cursor.execute("""
                    SELECT Credentials.website_id, Credentials.username, Credentials.password
                    FROM Credentials
                    JOIN userAccounts ON Credentials.loggedInUser = userAccounts.id
                    WHERE userAccounts.username = ?
                    """, (username,))
                    return cursor.fetchall()
                else:
                    return []

        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])

    def add_login(self, loggedInUser, website, webUsername, password):
        try:
            with sqlite3.connect(self.database) as connection:
                cursor = connection.cursor()
                user_id = self.get_user(loggedInUser)
                # Insert the new credentials into the Credentials table
                cursor.execute("INSERT INTO Credentials (loggedInUser, website_id, username, password) VALUES (?, ?, ?, ?)", (user_id, website, webUsername, password))
                connection.commit()

        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            
    def delete_login(self, loggedInUser, website, uname):
        try:
            with sqlite3.connect(self.database) as connection:
                print(loggedInUser, website, uname)
                cursor = connection.cursor()
                user_id = self.get_user(loggedInUser)
                print(f"FROM DB.py{loggedInUser}, {website}, {uname}")
                #input("Waiting...")
                # delete a login from the Credentials table
                cursor.execute("DELETE FROM Credentials WHERE loggedInUser = ? AND website_id = ? AND username = ?", (user_id, website, uname))
                connection.commit()
                return True 
        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            return False

    def get_user(self, loggedInUser):
        try:
            with sqlite3.connect(self.database) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM userAccounts WHERE username=?", (loggedInUser,))
                userId = cursor.fetchone()
                if userId:
                    userId = userId[0]
                    return userId
                else:
                    return None
        except sqlite3.Error as db_error:
            print("Error connecting to the database:", db_error.args[0])
            return None
            
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


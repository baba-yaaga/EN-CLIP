# Import necessary modules
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QLabel, QTextEdit, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtWidgets

from config import database
from valid_input import Validate
from DB import UserDBFuncs, NewUserDBFuncs
import sys

# Define the NewUserDialog class
class NewUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New User")
        layout = QVBoxLayout()

        # Create username label and line edit
        username_label = QLabel("Username:")
        self.username_lineedit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_lineedit)

        # Create password label and line edit
        password_label = QLabel("Password:")
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_lineedit)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button)

        # Create cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        # Set the layout
        self.setLayout(layout)


    def submit(self):
         # Retrieve the entered username and password
          username = self.username_lineedit.text()
          password = self.password_lineedit.text()

         # Validate the username format
          validator = Validate()
          if not validator.validate_username(username):
              return

          newUser = NewUserDBFuncs(database)
          if not newUser.user_exists(username):
              QMessageBox.critical(None, "Error", "That username already exists!!")
              return
         # Validate the password requirements and hash the password
          hashed_password = validator.validate_password(password)
          if not hashed_password:
              return  
          else:
            newUser.insert_user(username, hashed_password)
            QMessageBox.information(None, "SUCCESS", "User account created successfully!!")
         # Accept the dialog and indicate successful user creation
          self.accept()

# Define the Login class
class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.database = database
        layout = QVBoxLayout()

        # Create username label and line edit
        username_label = QLabel("Username:")
        self.username_lineedit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_lineedit)

        # Create password label and line edit
        password_label = QLabel("Password:")
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_lineedit)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button)

        # Create cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        # Set the layout
        self.setLayout(layout)

    def submit(self):
        # Retrieve the entered username and password
        self.username = self.username_lineedit.text()
        password = self.password_lineedit.text()

        # Validate the username format
        validator = Validate()
        if not validator.validate_username(self.username):
            return

        # Validate the password requirements
        if not validator.validate_password(password):
            return

        # Perform login
        user = UserDBFuncs(self.database)
        if not user.login(self.username, password):
          QMessageBox.critical(None, "Error", "Invalid Login!!")
          return  
        else:
          QMessageBox.information(None, "SUCCESS", "Login Successful!!")
          self.accept()


class UserWindow(QMainWindow):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EN-CLIP")
        self.resize(250, 300)
        
        # Used to execute addCredentials automagically when the user acknowledges no existing credentials 
        self.credentials_empty_signal = pyqtSignal()
        
        self.database = database
        self.username = username

        # Create a container widget
        container_widget = QWidget()

        # Create a layout for the container widget
        main_layout = QVBoxLayout(container_widget)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create the clipboard button
        self.clipboard_button = QPushButton("Clipboard")
        #self.clipboard_button.clicked.connect(self.clipboard_data_changed)
        
        # Get the application clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.clipboard_data_changed)
        
        # Create the logins button
        logins_button = QPushButton("Logins")
        logins_button.clicked.connect(self.show_logins)

        # Add the buttons to the button layout
        button_layout.addWidget(self.clipboard_button)
        button_layout.addWidget(logins_button)

        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        # Create a widget for the scroll area content
        self.scroll_content = QWidget()

        # Create a layout for the scroll area content
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Add the scroll area content to the scroll area
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        # Add the button layout and scroll area to the main layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.scroll_area)

        # Set the container widget as the central widget
        self.setCentralWidget(container_widget)

    def clipboard_data_changed(self):

        # Retrieve the clipboard contents
        clipboard_contents = [] 

        # Handle text data
        if self.clipboard.mimeData().hasText():             
            clipboard_contents.append(self.clipboard.text())
        # Handle image data
        if self.clipboard.mimeData().hasImage():
            pixmap = self.clipboard.pixmap()
            if not pixmap.isNull():
                clipboard_contents.append(pixmap)


        # Clear the existing contents in the scroll layout
        #self.clear_scroll_layout()

        # Add the clipboard contents to the scroll layout as separate QLabel widgets
        for content in clipboard_contents:
            if isinstance(content, str):  # If the content is text, create a QLabel with the text
                label = QLabel(content)
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow text selection
            elif isinstance(content, QPixmap):  # If the content is an image, create a QLabel with the image
                graphics_view = QGraphicsView()
                scene = QGraphicsScene()
                scene.addPixmap(content)
                graphics_view.setScene(scene)
                graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)  # Enable dragging of the image
                self.scroll_layout.addWidget(graphics_view)
            else:
                continue  # Skip unsupported data types
        
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow text selection
            self.scroll_layout.addWidget(label)

        # Update the scroll area widget
        self.scroll_area.widget().setLayout(self.scroll_layout)    



    def clear_scroll_layout(self):
        if self.scroll_layout.count():
            #print(self.scroll_layout.count())
            self.item = self.scroll_layout.takeAt(0)
            if self.item.widget():
                self.item.widget().deleteLater()

    def update_scrollable_content(self, clipboard_contents):
        # Clear the existing content in the scrollable area
        if hasattr(self, 'scrollable_area'):
            self.scrollable_area.deleteLater()
        self.scrollable_area = QWidget()
        layout = QVBoxLayout(self.scrollable_area)

        # Create a QLabel widget to display the content
        label = QLabel()
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow text selection
        
        # Convert each tuple to a string and join them with newline characters
        formatted_content = "\n".join("\n".join(item) for item in clipboard_contents)
      
        # Set the text content of the QLabel widget
        label.setText(formatted_content)

        # Add the QLabel widget to the layout
        layout.addWidget(label)

        # Set the scrollable area as the central widget
        self.setCentralWidget(self.scrollable_area)

    def show_logins(self):
        # Retrieve login credentials from the database
        user = UserDBFuncs(self.database)
        credentials = user.show_credentials(self.username)
        if not credentials:
          QMessageBox.information(self, "Credentials Are Empty", "You haven't added any logins yet!!")
          self.add_cred = addCredentials(self.username)
          self.add_cred.show()
        else:
          # Update the scrollable area with the login credentials
          self.update_scrollable_content(credentials)

# Define the add credentials class
class addCredentials(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Website Login")
        layout = QVBoxLayout()
        self.database = database
        self.loggedInUser = username
        
        # Create website label and line edit
        website_label = QLabel("Website:")
        self.website_lineedit = QLineEdit()
        layout.addWidget(website_label)
        layout.addWidget(self.website_lineedit)

        # Create username label and line edit
        username_label = QLabel("Username:")
        self.username_lineedit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_lineedit)

        # Create password label and line edit
        password_label = QLabel("Password:")
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_lineedit)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button)

        # Create cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        # Set the layout
        self.setLayout(layout)


    def submit(self):
         # Retrieve the entered website, username, and password
          website = self.website_lineedit.text()
          webUsername = self.username_lineedit.text()
          password = self.password_lineedit.text()

         # Validate the three fields aren't blank
          if not website or not webUsername or not password:
             QMessageBox.critical(self, "Error", "All Fields Must Be Completed!!")
             return
          else:
            user = UserDBFuncs(self.database)
            user.add_login(self.loggedInUser, website, webUsername, password)
            QMessageBox.information(None, "SUCCESS", "Website Credentials added successfully!!")
         # Accept the dialog and indicate successful user creation
          self.accept()


# Define the Ui_LoginWindow class
class Ui_LoginWindow(QMainWindow):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(250, 300)

        # Create central widget
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create login button
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(75, 60, 100, 28))
        self.loginButton.setObjectName("loginButton")

        # Create new user button
        self.newUserButton = QPushButton(self.centralwidget)
        self.newUserButton.setGeometry(QtCore.QRect(75, 100, 100, 28))
        self.newUserButton.setObjectName("newUserButton")

        # Set central widget
        LoginWindow.setCentralWidget(self.centralwidget)

        # Re-translate the UI components
        self.retranslateUi(LoginWindow)

        # Connect UI components to slots
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    # Define the retranslateUi method
    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "EN-CLIP"))
        self.loginButton.setText(_translate("LoginWindow", "Login"))
        self.newUserButton.setText(_translate("LoginWindow", "New User"))

    # Define the show_new_user_dialog method
    def show_new_user_dialog(self):
        dialog = NewUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # New user created, perform any additional actions
            pass

    def show_user_dialog(self):
        dialog = Login(self)
        if dialog.exec_() == QDialog.Accepted:
          username = dialog.username
          self.user_window = UserWindow(username)
          self.user_window.show()
        self.hide()

# Main entry point
if __name__ == "__main__":
    # Create an instance of the QApplication class
    app = QApplication(sys.argv)

    # Create an instance of the Ui_LoginWindow class
    login_window = Ui_LoginWindow()

    # Set up the user interface components defined in the Ui_LoginWindow class
    login_window.setupUi(login_window)
    
    sys.exit(app.exec_())

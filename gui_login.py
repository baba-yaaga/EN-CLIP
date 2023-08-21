# Import necessary modules
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMenu, QPushButton, QMessageBox, QScrollArea, QLabel, QTextEdit, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5 import QtCore, QtWidgets

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
        self.clipboard_contents = []
        # List to store the row layouts for each credential
        self.row_layouts = []
        # Holds credentials to be deleted from DB
        self.to_be_deleted = []

        # Create a container widget
        container_widget = QWidget()

        # Create a layout for the container widget
        self.main_layout = QVBoxLayout(container_widget)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()

        # Create the clipboard button
        self.clipboard_button = QPushButton("Clipboard")
        
        # Get the application clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard_button.clicked.connect(self.show_clipboard)
        self.clipboard.dataChanged.connect(self.clipboard_data_changed)
        
        # Create the logins button
        self.logins_button = QPushButton("Logins")
        self.logins_button.clicked.connect(self.show_logins)
        
        # Create add credentials button
        self.add_cred_button = QPushButton("+")
        self.add_cred_button.setMaximumSize(25,35)
        self.add_cred_button.clicked.connect(self.add_credentials)

        # Add the buttons to the button layout
        self.button_layout.addWidget(self.clipboard_button)
        self.button_layout.addWidget(self.logins_button)
        self.button_layout.addWidget(self.add_cred_button)

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
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.scroll_area)

        # Set the container widget as the central widget
        self.setCentralWidget(container_widget)

    def clipboard_data_changed(self):
        self.clear_scroll_layout()

        mime_data = self.clipboard.mimeData()
        
        # Handle text data
        if self.clipboard.mimeData().hasText():
            self.clipboard_contents.append(self.clipboard.text())
        # Handle image data
        elif self.clipboard.mimeData().hasImage():
            pixmap = self.clipboard.pixmap()  # This loads the image from the clipboard
            if not pixmap.isNull():
                self.clipboard_contents.append(pixmap)
        self.show_clipboard()
        
    def show_clipboard(self):
        self.clear_scroll_layout()

        # Add the clipboard contents to the scroll layout as separate QLabel widgets
        for content in self.clipboard_contents:
            if isinstance(content, str):  # If the content is text, create a QLabel with the text
                label = QLabel(content)
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
        self.scroll_content.setLayout(self.scroll_layout)

    def clear_layout(self, layout):
        while layout.count():
          item = layout.takeAt(0)
          if item and item.widget():
            widget = item.widget()
            widget.deleteLater()

    def clear_scroll_layout(self):
        # Clear each individual row layout
        for row_layout in self.row_layouts:
            self.clear_layout(row_layout)
        # Clear the scroll layout
        self.clear_layout(self.scroll_layout)

    def update_scrollable_content(self, credentials):
        # Clear the existing content in the scrollable area
        self.clear_scroll_layout()

        for credential in credentials:
            self.row_layout = QHBoxLayout()
            self.label = QLabel()
            self.delete_button = QPushButton("x")
            self.delete_button.setMaximumSize(12, 12)
            # Delete credentials 
            self.delete_button.clicked.connect(self.delete_credentials)
            self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            w, u, p = credential[0], credential[1], credential[2]
            formatted_content = f"WEBSITE: {w}\nUSERNAME: {u}\nPASSWORD: {p}\n"
            self.label.setText(formatted_content)

            self.row_layout.addWidget(self.delete_button)
            self.row_layout.addWidget(self.label)

            self.row_layouts.append(self.row_layout)  # Add the row layout to the list
            self.scroll_layout.addLayout(self.row_layout)

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
          self.clear_scroll_layout()
          self.update_scrollable_content(credentials)

    def add_credentials(self):
        # Retrieve login credentials from the database
        user = UserDBFuncs(self.database)
        self.add_cred = addCredentials(self.username)
        self.add_cred.show()

    def delete_credentials(self, username):
        clicked_button = self.sender()  # Get the delete button that was clicked
        if clicked_button:
          # Find the index of the clicked button
          index = None
        for i, row_layout in enumerate(self.row_layouts):
            delete_button = row_layout.itemAt(0)
            if delete_button and isinstance(delete_button.widget(), QPushButton) and clicked_button == delete_button.widget():
                index = i
                break

        if index is not None:
            row_layout = self.row_layouts[index]
            label_widget = row_layout.itemAt(1).widget()  # Assuming the label is at index 1
            credential_text = label_widget.text()

            lines = credential_text.split('\n')  # Split text into lines
            website = None
            uname = None
                
            for line in lines:
                parts = line.split(':')  # Split line into parts based on colon
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key == "WEBSITE":
                        website = value
                    elif key == "USERNAME":
                            uname = value
                    print(website, uname)
                if website is not None and uname is not None:                    
                    user = UserDBFuncs(self.database)
                    if user.delete_login(self.username, website, uname):
                      print(self.username, website, uname)
                      print(f" second del button {delete_button}")
                
                #for i in range(len(self.row_layouts) - 1, -1, -1):
                # Remove the credential layout at the determined index
                self.clear_layout(self.row_layouts[index])
                # Update the scroll area widget
                self.scroll_content.setLayout(self.scroll_layout)
                
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

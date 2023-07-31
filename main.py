import os, sys, subprocess
from PyQt5.QtWidgets import QApplication
from config import database
from valid_input import Validate
from gui_login import Ui_LoginWindow

from DB import NewUserDBFuncs

# Path to the db_startup.py script
DB_script = '/home/nlh/projects/enClip/db_startup.py'

# Execute db_startup.py to create the database and tables
subprocess.run(['python3', DB_script])

# Create an instance of the QApplication class
app = QApplication(sys.argv)

# Create an instance of the Ui_LoginWindow class
ui = Ui_LoginWindow()
ui.setupUi(ui)

# Connect the clicked signal of the "New User" button to the show_new_user_dialog method
ui.newUserButton.clicked.connect(ui.show_new_user_dialog)

ui.loginButton.clicked.connect(ui.show_user_dialog)

# Show the login window
ui.show()

# Start the application event loop
sys.exit(app.exec_())

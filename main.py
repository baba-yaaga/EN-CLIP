import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication

from user_manager import UserManager
from gui_login import Ui_LoginWindow

# Path to the DB.py script
DB_script = '/home/nlh/projects/enClip/DB.py'

# Execute DB.py to create the database
subprocess.run(['python3', DB_script])

# Create an instance of the UserManager class, passing the path to your database
#user_manager = UserManager(database='/home/nlh/projects/en-clip/en-clip.db')

# Create an instance of the QApplication class
app = QApplication(sys.argv)

# Create an instance of the Ui_LoginWindow class
ui = Ui_LoginWindow()
ui.setupUi(ui)

# Show the login window
ui.show()

# Connect the clicked signal of the "New User" button to the show_new_user_dialog method
ui.newUserButton.clicked.connect(ui.show_new_user_dialog)

# Start the application event loop
sys.exit(app.exec_())

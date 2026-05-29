#|------------------------------------------------------------------------------------------------------------------|#
#| This file contains the class that I will create for my app. I am simply separating it from the                   |#
#| passwordManager.py file so that there is more organization being introduced into the development of this app     |#
#| Author: Daniel Krutsick                                                                                          |#
#|------------------------------------------------------------------------------------------------------------------|#
import base64
import sqlite3
import os
from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui # For creating a GUI
from HashingUtils import keyDerivation, verifyPW
from cryptography.fernet import Fernet

#|------------------------------------------------------------------------------------------------------------------|#
#| This entire section is for helper functions that are designed specifically for the app, unlike HashingUtils.py,  |#
#|  which is specifically designed to help with any functionality of the key derivation of the database             |#
#|------------------------------------------------------------------------------------------------------------------|#
def setupCases() -> Optional[bool]:
    #-- Case 1: The directory and database exists       --#
    #-- Case 2: The directory exists, not the database  --#
    #-- Case 3: The directory and database do not exist --# 
    if(os.path.isfile("./Database/Passwords.db")):
        return True
    elif(os.path.isdir("./Database")):
        return False
    else:
        return

#|------------------------------------------------------------------------------------------------------------------|#
#| Helpful reminder of some of the imports from different Qt library additions                                      |#
#| QtWidgets:                                                                                                       |#
#|      All of the different preset objects that you can place onto the applicatio windows                          |#
#| QtCore:                                                                                                          |#
#|      All of the different options for the styling                                                                |#
#|------------------------------------------------------------------------------------------------------------------|#

class SetupPage(QtWidgets.QWidget):
    passwordAttempt = QtCore.Signal()

    def __init__(self):
        super().__init__()
        
        #-- All of my individual widgets and their defs     --#
        self.text = QtWidgets.QLabel("Please input your desired password for your database: ")
        self.inputPW = QtWidgets.QLineEdit()
        self.inputPW2 = QtWidgets.QLineEdit()
        self.confirmButton = QtWidgets.QPushButton()
        
        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.inputPW)
        self.layout.addWidget(self.inputPW2)
        self.layout.addWidget(self.confirmButton)

        #-- Events that happen on this page                 --#
        self.confirmButton.clicked.connect(self.inputPassword)

    def inputPassword(self):
        if self.inputPW == self.inputPW2:
            self.passwordAttempt.emit()
        else:
            print("Both passwords are incorrect")# Replace with a Qt object later

class ResetPage(QtWidgets.QWidget):
    confirmAttempt = QtCore.Signal()

    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.warningText = QtWidgets.QLabel("Resetting will delete your master password and ALL PASSWORDS IN THE DATABASE!" \
        "\nPlease know this before Confirming your database reset!!(Please enter the phrase \"I CONFIRM\" in the text box below)")
        self.inputConfirm = QtWidgets.QLineEdit()
        self.confirmButton = QtWidgets.QPushButton("Press to confirm")

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.warningText)
        self.layout.addWidget(self.inputConfirm)
        self.layout.addWidget(self.confirmButton)

        #-- Events that happen on this page                 --#
        self.confirmButton.clicked.connect(self.confirmedWipe)

    def confirmedWipe(self):
        if self.inputConfirm == "I CONFIRM":
            self.confirmAttempt.emit()
        else:
            print("Confirmation message incorrect") # Replace with a Qt object later


class NewPasswordPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.pw = QtWidgets.QLineEdit()

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pw)
        
        #-- Events that happen on this page                 --#

#|---------------------------------------|#
#| Page for logging in, self explanatory |#
#|---------------------------------------|#
class LoginPage(QtWidgets.QWidget):
    loginAttempt = QtCore.Signal()

    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.pw = QtWidgets.QLineEdit()
        self.loginButton = QtWidgets.QPushButton("Login")
        self.reset = QtWidgets.QPushButton("RESET PASSWORD")
        self.loginButton.setObjectName("loginButton")

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pw)
        self.layout.addWidget(self.loginButton)

        #-- Events that happen on this page                 --#
        self.loginButton.clicked.connect(self.login)


    def login(self):
        self.loginAttempt.emit()

#|----------------------------------------|#
#| Page for the vault, or after you login |#
#|----------------------------------------|#
class VaultPage(QtWidgets.QWidget):
    logoutSuccess = QtCore.Signal()

    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.passwordButton = QtWidgets.QPushButton("Push to see your passwords")

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.passwordButton)

        #-- Events that happen on this page                 --#
        self.passwordButton.clicked.connect(self.logout)

    def logout(self):
        self.logoutSuccess.emit()

#|----------------------------------------|#
#| The class maintaining the three pages  |#
#|----------------------------------------|#
class Stacks(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #-- Initialization of the stacked widget                    --#
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        #-- Initializing each individual page for the stack         --#
        self.loginPage = LoginPage()
        self.vaultPage = VaultPage()
        self.pwPage = NewPasswordPage()
        self.resetPage = ResetPage()
        self.setupPage = SetupPage()

        #-- Adding all of the widgets onto the stack                --#
        self.stack.addWidget(self.loginPage)
        self.stack.addWidget(self.vaultPage)
        self.stack.addWidget(self.pwPage)
        self.stack.addWidget(self.resetPage)
        self.stack.addWidget(self.setupPage)

        #-- Where the currentIndex is set at by default(Login Page) --#
        self.stack.setCurrentIndex(3)

        #-- All of the receivers for the signals sent by the pages  --#
        self.loginPage.loginAttempt.connect(self.handleLogin)
        self.vaultPage.logoutSuccess.connect(self.handleLogout)
        self.resetPage.confirmAttempt.connect(self.handleWipe)

    #-- What happens when you click the login button. Determines if the input password is correct or not    --#
    def handleLogin(self):
        with sqlite3.connect("./Database/Passwords.db") as conn:
            c = conn.cursor()

            verificationKey = c.execute("SELECT VerificationKey FROM master;")
            verify = verifyPW(verificationKey.fetchone()[0], self.loginPage.pw.text())

            if verify:
                print("It verified the password as correct")
                self.loginPage.pw.clear()
                self.stack.setCurrentIndex(1)
            else:
                print("It verified the password as incorrect")
            conn.commit()
            c.close()
        
    #-- Really easy, it logs you out when you click the button, no further logic                            --#
    def handleLogout(self):
        self.stack.setCurrentIndex(0)
        print("Successfully logged out")
    
    def handleWipe(self):
        with sqlite3.connect("./Database/Passwords.db") as conn:
            c = conn.cursor()

            c.execute("DELETE FROM master;")
            c.execute("DELETE FROM passwords;")

            conn.commit()
            c.close()
    
    def handleSetup(self):
        set = setupCases() # the returned value of what case to do
        match set:
            case True:
                with sqlite3.connect("./Database/Passwords.db") as conn:
                    c = conn.cursor()
                    c.execute("CREATE TABLE master (VerificationKey BLOB, CHECK(length(VerificationKey) = 48));")
                    c.execute("CREATE UNIQUE INDEX one_row_only_uidx ON master ((true));")
                    c.execute("CREATE TABLE passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, Service VARCHAR(255), Email VARCHAR(255), " \
                    "Username BLOB NOT NULL, Password BLOB NOT NULL, CHECK(length(Password) = 120 AND length(Username) = 120));")
                    
                    master = keyDerivation(self.setupPage.inputPW)
                    c.execute("INSERT INTO master (VerificationKey) VALUES (?)", (master,))
                    


                    self.setupPage.inputPW.clear()
                    self.setupPage.inputPW2.clear()

            case False:
                return
            case None:
                return
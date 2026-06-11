#|------------------------------------------------------------------------------------------------------------------|#
#| This file contains the class that I will create for my app. I am simply separating it from the                   |#
#| passwordManager.py file so that there is more organization being introduced into the development of this app     |#
#| Author: Daniel Krutsick                                                                                          |#
#|------------------------------------------------------------------------------------------------------------------|#
import base64 # For encoding into the proper key formatting for the fernet encryption algorithm
import sqlite3 # Library for interacting with the database created
import ctypes # This allows for me to use memset and a few other functions to overwrite buffers and release memory
import os # Used to check for the existence of the Database directory and file
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

# Creates the tables and commits them in the database for the first time someone sets up the password manager
def setupDatabase():
    with sqlite3.connect("./Database/Passwords.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE master (VerificationKey BLOB, CHECK(length(VerificationKey) = 48));")
        c.execute("CREATE UNIQUE INDEX one_row_only_uidx ON master ((true));")
        c.execute("CREATE TABLE passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, Service VARCHAR(255), Email VARCHAR(255), " \
        "Username BLOB NOT NULL, Password BLOB NOT NULL, CHECK(length(Password) = 120 AND length(Username) = 120));")

def insertIntoMaster(pw: str):
    key = keyDerivation(pw)
    with sqlite3.connect("./Database/Passwords.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO master (VerificationKey) VALUES (?)", (key,))

def insertIntoPasswords(pw: str, user: str, service:str, email:Optional[str], encKey:bytes):
    scheme = Fernet(encKey)
    blobPW = scheme.encrypt(pw)
    blobUser = scheme.encrypt(user)

    if email:
        with sqlite3.connect("./Database/Passwords.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO passwords (Service, Email, Username, Password) VALUES (?)", (service, email, blobUser, blobPW,))
    else:
        with sqlite3.connect("./Database/Passwords.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO passwords (Service, Username, Password) VALUES (?)", (service, blobUser, blobPW,))

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
        if self.inputPW.text() == self.inputPW2.text():
            self.passwordAttempt.emit()
        else:
            print("Both passwords are not the same")# Replace with a Qt object later

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
        if self.inputConfirm.text() == "I CONFIRM":
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
    resetClicked = QtCore.Signal()
    setupClicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.pw = QtWidgets.QLineEdit()
        self.loginButton = QtWidgets.QPushButton("Login")
        self.loginButton.setObjectName("loginButton")
        self.resetButton = QtWidgets.QPushButton("Click to Reset Database")
        self.setupButton = QtWidgets.QPushButton("Setup Password")
        self.errorMessage = QtWidgets.QLabel()

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pw)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.resetButton)
        self.layout.addWidget(self.setupButton)
        self.layout.addWidget(self.errorMessage)

        #-- Events that happen on this page                 --#
        self.loginButton.clicked.connect(self.login)
        self.resetButton.clicked.connect(self.reset)
        self.setupButton.clicked.connect(self.setup)

    def reset(self):
        self.resetClicked.emit()

    def login(self):
        self.loginAttempt.emit()
    
    def setup(self):
        self.setupClicked.emit()

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
    __key = None

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
        self.stack.addWidget(self.loginPage) # Index 0
        self.stack.addWidget(self.vaultPage) # Index 1
        self.stack.addWidget(self.pwPage)    # Index 2
        self.stack.addWidget(self.resetPage) # Index 3
        self.stack.addWidget(self.setupPage) # Index 4

        #-- Where the currentIndex is set at by default(Login Page) --#
        self.stack.setCurrentIndex(0)

        #-- All of the receivers for the signals sent by the pages  --#
        self.loginPage.loginAttempt.connect(self.handleLogin)
        self.loginPage.resetClicked.connect(self.resetClick)
        self.loginPage.setupClicked.connect(self.setupClick)
        self.vaultPage.logoutSuccess.connect(self.handleLogout)
        self.resetPage.confirmAttempt.connect(self.handleWipe)
        self.setupPage.passwordAttempt.connect(self.handleSetup)

    def setupClick(self):
        self.loginPage.pw.clear()
        self.loginPage.errorMessage.clear()
        self.stack.setCurrentIndex(4)

    def resetClick(self):
        self.loginPage.pw.clear()
        self.stack.setCurrentIndex(3)

    #-- What happens when you click the login button. Determines if the input password is correct or not        --#
    def handleLogin(self):
        try:
            with sqlite3.connect("./Database/Passwords.db") as conn:
                c = conn.cursor()

                verificationKey = c.execute("SELECT VerificationKey FROM master;")
                encKey = verifyPW(verificationKey.fetchone()[0], self.loginPage.pw.text())

                if encKey:
                    print("It verified the password as correct") # Remove this after testing is done
                    self.loginPage.pw.clear()
                    self.stack.setCurrentIndex(1)
                    encKey = base64.urlsafe_b64encode(encKey)
                    self.__key = encKey
                    return
                else:
                    print("It verified the password as incorrect") # Replace with a qt object
        except TypeError:
            errMsg = "There is no password setup for the password manager. Please click the setup button to create a password."
        self.loginPage.errorMessage.setText(errMsg)
            
    #-- Handles how to input a new password into the database along with its relational information             --#
    def handleNewPW():

        return
    
    #-- Really easy, it logs you out when you click the button, no further logic                                --#
    def handleLogout(self):
        self.stack.setCurrentIndex(0)
        # Fill this with more functions clearing the appropriate data for security purposes
        ctypes.memset(self.__key, 0, len(self.__key))
        print("Successfully logged out")
    
    def handleWipe(self):
        with sqlite3.connect("./Database/Passwords.db") as conn:
            c = conn.cursor()

            c.execute("DELETE FROM master;")
            c.execute("DELETE FROM passwords;")
        self.stack.setCurrentIndex(0) # Back to Login
    
    #-- Handles how to setup the database. Refer back to helper functions at the top for which each case means  --#
    def handleSetup(self):
        set = setupCases() # the returned value of what case to do
        match set:
            case True:
                insertIntoMaster(self.setupPage.inputPW.text())

                self.setupPage.inputPW.clear()
                self.setupPage.inputPW2.clear()
            case False:
                os.open("./Database/Passwords.db", "x")
                os.close()
                setupDatabase()
                insertIntoMaster(self.setupPage.inputPW.text())

                self.setupPage.inputPW.clear()
                self.setupPage.inputPW2.clear()
            case None:
                os.mkdir("./Database")
                os.open("./Database/Passwords.db", "x")
                os.close()
                setupDatabase()
                insertIntoMaster(self.setupPage.inputPW.text())

                self.setupPage.inputPW.clear()
                self.setupPage.inputPW2.clear()
        self.stack.setCurrentIndex(0) # Back to Login
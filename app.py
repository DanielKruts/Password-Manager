#|------------------------------------------------------------------------------------------------------------------|#
#| This file contains the class that I will create for my app. I am simply separating it from the                   |#
#| passwordManager.py file so that there is more organization being introduced into the development of this app     |#
#| Author: Daniel Krutsick                                                                                          |#
#|------------------------------------------------------------------------------------------------------------------|#
import base64
import sqlite3
from PySide6 import QtCore, QtWidgets, QtGui # For creating a GUI
from HashingUtils import keyDerivation, verifyPW
from cryptography.fernet import Fernet

#|------------------------------------------------------------------------------------------------------------------|#
#| Helpful reminder of some of the imports from different Qt library additions                                      |#
#| QtWidgets:                                                                                                       |#
#|      All of the different preset objects that you can place onto the applicatio windows                          |#
#| QtCore:                                                                                                          |#
#|      All of the different options for the styling                                                                |#
#|------------------------------------------------------------------------------------------------------------------|#

class NewPasswordPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #-- All of my individual widgets and their defs     --#
        self.pw = QtWidgets.QInputDialog()

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
        self.loginButton = QtWidgets.QPushButton()

        #-- All of the widgets added to this page           --#
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.pw)

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

        #-- Adding all of the widgets onto the stack                --#
        self.stack.addWidget(self.loginPage)
        self.stack.addWidget(self.vaultPage)
        self.stack.addWidget(self.pwPage)

        #-- Where the currentIndex is set at by default(Login Page) --#
        self.stack.setCurrentIndex(0)

        #-- All of the receivers for the signals sent by the pages  --#
        self.loginPage.loginAttempt.connect(self.handleLogin)
        self.vaultPage.logoutSuccess.connect(self.handleLogout)

    #-- What happens when you click the login button. Determines if the input password is correct or not    --#
    def handleLogin(self):
        with sqlite3.connect("./Database/Passwords.db") as conn:
            c = conn.cursor()

            verificationKey = c.execute("SELECT VerificationKey FROM master;")
            verify = verifyPW(verificationKey.fetchone()[0], self.loginPage.pw.text())

            if verify:
                print("It verified the password as correct")
                self.stack.setCurrentIndex(1)
            else:
                print("It verified the password as incorrect")
            conn.commit()
            c.close()
        
    #-- Really easy, it logs you out when you click the button, no further logic                            --#
    def handleLogout(self):
        self.stack.setCurrentIndex(0)
        print("Successfully logged out")
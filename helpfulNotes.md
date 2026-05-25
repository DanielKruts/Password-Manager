# Encrypting into a urlsafe encoding for Fernet
```
encryptionKey = base64.urlsafe_b64encode(verifyPW(verification, "My amazing password"))
f = Fernet(encryptionKey)
token = f.encrypt(b"This whole message")
```

# Example of inserting into the database using sqlite
```
verification = keyDerivation("My amazing password")
connection = sqlite3.connect("./Database/Passwords.db")
c = connection.cursor()

c.execute("INSERT INTO master (VerificationKey) VALUES (?);", (verification,))
connection.commit()
c.close()
```

# Example of how to structure a widget class in the PySide6 library
```
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
```
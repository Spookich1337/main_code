import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        button = QPushButton("Привет")
        button.clicked.connect(self.say_hi)
        layout.addWidget(button)

        button = QPushButton("Выйти")
        button.clicked.connect(self.close)
        layout.addWidget(button)

        self.setWindowTitle("Привет")
        self.show()

    def say_hi(self):
        print("Привет, мир!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
import PyQt6.QtWidgets
import PyQt6.QtCore
import sys

from database import Database

w = PyQt6.QtWidgets
c = PyQt6.QtCore

check = False
db = Database("test_bouquet_store.db")
user = ""

class AuthWindow(w.QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Auth Panel")

        self.setup_window()

        self.setup_widgets()

    def setup_widgets(self):

        # Поле логина
        self.log_label = w.QLabel("Логин", self)
        self.login = w.QLineEdit(self)

        # Поле пароля
        self.pass_label = w.QLabel("Пароль", self)
        self.password = w.QLineEdit(self)

        # Кнопка
        self.button = w.QPushButton("Register", self)
        self.button.clicked.connect(self.login_acc)

        # Лэйаут
        layout = w.QVBoxLayout()
        layout.addWidget(self.log_label)
        layout.addWidget(self.login)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setup_window(self):
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.resize(250, 100)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.size().height() / 2))
        self.setGeometry(window_pos.x(), window_pos.y(), 250, 100)

    def login_acc(self):
        global user
        user = db.get_user_by_login(self.login.text())
        global check
        if user and self.password.text() == user["password"]:
            check = True
            self.close()

    def closeEvent(self, event):
        if not check:
            sys.exit()
        else:
            from main import MainWindow
            self.close()
            self.window = MainWindow(user_data=user)


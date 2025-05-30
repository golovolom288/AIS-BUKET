import PyQt6.QtWidgets
import PyQt6.QtCore

import sys

from seller import SellerWindow

w = PyQt6.QtWidgets
c = PyQt6.QtCore


class MainWindow(w.QMainWindow):

    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("Main page")

        if user_data == "admin":
            from admin import AdminWindow
            self.window = AdminWindow()
            self.window.show()
        elif user_data == "seller":
            self.window = SellerWindow()
            self.window.show()
        else:
            self.auth_function()

    def auth_function(self):
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()


if __name__ == "__main__":
    app = w.QApplication(sys.argv)
    window = MainWindow("r")
    app.exec()

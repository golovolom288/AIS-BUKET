import PyQt6.QtWidgets
import PyQt6.QtCore

import sys

from manager import ManagerWindow
from seller import SellerWindow
from database import Database

w = PyQt6.QtWidgets
c = PyQt6.QtCore
db = Database("test_bouquet_store.db")


class MainWindow(w.QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("Main page")
        if not db.get_user_by_login("admin"):
            db.add_user('admin', 'admin', 'Иванов И.И.', 'admin', 'Главный администратор', 60000, 0)
        try:
            if user_data["role"] == "admin":
                from admin import AdminWindow
                self.window = AdminWindow(user_data)
                self.window.show()
        #     elif user_data == "seller":
        #         self.window = SellerWindow()
        #         self.window.show()
        #     elif user_data == "manager":
        #         self.window = ManagerWindow()
        #         self.window.show()
        except Exception:
            self.auth_function()

    def auth_function(self):
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()


if __name__ == "__main__":
    app = w.QApplication(sys.argv)
    window = MainWindow("r")
    app.exec()

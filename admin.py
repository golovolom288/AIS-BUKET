import PyQt6.QtWidgets
import PyQt6.QtCore

from database import Database

w = PyQt6.QtWidgets
c = PyQt6.QtCore
db = Database()
table_users_columns = [
    'id',
    'login',
    'full_name',
    'role',
    'salary'
]
table_results_columns = [
    'id',
    'user_id',
    'sale_date',
    'total_amount',
]
user_data = ""


class AdminWindow(w.QWidget):

    def __init__(self, user):
        super().__init__()

        global user_data
        user_data = user
        self.setWindowTitle(f"{user_data['position']} - {user_data['full_name']}")

        self.setup_window()

        self.setup_widgets()

    def setup_window(self):
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.resize(1000, 700)
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.size().height() / 2))
        self.setGeometry(window_pos.x(), window_pos.y(), 1000, 700)

    def setup_widgets(self):
        acc_change_btn = w.QPushButton("Сменить аккаунт", self)
        acc_change_btn.clicked.connect(self.change_acc)
        acc_change_btn.setFixedSize(130, 30)
        main_layout = w.QVBoxLayout(self)
        main_layout.addWidget(acc_change_btn, alignment=c.Qt.AlignmentFlag.AlignRight)
        self.setLayout(main_layout)

        tab = w.QTabWidget(self)
        tab.resize(self.size().width()-5, int(self.size().height()*0.9))
        tab.move(5, self.size().height() - tab.size().height()-5)
        tab.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # staff page

        staff_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        staff_page.setLayout(layout)

        button_add = w.QPushButton("Добавить", self)
        button_add.setFixedSize(100, 35)
        button_add.clicked.connect(self.create_add_user_form)
        button_change = w.QPushButton("Редактировать", self)
        button_change.setFixedSize(100, 35)
        button_change.clicked.connect(self.create_change_user_form)
        button_remove = w.QPushButton("Удалить", self)
        button_remove.setFixedSize(100, 35)
        button_remove.clicked.connect(self.create_delete_user_form)
        button_salary = w.QPushButton("Рассчитать зарплату", self)
        button_salary.setFixedSize(130, 35)
        button_salary.clicked.connect(self.result_salary)

        layout.addWidget(button_add, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_change, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_remove, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_salary, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)
        table = w.QTableWidget(len(db.get_model("users")), 5)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(5):
            table.setColumnWidth(i, int((table.size().width() - 20) / 5))
            table.setRowHeight(i, 15)
        for i in range(len(db.get_model("users"))):
            for j in range(5):
                table.setItem(i, j, w.QTableWidgetItem(str(db.get_model("users")[i][table_users_columns[j]])))
        table.setHorizontalHeaderLabels(["ID", "Логин", "Имя", "Роль", "Оклад"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table, 3, 3)
        layout.addChildLayout(table_layout)

        # results page

        results_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        results_page.setLayout(layout)

        label1 = w.QLabel("Период: ")
        label1.setStyleSheet("font-size: 18px; margin-top: 5px")
        
        start_date = w.QLineEdit()
        start_date.setFixedSize(100, 35)
        start_date.setStyleSheet("font-size: 18px; margin-top: 5px")
        
        label2 = w.QLabel("по")
        label2.setStyleSheet("font-size: 18px; margin-top: 5px")
        
        final_date = w.QLineEdit()
        final_date.setFixedSize(100, 35)
        final_date.setStyleSheet("font-size: 18px; margin-top: 5px")
        
        results_btn = w.QPushButton("Сформировать", self)
        results_btn.setFixedSize(130, 40)

        layout.addWidget(label1, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(start_date, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label2, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(final_date, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(results_btn, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)

        table = w.QTableWidget(len(db.get_model("sales")), 4)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(4):
            table.setColumnWidth(i, int((table.size().width() - 25) / 4))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["Дата", "Продавец", "Сумма", "Количество"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table, 1, 3)
        layout.addChildLayout(table_layout)



        # add pane to the tab widget
        tab.addTab(staff_page, 'Сотрудники')
        tab.addTab(results_page, 'Отчёты')

        main_layout.addWidget(tab)

    def change_acc(self):
        self.close()
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()

    def create_add_user_form(self):
        def add_user():
            salary = 0
            percent = 0
            if not login_edit.text() or not password_edit.text():
                self.window.close()
                self.window = AdminWindow(user_data)
                self.window.show()
                return
            if salary_edit.text():
                salary = float(salary_edit.text())
            if percent_edit.text():
                percent = percent_edit.text()
            db.add_user(
                login_edit.text(),
                password_edit.text(),
                fio_edit.text(),
                role_edit.currentText(),
                pos_edit.text(),
                salary,
                percent
            )
            self.window.close()
            self.window = AdminWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма добавления пользователя')
        self.window.setMinimumSize(200, 250)
        self.window.setMaximumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Логин:')
        login_edit = w.QLineEdit()

        label2 = w.QLabel('Пароль:')
        password_edit = w.QLineEdit()

        label3 = w.QLabel('ФИО:')
        fio_edit = w.QLineEdit()

        label4 = w.QLabel('Роль:')
        role_edit = w.QComboBox()
        role_edit.addItems(["admin", "manager", "seller"])

        label5 = w.QLabel('Пост:')
        pos_edit = w.QLineEdit()

        label6 = w.QLabel('Оклад:')
        salary_edit = w.QLineEdit()

        label7 = w.QLabel('Процент продаж:')
        percent_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(add_user)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, login_edit)
        layout.addRow(label2, password_edit)
        layout.addRow(label3, fio_edit)
        layout.addRow(label4, role_edit)
        layout.addRow(label5, pos_edit)
        layout.addRow(label6, salary_edit)
        layout.addRow(label7, percent_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_change_user_form(self):
        def change_user():
            id = 0
            salary = 0
            percent = 0
            for user in db.get_model("users"):
                if user["login"] == login_edit.currentText():
                    id = user["id"]
            if salary_edit.text():
                salary = float(salary_edit.text())
            if percent_edit.text():
                percent = percent_edit.text()
            db.update_user(
                id,
                login_edit.currentText(),
                password_edit.text(),
                fio_edit.text(),
                role_edit.currentText(),
                pos_edit.text(),
                salary,
                percent,
            )
            self.window.close()
            self.window = AdminWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма изменения пользователя')
        self.window.setMaximumSize(200, 250)
        self.window.setMinimumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Логин:')
        login_edit = w.QComboBox()
        for user in db.get_model("users"):
            if user != user_data:
                login_edit.addItem(user["login"])

        label2 = w.QLabel('Пароль:')
        password_edit = w.QLineEdit()

        label3 = w.QLabel('ФИО:')
        fio_edit = w.QLineEdit()

        label4 = w.QLabel('Роль:')
        role_edit = w.QComboBox()
        role_edit.addItems(["admin", "manager", "seller"])

        label5 = w.QLabel('Пост:')
        pos_edit = w.QLineEdit()

        label6 = w.QLabel('Оклад:')
        salary_edit = w.QLineEdit()

        label7 = w.QLabel('Процент продаж:')
        percent_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(change_user)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, login_edit)
        layout.addRow(label2, password_edit)
        layout.addRow(label3, fio_edit)
        layout.addRow(label4, role_edit)
        layout.addRow(label5, pos_edit)
        layout.addRow(label6, salary_edit)
        layout.addRow(label7, percent_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_delete_user_form(self):
        def delete_user():
            db.delete_user(db.get_user_by_login(login_edit.currentText())["id"])
            self.window.close()
            self.window = AdminWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма удаления пользователя')
        self.window.setMinimumSize(200, 100)
        self.window.setMaximumSize(200, 100)
        self.window.resize(200, 100)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Логин:')
        login_edit = w.QComboBox()
        for user in db.get_model("users"):
            if user != user_data:
                login_edit.addItem(user["login"])

        delete_button = w.QPushButton("Удалить")
        delete_button.clicked.connect(delete_user)
        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, login_edit)
        layout.addRow(delete_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def result_salary(self):
        def get_result(login):
            selected_user = ""
            for user in db.get_model("users"):
                if user["login"] == login:
                    selected_user = user
            self.window.close()
            self.window = w.QWidget()
            screen_size = None
            for screen in w.QApplication.screens():
                screen_size = screen.size()
            self.window.setWindowTitle('Форма расчёта з/п пользователя')
            self.window.setMinimumSize(200, 200)
            self.window.setMaximumSize(200, 200)
            self.window.resize(200, 200)
            window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                                  int(screen_size.height() / 2) - int(self.window.size().height() / 2))
            self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

            # Создать экземпляр QFormLayout
            layout = w.QFormLayout()

            # Создать виджеты для формы
            label1 = w.QLabel('Логин: ' + str(selected_user["login"]))
            label2 = w.QLabel('Процент продаж: ' + str(selected_user["sales_percent"]))
            label3 = w.QLabel('Оклад: ' + str(selected_user["salary"]))
            label_result = w.QLabel(str(selected_user["salary"] + selected_user["salary"]*selected_user["sales_percent"]/100))
            exit_button = w.QPushButton("ОК")
            exit_button.clicked.connect(self.exit_from_form)

            # Добавить виджеты в QFormLayout
            layout.addRow(label1)
            layout.addRow(label2)
            layout.addRow(label3)
            layout.addRow(label_result)
            layout.addRow(exit_button)

            self.window.setLayout(layout)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма расчёта з/п пользователя')
        self.window.setMinimumSize(200, 200)
        self.window.setMaximumSize(200, 200)
        self.window.resize(200, 200)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Логин:')
        login_edit = w.QComboBox()
        label2 = w.QLabel('Начальная дата:')
        label3 = w.QLabel('Конечная дата:')
        for user in db.get_model("users"):
            login_edit.addItem(user["login"])
        start_date = w.QDateEdit()
        end_date = w.QDateEdit()

        result_button = w.QPushButton("Рассчитать")
        result_button.clicked.connect(lambda: get_result(login_edit.currentText()))
        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, login_edit)
        layout.addRow(label2, start_date)
        layout.addRow(label3, end_date)
        layout.addRow(result_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def exit_from_form(self):
        self.window.close()
        self.window = AdminWindow(user_data)
        self.window.show()





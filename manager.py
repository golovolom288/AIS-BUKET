import PyQt6.QtWidgets
import PyQt6.QtCore

import sys

from database import Database

w = PyQt6.QtWidgets
c = PyQt6.QtCore
db = Database()
table_products_columns = [
    'id',
    'article',
    'name',
    'supplier_id',
    'description',
    'price',
    'quantity'
]
table_supplier_columns = [
    'id',
    'name',
    'contact_person',
    'phone',
    'email',
    'address'
]
user_data = ""


class ManagerWindow(w.QWidget):

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
        tab.resize(self.size().width() - 5, int(self.size().height() * 0.9))
        tab.move(5, self.size().height() - tab.size().height() - 5)
        tab.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # products page

        staff_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        staff_page.setLayout(layout)

        button_add_flowers = w.QPushButton("Добавить цветы", self)
        button_add_flowers.setFixedSize(100, 35)
        button_add_flowers.clicked.connect(self.create_add_flowers_form)

        button_change_flowers = w.QPushButton("Редактировать", self)
        button_change_flowers.setFixedSize(100, 35)
        button_change_flowers.clicked.connect(self.create_change_flowers_form)

        button_remove = w.QPushButton("Удалить", self)
        button_remove.setFixedSize(130, 35)
        button_remove.clicked.connect(self.create_delete_flowers_form)

        layout.addWidget(button_add_flowers, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_change_flowers, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_remove, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)

        table = w.QTableWidget(len(db.get_model("products")), 7)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(7):
            table.setColumnWidth(i, int((table.size().width()) / 7))
            table.setRowHeight(i, 15)
        for i in range(len(db.get_model("products"))):
            for j in range(7):
                if table_products_columns[j] == "supplier_id":
                    for supplier in db.get_model("suppliers"):
                        if supplier["id"] == db.get_model("products")[i][table_products_columns[j]]:
                            table.setItem(i, j, w.QTableWidgetItem(supplier["name"]))
                else:
                    table.setItem(i, j, w.QTableWidgetItem(str(db.get_model("products")[i][table_products_columns[j]])))
        table.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Поставщик", "Описание", "Цена", "Количество"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table, 3, 3)
        layout.addChildLayout(table_layout)

        # supplier page

        supplier_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        supplier_page.setLayout(layout)

        button_add_supplier = w.QPushButton("Добавить", self)
        button_add_supplier.setFixedSize(100, 35)
        button_add_supplier.clicked.connect(self.create_add_supplier_form)
        button_change_supplier = w.QPushButton("Редактировать", self)
        button_change_supplier.setFixedSize(100, 35)
        button_change_supplier.clicked.connect(self.create_change_supplier_form)
        button_remove = w.QPushButton("Удалить", self)
        button_remove.setFixedSize(100, 35)
        button_remove.clicked.connect(self.create_delete_supplier_form)

        layout.addWidget(button_add_supplier, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_change_supplier, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_remove, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)

        table = w.QTableWidget(len(db.get_model("suppliers")), 6)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(len(db.get_model("suppliers"))):
            table.setColumnWidth(i, int((table.size().width()-30) / 6))
            table.setRowHeight(i, 15)
            for j in range(6):
                table.setItem(i, j, w.QTableWidgetItem(str(db.get_model("suppliers")[i][table_supplier_columns[j]])))
        table.setHorizontalHeaderLabels(["ID", "Название", "Контактное лицо", "Телефон", "Email", "Адрес"])
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

        table = w.QTableWidget(3, 4)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(4):
            table.setColumnWidth(i, int((table.size().width() - 25) / 4))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["Дата", "Продавец", "Сумма", "Количество"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table, 1, 3)
        layout.addChildLayout(table_layout)

        # add pane to the tab widget
        tab.addTab(staff_page, 'Товары')
        tab.addTab(supplier_page, 'Поставщики')
        tab.addTab(results_page, 'Отчёты')

        main_layout.addWidget(tab)

    def change_acc(self):
        self.close()
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()

    def create_add_flowers_form(self):
        def add_flowers():
            quantity = 0
            supplier_id = 0
            if not article_edit.text() or not name_edit.text() or not price_edit.text() or not quantity_edit.text():
                self.window.close()
                self.window = ManagerWindow(user_data)
                self.window.show()
                return
            for supplier in db.get_model("suppliers"):
                if supplier["name"] == supplier_id_edit.currentText():
                    supplier_id = supplier["id"]
            if quantity_edit.text():
                quantity = quantity_edit.text()
            db.add_product(
                article_edit.text(),
                name_edit.text(),
                supplier_id,
                description_edit.text(),
                int(price_edit.text()),
                quantity,
                photo_path_edit.text(),
            )
            self.window.close()
            self.window = ManagerWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма добавления цветов')
        self.window.setMinimumSize(200, 250)
        self.window.setMaximumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Артикл:')
        article_edit = w.QLineEdit()

        label2 = w.QLabel('Название:')
        name_edit = w.QLineEdit()

        label3 = w.QLabel('Поставщик:')
        supplier_id_edit = w.QComboBox()
        for supplier in db.get_model("suppliers"):
            supplier_id_edit.addItem(supplier["name"])

        label4 = w.QLabel('Описание:')
        description_edit = w.QLineEdit()

        label5 = w.QLabel('Цена:')
        price_edit = w.QLineEdit()

        label6 = w.QLabel('Фотография:')
        photo_path_edit = w.QLineEdit()

        label7 = w.QLabel('Количество:')
        quantity_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(add_flowers)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, article_edit)
        layout.addRow(label2, name_edit)
        layout.addRow(label3, supplier_id_edit)
        layout.addRow(label4, description_edit)
        layout.addRow(label5, price_edit)
        layout.addRow(label6, photo_path_edit)
        layout.addRow(label7, quantity_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_change_flowers_form(self):
        def change_flowers():
            quantity = 0
            supplier_id = 0
            id = 0
            price = 0
            if price_edit.text():
                price = int(price_edit.text())
            for supplier in db.get_model("suppliers"):
                if supplier["name"] == supplier_id_edit.currentText():
                    supplier_id = supplier["id"]
            for product in db.get_model("products"):
                if product["article"] == article_edit.currentText():
                    id = product["id"]
            if quantity_edit.text():
                quantity = quantity_edit.text()
            db.update_product(
                id,
                article_edit.currentText(),
                name_edit.text(),
                supplier_id,
                description_edit.text(),
                price,
                quantity,
                photo_path_edit.text(),
            )
            self.window.close()
            self.window = ManagerWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма добавления цветов')
        self.window.setMinimumSize(200, 250)
        self.window.setMaximumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Артикл:')
        article_edit = w.QComboBox()
        for article in db.get_model("products"):
            article_edit.addItem(article["article"])

        label2 = w.QLabel('Название:')
        name_edit = w.QLineEdit()

        label3 = w.QLabel('Поставщик:')
        supplier_id_edit = w.QComboBox()
        for supplier in db.get_model("suppliers"):
            supplier_id_edit.addItem(supplier["name"])

        label4 = w.QLabel('Описание:')
        description_edit = w.QLineEdit()

        label5 = w.QLabel('Цена:')
        price_edit = w.QLineEdit()

        label6 = w.QLabel('Фотография:')
        photo_path_edit = w.QLineEdit()

        label7 = w.QLabel('Количество:')
        quantity_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(change_flowers)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, article_edit)
        layout.addRow(label2, name_edit)
        layout.addRow(label3, supplier_id_edit)
        layout.addRow(label4, description_edit)
        layout.addRow(label5, price_edit)
        layout.addRow(label6, photo_path_edit)
        layout.addRow(label7, quantity_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_delete_flowers_form(self):
        def delete_flowers():
            db.delete_product(db.get_product_by_article(article_edit.currentText())["id"])
            self.window.close()
            self.window = ManagerWindow(user_data)
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
        label1 = w.QLabel('Артикул:')
        article_edit = w.QComboBox()
        for product in db.get_model("products"):
            if product != user_data:
                article_edit.addItem(product["article"])

        delete_button = w.QPushButton("Удалить")
        delete_button.clicked.connect(delete_flowers)
        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, article_edit)
        layout.addRow(delete_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_change_supplier_form(self):
        def add_supplier():
            id = 0
            if not phone_edit.text() or not contact_person_edit.text() or not address_edit.text() or not email_edit:
                self.window.close()
                self.window = ManagerWindow(user_data)
                self.window.show()
                return
            for supplier in db.get_model("suppliers"):
                if supplier["name"] == name_edit.currentText():
                    id = supplier["id"]
            db.update_supplier(
                id,
                name_edit.currentText(),
                contact_person_edit.text(),
                phone_edit.text(),
                email_edit.text(),
                address_edit.text(),
            )
            self.window.close()
            self.window = ManagerWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма добавления цветов')
        self.window.setMinimumSize(200, 250)
        self.window.setMaximumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Название:')
        name_edit = w.QComboBox()
        for supplier in db.get_model("suppliers"):
            name_edit.addItem(supplier["name"])

        label2 = w.QLabel('Контактное лицо:')
        contact_person_edit = w.QLineEdit()

        label3 = w.QLabel('Номер телефона:')
        phone_edit = w.QLineEdit()

        label4 = w.QLabel('Эл. почта:')
        email_edit = w.QLineEdit()

        label5 = w.QLabel('Адрес:')
        address_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(add_supplier)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, name_edit)
        layout.addRow(label2, contact_person_edit)
        layout.addRow(label3, phone_edit)
        layout.addRow(label4, email_edit)
        layout.addRow(label5, address_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_add_supplier_form(self):
        def add_supplier():
            if not name_edit.text() or not phone_edit.text() or not contact_person_edit.text() or not address_edit.text() or not email_edit:
                self.window.close()
                self.window = ManagerWindow(user_data)
                self.window.show()
                return

            db.add_supplier(
                name_edit.text(),
                contact_person_edit.text(),
                phone_edit.text(),
                email_edit.text(),
                address_edit.text(),
            )
            self.window.close()
            self.window = ManagerWindow(user_data)
            self.window.show()

        self.close()
        self.window = w.QWidget()
        screen_size = None
        for screen in w.QApplication.screens():
            screen_size = screen.size()
        self.window.setWindowTitle('Форма добавления цветов')
        self.window.setMinimumSize(200, 250)
        self.window.setMaximumSize(200, 250)
        self.window.resize(200, 250)
        window_pos = c.QPoint(int(screen_size.width() / 2) - int(self.window.size().width() / 2),
                              int(screen_size.height() / 2) - int(self.window.size().height() / 2))
        self.window.setGeometry(window_pos.x(), window_pos.y(), 250, 200)

        # Создать экземпляр QFormLayout
        layout = w.QFormLayout()

        # Создать виджеты для формы
        label1 = w.QLabel('Название:')
        name_edit = w.QLineEdit()

        label2 = w.QLabel('Контактное лицо:')
        contact_person_edit = w.QLineEdit()

        label3 = w.QLabel('Номер телефона:')
        phone_edit = w.QLineEdit()

        label4 = w.QLabel('Эл. почта:')
        email_edit = w.QLineEdit()

        label5 = w.QLabel('Адрес:')
        address_edit = w.QLineEdit()

        save_button = w.QPushButton("Сохранить")
        save_button.clicked.connect(add_supplier)

        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, name_edit)
        layout.addRow(label2, contact_person_edit)
        layout.addRow(label3, phone_edit)
        layout.addRow(label4, email_edit)
        layout.addRow(label5, address_edit)
        layout.addRow(save_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def create_delete_supplier_form(self):
        def delete_flowers():
            db.delete_product(db.get_product_by_article(name_edit.currentText())["id"])
            self.window.close()
            self.window = ManagerWindow(user_data)
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
        label1 = w.QLabel('Артикул:')
        name_edit = w.QComboBox()
        for supplier in db.get_model("suppliers"):
            name_edit.addItem(supplier["name"])

        delete_button = w.QPushButton("Удалить")
        delete_button.clicked.connect(delete_flowers)
        exit_button = w.QPushButton("Отмена")
        exit_button.clicked.connect(self.exit_from_form)

        # Добавить виджеты в QFormLayout
        layout.addRow(label1, name_edit)
        layout.addRow(delete_button)
        layout.addRow(exit_button)

        self.window.setLayout(layout)
        self.window.show()

    def exit_from_form(self):
        self.window.close()
        self.window = ManagerWindow(user_data)
        self.window.show()


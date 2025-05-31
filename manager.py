import PyQt6.QtWidgets
import PyQt6.QtCore

import sys

w = PyQt6.QtWidgets
c = PyQt6.QtCore


class ManagerWindow(w.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AdminPanel")

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

        button_add_bouquet = w.QPushButton("Добавить букет", self)
        button_add_bouquet.setFixedSize(100, 35)

        button_change = w.QPushButton("Редактировать", self)
        button_change.setFixedSize(100, 35)

        button_remove = w.QPushButton("Удалить", self)
        button_remove.setFixedSize(130, 35)

        layout.addWidget(button_add_flowers, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_add_bouquet, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_change, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_remove, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)

        table = w.QTableWidget(3, 7)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(5):
            table.setColumnWidth(i, int((table.size().width()+70) / 7))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Количество", "Поставщик"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table, 3, 3)
        layout.addChildLayout(table_layout)

        # supplier page

        supplier_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        supplier_page.setLayout(layout)

        button_add = w.QPushButton("Добавить", self)
        button_add.setFixedSize(100, 35)
        button_change = w.QPushButton("Редактировать", self)
        button_change.setFixedSize(100, 35)
        button_remove = w.QPushButton("Удалить", self)
        button_remove.setFixedSize(100, 35)

        layout.addWidget(button_add, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_change, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(button_remove, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)

        table = w.QTableWidget(3, 5)
        table.setGeometry(10, 70, self.size().width() - 25, 500)
        for i in range(5):
            table.setColumnWidth(i, int((table.size().width()-30) / 5))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["ID", "Название", "Контактное лицо", "Телефон", "Email"])
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


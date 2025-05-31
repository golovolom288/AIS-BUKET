import PyQt6.QtWidgets
import PyQt6.QtCore

import sys

w = PyQt6.QtWidgets
c = PyQt6.QtCore


class SellerWindow(w.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SellerPanel")

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

        # sells page

        staff_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        staff_page.setLayout(layout)
        label_search = w.QLabel("Поиск: ")
        label_search.setStyleSheet("font-size: 18px;")
        search = w.QLineEdit()
        search.setStyleSheet("margin-top: 3px")
        search.setFixedSize(200, 25)
        label_shop = w.QLabel("Корзина")
        label_shop.setStyleSheet("font-size: 18px; margin-left: 490px")
        layout.addWidget(label_search, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(search, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label_shop, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)
        table_products = w.QTableWidget(3, 6)
        table_products.setGeometry(10, 60, int(self.size().width()*0.6), 500)
        for i in range(6):
            table_products.setColumnWidth(i, int((table_products.size().width()-15) / 6))
            table_products.setRowHeight(i, 15)
        table_products.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Остаток"])
        table_shop = w.QTableWidget(3, 4)
        table_shop.setGeometry(self.size().width()-350, 60, int(self.size().width() * 0.3), 500)
        for i in range(4):
            table_shop.setColumnWidth(i, int((table_shop.size().width() - 15) / 4))
            table_shop.setRowHeight(i, 15)
        table_shop.setHorizontalHeaderLabels(["Товар", "Цена", "Кол-во", "Сумма"])
        table_layout = w.QGridLayout()
        table_layout.addWidget(table_products)
        table_layout.addWidget(table_shop)
        table_layout.setSpacing(30)
        layout.addChildLayout(table_layout)

        # storage page

        results_page = w.QWidget(self)
        layout = w.QHBoxLayout()
        results_page.setLayout(layout)
        table = w.QTableWidget(3, 6)
        table.setGeometry(10, 70, self.size().width()-45, 500)
        for i in range(6):
            table.setColumnWidth(i, int((table.size().width() - 15) / 6))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Количество"])
        layout.addWidget(table)

        # write-off page

        write_off_page = w.QWidget(self)
        layout = w.QGridLayout()
        write_off_page.setLayout(layout)

        label_product = w.QLabel("Товар:")
        label_product.setStyleSheet("font-size: 18px;")

        label_count = w.QLabel("Количество:")
        label_count.setStyleSheet("font-size: 18px;")

        label_reason = w.QLabel("Причина:")
        label_reason.setStyleSheet("font-size: 18px;")

        label_table = w.QLabel("Cписания")
        label_table.setStyleSheet("font-size: 18px;")

        ledit_product = w.QLineEdit()
        ledit_product.setStyleSheet("font-size: 18px;")
        ledit_product.setFixedSize(120, 25)

        ledit_count = w.QLineEdit()
        ledit_count.setStyleSheet("font-size: 18px;")
        ledit_count.setFixedSize(120, 25)

        ledit_reason = w.QLineEdit()
        ledit_reason.setStyleSheet("font-size: 18px;")
        ledit_reason.setFixedSize(120, 25)

        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        spacer = w.QSpacerItem(20, 40, w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Expanding)
        table = w.QTableWidget(3, 4)
        table.setGeometry(10, 70, self.size().width() - 45, 500)
        for i in range(4):
            table.setColumnWidth(i, int((table.size().width() - 30) / 4))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Количество"])

        button_accept = w.QPushButton("Списать")
        button_accept.setFixedSize(100, 30)
        layout.addWidget(label_product, 0, 0)
        layout.addWidget(label_count, 1, 0)
        layout.addWidget(label_reason, 2, 0)
        layout.addWidget(ledit_product, 0, 1)
        layout.addWidget(ledit_count, 1, 1)
        layout.addWidget(ledit_reason, 2, 1)
        layout.addWidget(button_accept, 3, 1)
        layout.addWidget(label_table, 4, 0)
        layout.addWidget(table, 5, 0, 5, 4)

        layout.addItem(spacer, 0, 0, 3, 3)
        layout.addItem(spacer, 5, 0)
        layout.setColumnStretch(3, 3)

        # add pane to the tab widget
        tab.addTab(staff_page, 'Продажи')
        tab.addTab(results_page, 'Склад')
        tab.addTab(write_off_page, 'Списания')

        main_layout.addWidget(tab)

    def change_acc(self):
        self.close()
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()

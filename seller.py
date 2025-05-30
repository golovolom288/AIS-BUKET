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
        label_shop.setStyleSheet("font-size: 18px; margin-left: 500px")
        layout.addWidget(label_search, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(search, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label_shop, alignment=c.Qt.AlignmentFlag.AlignTop | c.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)
        table = w.QTableWidget(3, 6)
        table.setGeometry(10, 70, int(self.size().width()*0.6), 500)
        for i in range(6):
            table.setColumnWidth(i, int((table.size().width() - 20) / 5))
            table.setRowHeight(i, 15)
        table.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Остаток"])
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
        tab.addTab(staff_page, 'Продажи')
        tab.addTab(results_page, 'Склад')

        main_layout.addWidget(tab)

    def change_acc(self):
        self.close()
        from auth import AuthWindow
        self.window = AuthWindow()
        self.window.show()
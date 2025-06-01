import PyQt6.QtWidgets as w
import PyQt6.QtCore as c
import sys
from datetime import datetime
from database import Database


class SellerWindow(w.QWidget):

    def __init__(self, current_user_id=None):
        super().__init__()
        self.db = Database()
        self.current_user_id = current_user_id

        self.setWindowTitle("SellerPanel")

        self.setup_window()
        self.setup_widgets()

        self.load_products_for_sale_data()
        self.load_storage_data()
        self.load_write_off_history_data()

    def setup_window(self):
        screen = w.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
        else:
            screen_geometry = c.QRect(0, 0, 1920, 1080)

        self.setFixedSize(1000, 700)

        window_rect = self.frameGeometry()
        center_point = screen_geometry.center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())

    def setup_widgets(self):
        main_layout = w.QVBoxLayout(self)

        top_bar_layout = w.QHBoxLayout()
        acc_change_btn = w.QPushButton("Сменить аккаунт", self)
        acc_change_btn.clicked.connect(self.change_acc)
        acc_change_btn.setFixedSize(130, 30)
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(acc_change_btn)
        main_layout.addLayout(top_bar_layout)

        tab_widget = w.QTabWidget(self)
        tab_widget.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # === Страница "Продажи" (sells_page_widget) ===
        sells_page_widget = w.QWidget()
        sells_page_layout = w.QVBoxLayout(sells_page_widget)

        sells_top_controls_layout = w.QHBoxLayout()
        label_search = w.QLabel("Поиск: ")
        label_search.setStyleSheet("font-size: 18px;")
        self.sells_search_lineedit = w.QLineEdit()
        self.sells_search_lineedit.setStyleSheet("margin-top: 3px")
        self.sells_search_lineedit.setFixedSize(200, 25)

        label_shop_title = w.QLabel("Корзина")
        label_shop_title.setStyleSheet("font-size: 18px;")

        sells_top_controls_layout.addWidget(label_search)
        sells_top_controls_layout.addWidget(self.sells_search_lineedit)
        sells_top_controls_layout.addStretch(1)
        sells_top_controls_layout.addWidget(label_shop_title)
        sells_page_layout.addLayout(sells_top_controls_layout)

        sells_tables_layout = w.QHBoxLayout()

        self.table_products_for_sale = w.QTableWidget()
        self.table_products_for_sale.setColumnCount(6)
        self.table_products_for_sale.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Тип", "Цена", "Остаток"])
        self.table_products_for_sale.horizontalHeader().setSectionResizeMode(w.QHeaderView.ResizeMode.Stretch)
        self.table_products_for_sale.setSelectionBehavior(w.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_products_for_sale.setEditTriggers(w.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table_shop = w.QTableWidget()
        self.table_shop.setColumnCount(4)
        self.table_shop.setHorizontalHeaderLabels(["Товар", "Цена", "Кол-во", "Сумма"])
        self.table_shop.horizontalHeader().setSectionResizeMode(w.QHeaderView.ResizeMode.Stretch)
        self.table_shop.setSelectionBehavior(w.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_shop.setEditTriggers(w.QAbstractItemView.EditTrigger.NoEditTriggers)


        sells_tables_layout.addWidget(self.table_products_for_sale, 2)
        sells_tables_layout.addWidget(self.table_shop, 1)
        sells_page_layout.addLayout(sells_tables_layout)

        # === Страница "Склад" (storage_page_widget) ===
        storage_page_widget = w.QWidget()
        storage_page_layout = w.QVBoxLayout(storage_page_widget)

        self.table_storage = w.QTableWidget()
        self.table_storage.setColumnCount(6)
        self.table_storage.setHorizontalHeaderLabels(["ID", "Артикул", "Название", "Поставщик", "Цена", "Количество"])
        self.table_storage.horizontalHeader().setSectionResizeMode(w.QHeaderView.ResizeMode.Stretch)
        self.table_storage.setSelectionBehavior(w.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_storage.setEditTriggers(w.QAbstractItemView.EditTrigger.NoEditTriggers)
        storage_page_layout.addWidget(self.table_storage)

        # === Страница "Списания" (write_off_page_widget) ===
        write_off_page_widget = w.QWidget()
        write_off_page_layout = w.QVBoxLayout(write_off_page_widget)

        write_off_form_layout = w.QGridLayout()
        label_product = w.QLabel("Товар (Артикул/ID):")
        label_product.setStyleSheet("font-size: 18px;")
        self.wo_ledit_product = w.QLineEdit()
        self.wo_ledit_product.setStyleSheet("font-size: 18px;")
        self.wo_ledit_product.setFixedSize(150, 25)

        label_count = w.QLabel("Количество:")
        label_count.setStyleSheet("font-size: 18px;")
        self.wo_ledit_count = w.QLineEdit()
        self.wo_ledit_count.setStyleSheet("font-size: 18px;")
        self.wo_ledit_count.setFixedSize(120, 25)

        label_reason = w.QLabel("Причина:")
        label_reason.setStyleSheet("font-size: 18px;")
        self.wo_ledit_reason = w.QLineEdit()
        self.wo_ledit_reason.setStyleSheet("font-size: 18px;")
        self.wo_ledit_reason.setFixedSize(200, 25)

        button_accept_write_off = w.QPushButton("Списать")
        button_accept_write_off.setFixedSize(100, 30)

        write_off_form_layout.addWidget(label_product, 0, 0)
        write_off_form_layout.addWidget(self.wo_ledit_product, 0, 1)
        write_off_form_layout.addWidget(label_count, 1, 0)
        write_off_form_layout.addWidget(self.wo_ledit_count, 1, 1)
        write_off_form_layout.addWidget(label_reason, 2, 0)
        write_off_form_layout.addWidget(self.wo_ledit_reason, 2, 1)
        write_off_form_layout.addWidget(button_accept_write_off, 3, 1, alignment=c.Qt.AlignmentFlag.AlignRight)
        write_off_form_layout.setColumnStretch(2, 1)
        write_off_page_layout.addLayout(write_off_form_layout)

        label_history_title = w.QLabel("История списаний")
        label_history_title.setStyleSheet("font-size: 18px; margin-top: 15px;")
        write_off_page_layout.addWidget(label_history_title)

        self.table_write_off_history = w.QTableWidget()
        self.table_write_off_history.setColumnCount(7)
        self.table_write_off_history.setHorizontalHeaderLabels(["ID", "Дата", "Артикул", "Название", "Кол-во", "Причина", "Пользователь"])
        self.table_write_off_history.horizontalHeader().setSectionResizeMode(w.QHeaderView.ResizeMode.Stretch)

        self.table_write_off_history.setSelectionBehavior(w.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_write_off_history.setEditTriggers(w.QAbstractItemView.EditTrigger.NoEditTriggers)
        write_off_page_layout.addWidget(self.table_write_off_history)

        tab_widget.addTab(sells_page_widget, 'Продажи')
        tab_widget.addTab(storage_page_widget, 'Склад')
        tab_widget.addTab(write_off_page_widget, 'Списания')

        main_layout.addWidget(tab_widget)

    def load_products_for_sale_data(self, filter_text=""):
        products_from_db = self.db.get_all_products()

        filtered_products = []
        if filter_text:
            filter_text = filter_text.lower()
            for p in products_from_db:
                if (filter_text in str(p.get('id','')).lower() or
                    filter_text in p.get('article','').lower() or
                    filter_text in p.get('name','').lower() or
                    (p.get('description') and filter_text in p.get('description','').lower()) or
                    filter_text in str(p.get('price','')).lower()):
                    filtered_products.append(p)
        else:
            filtered_products = products_from_db
        column_keys_for_sale = ['id', 'article', 'name', 'description', 'price', 'quantity'] 

        self.populate_table(self.table_products_for_sale, filtered_products, column_keys_for_sale)

        for r in range(self.table_products_for_sale.rowCount()):
            first_item = self.table_products_for_sale.item(r, 0)
            if first_item:
                product_data_for_row = first_item.data(c.Qt.ItemDataRole.UserRole)
                if product_data_for_row:
                    for col_idx_fill in range(self.table_products_for_sale.columnCount()):
                        item_to_fill = self.table_products_for_sale.item(r, col_idx_fill)
                        if item_to_fill:
                            item_to_fill.setData(c.Qt.ItemDataRole.UserRole, product_data_for_row)

    def load_storage_data(self, filter_text=""):
        products_from_db = self.db.get_all_products() 

        filtered_products = []
        if filter_text:
            filter_text = filter_text.lower()
            for p in products_from_db:
                if (filter_text in str(p.get('id','')).lower() or
                    filter_text in p.get('article','').lower() or
                    filter_text in p.get('name','').lower() or
                    (p.get('supplier_name') and filter_text in p.get('supplier_name','').lower()) or
                    filter_text in str(p.get('price','')).lower() or
                    filter_text in str(p.get('quantity','')).lower()):
                    filtered_products.append(p)
        else:
            filtered_products = products_from_db

        column_keys_for_storage = ['id', 'article', 'name', 'supplier_name', 'price', 'quantity']

        self.populate_table(self.table_storage, filtered_products, column_keys_for_storage)

    def load_write_off_history_data(self):
        write_offs_from_db = self.db.get_all_write_offs()

        column_keys_for_write_offs = ['id', 'write_off_date', 'product_article', 'product_name', 'quantity', 'reason', 'user_name']

        formatted_write_offs = []
        for wo_item_dict in write_offs_from_db:
            item_copy = dict(wo_item_dict) 
            try:
                date_str = str(item_copy.get('write_off_date', ''))
                if '.' in date_str:
                    date_str = date_str.split('.')[0]

                if date_str:
                    try:
                        datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
                    except ValueError:
                        # Если нет, конвертируем из формата SQLite
                        dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        item_copy['write_off_date'] = dt_obj.strftime('%d.%m.%Y %H:%M:%S')
            except (ValueError, TypeError) as e:
                item_copy['write_off_date'] = item_copy.get('write_off_date', '')
            formatted_write_offs.append(item_copy)

        self.populate_table(self.table_write_off_history, formatted_write_offs, column_keys_for_write_offs)

    def populate_table(self, table_widget: w.QTableWidget, data: list, column_keys: list):
        table_widget.setRowCount(0)
        if not data:
            return

        table_widget.setRowCount(len(data))
        # Убедимся, что количество колонок в виджете соответствует column_keys
        if table_widget.columnCount() != len(column_keys):
            table_widget.setColumnCount(len(column_keys))

        for row_idx, item_data_dict in enumerate(data):
            row_user_data = dict(item_data_dict)

            for col_idx, key in enumerate(column_keys):
                value = item_data_dict.get(key)

                if value is None:
                    cell_value_str = ""
                elif isinstance(value, float):
                    cell_value_str = f"{value:.2f}"
                else:
                    cell_value_str = str(value)

                table_item = w.QTableWidgetItem(cell_value_str)

                if col_idx == 0:
                    table_item.setData(c.Qt.ItemDataRole.UserRole, row_user_data)

                table_widget.setItem(row_idx, col_idx, table_item)

    def change_acc(self):
        self.close()
        from auth import AuthWindow
        self.auth_window_instance = AuthWindow()
        self.auth_window_instance.show()

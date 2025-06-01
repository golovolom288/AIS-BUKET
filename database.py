# database.py
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any


class Database:
    def __init__(self, db_name='bouquet_store.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Устанавливает соединение с базой данных."""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False, commit: bool = False) -> Any:
        """
        Универсальный метод для выполнения SQL-запросов.
        """
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                self.conn.commit()
                return cursor.lastrowid
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            print(f"Запрос: {query}")
            print(f"Параметры: {params}")
            if commit:
                self.conn.rollback()
            return None

    def create_tables(self):
        """Создание таблиц, если они не существуют."""
        # Пользователи (Сотрудники)
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'seller')), -- Из ТЗ
                position TEXT, -- Должность из ТЗ, может быть уточнением роли
                salary REAL DEFAULT 0,
                sales_percent REAL DEFAULT 0 -- Процент от продаж
            )
        ''')

        # Поставщики
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT
            )
        ''')

        # Товары
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                supplier_id INTEGER,
                description TEXT,
                price REAL NOT NULL,
                photo_path TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
            )
        ''')

        # Продажи (Чеки)
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,         -- Продавец, оформивший продажу
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT -- Нельзя удалить пользователя, если у него есть продажи
            )
        ''')

        # Позиции в продаже
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL,
                price_at_sale REAL NOT NULL,      -- Цена товара на момент продажи
                FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE, -- Если удаляется продажа, удаляются и ее позиции
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT -- Нельзя удалить товар, если он есть в продажах
            )
        ''')
        self.conn.commit() # Коммитим создание таблиц

    # --- Методы для Пользователей (Сотрудников) ---
    def add_user(self, login: str, password: str, full_name: str, role: str, position: str = None, salary: float = 0, sales_percent: float = 0) -> Optional[int]:
        query = '''
            INSERT INTO users (login, password, full_name, role, position, salary, sales_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.close()
        return self.execute_query(query, (login, password, full_name, role, position, salary, sales_percent), commit=True)

    def get_user_by_login(self, login: str) -> Optional[sqlite3.Row]:
        query = "SELECT * FROM users WHERE login = ?"
        return self.execute_query(query, (login,), fetch_one=True)

    def authenticate_user(self, login: str, password: str) -> Optional[Dict]:
        user_row = self.get_user_by_login(login)
        if user_row:
            if password == user_row['password']:
                return dict(user_row)
        return None

    def get_all_users(self) -> List[Dict]:
        rows = self.execute_query("SELECT * FROM users ORDER BY full_name", fetch_all=True)
        return [dict(row) for row in rows] if rows else []

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        row = self.execute_query("SELECT * FROM users WHERE id = ?", (user_id,), fetch_one=True)
        return dict(row) if row else None

    def update_user(self, user_id: int, login: str, password: str, full_name: str, role: str, position: Optional[str], salary: float = 0, sales_percent: float = 0) -> bool:
        query_parts = ["login = ?"]
        params = [login]
        if password:
            query_parts.append("password = ?")
            params.append(password)
        if full_name:
            query_parts.append("full_name = ?")
            params.append(full_name)
        if role:
            query_parts.append("role = ?")
            params.append(role)
        if position:
            query_parts.append("position = ?")
            params.append(position)
        if salary != 0:
            query_parts.append("salary = ?")
            params.append(salary)
        if sales_percent != 0:
            query_parts.append("sales_percent = ?")
            params.append(sales_percent)
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(query_parts)} WHERE id = ?"
        return self.execute_query(query, tuple(params), commit=True) is not None

    def delete_user(self, user_id: int) -> bool:
        return self.execute_query("DELETE FROM users WHERE id = ?", (user_id,), commit=True) is not None

    # --- Методы для Товаров ---
    def add_product(self, article: str, name: str, supplier_id: Optional[int], description: Optional[str], price: float, photo_path: Optional[str], quantity: int) -> Optional[int]:
        query = '''
            INSERT INTO products (article, name, supplier_id, description, price, photo_path, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (article, name, supplier_id, description, price, photo_path, quantity), commit=True)

    def get_all_products(self) -> List[Dict]:
        # JOIN с поставщиками для отображения имени поставщика
        query = """
            SELECT p.*, s.name as supplier_name
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            ORDER BY p.name
        """
        rows = self.execute_query(query, fetch_all=True)
        return [dict(row) for row in rows] if rows else []

    def get_model(self, model_name):
        model = self.execute_query(f"SELECT * FROM {model_name}", fetch_all=True)
        return model

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        query = """
            SELECT p.*, s.name as supplier_name
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.id = ?
        """
        row = self.execute_query(query, (product_id,), fetch_one=True)
        return dict(row) if row else None

    def get_product_by_article(self, article: str) -> Optional[Dict]:
        query = """
            SELECT p.*, s.name as supplier_name
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.article = ?
        """
        row = self.execute_query(query, (article,), fetch_one=True)
        return dict(row) if row else None

    def update_product(self, product_id: int, article: str, name: str, supplier_id: Optional[int], description: Optional[str], price: float, photo_path: Optional[str], quantity: int) -> bool:
        query = '''
            UPDATE products
            SET article = ?, name = ?, supplier_id = ?, description = ?, price = ?, photo_path = ?, quantity = ?
            WHERE id = ?
        '''
        return self.execute_query(query, (article, name, supplier_id, description, price, photo_path, quantity, product_id), commit=True) is not None

    def delete_product(self, product_id: int) -> bool:
        try:
            return self.execute_query("DELETE FROM products WHERE id = ?", (product_id,), commit=True) is not None
        except sqlite3.IntegrityError:
            print(f"Невозможно удалить товар ID={product_id}, так как он используется в продажах.")
            return False

    def update_product_quantity(self, product_id: int, quantity_change: int) -> bool:
        """Изменяет количество товара. quantity_change может быть положительным (приход) или отрицательным (продажа, списание)."""
        query = "UPDATE products SET quantity = quantity + ? WHERE id = ?"
        product = self.get_product_by_id(product_id)
        if product and (product['quantity'] + quantity_change < 0):
            print(f"Ошибка: Недостаточно товара ID={product_id} для изменения на {quantity_change}. Текущий остаток: {product['quantity']}")
            return False
        return self.execute_query(query, (quantity_change, product_id), commit=True) is not None

    # --- Методы для Поставщиков ---
    def add_supplier(self, name: str, contact_person: Optional[str] = None, phone: Optional[str] = None, email: Optional[str] = None, address: Optional[str] = None) -> Optional[int]:
        query = '''
            INSERT INTO suppliers (name, contact_person, phone, email, address)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (name, contact_person, phone, email, address), commit=True)

    def get_all_suppliers(self) -> List[Dict]:
        rows = self.execute_query("SELECT * FROM suppliers ORDER BY name", fetch_all=True)
        return [dict(row) for row in rows] if rows else []

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Dict]:
        row = self.execute_query("SELECT * FROM suppliers WHERE id = ?", (supplier_id,), fetch_one=True)
        return dict(row) if row else None

    def update_supplier(self, supplier_id: int, name: str, contact_person: Optional[str], phone: Optional[str], email: Optional[str], address: Optional[str]) -> bool:
        query = '''
            UPDATE suppliers
            SET name = ?, contact_person = ?, phone = ?, email = ?, address = ?
            WHERE id = ?
        '''
        return self.execute_query(query, (name, contact_person, phone, email, address, supplier_id), commit=True) is not None

    def delete_supplier(self, supplier_id: int) -> bool:
        return self.execute_query("DELETE FROM suppliers WHERE id = ?", (supplier_id,), commit=True) is not None

    # --- Методы для Продаж ---
    def create_sale(self, user_id: int, items: List[Dict]) -> Optional[int]:
        """
        Создает новую продажу и ее позиции.
        """
        if not items:
            return None

        total_amount = sum(item['quantity'] * item['price_at_sale'] for item in items)

        sale_query = "INSERT INTO sales (user_id, total_amount) VALUES (?, ?)"
        sale_id = self.execute_query(sale_query, (user_id, total_amount), commit=False)

        if not sale_id:
            self.conn.rollback()
            return None

        try:
            for item in items:
                # Проверяем достаточность товара на складе
                product = self.get_product_by_id(item['product_id'])
                if not product or product['quantity'] < item['quantity']:
                    print(f"Ошибка: Недостаточно товара '{product['name'] if product else 'ID:'+str(item['product_id'])}' на складе.")
                    self.conn.rollback()
                    return None

                item_query = "INSERT INTO sale_items (sale_id, product_id, quantity_sold, price_at_sale) VALUES (?, ?, ?, ?)"
                self.execute_query(item_query, (sale_id, item['product_id'], item['quantity'], item['price_at_sale']), commit=False)
                self.update_product_quantity(item['product_id'], -item['quantity']) # commit=False внутри, т.к. основной коммит будет в конце

            self.conn.commit()
            return sale_id
        except sqlite3.Error as e:
            print(f"Ошибка при создании позиций продажи: {e}")
            self.conn.rollback()
            return None

    def get_sales_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None, user_id_filter: Optional[int] = None) -> List[Dict]:
        query = """
            SELECT s.id as sale_id, s.sale_date, s.total_amount,
                   u.full_name as seller_name,
                   (SELECT COUNT(*) FROM sale_items si WHERE si.sale_id = s.id) as items_count
            FROM sales s
            JOIN users u ON s.user_id = u.id
        """
        conditions = []
        params = []
        if start_date:
            conditions.append("date(s.sale_date) >= date(?)")
            params.append(start_date)
        if end_date:
            conditions.append("date(s.sale_date) <= date(?)")
            params.append(end_date)
        if user_id_filter:
            conditions.append("s.user_id = ?")
            params.append(user_id_filter)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY s.sale_date DESC"

        rows = self.execute_query(query, tuple(params), fetch_all=True)
        return [dict(row) for row in rows] if rows else []

    def get_sale_details(self, sale_id: int) -> Optional[Dict]:
        sale_info_query = """
            SELECT s.id as sale_id, s.sale_date, s.total_amount,
                   u.id as seller_id, u.full_name as seller_name, u.role as seller_role
            FROM sales s
            JOIN users u ON s.user_id = u.id
            WHERE s.id = ?
        """
        sale_info = self.execute_query(sale_info_query, (sale_id,), fetch_one=True)
        if not sale_info:
            return None

        items_query = """
            SELECT si.product_id, p.article, p.name as product_name,
                   si.quantity_sold, si.price_at_sale,
                   (si.quantity_sold * si.price_at_sale) as item_total_amount
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        """
        items = self.execute_query(items_query, (sale_id,), fetch_all=True)

        result = dict(sale_info)
        result['items'] = [dict(item) for item in items] if items else []
        return result

    # --- Дополнительные методы (согласно ТЗ) ---

    def calculate_seller_salary(self, seller_id: int, start_date_str: str, end_date_str: str) -> Optional[Dict]:
        """
        Расчет зарплаты продавца за месяц (оклад + процент).
        """
        seller = self.get_user_by_id(seller_id)
        if not seller or seller['role'] != 'seller':
            print(f"Пользователь ID={seller_id} не найден или не является продавцом.")
            return None

        # Получаем продажи этого продавца за период
        sales_for_period = self.get_sales_report(start_date_str, end_date_str, seller_id_filter=seller_id)

        total_sales_amount = sum(sale['total_amount'] for sale in sales_for_period)

        base_salary = seller.get('salary', 0.0)
        sales_percent = seller.get('sales_percent', 0.0) / 100.0

        bonus_from_sales = total_sales_amount * sales_percent
        final_salary = base_salary + bonus_from_sales

        return {
            'seller_id': seller_id,
            'full_name': seller['full_name'],
            'base_salary': base_salary,
            'total_sales_amount_period': total_sales_amount,
            'sales_percent_rate': seller.get('sales_percent', 0.0),
            'bonus_from_sales': bonus_from_sales,
            'final_salary': final_salary,
            'period_start': start_date_str,
            'period_end': end_date_str
        }


# --- Пример использования (для тестирования) ---
if __name__ == '__main__':
    db = Database('test_bouquet_store.db')

    # Добавление пользователей
    admin_id = db.add_user('admin', 'adminpass', 'Иванов И.И.', 'administrator', 'Главный администратор', 60000, 0)
    manager_id = db.add_user('manager', 'managerpass', 'Петров П.П.', 'manager', 'Старший менеджер', 50000, 5)
    seller_id = db.add_user('seller1', 'sellerpass', 'Сидорова А.А.', 'seller', 'Продавец-консультант', 30000, 10)
    print(f"Добавлены пользователи: admin_id={admin_id}, manager_id={manager_id}, seller_id={seller_id}")

    # Аутентификация
    authed_user = db.authenticate_user('seller1', 'sellerpass')
    if authed_user:
        print(f"Аутентификация успешна: {authed_user['full_name']}, роль: {authed_user['role']}")
    else:
        print("Ошибка аутентификации")

    # Поставщики
    sup1_id = db.add_supplier("Цветочная База №1", "Анна", "88001002030", "zakaz@flowerbase1.com")
    sup2_id = db.add_supplier("Мир Упаковки", "Виктор", "88002003040")
    print(f"Добавлены поставщики: sup1_id={sup1_id}, sup2_id={sup2_id}")
    print("Все поставщики:", db.get_all_suppliers())

    # Товары
    if sup1_id:
        prod1_id = db.add_product('R001', 'Роза красная 60см', sup1_id, 'Классическая красная роза', 150.00, 'img/rose_red.jpg', 100)
        prod2_id = db.add_product('L005', 'Лилия белая', sup1_id, 'Ароматная белая лилия', 250.00, 'img/lily_white.jpg', 50)
        print(f"Добавлены товары: prod1_id={prod1_id}, prod2_id={prod2_id}")

    if sup2_id:
        prod3_id = db.add_product('P010', 'Упаковочная бумага крафт', sup2_id, 'Рулон 10м', 300.00, 'img/craft_paper.jpg', 30)
        print(f"Добавлен товар: prod3_id={prod3_id}")

    print("Все товары:", db.get_all_products())
    if prod1_id:
        print("Товар по ID:", db.get_product_by_id(prod1_id))

    # Обновление товара
    if prod1_id:
        db.update_product(prod1_id, 'R001-NEW', 'Роза Алая 70см', sup1_id, 'Улучшенная красная роза', 180.00, 'img/rose_scarlet.jpg', 90)
        print("Обновленный товар:", db.get_product_by_id(prod1_id))

    # Продажа
    if seller_id and prod1_id and prod2_id:
        sale_items = [
            {'product_id': prod1_id, 'quantity': 2, 'price_at_sale': 180.00},
            {'product_id': prod2_id, 'quantity': 1, 'price_at_sale': 250.00}
        ]
        new_sale_id = db.create_sale(seller_id, sale_items)
        if new_sale_id:
            print(f"Создана продажа ID: {new_sale_id}")
            print("Детали продажи:", db.get_sale_details(new_sale_id))
            print("Остаток Розы Алой:", db.get_product_by_id(prod1_id)['quantity'])
        else:
            print("Не удалось создать продажу.")

    # Отчет по продажам
    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"Отчет по продажам за {today_str}:", db.get_sales_report(start_date=today_str, end_date=today_str))
    if seller_id:
        print(f"Отчет по продажам для продавца ID {seller_id} за {today_str}:", db.get_sales_report(start_date=today_str, end_date=today_str, user_id_filter=seller_id))

    # Расчет зарплаты
    if seller_id:
        start_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        end_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_month_str = end_month.strftime('%Y-%m-%d')

        salary_info = db.calculate_seller_salary(seller_id, start_month, end_month_str)
        if salary_info:
            print(f"\nРасчет зарплаты для {salary_info['full_name']} за период {start_month} - {end_month_str}:")
            print(f"  Оклад: {salary_info['base_salary']:.2f} руб.")
            print(f"  Сумма продаж за период: {salary_info['total_sales_amount_period']:.2f} руб.")
            print(f"  Процент от продаж: {salary_info['sales_percent_rate']:.1f}%")
            print(f"  Бонус от продаж: {salary_info['bonus_from_sales']:.2f} руб.")
            print(f"  Итого к выплате: {salary_info['final_salary']:.2f} руб.")
        else:
            print(f"Не удалось рассчитать зарплату для продавца ID={seller_id}")

    # Закрытие соединения
    db.close()

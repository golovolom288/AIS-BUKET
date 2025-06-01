# database.py
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any


class Database:
    def __init__(self, db_name='bouquet_store.db'): # Используем одно имя БД по умолчанию
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False, commit: bool = False) -> Any:
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
            return True # Для операций типа UPDATE, DELETE без fetch, но с commit=True
        except sqlite3.IntegrityError as e:
            # Для тестового блока if __name__ == '__main__' можно не выводить эту ошибку,
            # так как мы будем проверять наличие записи перед вставкой.
            # Для обычных вызовов методов add_... важно, чтобы None возвращался.
            # print(f"Ошибка целостности данных (возможно, дубликат UNIQUE): {e}")
            # print(f"Запрос: {query}")
            # print(f"Параметры: {params}")
            if commit:
                self.conn.rollback()
            return None
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            print(f"Запрос: {query}")
            print(f"Параметры: {params}")
            if commit:
                self.conn.rollback()
            return None

    def create_tables(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, -- В реальном приложении храните хеши паролей!
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('administrator', 'manager', 'seller')),
                position TEXT,
                salary REAL DEFAULT 0,
                sales_percent REAL DEFAULT 0
            )
        ''')
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
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL,
                price_at_sale REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
            )
        ''')
        # Таблица для списаний
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS write_offs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,       -- Пользователь, совершивший списание
                quantity INTEGER NOT NULL,
                reason TEXT NOT NULL,
                write_off_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
            )
        ''')
        self.conn.commit()

    # --- Методы для Пользователей ---
    def add_user(self, login: str, password: str, full_name: str, role: str, position: str = None, salary: float = 0, sales_percent: float = 0) -> Optional[int]:
        query = '''
            INSERT INTO users (login, password, full_name, role, position, salary, sales_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (login, password, full_name, role, position, salary, sales_percent), commit=True)

    def get_user_by_login(self, login: str) -> Optional[sqlite3.Row]:
        return self.execute_query("SELECT * FROM users WHERE login = ?", (login,), fetch_one=True)

    def authenticate_user(self, login: str, password: str) -> Optional[Dict]:
        user_row = self.get_user_by_login(login)
        if user_row and user_row['password'] == password: # Простая проверка, нужна замена на хеши
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
            query_parts.append("password = ?") # Пароль должен быть хеширован перед сохранением
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
        # В SQLite ON DELETE RESTRICT по умолчанию, так что IntegrityError будет возбужден, если товар используется.
        return self.execute_query("DELETE FROM products WHERE id = ?", (product_id,), commit=True) is not None

    def update_product_quantity(self, product_id: int, quantity_change: int, by_sale: bool = False) -> bool:
        """
        Изменяет количество товара.
        quantity_change: положительное (приход), отрицательное (продажа, списание).
        by_sale: если True, то commit=False, так как коммит будет в методе create_sale.
        """
        product = self.get_product_by_id(product_id) # Этот вызов использует свой курсор и соединение
        if product and (product['quantity'] + quantity_change < 0):
            # print(f"Ошибка: Недостаточно товара ID={product_id} для изменения на {quantity_change}. Остаток: {product['quantity']}")
            return False
        
        query = "UPDATE products SET quantity = quantity + ? WHERE id = ?"
        # Если это часть большей транзакции (как продажа), коммит будет позже.
        return self.execute_query(query, (quantity_change, product_id), commit=not by_sale) is not None


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
    
    def get_supplier_by_name(self, name: str) -> Optional[Dict]: # Добавлен для тестового блока
        row = self.execute_query("SELECT * FROM suppliers WHERE name = ?", (name,), fetch_one=True)
        return dict(row) if row else None

    def update_supplier(self, supplier_id: int, name: str, contact_person: Optional[str], phone: Optional[str], email: Optional[str], address: Optional[str]) -> bool:
        query = '''
            UPDATE suppliers SET name = ?, contact_person = ?, phone = ?, email = ?, address = ? WHERE id = ?
        '''
        return self.execute_query(query, (name, contact_person, phone, email, address, supplier_id), commit=True) is not None

    def delete_supplier(self, supplier_id: int) -> bool:
        return self.execute_query("DELETE FROM suppliers WHERE id = ?", (supplier_id,), commit=True) is not None

    # --- Методы для Продаж ---
    def create_sale(self, user_id: int, items: List[Dict]) -> Optional[int]:
        if not items: return None
        
        if not self.conn: self.connect()
        cursor = self.conn.cursor() # Используем один курсор для транзакции
        try:
            # Рассчитываем общую сумму
            total_amount = sum(item['quantity'] * item['price_at_sale'] for item in items)
            
            # 1. Создаем запись о продаже
            sale_query = "INSERT INTO sales (user_id, total_amount) VALUES (?, ?)"
            cursor.execute(sale_query, (user_id, total_amount))
            sale_id = cursor.lastrowid
            if not sale_id:
                self.conn.rollback()
                return None

            # 2. Добавляем позиции продажи и обновляем количество товаров
            for item in items:
                # Проверка остатка (еще раз, на всякий случай, если много одновременных операций)
                product_check_query = "SELECT quantity FROM products WHERE id = ?"
                cursor.execute(product_check_query, (item['product_id'],))
                product_row = cursor.fetchone()
                if not product_row or product_row['quantity'] < item['quantity']:
                    # print(f"Ошибка при создании продажи: Недостаточно товара ID {item['product_id']}.")
                    self.conn.rollback()
                    return None
                
                item_query = "INSERT INTO sale_items (sale_id, product_id, quantity_sold, price_at_sale) VALUES (?, ?, ?, ?)"
                cursor.execute(item_query, (sale_id, item['product_id'], item['quantity'], item['price_at_sale']))
                
                # Обновление количества товара
                update_qty_query = "UPDATE products SET quantity = quantity - ? WHERE id = ?"
                cursor.execute(update_qty_query, (item['quantity'], item['product_id']))
                if cursor.rowcount == 0: # Если по какой-то причине товар не обновился
                    self.conn.rollback()
                    return None
            
            self.conn.commit()
            return sale_id
        except sqlite3.Error as e:
            # print(f"Ошибка БД при создании продажи: {e}")
            if self.conn: self.conn.rollback()
            return None

    def get_sales_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None, user_id_filter: Optional[int] = None) -> List[Dict]:
        query = """
            SELECT s.id as sale_id, s.sale_date, s.total_amount, u.full_name as seller_name,
                   (SELECT COUNT(*) FROM sale_items si WHERE si.sale_id = s.id) as items_count
            FROM sales s JOIN users u ON s.user_id = u.id
        """
        conditions, params = [], []
        if start_date: conditions.append("date(s.sale_date) >= date(?)"); params.append(start_date)
        if end_date: conditions.append("date(s.sale_date) <= date(?)"); params.append(end_date)
        if user_id_filter: conditions.append("s.user_id = ?"); params.append(user_id_filter)
        if conditions: query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY s.sale_date DESC"
        rows = self.execute_query(query, tuple(params), fetch_all=True)
        return [dict(row) for row in rows] if rows else []

    def get_sale_details(self, sale_id: int) -> Optional[Dict]:
        # ... (код остается прежним, он корректен)
        sale_info_query = "SELECT s.*, u.full_name as seller_name, u.role as seller_role FROM sales s JOIN users u ON s.user_id = u.id WHERE s.id = ?"
        sale_info = self.execute_query(sale_info_query, (sale_id,), fetch_one=True)
        if not sale_info: return None
        items_query = "SELECT si.*, p.article, p.name as product_name, (si.quantity_sold * si.price_at_sale) as item_total_amount FROM sale_items si JOIN products p ON si.product_id = p.id WHERE si.sale_id = ?"
        items = self.execute_query(items_query, (sale_id,), fetch_all=True)
        result = dict(sale_info)
        result['items'] = [dict(item) for item in items] if items else []
        return result

    def calculate_seller_salary(self, seller_id: int, start_date_str: str, end_date_str: str) -> Optional[Dict]:
        # ... (код остается прежним, он корректен)
        seller = self.get_user_by_id(seller_id)
        if not seller or seller['role'] != 'seller': return None
        sales_for_period = self.get_sales_report(start_date_str, end_date_str, user_id_filter=seller_id)
        total_sales_amount = sum(s['total_amount'] for s in sales_for_period)
        base_salary = seller.get('salary', 0.0)
        sales_percent_rate = seller.get('sales_percent', 0.0)
        bonus_from_sales = total_sales_amount * (sales_percent_rate / 100.0)
        final_salary = base_salary + bonus_from_sales
        return {'seller_id': seller_id, 'full_name': seller['full_name'], 'base_salary': base_salary,
                'total_sales_amount_period': total_sales_amount, 'sales_percent_rate': sales_percent_rate,
                'bonus_from_sales': bonus_from_sales, 'final_salary': final_salary,
                'period_start': start_date_str, 'period_end': end_date_str}

    # --- Методы для Списаний ---
    def add_write_off(self, product_id: int, user_id: int, quantity: int, reason: str) -> Optional[int]:
        """Добавляет запись о списании и обновляет количество товара."""
        if not self.conn: self.connect()
        cursor = self.conn.cursor()
        try:
            # 1. Проверяем наличие товара и достаточное количество
            product_check_query = "SELECT quantity FROM products WHERE id = ?"
            cursor.execute(product_check_query, (product_id,))
            product_row = cursor.fetchone()
            if not product_row or product_row['quantity'] < quantity:
                # print(f"Ошибка списания: Недостаточно товара ID {product_id} или товар не найден.")
                return None # Не откатываем, т.к. ничего не сделали

            # 2. Добавляем запись о списании
            wo_query = "INSERT INTO write_offs (product_id, user_id, quantity, reason) VALUES (?, ?, ?, ?)"
            cursor.execute(wo_query, (product_id, user_id, quantity, reason))
            write_off_id = cursor.lastrowid
            if not write_off_id:
                self.conn.rollback()
                return None

            # 3. Обновляем количество товара
            update_qty_query = "UPDATE products SET quantity = quantity - ? WHERE id = ?"
            cursor.execute(update_qty_query, (quantity, product_id))
            if cursor.rowcount == 0: # Если товар не обновился
                self.conn.rollback() # Откатываем и запись о списании
                return None
            
            self.conn.commit()
            return write_off_id
        except sqlite3.Error as e:
            # print(f"Ошибка БД при списании: {e}")
            if self.conn: self.conn.rollback()
            return None

    def get_all_write_offs(self) -> List[Dict]:
        query = """
            SELECT wo.id, wo.product_id, p.article as product_article, p.name as product_name,
                   wo.quantity, wo.reason, wo.write_off_date,
                   u.full_name as user_name, u.id as user_id
            FROM write_offs wo
            JOIN products p ON wo.product_id = p.id
            JOIN users u ON wo.user_id = u.id
            ORDER BY wo.write_off_date DESC
        """
        rows = self.execute_query(query, fetch_all=True)
        return [dict(row) for row in rows] if rows else []

# --- Пример использования (для тестирования) ---
if __name__ == '__main__':
    # Для "чистого" теста можно удалить файл БД перед первым запуском
    # import os
    # db_file = 'bouquet_store.db'
    # if os.path.exists(db_file):
    #     os.remove(db_file)
    # print(f"Файл {db_file} удален для чистого теста.")

    db = Database('bouquet_store.db') # Используем основное имя БД

    # Инициализация ID переменных
    admin_id, manager_id, seller_id = None, None, None
    sup1_id, sup2_id = None, None
    prod1_id, prod2_id, prod3_id = None, None, None

    # --- Добавление или получение существующих записей ---
    def get_or_create_user(login, password, full_name, role, **kwargs):
        user = db.get_user_by_login(login)
        if user:
            print(f"Пользователь '{login}' уже существует. ID: {user['id']}")
            return user['id']
        else:
            user_id = db.add_user(login, password, full_name, role, **kwargs)
            print(f"Добавлен пользователь '{login}'. ID: {user_id}")
            return user_id

    def get_or_create_supplier(name, **kwargs):
        supplier = db.get_supplier_by_name(name)
        if supplier:
            print(f"Поставщик '{name}' уже существует. ID: {supplier['id']}")
            return supplier['id']
        else:
            supplier_id = db.add_supplier(name, **kwargs)
            print(f"Добавлен поставщик '{name}'. ID: {supplier_id}")
            return supplier_id

    def get_or_create_product(article, name, supplier_id_val, **kwargs):
        product = db.get_product_by_article(article)
        if product:
            print(f"Товар '{article}' уже существует. ID: {product['id']}")
            return product['id']
        elif supplier_id_val is not None: # Добавляем только если есть поставщик
            product_id = db.add_product(article, name, supplier_id_val, **kwargs)
            print(f"Добавлен товар '{article}'. ID: {product_id}")
            return product_id
        return None

    admin_id = get_or_create_user('admin', 'adminpass', 'Иванов И.И.', 'administrator', position='Главный администратор', salary=60000)
    manager_id = get_or_create_user('manager', 'managerpass', 'Петров П.П.', 'manager', position='Старший менеджер', salary=50000, sales_percent=5)
    seller_id = get_or_create_user('seller1', 'sellerpass', 'Сидорова А.А.', 'seller', position='Продавец-консультант', salary=30000, sales_percent=10)

    authed_user = db.authenticate_user('seller1', 'sellerpass')
    if authed_user:
        print(f"Аутентификация успешна: {authed_user['full_name']}, роль: {authed_user['role']}")
    else:
        print("Ошибка аутентификации для seller1")

    sup1_id = get_or_create_supplier("Цветочная База №1", contact_person="Анна", phone="88001002030", email="zakaz@flowerbase1.com")
    sup2_id = get_or_create_supplier("Мир Упаковки", contact_person="Виктор", phone="88002003040")
    
    prod1_id = get_or_create_product('R001', 'Роза красная 60см', sup1_id, description='Классическая красная роза', price=150.00, photo_path='img/rose_red.jpg', quantity=100)
    prod2_id = get_or_create_product('L005', 'Лилия белая', sup1_id, description='Ароматная белая лилия', price=250.00, photo_path='img/lily_white.jpg', quantity=50)
    prod3_id = get_or_create_product('P010', 'Упаковочная бумага крафт', sup2_id, description='Рулон 10м', price=300.00, photo_path='img/craft_paper.jpg', quantity=30)

    print("\nВсе товары:", db.get_all_products())
    if prod1_id:
        prod1_data_before_update = db.get_product_by_id(prod1_id)
        print(f"Товар по ID ({prod1_id}): {prod1_data_before_update}")
        # Обновление товара (только если артикул не изменен)
        if prod1_data_before_update and prod1_data_before_update['article'] == 'R001':
             if db.update_product(prod1_id, 'R001-NEW', 'Роза Алая 70см', sup1_id, 'Улучшенная красная роза', 180.00, 'img/rose_scarlet.jpg', 90):
                print("Обновленный товар (R001-NEW):", db.get_product_by_id(prod1_id))
             else:
                print(f"Не удалось обновить товар ID {prod1_id}")
        elif prod1_data_before_update:
             print(f"Товар {prod1_data_before_update['name']} ({prod1_data_before_update['article']}) уже был обновлен или изменен.")


    # Продажа
    if seller_id and prod1_id and prod2_id:
        p1_current = db.get_product_by_id(prod1_id)
        p2_current = db.get_product_by_id(prod2_id)
        if p1_current and p1_current['quantity'] >= 2 and p2_current and p2_current['quantity'] >= 1:
            sale_items = [
                {'product_id': prod1_id, 'quantity': 2, 'price_at_sale': p1_current['price']},
                {'product_id': prod2_id, 'quantity': 1, 'price_at_sale': p2_current['price']}
            ]
            new_sale_id = db.create_sale(seller_id, sale_items)
            if new_sale_id:
                print(f"\nСоздана продажа ID: {new_sale_id}")
                print("Детали продажи:", db.get_sale_details(new_sale_id))
                updated_p1 = db.get_product_by_id(prod1_id)
                if updated_p1: print(f"Остаток товара '{updated_p1['name']}': {updated_p1['quantity']}")
            else:
                print("Не удалось создать тестовую продажу.")
        else:
            print("\nНедостаточно товаров для тестовой продажи или товары не найдены.")
    else:
        print("\nНе все ID для тестовой продажи определены (seller_id, prod1_id, prod2_id).")

    # Отчет по продажам
    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"\nОтчет по продажам за {today_str}:", db.get_sales_report(start_date=today_str, end_date=today_str))

    # Расчет зарплаты
    if seller_id:
        start_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        end_month_dt = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_month_str = end_month_dt.strftime('%Y-%m-%d')
        salary_info = db.calculate_seller_salary(seller_id, start_month, end_month_str)
        if salary_info:
            print(f"\nРасчет зарплаты для {salary_info['full_name']} за период {start_month} - {end_month_str}:")
            # ... (остальной вывод зарплаты)
            print(f"  Итого к выплате: {salary_info['final_salary']:.2f} руб.")

    # Тест списания
    if admin_id and prod3_id:
        p3_current = db.get_product_by_id(prod3_id)
        if p3_current and p3_current['quantity'] >= 1:
            wo_id = db.add_write_off(product_id=prod3_id, user_id=admin_id, quantity=1, reason="Тестовое списание: бой при транспортировке")
            if wo_id:
                print(f"\nУспешно списан товар ID {prod3_id} ('{p3_current['name']}'), запись о списании ID: {wo_id}")
                print(f"Новый остаток: {db.get_product_by_id(prod3_id)['quantity']}")
            else:
                print(f"\nНе удалось списать товар ID {prod3_id}")
        elif p3_current:
            print(f"\nНедостаточно товара '{p3_current['name']}' для тестового списания.")

    print("\nВсе списания:", db.get_all_write_offs())

    db.close()
    print("\nСоединение с БД закрыто.")

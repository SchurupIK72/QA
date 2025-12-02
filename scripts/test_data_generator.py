"""
Генератор тестовых данных для QA проектов
Версия: 1.2.0

Новое в 1.2.0:
- Режим эквивалентного разбиения (Boundary Value Analysis)
- Генерация граничных значений для строковых и числовых данных
- Поддержка кириллицы в генерации строк
"""

import random
import string
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

# Путь к папке для сохранения тестовых данных
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TestData")


class TestDataGenerator:
    """Генератор различных типов тестовых данных"""
    
    def __init__(self, locale: str = "ru"):
        """
        Инициализация генератора
        
        Args:
            locale: Локаль для генерации данных (ru/en)
        """
        self.locale = locale
        self._init_data_pools()
    
    def _init_data_pools(self):
        """Инициализация пулов данных для генерации"""
        
        # Русские имена
        self.first_names_ru = [
            "Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей",
            "Артём", "Илья", "Кирилл", "Михаил", "Никита", "Матвей",
            "Анна", "Мария", "Елена", "Ольга", "Ирина", "Наталья",
            "Татьяна", "Екатерина", "Юлия", "София", "Анастасия", "Виктория"
        ]
        
        # Русские фамилии
        self.last_names_ru = [
            "Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Попов",
            "Васильев", "Соколов", "Михайлов", "Новиков", "Фёдоров", "Морозов",
            "Волков", "Алексеев", "Лебедев", "Семёнов", "Егоров", "Павлов"
        ]
        
        # Английские имена
        self.first_names_en = [
            "John", "James", "Robert", "Michael", "William", "David",
            "Richard", "Joseph", "Thomas", "Charles", "Christopher", "Daniel",
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara",
            "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa"
        ]
        
        # Английские фамилии
        self.last_names_en = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
            "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"
        ]
        
        # Домены для email
        self.email_domains = [
            "gmail.com", "yahoo.com", "outlook.com", "mail.ru", 
            "yandex.ru", "test.com", "example.com", "hotmail.com"
        ]
        
        # Типичные пароли для тестирования
        self.password_patterns = [
            "Password123!", "Test@2024", "Qwerty123", "Admin@123",
            "User12345!", "Test!Pass1", "MyPass@123", "Secure#2024"
        ]
    
    # ==================== ПЕРСОНАЛЬНЫЕ ДАННЫЕ ====================
    
    def generate_first_name(self, gender: str = None) -> str:
        """
        Генерация имени
        
        Args:
            gender: Пол (male/female/None - любой)
        
        Returns:
            Случайное имя
        """
        if self.locale == "ru":
            names = self.first_names_ru
        else:
            names = self.first_names_en
        
        return random.choice(names)
    
    def generate_last_name(self) -> str:
        """Генерация фамилии"""
        if self.locale == "ru":
            return random.choice(self.last_names_ru)
        else:
            return random.choice(self.last_names_en)
    
    def generate_full_name(self) -> str:
        """Генерация полного имени"""
        return f"{self.generate_first_name()} {self.generate_last_name()}"
    
    def generate_nickname(self, length: int = None) -> str:
        """
        Генерация никнейма
        
        Args:
            length: Длина никнейма (если не указано, случайная 6-12)
        
        Returns:
            Случайный никнейм
        """
        if length is None:
            length = random.randint(6, 12)
        
        # Комбинация из букв и цифр
        chars = string.ascii_lowercase + string.digits
        nickname = ''.join(random.choice(chars) for _ in range(length))
        
        # Добавляем префикс для читаемости
        prefixes = ["user", "player", "gamer", "test", "qa", "demo"]
        return f"{random.choice(prefixes)}{nickname}"
    
    def generate_email(self, name: str = None) -> str:
        """
        Генерация email адреса
        
        Args:
            name: Имя для email (если не указано, генерируется случайное)
        
        Returns:
            Email адрес
        """
        if name is None:
            name = self.generate_nickname()
        else:
            # Очистка имени для email
            name = name.lower().replace(" ", ".").replace("_", "")
        
        domain = random.choice(self.email_domains)
        timestamp = random.randint(1, 9999)
        
        return f"{name}{timestamp}@{domain}"
    
    def generate_phone(self, country_code: str = "+7") -> str:
        """
        Генерация номера телефона
        
        Args:
            country_code: Код страны (по умолчанию +7 для России)
        
        Returns:
            Номер телефона
        """
        if country_code == "+7":
            # Российский формат: +7 9XX XXX-XX-XX
            return f"+7 9{random.randint(10, 99)} {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        else:
            # Общий формат
            return f"{country_code} {random.randint(1000000000, 9999999999)}"
    
    # ==================== ПАРОЛИ И БЕЗОПАСНОСТЬ ====================
    
    def generate_password(self, 
                         length: int = 12,
                         use_upper: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True) -> str:
        """
        Генерация пароля
        
        Args:
            length: Длина пароля
            use_upper: Использовать заглавные буквы
            use_digits: Использовать цифры
            use_special: Использовать специальные символы
        
        Returns:
            Сгенерированный пароль
        """
        chars = string.ascii_lowercase
        
        if use_upper:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*"
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    def generate_weak_password(self) -> str:
        """Генерация слабого пароля для негативных тестов"""
        weak_passwords = ["123456", "password", "12345678", "qwerty", "abc123", "111111"]
        return random.choice(weak_passwords)
    
    def generate_strong_password(self) -> str:
        """Генерация надежного пароля"""
        return random.choice(self.password_patterns)
    
    # ==================== ЧИСЛОВЫЕ ДАННЫЕ ====================
    
    def generate_integer(self, min_val: int = 0, max_val: int = 100) -> int:
        """Генерация случайного целого числа"""
        return random.randint(min_val, max_val)
    
    def generate_float(self, min_val: float = 0.0, max_val: float = 100.0, decimals: int = 2) -> float:
        """Генерация случайного числа с плавающей точкой"""
        value = random.uniform(min_val, max_val)
        return round(value, decimals)
    
    def generate_price(self, min_price: float = 1.0, max_price: float = 1000.0) -> float:
        """Генерация цены"""
        return round(random.uniform(min_price, max_price), 2)
    
    def generate_currency_amount(self, currency: str = "soft", min_val: int = 100, max_val: int = 10000) -> int:
        """
        Генерация игровой валюты
        
        Args:
            currency: Тип валюты (soft/hard/premium)
            min_val: Минимальное значение
            max_val: Максимальное значение
        
        Returns:
            Количество валюты
        """
        return random.randint(min_val, max_val)
    
    # ==================== ДАТЫ И ВРЕМЯ ====================
    
    def generate_date(self, 
                     start_date: datetime = None,
                     end_date: datetime = None,
                     format: str = "%Y-%m-%d") -> str:
        """
        Генерация случайной даты
        
        Args:
            start_date: Начальная дата (по умолчанию - год назад)
            end_date: Конечная дата (по умолчанию - сегодня)
            format: Формат даты
        
        Returns:
            Дата в указанном формате
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime(format)
    
    def generate_birth_date(self, min_age: int = 18, max_age: int = 65) -> str:
        """Генерация даты рождения"""
        today = datetime.now()
        start_date = today - timedelta(days=max_age * 365)
        end_date = today - timedelta(days=min_age * 365)
        
        return self.generate_date(start_date, end_date, "%d.%m.%Y")
    
    def generate_future_date(self, days_ahead: int = 30) -> str:
        """Генерация будущей даты"""
        future_date = datetime.now() + timedelta(days=random.randint(1, days_ahead))
        return future_date.strftime("%Y-%m-%d")
    
    # ==================== ТЕКСТОВЫЕ ДАННЫЕ ====================
    
    def generate_text(self, min_words: int = 5, max_words: int = 20) -> str:
        """Генерация случайного текста (Lorem Ipsum)"""
        words = [
            "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
            "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
            "incididunt", "ut", "labore", "et", "dolore", "magna",
            "aliqua", "enim", "ad", "minim", "veniam", "quis"
        ]
        
        num_words = random.randint(min_words, max_words)
        text = ' '.join(random.choice(words) for _ in range(num_words))
        return text.capitalize() + "."
    
    def generate_description(self) -> str:
        """Генерация описания"""
        return self.generate_text(10, 30)
    
    def generate_comment(self) -> str:
        """Генерация комментария"""
        return self.generate_text(5, 15)
    
    # ==================== ИГРОВЫЕ ДАННЫЕ ====================
    
    def generate_character_name(self) -> str:
        """Генерация имени персонажа"""
        prefixes = ["Dark", "Mighty", "Swift", "Brave", "Iron", "Shadow", "Golden", "Storm"]
        suffixes = ["Warrior", "Knight", "Mage", "Assassin", "Hunter", "Paladin", "Rogue", "Berserker"]
        
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def generate_character_stats(self) -> Dict[str, int]:
        """Генерация характеристик персонажа"""
        return {
            "strength": random.randint(1, 100),
            "agility": random.randint(1, 100),
            "intelligence": random.randint(1, 100),
            "vitality": random.randint(1, 100),
            "luck": random.randint(1, 100),
            "level": random.randint(1, 50)
        }
    
    def generate_item_name(self) -> str:
        """Генерация названия предмета"""
        qualities = ["Common", "Rare", "Epic", "Legendary", "Mythic"]
        types = ["Sword", "Shield", "Armor", "Helmet", "Boots", "Ring", "Amulet", "Potion"]
        
        return f"{random.choice(qualities)} {random.choice(types)}"
    
    # ==================== ЭКВИВАЛЕНТНОЕ РАЗБИЕНИЕ (BVA) ====================
    
    def get_boundary_lengths(self, min_len: int, max_len: int) -> List[Dict[str, Any]]:
        """
        Получение граничных значений длины для тестирования
        
        Args:
            min_len: Минимальная допустимая длина
            max_len: Максимальная допустимая длина
        
        Returns:
            Список словарей с длиной, типом границы и ожидаемым результатом
        """
        boundaries = []
        
        # Ниже минимума (невалидное)
        if min_len > 0:
            boundaries.append({
                "length": min_len - 1,
                "boundary_type": "below_min",
                "description": f"Ниже минимума ({min_len - 1} < {min_len})",
                "expected_valid": False
            })
        
        # Минимум (валидное)
        boundaries.append({
            "length": min_len,
            "boundary_type": "min",
            "description": f"Минимум ({min_len})",
            "expected_valid": True
        })
        
        # Выше минимума (валидное)
        if min_len + 1 <= max_len:
            boundaries.append({
                "length": min_len + 1,
                "boundary_type": "above_min",
                "description": f"Выше минимума ({min_len + 1})",
                "expected_valid": True
            })
        
        # Ниже максимума (валидное)
        if max_len - 1 >= min_len and max_len - 1 != min_len + 1:
            boundaries.append({
                "length": max_len - 1,
                "boundary_type": "below_max",
                "description": f"Ниже максимума ({max_len - 1})",
                "expected_valid": True
            })
        
        # Максимум (валидное)
        boundaries.append({
            "length": max_len,
            "boundary_type": "max",
            "description": f"Максимум ({max_len})",
            "expected_valid": True
        })
        
        # Выше максимума (невалидное)
        boundaries.append({
            "length": max_len + 1,
            "boundary_type": "above_max",
            "description": f"Выше максимума ({max_len + 1} > {max_len})",
            "expected_valid": False
        })
        
        return boundaries
    
    def generate_string_exact_length(self, 
                                     length: int,
                                     use_letters: bool = True,
                                     use_digits: bool = False,
                                     use_special: bool = False,
                                     use_cyrillic: bool = False,
                                     use_uppercase: bool = False) -> str:
        """
        Генерация строки точной длины с заданными параметрами
        
        Args:
            length: Точная длина строки
            use_letters: Использовать латинские буквы
            use_digits: Использовать цифры
            use_special: Использовать специальные символы
            use_cyrillic: Использовать кириллицу
            use_uppercase: Использовать заглавные буквы
        
        Returns:
            Строка заданной длины
        """
        chars = ""
        
        if use_letters:
            chars += string.ascii_lowercase
            if use_uppercase:
                chars += string.ascii_uppercase
        
        if use_cyrillic:
            chars += "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            if use_uppercase:
                chars += "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        
        if use_digits:
            chars += string.digits
        
        if use_special:
            chars += "!@#$%^&*_-+="
        
        # Если ничего не выбрано, используем латиницу по умолчанию
        if not chars:
            chars = string.ascii_lowercase
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_boundary_test_data(self,
                                    field_name: str,
                                    min_len: int,
                                    max_len: int,
                                    use_letters: bool = True,
                                    use_digits: bool = False,
                                    use_special: bool = False,
                                    use_cyrillic: bool = False,
                                    use_uppercase: bool = False) -> List[Dict[str, Any]]:
        """
        Генерация тестовых данных по технике эквивалентного разбиения (BVA)
        
        Args:
            field_name: Название поля (login, password, nickname и т.д.)
            min_len: Минимальная допустимая длина
            max_len: Максимальная допустимая длина
            use_letters: Использовать латинские буквы
            use_digits: Использовать цифры
            use_special: Использовать специальные символы
            use_cyrillic: Использовать кириллицу
            use_uppercase: Использовать заглавные буквы
        
        Returns:
            Список тестовых данных с граничными значениями
        """
        boundaries = self.get_boundary_lengths(min_len, max_len)
        test_data = []
        
        for boundary in boundaries:
            value = self.generate_string_exact_length(
                length=boundary["length"],
                use_letters=use_letters,
                use_digits=use_digits,
                use_special=use_special,
                use_cyrillic=use_cyrillic,
                use_uppercase=use_uppercase
            )
            
            test_data.append({
                "field": field_name,
                "value": value,
                "length": boundary["length"],
                "boundary_type": boundary["boundary_type"],
                "description": boundary["description"],
                "expected_valid": boundary["expected_valid"],
                "test_case": f"{'POSITIVE' if boundary['expected_valid'] else 'NEGATIVE'}: {field_name} - {boundary['description']}"
            })
        
        return test_data
    
    def generate_numeric_boundary_test_data(self,
                                            field_name: str,
                                            min_val: int,
                                            max_val: int) -> List[Dict[str, Any]]:
        """
        Генерация тестовых данных для числовых полей по технике BVA
        
        Args:
            field_name: Название поля
            min_val: Минимальное допустимое значение
            max_val: Максимальное допустимое значение
        
        Returns:
            Список тестовых данных с граничными значениями
        """
        test_data = []
        
        boundaries = [
            (min_val - 1, "below_min", f"Ниже минимума ({min_val - 1})", False),
            (min_val, "min", f"Минимум ({min_val})", True),
            (min_val + 1, "above_min", f"Выше минимума ({min_val + 1})", True),
            (max_val - 1, "below_max", f"Ниже максимума ({max_val - 1})", True),
            (max_val, "max", f"Максимум ({max_val})", True),
            (max_val + 1, "above_max", f"Выше максимума ({max_val + 1})", False),
        ]
        
        for value, boundary_type, description, expected_valid in boundaries:
            test_data.append({
                "field": field_name,
                "value": value,
                "boundary_type": boundary_type,
                "description": description,
                "expected_valid": expected_valid,
                "test_case": f"{'POSITIVE' if expected_valid else 'NEGATIVE'}: {field_name} - {description}"
            })
        
        return test_data
    
    # ==================== МАССОВАЯ ГЕНЕРАЦИЯ ====================
    
    def generate_user(self) -> Dict[str, Any]:
        """Генерация полного набора данных пользователя"""
        first_name = self.generate_first_name()
        last_name = self.generate_last_name()
        
        return {
            "id": random.randint(1000, 999999),
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "nickname": self.generate_nickname(),
            "email": self.generate_email(first_name.lower()),
            "phone": self.generate_phone(),
            "password": self.generate_strong_password(),
            "birth_date": self.generate_birth_date(),
            "created_at": self.generate_date(),
            "is_active": random.choice([True, False]),
            "balance_soft": self.generate_currency_amount("soft", 100, 5000),
            "balance_hard": self.generate_currency_amount("hard", 0, 1000)
        }
    
    def generate_users(self, count: int = 10) -> List[Dict[str, Any]]:
        """Генерация списка пользователей"""
        return [self.generate_user() for _ in range(count)]
    
    def generate_character(self) -> Dict[str, Any]:
        """Генерация игрового персонажа"""
        return {
            "id": random.randint(1000, 999999),
            "name": self.generate_character_name(),
            "level": random.randint(1, 50),
            "experience": random.randint(0, 1000000),
            "stats": self.generate_character_stats(),
            "rarity": random.choice(["Common", "Rare", "Epic", "Legendary"]),
            "price": self.generate_price(100, 10000),
            "created_at": self.generate_date()
        }
    
    def generate_characters(self, count: int = 10) -> List[Dict[str, Any]]:
        """Генерация списка персонажей"""
        return [self.generate_character() for _ in range(count)]
    
    # ==================== ЭКСПОРТ ====================
    
    def export_to_json(self, data: Any, filename: str, output_dir: str = None):
        """
        Экспорт данных в JSON файл
        
        Args:
            data: Данные для экспорта
            filename: Имя файла
            output_dir: Папка для сохранения (по умолчанию TestData)
        """
        if output_dir is None:
            output_dir = TEST_DATA_DIR
        
        # Создаем папку если не существует
        os.makedirs(output_dir, exist_ok=True)
        
        # Полный путь к файлу
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Данные экспортированы в {filepath}")
    
    def export_to_csv(self, data: List[Dict], filename: str, output_dir: str = None):
        """
        Экспорт данных в CSV файл
        
        Args:
            data: Список словарей для экспорта
            filename: Имя файла
            output_dir: Папка для сохранения (по умолчанию TestData)
        """
        import csv
        
        if not data:
            print("❌ Нет данных для экспорта")
            return
        
        if output_dir is None:
            output_dir = TEST_DATA_DIR
        
        # Создаем папку если не существует
        os.makedirs(output_dir, exist_ok=True)
        
        # Полный путь к файлу
        filepath = os.path.join(output_dir, filename)
        
        keys = data[0].keys()
        
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Данные экспортированы в {filepath}")


# ==================== ИНТЕРАКТИВНАЯ КОНСОЛЬ ====================

class InteractiveConsole:
    """Интерактивная консоль для генерации тестовых данных"""
    
    def __init__(self):
        self.generator = None
        self.locale = "ru"
        self.last_generated_data = None
    
    def clear_screen(self):
        """Очистка экрана (кроссплатформенная)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Вывод заголовка"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_menu(self, title: str, options: List[tuple]):
        """
        Вывод меню с опциями
        
        Args:
            title: Заголовок меню
            options: Список кортежей (номер, описание)
        """
        self.print_header(title)
        for num, desc in options:
            print(f"  {num}. {desc}")
        print("=" * 70)
    
    def get_input(self, prompt: str, default: Any = None, input_type: type = str) -> Any:
        """
        Получение ввода от пользователя с валидацией
        
        Args:
            prompt: Текст запроса
            default: Значение по умолчанию
            input_type: Тип ожидаемых данных (str, int, float)
        
        Returns:
            Введенное значение
        """
        while True:
            try:
                if default is not None:
                    user_input = input(f"{prompt} [{default}]: ").strip()
                    if not user_input:
                        return default
                else:
                    user_input = input(f"{prompt}: ").strip()
                
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input
            except ValueError:
                print(f"❌ Ошибка: введите корректное значение типа {input_type.__name__}")
    
    def get_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Получение ответа да/нет"""
        default_str = "Y/n" if default else "y/N"
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes', 'д', 'да']
    
    def initialize_generator(self):
        """Инициализация генератора с выбором локали"""
        self.print_header("НАСТРОЙКА ГЕНЕРАТОРА")
        print("\nВыберите локаль для генерации данных:")
        print("  1. Русский (ru)")
        print("  2. Английский (en)")
        
        choice = self.get_input("Ваш выбор", "1")
        self.locale = "en" if choice == "2" else "ru"
        
        self.generator = TestDataGenerator(locale=self.locale)
        print(f"\n✅ Генератор инициализирован (локаль: {self.locale})")
        input("\nНажмите Enter для продолжения...")
    
    def generate_users_interactive(self):
        """Интерактивная генерация пользователей"""
        self.print_header("ГЕНЕРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ")
        
        count = self.get_input("Количество пользователей", 10, int)
        
        print("\n⏳ Генерация пользователей...")
        users = self.generator.generate_users(count)
        
        print(f"\n✅ Сгенерировано {len(users)} пользователей:\n")
        print("-" * 70)
        
        for i, user in enumerate(users, 1):
            print(f"{i}. {user['full_name']}")
            print(f"   📧 Email: {user['email']}")
            print(f"   👤 Nickname: {user['nickname']}")
            print(f"   📱 Phone: {user['phone']}")
            print(f"   🔑 Password: {user['password']}")
            print(f"   💰 Баланс: Soft={user['balance_soft']}, Hard={user['balance_hard']}")
            print()
        
        self.last_generated_data = users
        self.offer_export(users, "users")
    
    def generate_characters_interactive(self):
        """Интерактивная генерация персонажей"""
        self.print_header("ГЕНЕРАЦИЯ ИГРОВЫХ ПЕРСОНАЖЕЙ")
        
        count = self.get_input("Количество персонажей", 5, int)
        
        print("\n⏳ Генерация персонажей...")
        characters = self.generator.generate_characters(count)
        
        print(f"\n✅ Сгенерировано {len(characters)} персонажей:\n")
        print("-" * 70)
        
        for i, char in enumerate(characters, 1):
            print(f"{i}. ⚔️ {char['name']} (Level {char['level']})")
            print(f"   🌟 Редкость: {char['rarity']}")
            print(f"   💎 Цена: {char['price']}")
            print(f"   📊 Характеристики:")
            for stat, value in char['stats'].items():
                print(f"      • {stat.capitalize()}: {value}")
            print()
        
        self.last_generated_data = characters
        self.offer_export(characters, "characters")
    
    def generate_emails_interactive(self):
        """Интерактивная генерация email адресов"""
        self.print_header("ГЕНЕРАЦИЯ EMAIL АДРЕСОВ")
        
        count = self.get_input("Количество email адресов", 10, int)
        use_names = self.get_yes_no("Использовать реальные имена", True)
        
        print("\n⏳ Генерация email адресов...")
        emails = []
        
        for _ in range(count):
            if use_names:
                name = self.generator.generate_first_name().lower()
                email = self.generator.generate_email(name)
            else:
                email = self.generator.generate_email()
            emails.append({"email": email})
        
        print(f"\n✅ Сгенерировано {len(emails)} email адресов:\n")
        print("-" * 70)
        
        for i, item in enumerate(emails, 1):
            print(f"{i}. {item['email']}")
        
        self.last_generated_data = emails
        self.offer_export(emails, "emails")
    
    def generate_passwords_interactive(self):
        """Интерактивная генерация паролей"""
        self.print_header("ГЕНЕРАЦИЯ ПАРОЛЕЙ")
        
        count = self.get_input("Количество паролей", 10, int)
        length = self.get_input("Длина пароля", 12, int)
        
        print("\nНастройки пароля:")
        use_upper = self.get_yes_no("Использовать заглавные буквы", True)
        use_digits = self.get_yes_no("Использовать цифры", True)
        use_special = self.get_yes_no("Использовать специальные символы", True)
        
        print("\n⏳ Генерация паролей...")
        passwords = []
        
        for _ in range(count):
            password = self.generator.generate_password(length, use_upper, use_digits, use_special)
            passwords.append({"password": password})
        
        print(f"\n✅ Сгенерировано {len(passwords)} паролей:\n")
        print("-" * 70)
        
        for i, item in enumerate(passwords, 1):
            print(f"{i}. {item['password']}")
        
        self.last_generated_data = passwords
        self.offer_export(passwords, "passwords")
    
    def generate_phones_interactive(self):
        """Интерактивная генерация телефонов"""
        self.print_header("ГЕНЕРАЦИЯ НОМЕРОВ ТЕЛЕФОНОВ")
        
        count = self.get_input("Количество номеров", 10, int)
        
        print("\nВыберите код страны:")
        print("  1. +7 (Россия/Казахстан)")
        print("  2. +1 (США/Канада)")
        print("  3. +44 (Великобритания)")
        print("  4. +49 (Германия)")
        print("  5. Другой")
        
        choice = self.get_input("Ваш выбор", "1")
        
        country_codes = {
            "1": "+7",
            "2": "+1",
            "3": "+44",
            "4": "+49"
        }
        
        if choice == "5":
            country_code = self.get_input("Введите код страны", "+7")
        else:
            country_code = country_codes.get(choice, "+7")
        
        print("\n⏳ Генерация телефонов...")
        phones = []
        
        for _ in range(count):
            phone = self.generator.generate_phone(country_code)
            phones.append({"phone": phone})
        
        print(f"\n✅ Сгенерировано {len(phones)} номеров:\n")
        print("-" * 70)
        
        for i, item in enumerate(phones, 1):
            print(f"{i}. {item['phone']}")
        
        self.last_generated_data = phones
        self.offer_export(phones, "phones")
    
    def generate_prices_interactive(self):
        """Интерактивная генерация цен"""
        self.print_header("ГЕНЕРАЦИЯ ЦЕН")
        
        count = self.get_input("Количество цен", 20, int)
        min_price = self.get_input("Минимальная цена", 1.0, float)
        max_price = self.get_input("Максимальная цена", 1000.0, float)
        
        print("\n⏳ Генерация цен...")
        prices = []
        
        for _ in range(count):
            price = self.generator.generate_price(min_price, max_price)
            prices.append({"price": price})
        
        print(f"\n✅ Сгенерировано {len(prices)} цен:\n")
        print("-" * 70)
        
        for i, item in enumerate(prices, 1):
            print(f"{i}. ${item['price']:.2f}")
        
        self.last_generated_data = prices
        self.offer_export(prices, "prices")
    
    def generate_dates_interactive(self):
        """Интерактивная генерация дат"""
        self.print_header("ГЕНЕРАЦИЯ ДАТ")
        
        count = self.get_input("Количество дат", 10, int)
        
        print("\nТип дат:")
        print("  1. Случайные даты (последний год)")
        print("  2. Даты рождения (18-65 лет)")
        print("  3. Будущие даты (следующие 30 дней)")
        
        choice = self.get_input("Ваш выбор", "1")
        
        print("\n⏳ Генерация дат...")
        dates = []
        
        for _ in range(count):
            if choice == "2":
                date = self.generator.generate_birth_date()
            elif choice == "3":
                date = self.generator.generate_future_date()
            else:
                date = self.generator.generate_date()
            
            dates.append({"date": date})
        
        print(f"\n✅ Сгенерировано {len(dates)} дат:\n")
        print("-" * 70)
        
        for i, item in enumerate(dates, 1):
            print(f"{i}. {item['date']}")
        
        self.last_generated_data = dates
        self.offer_export(dates, "dates")
    
    def generate_custom_data(self):
        """Генерация произвольных комбинаций данных"""
        self.print_header("ГЕНЕРАЦИЯ ПРОИЗВОЛЬНЫХ ДАННЫХ")
        
        count = self.get_input("Количество записей", 10, int)
        
        print("\nВыберите поля для генерации (через запятую):")
        print("Доступные поля:")
        print("  1. name - Полное имя")
        print("  2. email - Email адрес")
        print("  3. phone - Телефон")
        print("  4. password - Пароль")
        print("  5. nickname - Никнейм")
        print("  6. price - Цена")
        print("  7. date - Дата")
        print("  8. balance - Баланс (soft/hard)")
        print("  9. character_name - Имя персонажа")
        print("  10. item_name - Название предмета")
        
        fields_input = self.get_input("\nВведите номера через запятую", "1,2,3")
        selected_fields = [f.strip() for f in fields_input.split(",")]
        
        field_mapping = {
            "1": "name", "2": "email", "3": "phone", "4": "password",
            "5": "nickname", "6": "price", "7": "date", "8": "balance",
            "9": "character_name", "10": "item_name"
        }
        
        fields_to_generate = [field_mapping.get(f, f) for f in selected_fields]
        
        print(f"\n⏳ Генерация {count} записей с полями: {', '.join(fields_to_generate)}...")
        custom_data = []
        
        for _ in range(count):
            record = {}
            for field in fields_to_generate:
                if field == "name":
                    record["name"] = self.generator.generate_full_name()
                elif field == "email":
                    record["email"] = self.generator.generate_email()
                elif field == "phone":
                    record["phone"] = self.generator.generate_phone()
                elif field == "password":
                    record["password"] = self.generator.generate_strong_password()
                elif field == "nickname":
                    record["nickname"] = self.generator.generate_nickname()
                elif field == "price":
                    record["price"] = self.generator.generate_price()
                elif field == "date":
                    record["date"] = self.generator.generate_date()
                elif field == "balance":
                    record["balance_soft"] = self.generator.generate_currency_amount("soft")
                    record["balance_hard"] = self.generator.generate_currency_amount("hard")
                elif field == "character_name":
                    record["character_name"] = self.generator.generate_character_name()
                elif field == "item_name":
                    record["item_name"] = self.generator.generate_item_name()
            
            custom_data.append(record)
        
        print(f"\n✅ Сгенерировано {len(custom_data)} записей:\n")
        print("-" * 70)
        
        for i, record in enumerate(custom_data, 1):
            print(f"{i}. {record}")
        
        self.last_generated_data = custom_data
        self.offer_export(custom_data, "custom_data")
    
    def generate_boundary_data_interactive(self):
        """Интерактивная генерация данных по технике эквивалентного разбиения (BVA)"""
        self.print_header("ЭКВИВАЛЕНТНОЕ РАЗБИЕНИЕ (BOUNDARY VALUE ANALYSIS)")
        
        print("\n📋 Техника граничных значений генерирует тестовые данные")
        print("   для проверки границ допустимых значений.")
        print("\n   Для диапазона 3-16 символов будут созданы значения:")
        print("   • 2 символа  (ниже минимума - NEGATIVE)")
        print("   • 3 символа  (минимум - POSITIVE)")
        print("   • 4 символа  (выше минимума - POSITIVE)")
        print("   • 15 символов (ниже максимума - POSITIVE)")
        print("   • 16 символов (максимум - POSITIVE)")
        print("   • 17 символов (выше максимума - NEGATIVE)")
        
        print("\n" + "-" * 70)
        print("Выберите тип данных:")
        print("  1. Строковые данные (логин, пароль, никнейм и т.д.)")
        print("  2. Числовые данные (возраст, количество, уровень и т.д.)")
        
        data_type = self.get_input("\nВаш выбор", "1")
        
        if data_type == "2":
            self._generate_numeric_boundary_interactive()
        else:
            self._generate_string_boundary_interactive()
    
    def _generate_string_boundary_interactive(self):
        """Генерация граничных строковых данных"""
        print("\n" + "=" * 70)
        print("  НАСТРОЙКА СТРОКОВЫХ ГРАНИЧНЫХ ДАННЫХ")
        print("=" * 70)
        
        # Название поля
        print("\nПресеты полей:")
        print("  1. login (логин)")
        print("  2. password (пароль)")
        print("  3. nickname (никнейм)")
        print("  4. username (имя пользователя)")
        print("  5. Другое (ввести вручную)")
        
        preset = self.get_input("Выберите поле", "1")
        
        presets = {
            "1": ("login", 3, 16),
            "2": ("password", 8, 32),
            "3": ("nickname", 3, 20),
            "4": ("username", 4, 24),
        }
        
        if preset in presets:
            field_name, default_min, default_max = presets[preset]
        else:
            field_name = self.get_input("Введите название поля", "field")
            default_min, default_max = 1, 10
        
        # Границы
        min_len = self.get_input(f"Минимальная длина для {field_name}", default_min, int)
        max_len = self.get_input(f"Максимальная длина для {field_name}", default_max, int)
        
        if min_len < 0:
            print("❌ Минимальная длина не может быть отрицательной")
            return
        
        if max_len < min_len:
            print("❌ Максимальная длина не может быть меньше минимальной")
            return
        
        # Параметры генерации
        print("\n⚙️ Параметры генерации строк:")
        use_letters = self.get_yes_no("Использовать латинские буквы", True)
        use_cyrillic = self.get_yes_no("Использовать кириллицу", False)
        use_uppercase = self.get_yes_no("Использовать заглавные буквы", False)
        use_digits = self.get_yes_no("Использовать цифры", True)
        use_special = self.get_yes_no("Использовать спецсимволы (!@#$%^&*)", False)
        
        # Генерация
        print(f"\n⏳ Генерация граничных значений для '{field_name}' ({min_len}-{max_len} символов)...")
        
        test_data = self.generator.generate_boundary_test_data(
            field_name=field_name,
            min_len=min_len,
            max_len=max_len,
            use_letters=use_letters,
            use_digits=use_digits,
            use_special=use_special,
            use_cyrillic=use_cyrillic,
            use_uppercase=use_uppercase
        )
        
        # Вывод результатов
        print(f"\n✅ Сгенерировано {len(test_data)} тестовых значений:\n")
        print("-" * 70)
        
        for i, item in enumerate(test_data, 1):
            status = "✅ POSITIVE" if item["expected_valid"] else "❌ NEGATIVE"
            print(f"\n{i}. {status}")
            print(f"   📋 Тест-кейс: {item['test_case']}")
            print(f"   📏 Длина: {item['length']} символов")
            print(f"   📝 Значение: {item['value']}")
            print(f"   🎯 Тип границы: {item['boundary_type']}")
        
        self.last_generated_data = test_data
        self.offer_export(test_data, f"bva_{field_name}")
    
    def _generate_numeric_boundary_interactive(self):
        """Генерация граничных числовых данных"""
        print("\n" + "=" * 70)
        print("  НАСТРОЙКА ЧИСЛОВЫХ ГРАНИЧНЫХ ДАННЫХ")
        print("=" * 70)
        
        # Название поля
        print("\nПресеты полей:")
        print("  1. age (возраст)")
        print("  2. level (уровень)")
        print("  3. quantity (количество)")
        print("  4. score (очки)")
        print("  5. Другое (ввести вручную)")
        
        preset = self.get_input("Выберите поле", "1")
        
        presets = {
            "1": ("age", 18, 100),
            "2": ("level", 1, 100),
            "3": ("quantity", 1, 999),
            "4": ("score", 0, 10000),
        }
        
        if preset in presets:
            field_name, default_min, default_max = presets[preset]
        else:
            field_name = self.get_input("Введите название поля", "field")
            default_min, default_max = 0, 100
        
        # Границы
        min_val = self.get_input(f"Минимальное значение для {field_name}", default_min, int)
        max_val = self.get_input(f"Максимальное значение для {field_name}", default_max, int)
        
        if max_val < min_val:
            print("❌ Максимальное значение не может быть меньше минимального")
            return
        
        # Генерация
        print(f"\n⏳ Генерация граничных значений для '{field_name}' ({min_val}-{max_val})...")
        
        test_data = self.generator.generate_numeric_boundary_test_data(
            field_name=field_name,
            min_val=min_val,
            max_val=max_val
        )
        
        # Вывод результатов
        print(f"\n✅ Сгенерировано {len(test_data)} тестовых значений:\n")
        print("-" * 70)
        
        for i, item in enumerate(test_data, 1):
            status = "✅ POSITIVE" if item["expected_valid"] else "❌ NEGATIVE"
            print(f"\n{i}. {status}")
            print(f"   📋 Тест-кейс: {item['test_case']}")
            print(f"   🔢 Значение: {item['value']}")
            print(f"   🎯 Тип границы: {item['boundary_type']}")
        
        self.last_generated_data = test_data
        self.offer_export(test_data, f"bva_{field_name}")
    
    def offer_export(self, data: Any, default_name: str):
        """Предложение экспорта данных"""
        print("\n" + "-" * 70)
        if self.get_yes_no("Экспортировать данные в файл?", True):
            self.export_data_interactive(data, default_name)
    
    def export_data_interactive(self, data: Any = None, default_name: str = "data"):
        """Интерактивный экспорт данных"""
        if data is None:
            if self.last_generated_data is None:
                print("\n❌ Нет данных для экспорта. Сначала сгенерируйте данные.")
                input("\nНажмите Enter для продолжения...")
                return
            data = self.last_generated_data
        
        self.print_header("ЭКСПОРТ ДАННЫХ")
        
        print("\nВыберите формат экспорта:")
        print("  1. JSON")
        print("  2. CSV")
        print("  3. Оба формата")
        
        choice = self.get_input("Ваш выбор", "1")
        
        filename = self.get_input("Имя файла (без расширения)", default_name)
        
        print("\n⏳ Экспорт данных...")
        
        if choice in ["1", "3"]:
            self.generator.export_to_json(data, f"{filename}.json")
        
        if choice in ["2", "3"]:
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                self.generator.export_to_csv(data, f"{filename}.csv")
            else:
                print("⚠️ CSV экспорт доступен только для списков словарей")
        
        print("\n✅ Экспорт завершен!")
        input("\nНажмите Enter для продолжения...")
    
    def show_main_menu(self):
        """Отображение главного меню"""
        while True:
            self.clear_screen()
            
            options = [
                ("1", "👥 Генерация пользователей"),
                ("2", "⚔️ Генерация игровых персонажей"),
                ("3", "📧 Генерация email адресов"),
                ("4", "🔑 Генерация паролей"),
                ("5", "📱 Генерация телефонов"),
                ("6", "💰 Генерация цен"),
                ("7", "📅 Генерация дат"),
                ("8", "🔧 Генерация произвольных данных"),
                ("9", "🎯 Эквивалентное разбиение (BVA)"),
                ("10", "💾 Экспорт последних данных"),
                ("0", "🚪 Выход")
            ]
            
            self.print_menu("ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ - ГЛАВНОЕ МЕНЮ", options)
            print(f"\nТекущая локаль: {self.locale.upper()}")
            print(f"📁 Папка экспорта: {TEST_DATA_DIR}")
            
            choice = self.get_input("\nВыберите действие", "0")
            
            if choice == "1":
                self.generate_users_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "2":
                self.generate_characters_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "3":
                self.generate_emails_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "4":
                self.generate_passwords_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "5":
                self.generate_phones_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "6":
                self.generate_prices_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "7":
                self.generate_dates_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "8":
                self.generate_custom_data()
                input("\nНажмите Enter для продолжения...")
            elif choice == "9":
                self.generate_boundary_data_interactive()
                input("\nНажмите Enter для продолжения...")
            elif choice == "10":
                self.export_data_interactive()
            elif choice == "0":
                print("\n👋 До свидания!")
                break
            else:
                print("\n❌ Неверный выбор. Попробуйте снова.")
                input("\nНажмите Enter для продолжения...")
    
    def run(self):
        """Запуск консоли"""
        self.clear_screen()
        self.print_header("ДОБРО ПОЖАЛОВАТЬ В ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ!")
        print("\nЭтот инструмент поможет вам создать тестовые данные для QA проектов.")
        input("\nНажмите Enter для начала...")
        
        self.initialize_generator()
        self.show_main_menu()


# ==================== ЗАПУСК ====================

def main():
    """Запуск интерактивной консоли"""
    console = InteractiveConsole()
    console.run()


if __name__ == "__main__":
    main()

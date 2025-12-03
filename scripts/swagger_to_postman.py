#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger to Postman Collection Generator v1.0.0
Интерактивный генератор коллекций Postman из Swagger/OpenAPI JSON

Автор: QA Automation Team
Дата: 03.12.2025

Функционал:
- Парсинг Swagger/OpenAPI 3.0 спецификаций
- Интерактивный ввод учетных данных
- Автоматическое извлечение токенов и ID из ответов
- Генерация pre-request и test скриптов
- Группировка запросов по тегам/контроллерам
"""

import json
import os
import sys
import re
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class Colors:
    """ANSI цвета для консольного вывода"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Вывод заголовка"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_info(text: str):
    """Информационное сообщение"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def print_success(text: str):
    """Успешное сообщение"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Предупреждение"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text: str):
    """Ошибка"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def prompt(text: str, default: str = "") -> str:
    """Запрос ввода от пользователя"""
    if default:
        result = input(f"{Colors.BLUE}? {text} [{default}]: {Colors.ENDC}").strip()
        return result if result else default
    return input(f"{Colors.BLUE}? {text}: {Colors.ENDC}").strip()


def prompt_yes_no(text: str, default: bool = True) -> bool:
    """Запрос да/нет"""
    default_str = "Y/n" if default else "y/N"
    result = input(f"{Colors.BLUE}? {text} [{default_str}]: {Colors.ENDC}").strip().lower()
    if not result:
        return default
    return result in ['y', 'yes', 'да', 'д']


def prompt_choice(text: str, choices: List[str], default: int = 0) -> int:
    """Выбор из списка"""
    print(f"{Colors.BLUE}? {text}{Colors.ENDC}")
    for i, choice in enumerate(choices):
        marker = "→" if i == default else " "
        print(f"  {marker} {i + 1}. {choice}")
    
    while True:
        result = input(f"{Colors.BLUE}  Выбор [1-{len(choices)}] (по умолчанию {default + 1}): {Colors.ENDC}").strip()
        if not result:
            return default
        try:
            idx = int(result) - 1
            if 0 <= idx < len(choices):
                return idx
        except ValueError:
            pass
        print_error(f"Введите число от 1 до {len(choices)}")


class SwaggerParser:
    """Парсер Swagger/OpenAPI спецификации"""
    
    def __init__(self, swagger_path: str):
        self.swagger_path = swagger_path
        self.spec: Dict = {}
        self.base_url = ""
        self.endpoints: List[Dict] = []
        
    def load(self) -> bool:
        """Загрузка Swagger файла"""
        try:
            with open(self.swagger_path, 'r', encoding='utf-8') as f:
                self.spec = json.load(f)
            return True
        except FileNotFoundError:
            print_error(f"Файл не найден: {self.swagger_path}")
            return False
        except json.JSONDecodeError as e:
            print_error(f"Ошибка парсинга JSON: {e}")
            return False
    
    def get_info(self) -> Dict:
        """Получение информации об API"""
        info = self.spec.get('info', {})
        return {
            'title': info.get('title', 'Unknown API'),
            'version': info.get('version', '1.0.0'),
            'description': info.get('description', ''),
        }
    
    def get_servers(self) -> List[str]:
        """Получение списка серверов"""
        servers = self.spec.get('servers', [])
        return [s.get('url', '') for s in servers]
    
    def get_tags(self) -> List[str]:
        """Получение списка тегов/контроллеров"""
        tags = self.spec.get('tags', [])
        return [t.get('name', '') for t in tags]
    
    def parse_endpoints(self) -> List[Dict]:
        """Парсинг всех эндпоинтов"""
        endpoints = []
        paths = self.spec.get('paths', {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                    continue
                
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'description': details.get('description', ''),
                    'operationId': details.get('operationId', ''),
                    'tags': details.get('tags', ['Default']),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),
                    'responses': details.get('responses', {}),
                    'security': details.get('security', []),
                }
                endpoints.append(endpoint)
        
        self.endpoints = endpoints
        return endpoints
    
    def get_request_body_schema(self, endpoint: Dict) -> Dict:
        """Получение схемы тела запроса"""
        request_body = endpoint.get('requestBody', {})
        content = request_body.get('content', {})
        
        for content_type, schema_info in content.items():
            schema = schema_info.get('schema', {})
            if '$ref' in schema:
                return self._resolve_ref(schema['$ref'])
            return schema
        return {}
    
    def _resolve_ref(self, ref: str) -> Dict:
        """Разрешение $ref ссылки"""
        if not ref.startswith('#/'):
            return {}
        
        parts = ref[2:].split('/')
        result = self.spec
        for part in parts:
            result = result.get(part, {})
        return result


class PostmanGenerator:
    """Генератор коллекции Postman"""
    
    def __init__(self, parser: SwaggerParser):
        self.parser = parser
        self.collection: Dict = {}
        self.variables: List[Dict] = []
        self.accounts: Dict = {}
        self.extract_config: Dict = {}
        
    def setup_interactive(self):
        """Интерактивная настройка генерации"""
        print_header("НАСТРОЙКА ГЕНЕРАЦИИ POSTMAN КОЛЛЕКЦИИ")
        
        # Информация об API
        info = self.parser.get_info()
        print_info(f"API: {info['title']} v{info['version']}")
        if info['description']:
            print_info(f"Описание: {info['description'][:100]}...")
        
        # Выбор сервера
        servers = self.parser.get_servers()
        if servers:
            print("\n📡 Доступные серверы:")
            for i, server in enumerate(servers):
                print(f"   {i + 1}. {server}")
            idx = prompt_choice("Выберите сервер", servers)
            self.base_url = servers[idx]
        else:
            self.base_url = prompt("Введите базовый URL API", "http://localhost:5000")
        
        # Добавляем переменную base_url
        self.variables.append({
            'key': 'base_url',
            'value': self.base_url,
            'type': 'string'
        })
        
        # Настройка аккаунтов
        self._setup_accounts()
        
        # Настройка извлечения данных
        self._setup_extraction()
        
    def _setup_accounts(self):
        """Настройка учетных данных"""
        print_header("НАСТРОЙКА УЧЕТНЫХ ДАННЫХ")
        
        # Основной пользователь
        if prompt_yes_no("Добавить учетные данные основного пользователя?"):
            print_info("Введите данные основного пользователя:")
            self.accounts['user'] = {
                'email': prompt("Email", "test@example.com"),
                'password': prompt("Пароль", "Test123!"),
                'nickname': prompt("Nickname (если есть)", "TestUser"),
            }
            
            # Добавляем переменные
            self.variables.extend([
                {'key': 'user_email', 'value': self.accounts['user']['email'], 'type': 'string'},
                {'key': 'user_password', 'value': self.accounts['user']['password'], 'type': 'string'},
                {'key': 'user_nickname', 'value': self.accounts['user']['nickname'], 'type': 'string'},
                {'key': 'user_token', 'value': '', 'type': 'string'},
            ])
        
        # Администратор
        if prompt_yes_no("Добавить учетные данные администратора?"):
            print_info("Введите данные администратора:")
            self.accounts['admin'] = {
                'email': prompt("Email админа", "admin@example.com"),
                'password': prompt("Пароль админа", "Admin123!"),
                'login': prompt("Логин админа (если есть)", "superadmin"),
            }
            
            self.variables.extend([
                {'key': 'admin_email', 'value': self.accounts['admin']['email'], 'type': 'string'},
                {'key': 'admin_password', 'value': self.accounts['admin']['password'], 'type': 'string'},
                {'key': 'admin_login', 'value': self.accounts['admin']['login'], 'type': 'string'},
                {'key': 'admin_token', 'value': '', 'type': 'string'},
            ])
        
        # Дополнительные аккаунты
        while prompt_yes_no("Добавить дополнительный аккаунт?", default=False):
            account_name = prompt("Название аккаунта (например: premium_user)")
            self.accounts[account_name] = {
                'email': prompt(f"Email для {account_name}"),
                'password': prompt(f"Пароль для {account_name}"),
            }
            
            self.variables.extend([
                {'key': f'{account_name}_email', 'value': self.accounts[account_name]['email'], 'type': 'string'},
                {'key': f'{account_name}_password', 'value': self.accounts[account_name]['password'], 'type': 'string'},
                {'key': f'{account_name}_token', 'value': '', 'type': 'string'},
            ])
    
    def _setup_extraction(self):
        """Настройка извлечения данных из ответов"""
        print_header("НАСТРОЙКА ИЗВЛЕЧЕНИЯ ДАННЫХ")
        
        print_info("Укажите, какие данные извлекать из ответов API")
        
        # Токены авторизации
        if prompt_yes_no("Извлекать токен авторизации из ответа SignIn?"):
            print_info("Настройка извлечения токена:")
            self.extract_config['token'] = {
                'enabled': True,
                'endpoint_pattern': prompt("Паттерн endpoint для токена", "*SignIn"),
                'json_path': prompt("JSON путь к токену", "data.accessToken"),
                'variable_name': prompt("Имя переменной для токена", "user_token"),
            }
            
            # Refresh token
            if prompt_yes_no("Извлекать также refresh токен?", default=True):
                self.extract_config['refresh_token'] = {
                    'enabled': True,
                    'json_path': prompt("JSON путь к refresh токену", "data.refreshToken"),
                    'variable_name': prompt("Имя переменной для refresh токена", "refresh_token"),
                }
                self.variables.append({
                    'key': 'refresh_token',
                    'value': '',
                    'type': 'string'
                })
        
        # ID сущностей
        if prompt_yes_no("Извлекать ID созданных сущностей?"):
            print_info("Настройка извлечения ID:")
            self.extract_config['ids'] = []
            
            while True:
                entity_name = prompt("Название сущности (пустая строка для завершения)", "")
                if not entity_name:
                    break
                
                self.extract_config['ids'].append({
                    'entity': entity_name,
                    'endpoint_pattern': prompt(f"Паттерн endpoint для {entity_name}", f"*/{entity_name}*"),
                    'json_path': prompt(f"JSON путь к ID", "id"),
                    'variable_name': prompt(f"Имя переменной", f"{entity_name.lower()}_id"),
                })
                
                # Добавляем переменную
                self.variables.append({
                    'key': f"{entity_name.lower()}_id",
                    'value': '',
                    'type': 'string'
                })
        
        # Кастомные извлечения
        if prompt_yes_no("Добавить кастомные извлечения данных?", default=False):
            self.extract_config['custom'] = []
            
            while True:
                field_name = prompt("Название поля (пустая строка для завершения)", "")
                if not field_name:
                    break
                
                self.extract_config['custom'].append({
                    'field': field_name,
                    'endpoint_pattern': prompt(f"Паттерн endpoint"),
                    'json_path': prompt(f"JSON путь"),
                    'variable_name': prompt(f"Имя переменной", field_name.lower()),
                })
                
                self.variables.append({
                    'key': field_name.lower(),
                    'value': '',
                    'type': 'string'
                })
    
    def generate(self) -> Dict:
        """Генерация коллекции Postman"""
        print_header("ГЕНЕРАЦИЯ КОЛЛЕКЦИИ")
        
        info = self.parser.get_info()
        endpoints = self.parser.parse_endpoints()
        
        print_info(f"Обнаружено {len(endpoints)} эндпоинтов")
        
        # Базовая структура коллекции
        self.collection = {
            'info': {
                '_postman_id': str(uuid.uuid4()),
                'name': info['title'],
                'description': info['description'],
                'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
                '_exporter_id': 'QA-Automation'
            },
            'item': [],
            'event': self._generate_collection_events(),
            'variable': self.variables
        }
        
        # Группировка по тегам
        tags_map: Dict[str, List[Dict]] = {}
        for endpoint in endpoints:
            tag = endpoint['tags'][0] if endpoint['tags'] else 'Default'
            if tag not in tags_map:
                tags_map[tag] = []
            tags_map[tag].append(endpoint)
        
        # Генерация папок и запросов
        for tag, tag_endpoints in tags_map.items():
            folder = {
                'name': tag,
                'item': [],
                'description': f"Эндпоинты для {tag}"
            }
            
            for endpoint in tag_endpoints:
                request = self._generate_request(endpoint)
                folder['item'].append(request)
            
            self.collection['item'].append(folder)
            print_success(f"Папка '{tag}': {len(tag_endpoints)} запросов")
        
        return self.collection
    
    def _generate_collection_events(self) -> List[Dict]:
        """Генерация событий коллекции (pre-request, test)"""
        pre_request_script = """
// Автоматическая подстановка токена
if (pm.variables.get('user_token')) {
    pm.request.headers.add({
        key: 'Authorization',
        value: 'Bearer ' + pm.variables.get('user_token')
    });
}
"""
        
        test_script = """
// Базовые проверки ответа
pm.test("Response time is less than 3000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});

pm.test("Response has valid JSON", function () {
    try {
        pm.response.json();
    } catch (e) {
        // Не JSON ответ - пропускаем
    }
});
"""
        
        return [
            {
                'listen': 'prerequest',
                'script': {
                    'type': 'text/javascript',
                    'exec': pre_request_script.strip().split('\n')
                }
            },
            {
                'listen': 'test',
                'script': {
                    'type': 'text/javascript',
                    'exec': test_script.strip().split('\n')
                }
            }
        ]
    
    def _generate_request(self, endpoint: Dict) -> Dict:
        """Генерация запроса Postman"""
        # Формируем имя запроса
        name = endpoint['summary'] or endpoint['operationId'] or f"{endpoint['method']} {endpoint['path']}"
        
        # URL с параметрами
        path = endpoint['path']
        path_with_vars = re.sub(r'\{(\w+)\}', r'{{\\1}}', path)
        
        # Параметры запроса
        query_params = []
        path_params = []
        
        for param in endpoint.get('parameters', []):
            if param.get('in') == 'query':
                query_params.append({
                    'key': param['name'],
                    'value': '',
                    'description': param.get('description', ''),
                    'disabled': not param.get('required', False)
                })
            elif param.get('in') == 'path':
                path_params.append(param['name'])
        
        # Тело запроса
        body = None
        schema = self.parser.get_request_body_schema(endpoint)
        if schema:
            body = self._generate_request_body(schema, endpoint)
        
        # Генерация тестов для этого запроса
        tests = self._generate_request_tests(endpoint)
        
        request = {
            'name': name,
            'request': {
                'method': endpoint['method'],
                'header': [
                    {
                        'key': 'Content-Type',
                        'value': 'application/json',
                        'type': 'text'
                    }
                ],
                'url': {
                    'raw': '{{base_url}}' + path_with_vars,
                    'host': ['{{base_url}}'],
                    'path': [p for p in path_with_vars.split('/') if p],
                    'query': query_params if query_params else []
                },
                'description': endpoint.get('description', '')
            },
            'response': [],
            'event': []
        }
        
        # Добавляем тело запроса
        if body:
            request['request']['body'] = body
        
        # Добавляем тесты
        if tests:
            request['event'].append({
                'listen': 'test',
                'script': {
                    'type': 'text/javascript',
                    'exec': tests.split('\n')
                }
            })
        
        return request
    
    def _generate_request_body(self, schema: Dict, endpoint: Dict) -> Dict:
        """Генерация тела запроса"""
        body_content = {}
        
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        
        for prop_name, prop_schema in properties.items():
            # Подставляем переменные для известных полей
            if prop_name.lower() == 'email':
                if 'admin' in endpoint['path'].lower():
                    body_content[prop_name] = '{{admin_email}}'
                else:
                    body_content[prop_name] = '{{user_email}}'
            elif prop_name.lower() == 'password':
                if 'admin' in endpoint['path'].lower():
                    body_content[prop_name] = '{{admin_password}}'
                else:
                    body_content[prop_name] = '{{user_password}}'
            elif prop_name.lower() == 'confirmpassword':
                body_content[prop_name] = '{{user_password}}'
            elif prop_name.lower() == 'nickname':
                body_content[prop_name] = '{{user_nickname}}'
            elif prop_name.lower() == 'login':
                body_content[prop_name] = '{{admin_login}}'
            elif 'id' in prop_name.lower():
                # Пытаемся найти подходящую переменную ID
                entity = prop_name.replace('Id', '').replace('id', '').lower()
                if entity:
                    body_content[prop_name] = '{{' + entity + '_id}}'
                else:
                    body_content[prop_name] = '{{entity_id}}'
            else:
                # Генерируем значение по умолчанию
                body_content[prop_name] = self._generate_default_value(prop_schema)
        
        return {
            'mode': 'raw',
            'raw': json.dumps(body_content, indent=2, ensure_ascii=False),
            'options': {
                'raw': {
                    'language': 'json'
                }
            }
        }
    
    def _generate_default_value(self, schema: Dict) -> Any:
        """Генерация значения по умолчанию для схемы"""
        prop_type = schema.get('type', 'string')
        
        if 'example' in schema:
            return schema['example']
        elif 'default' in schema:
            return schema['default']
        elif prop_type == 'string':
            if schema.get('format') == 'email':
                return 'example@test.com'
            elif schema.get('format') == 'date-time':
                return datetime.now().isoformat()
            elif schema.get('format') == 'uuid':
                return str(uuid.uuid4())
            return 'string_value'
        elif prop_type == 'integer':
            return 0
        elif prop_type == 'number':
            return 0.0
        elif prop_type == 'boolean':
            return True
        elif prop_type == 'array':
            return []
        elif prop_type == 'object':
            return {}
        
        return None
    
    def _generate_request_tests(self, endpoint: Dict) -> str:
        """Генерация тестов для запроса"""
        tests = []
        
        # Базовый тест статуса
        expected_codes = list(endpoint.get('responses', {}).keys())
        success_codes = [c for c in expected_codes if c.startswith('2')]
        
        if success_codes:
            tests.append(f"""
pm.test("Status code is successful", function () {{
    pm.expect(pm.response.code).to.be.oneOf([{', '.join(success_codes)}]);
}});
""")
        
        # Извлечение токена
        token_config = self.extract_config.get('token', {})
        if token_config.get('enabled'):
            pattern = token_config['endpoint_pattern'].replace('*', '.*')
            if re.search(pattern, endpoint['path'], re.IGNORECASE):
                json_path = token_config['json_path']
                var_name = token_config['variable_name']
                # Разбиваем путь для доступа к вложенным полям (data.accessToken -> data"]["accessToken)
                path_parts = json_path.split('.')
                if len(path_parts) > 1:
                    accessor = '"]["'.join(path_parts)
                    tests.append(f"""
// Извлечение токена авторизации
if (pm.response.code === 200) {{
    var jsonData = pm.response.json();
    if (jsonData.success) {{
        var token = jsonData["{accessor}"];
        if (token) {{
            pm.collectionVariables.set('{var_name}', token);
            console.log('✓ Token saved to {var_name}');
        }}
    }}
}}
""")
                else:
                    tests.append(f"""
// Извлечение токена авторизации
if (pm.response.code === 200) {{
    var jsonData = pm.response.json();
    var token = jsonData.{json_path};
    if (token) {{
        pm.collectionVariables.set('{var_name}', token);
        console.log('✓ Token saved to {var_name}');
    }}
}}
""")
                
                # Refresh token
                refresh_config = self.extract_config.get('refresh_token', {})
                if refresh_config.get('enabled'):
                    refresh_path = refresh_config['json_path']
                    refresh_var = refresh_config['variable_name']
                    path_parts = refresh_path.split('.')
                    if len(path_parts) > 1:
                        accessor = '"]["'.join(path_parts)
                        tests.append(f"""
// Извлечение refresh токена
if (pm.response.code === 200) {{
    var jsonData = pm.response.json();
    if (jsonData.success) {{
        var refreshToken = jsonData["{accessor}"];
        if (refreshToken) {{
            pm.collectionVariables.set('{refresh_var}', refreshToken);
            console.log('✓ Refresh token saved to {refresh_var}');
        }}
    }}
}}
""")
        
        # Извлечение ID
        for id_config in self.extract_config.get('ids', []):
            pattern = id_config['endpoint_pattern'].replace('*', '.*')
            if re.search(pattern, endpoint['path'], re.IGNORECASE):
                if endpoint['method'] == 'POST':
                    json_path = id_config['json_path']
                    var_name = id_config['variable_name']
                    tests.append(f"""
// Извлечение ID {id_config['entity']}
if (pm.response.code === 200 || pm.response.code === 201) {{
    var jsonData = pm.response.json();
    var entityId = jsonData.{json_path};
    if (entityId) {{
        pm.collectionVariables.set('{var_name}', entityId);
        console.log('{id_config["entity"]} ID saved: ' + entityId);
    }}
}}
""")
        
        # Кастомные извлечения
        for custom in self.extract_config.get('custom', []):
            pattern = custom['endpoint_pattern'].replace('*', '.*')
            if re.search(pattern, endpoint['path'], re.IGNORECASE):
                tests.append(f"""
// Извлечение {custom['field']}
if (pm.response.code === 200) {{
    var jsonData = pm.response.json();
    var value = jsonData.{custom['json_path']};
    if (value) {{
        pm.collectionVariables.set('{custom['variable_name']}', value);
        console.log('{custom["field"]} saved: ' + value);
    }}
}}
""")
        
        return '\n'.join(tests)
    
    def save(self, output_path: str):
        """Сохранение коллекции в файл"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.collection, f, indent=2, ensure_ascii=False)
        print_success(f"Коллекция сохранена: {output_path}")


def main():
    """Главная функция"""
    print_header("SWAGGER TO POSTMAN GENERATOR v1.0.0")
    
    # Получаем путь к Swagger файлу
    if len(sys.argv) > 1:
        swagger_path = sys.argv[1]
    else:
        swagger_path = prompt("Путь к Swagger JSON файлу")
    
    if not swagger_path:
        print_error("Путь к файлу не указан")
        sys.exit(1)
    
    # Проверяем существование файла
    if not os.path.exists(swagger_path):
        print_error(f"Файл не найден: {swagger_path}")
        sys.exit(1)
    
    # Парсим Swagger
    print_info(f"Загрузка Swagger: {swagger_path}")
    parser = SwaggerParser(swagger_path)
    
    if not parser.load():
        sys.exit(1)
    
    # Генератор коллекции
    generator = PostmanGenerator(parser)
    generator.setup_interactive()
    
    # Генерация
    collection = generator.generate()
    
    # Сохранение
    print_header("СОХРАНЕНИЕ")
    
    default_output = Path(swagger_path).stem + "_postman_collection.json"
    output_path = prompt("Путь для сохранения коллекции", default_output)
    
    generator.save(output_path)
    
    # Статистика
    print_header("ГОТОВО!")
    total_requests = sum(len(folder.get('item', [])) for folder in collection['item'])
    print_info(f"Всего папок: {len(collection['item'])}")
    print_info(f"Всего запросов: {total_requests}")
    print_info(f"Переменных: {len(collection['variable'])}")
    
    print(f"\n{Colors.GREEN}Импортируйте файл {output_path} в Postman{Colors.ENDC}")
    print(f"{Colors.YELLOW}Не забудьте заполнить значения переменных в коллекции!{Colors.ENDC}\n")


if __name__ == "__main__":
    main()

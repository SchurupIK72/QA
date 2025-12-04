#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger to API Checklist Generator v1.0.0
Генератор API чек-листа из Swagger/OpenAPI спецификации

Автор: QA Automation Team
Дата: 04.12.2025

Функционал:
- Парсинг Swagger/OpenAPI 3.0 спецификаций
- Автоматическая генерация тест-кейсов для каждого эндпоинта
- Генерация позитивных и негативных сценариев
- Поддержка различных типов проверок (валидация, авторизация, безопасность)
- Вывод в CSV формате

Использование:
    python swagger_to_api_checklist.py <swagger.json> <output.csv> [--project "Название проекта"]
"""

import json
import csv
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class TestCase:
    """Представление одного тест-кейса"""
    section: str
    endpoint: str
    method: str
    test_type: str
    input_data: str
    expected_code: str
    expected_result: str
    actual_result: str = ""
    proofs: str = ""
    comment: str = ""
    qa: str = ""


@dataclass
class EndpointInfo:
    """Информация об эндпоинте"""
    path: str
    method: str
    summary: str
    description: str
    tags: List[str]
    parameters: List[Dict]
    request_body: Optional[Dict]
    responses: Dict[str, Dict]
    security: List[Dict]
    operation_id: str


class SwaggerParser:
    """Парсер Swagger/OpenAPI спецификации"""
    
    def __init__(self, swagger_path: str):
        self.swagger_path = swagger_path
        self.spec: Dict = {}
        self.endpoints: List[EndpointInfo] = []
        
    def load(self) -> bool:
        """Загрузка Swagger файла"""
        try:
            with open(self.swagger_path, 'r', encoding='utf-8') as f:
                self.spec = json.load(f)
            return True
        except FileNotFoundError:
            print(f"❌ Файл не найден: {self.swagger_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
            return False
    
    def get_info(self) -> Dict:
        """Получение информации об API"""
        info = self.spec.get('info', {})
        return {
            'title': info.get('title', 'Unknown API'),
            'version': info.get('version', '1.0.0'),
            'description': info.get('description', ''),
        }
    
    def get_tags(self) -> List[str]:
        """Получение списка тегов/контроллеров"""
        tags = self.spec.get('tags', [])
        return [t.get('name', '') for t in tags]
    
    def resolve_ref(self, ref: str) -> Dict:
        """Разрешение $ref ссылки"""
        if not ref or not ref.startswith('#/'):
            return {}
        
        parts = ref[2:].split('/')
        result = self.spec
        for part in parts:
            result = result.get(part, {})
        return result
    
    def get_schema_properties(self, schema: Dict) -> Dict[str, Dict]:
        """Получение свойств схемы (разрешает $ref)"""
        if '$ref' in schema:
            schema = self.resolve_ref(schema['$ref'])
        return schema.get('properties', {})
    
    def get_required_fields(self, schema: Dict) -> List[str]:
        """Получение обязательных полей схемы"""
        if '$ref' in schema:
            schema = self.resolve_ref(schema['$ref'])
        return schema.get('required', [])
    
    def parse_endpoints(self) -> List[EndpointInfo]:
        """Парсинг всех эндпоинтов"""
        endpoints = []
        paths = self.spec.get('paths', {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                    continue
                
                # Получаем requestBody схему
                request_body = None
                rb = details.get('requestBody', {})
                if rb:
                    content = rb.get('content', {})
                    for content_type, schema_info in content.items():
                        schema = schema_info.get('schema', {})
                        if '$ref' in schema:
                            schema = self.resolve_ref(schema['$ref'])
                        request_body = schema
                        break
                
                endpoint = EndpointInfo(
                    path=path,
                    method=method.upper(),
                    summary=details.get('summary', ''),
                    description=details.get('description', ''),
                    tags=details.get('tags', ['Default']),
                    parameters=details.get('parameters', []),
                    request_body=request_body,
                    responses=details.get('responses', {}),
                    security=details.get('security', []),
                    operation_id=details.get('operationId', '')
                )
                endpoints.append(endpoint)
        
        self.endpoints = endpoints
        return endpoints


class TestCaseGenerator:
    """Генератор тест-кейсов на основе эндпоинтов"""
    
    # Стандартные типы тестов
    TEST_TYPES = {
        'positive': 'Positive',
        'validation': 'Validation',
        'unauthorized': 'Unauthorized',
        'forbidden': 'Forbidden',
        'not_found': 'Not Found',
        'duplicate': 'Duplicate',
        'rate_limit': 'Rate-Limit',
        'missing_field': 'Validation - missing field',
        'invalid_format': 'Validation - invalid format',
        'content_type': 'Content-Type Missing',
        'state': 'State',
    }
    
    # Поля для валидации
    VALIDATION_FIELDS = {
        'email': {
            'invalid_value': '"invalid"',
            'error': 'Ошибка валидации email',
            'code': '400'
        },
        'password': {
            'invalid_value': '"123"',
            'error': 'Ошибка валидации пароля',
            'code': '400'
        },
        'confirmPassword': {
            'invalid_value': '"different_password"',
            'error': 'Пароли должны совпадать',
            'code': '400'
        },
        'nickname': {
            'invalid_value': '""',
            'error': 'Никнейм не может быть пустым',
            'code': '400'
        },
    }
    
    def __init__(self, parser: SwaggerParser):
        self.parser = parser
        self.test_cases: List[TestCase] = []
        
    def generate_all(self) -> List[TestCase]:
        """Генерация всех тест-кейсов"""
        self.test_cases = []
        
        for endpoint in self.parser.endpoints:
            cases = self.generate_for_endpoint(endpoint)
            self.test_cases.extend(cases)
        
        return self.test_cases
    
    def generate_for_endpoint(self, endpoint: EndpointInfo) -> List[TestCase]:
        """Генерация тест-кейсов для одного эндпоинта"""
        cases = []
        section = endpoint.tags[0] if endpoint.tags else 'Default'
        
        # 1. Позитивный тест
        cases.append(self._generate_positive(endpoint, section))
        
        # 2. Тесты валидации (если есть requestBody)
        if endpoint.request_body:
            cases.extend(self._generate_validation_tests(endpoint, section))
        
        # 3. Тесты авторизации (если endpoint требует токен)
        if self._requires_auth(endpoint):
            cases.extend(self._generate_auth_tests(endpoint, section))
        
        # 4. Not Found тест (если есть path параметр с id)
        if self._has_id_param(endpoint):
            cases.append(self._generate_not_found(endpoint, section))
        
        # 5. Дополнительные тесты в зависимости от ответов
        cases.extend(self._generate_response_based_tests(endpoint, section))
        
        return cases
    
    def _generate_positive(self, endpoint: EndpointInfo, section: str) -> TestCase:
        """Генерация позитивного теста"""
        input_data = self._generate_input_data(endpoint, positive=True)
        expected_code = self._get_success_code(endpoint)
        expected_result = self._get_success_description(endpoint)
        
        return TestCase(
            section=section,
            endpoint=endpoint.path,
            method=endpoint.method,
            test_type=self.TEST_TYPES['positive'],
            input_data=input_data,
            expected_code=expected_code,
            expected_result=expected_result
        )
    
    def _generate_validation_tests(self, endpoint: EndpointInfo, section: str) -> List[TestCase]:
        """Генерация тестов валидации"""
        cases = []
        
        if not endpoint.request_body:
            return cases
        
        properties = endpoint.request_body.get('properties', {})
        required = endpoint.request_body.get('required', [])
        
        # Тест для каждого валидируемого поля
        for field_name, field_schema in properties.items():
            if field_name.lower() in [f.lower() for f in self.VALIDATION_FIELDS.keys()]:
                validation = self._get_validation_for_field(field_name)
                if validation:
                    body = self._generate_body_with_invalid_field(
                        properties, field_name, validation['invalid_value']
                    )
                    cases.append(TestCase(
                        section=section,
                        endpoint=endpoint.path,
                        method=endpoint.method,
                        test_type=f"Validation - {field_name}",
                        input_data=body,
                        expected_code=validation['code'],
                        expected_result=validation['error']
                    ))
        
        # Тест на отсутствие обязательного поля
        for req_field in required:
            if req_field in properties:
                body = self._generate_body_without_field(properties, req_field)
                cases.append(TestCase(
                    section=section,
                    endpoint=endpoint.path,
                    method=endpoint.method,
                    test_type=f"Validation - missing {req_field}",
                    input_data=body,
                    expected_code="400",
                    expected_result=f"Отсутствует обязательное поле {req_field}"
                ))
                break  # Один тест достаточно
        
        return cases
    
    def _generate_auth_tests(self, endpoint: EndpointInfo, section: str) -> List[TestCase]:
        """Генерация тестов авторизации"""
        cases = []
        
        # Unauthorized - без токена
        cases.append(TestCase(
            section=section,
            endpoint=endpoint.path,
            method=endpoint.method,
            test_type=self.TEST_TYPES['unauthorized'],
            input_data="без токена",
            expected_code="401",
            expected_result="Требуется авторизация"
        ))
        
        # Forbidden - неверный токен (для admin эндпоинтов)
        if '/admin/' in endpoint.path.lower():
            cases.append(TestCase(
                section=section,
                endpoint=endpoint.path,
                method=endpoint.method,
                test_type=self.TEST_TYPES['forbidden'],
                input_data="Authorization: Bearer $USER_TOKEN",
                expected_code="403",
                expected_result="Доступ запрещен"
            ))
        
        return cases
    
    def _generate_not_found(self, endpoint: EndpointInfo, section: str) -> TestCase:
        """Генерация теста Not Found"""
        input_data = self._generate_input_data(endpoint, positive=True)
        input_data = input_data.replace('valid_uuid', 'non_existent_uuid')
        
        return TestCase(
            section=section,
            endpoint=endpoint.path,
            method=endpoint.method,
            test_type=self.TEST_TYPES['not_found'],
            input_data=f"id=non_existent_uuid + токен",
            expected_code="404",
            expected_result=self._get_not_found_message(endpoint)
        )
    
    def _generate_response_based_tests(self, endpoint: EndpointInfo, section: str) -> List[TestCase]:
        """Генерация тестов на основе описанных ответов"""
        cases = []
        responses = endpoint.responses
        
        # Проверяем специфические коды ответов
        for code, response_info in responses.items():
            code_int = int(code) if code.isdigit() else 0
            description = response_info.get('description', '')
            
            # 409 - Conflict (duplicate, already exists)
            if code == '409' and 'duplicate' not in description.lower():
                if 'exists' in description.lower() or 'уже' in description.lower():
                    cases.append(TestCase(
                        section=section,
                        endpoint=endpoint.path,
                        method=endpoint.method,
                        test_type=self.TEST_TYPES['duplicate'],
                        input_data=self._generate_input_data(endpoint, positive=True),
                        expected_code="409",
                        expected_result=description or "Уже существует"
                    ))
            
            # 429 - Rate limit
            if code == '429':
                cases.append(TestCase(
                    section=section,
                    endpoint=endpoint.path,
                    method=endpoint.method,
                    test_type=self.TEST_TYPES['rate_limit'],
                    input_data="10 запросов подряд",
                    expected_code="429",
                    expected_result="Превышен лимит запросов"
                ))
        
        return cases
    
    def _generate_input_data(self, endpoint: EndpointInfo, positive: bool = True) -> str:
        """Генерация входных данных для теста"""
        parts = []
        
        # Параметры пути
        path_params = [p for p in endpoint.parameters if p.get('in') == 'path']
        for param in path_params:
            param_name = param.get('name', 'id')
            parts.append(f"{param_name}=valid_uuid")
        
        # Тело запроса
        if endpoint.request_body:
            body = self._generate_sample_body(endpoint.request_body.get('properties', {}))
            parts.append(body)
        
        # Токен (если требуется)
        if self._requires_auth(endpoint):
            if '/admin/' in endpoint.path.lower():
                parts.append("+ админ токен")
            else:
                parts.append("+ токен")
        
        return " ".join(parts) if parts else "без параметров"
    
    def _generate_sample_body(self, properties: Dict) -> str:
        """Генерация примера тела запроса"""
        body = {}
        
        for name, schema in properties.items():
            prop_type = schema.get('type', 'string')
            
            # Подставляем переменные для известных полей
            name_lower = name.lower()
            if 'email' in name_lower:
                if 'admin' in name_lower:
                    body[name] = "admin@example.com"
                else:
                    body[name] = "test@example.com"
            elif 'password' in name_lower:
                body[name] = "Test123!"
            elif 'confirm' in name_lower and 'password' in name_lower:
                body[name] = "Test123!"
            elif 'nickname' in name_lower:
                body[name] = "TestUser"
            elif 'login' in name_lower:
                body[name] = "superadmin"
            elif 'id' in name_lower:
                body[name] = "valid_uuid"
            elif 'code' in name_lower:
                body[name] = "getcode"
            elif prop_type == 'string':
                body[name] = "string_value"
            elif prop_type == 'integer':
                body[name] = 0
            elif prop_type == 'number':
                body[name] = 0.0
            elif prop_type == 'boolean':
                body[name] = True
            elif prop_type == 'array':
                body[name] = []
        
        return json.dumps(body, ensure_ascii=False)
    
    def _generate_body_with_invalid_field(
        self, properties: Dict, invalid_field: str, invalid_value: str
    ) -> str:
        """Генерация тела с невалидным полем"""
        body = {}
        
        for name, schema in properties.items():
            if name.lower() == invalid_field.lower():
                body[name] = invalid_value
            else:
                body[name] = self._get_default_value(name, schema)
        
        # Форматируем как JSON строку без лишних кавычек для invalid_value
        result = json.dumps(body, ensure_ascii=False)
        # Заменяем строковое представление на чистое значение
        result = result.replace(f'"{invalid_value}"', invalid_value)
        return result
    
    def _generate_body_without_field(self, properties: Dict, exclude_field: str) -> str:
        """Генерация тела без одного поля"""
        body = {}
        
        for name, schema in properties.items():
            if name != exclude_field:
                body[name] = self._get_default_value(name, schema)
        
        return json.dumps(body, ensure_ascii=False)
    
    def _get_default_value(self, name: str, schema: Dict) -> Any:
        """Получение значения по умолчанию для поля"""
        name_lower = name.lower()
        prop_type = schema.get('type', 'string')
        
        if 'email' in name_lower:
            return "test@example.com"
        elif 'password' in name_lower:
            return "Test123!"
        elif 'nickname' in name_lower:
            return "TestUser"
        elif prop_type == 'string':
            return "value"
        elif prop_type == 'integer':
            return 0
        elif prop_type == 'boolean':
            return True
        
        return "value"
    
    def _get_validation_for_field(self, field_name: str) -> Optional[Dict]:
        """Получение параметров валидации для поля"""
        for key, validation in self.VALIDATION_FIELDS.items():
            if key.lower() == field_name.lower():
                return validation
        return None
    
    def _requires_auth(self, endpoint: EndpointInfo) -> bool:
        """Проверка, требует ли эндпоинт авторизации"""
        # Проверяем по security
        if endpoint.security:
            return True
        
        # Проверяем по пути (эвристика)
        no_auth_paths = ['/auth/signup', '/auth/signin', '/auth/restore', '/auth/reset', 
                         '/auth/sendverification', '/auth/verifyemail', '/buildinginfo']
        for no_auth in no_auth_paths:
            if no_auth in endpoint.path.lower():
                return False
        
        # Большинство API эндпоинтов требуют авторизации
        return '/api/' in endpoint.path or '/admin/' in endpoint.path
    
    def _has_id_param(self, endpoint: EndpointInfo) -> bool:
        """Проверка наличия ID параметра в пути"""
        return '{id}' in endpoint.path or any(
            p.get('in') == 'path' and 'id' in p.get('name', '').lower()
            for p in endpoint.parameters
        )
    
    def _get_success_code(self, endpoint: EndpointInfo) -> str:
        """Получение успешного кода ответа"""
        for code in ['200', '201', '204']:
            if code in endpoint.responses:
                return code
        return '200'
    
    def _get_success_description(self, endpoint: EndpointInfo) -> str:
        """Получение описания успешного ответа"""
        for code in ['200', '201', '204']:
            if code in endpoint.responses:
                response = endpoint.responses[code]
                desc = response.get('description', '')
                if desc:
                    return desc
        
        # Генерируем описание на основе метода
        method = endpoint.method
        summary = endpoint.summary
        
        if method == 'GET':
            return summary or "Данные получены"
        elif method == 'POST':
            return summary or "Создано успешно"
        elif method == 'PUT' or method == 'PATCH':
            return summary or "Обновлено успешно"
        elif method == 'DELETE':
            return summary or "Удалено успешно"
        
        return summary or "Успешно"
    
    def _get_not_found_message(self, endpoint: EndpointInfo) -> str:
        """Получение сообщения для Not Found"""
        # Пытаемся определить сущность по пути
        path = endpoint.path.lower()
        
        if '/user' in path:
            return "Пользователь не найден"
        elif '/character' in path:
            return "Персонаж не найден"
        elif '/building' in path:
            return "Здание не найдено"
        elif '/match' in path:
            return "Матч не найден"
        elif '/event' in path:
            return "Событие не найдено"
        elif '/tournament' in path:
            return "Турнир не найден"
        elif '/admin' in path:
            return "Администратор не найден"
        elif '/role' in path:
            return "Роль не найдена"
        
        return "Не найдено"


class ChecklistWriter:
    """Запись чек-листа в CSV"""
    
    # Заголовки CSV файла
    HEADERS = [
        '№',
        'Section',
        'Endpoint',
        'Method',
        'Type',
        'Input (Body / Params / Token)',
        'Expected Code',
        'Expected Result',
        'Actual Result',
        'Proofs',
        'Comment',
        'QA'
    ]
    
    def __init__(self, test_cases: List[TestCase], project_name: str = ""):
        self.test_cases = test_cases
        self.project_name = project_name
    
    def write_csv(self, output_path: str):
        """Запись в CSV файл"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Заголовок с названием проекта
            if self.project_name:
                writer.writerow([f"API Чек-лист: {self.project_name}"])
            else:
                writer.writerow(["API Чек-лист"])
            
            # Заголовки колонок
            writer.writerow(self.HEADERS)
            
            # Данные
            for idx, tc in enumerate(self.test_cases, 1):
                row = [
                    idx,
                    tc.section,
                    tc.endpoint,
                    tc.method,
                    tc.test_type,
                    tc.input_data,
                    tc.expected_code,
                    tc.expected_result,
                    tc.actual_result,
                    tc.proofs,
                    tc.comment,
                    tc.qa
                ]
                writer.writerow(row)
            
            # Легенда
            writer.writerow([])
            writer.writerow(["Легенда:"])
            writer.writerow(["Actual Result", "- Фактический код ответа и результат"])
            writer.writerow(["Proofs", "- Доказательства (скриншоты, логи)"])
            writer.writerow(["X", "- Баг (результат не соответствует ожидаемому)"])
            writer.writerow([])
            writer.writerow(["Типы тестов:"])
            writer.writerow(["Positive", "- Успешный сценарий с валидными данными"])
            writer.writerow(["Validation", "- Проверка валидации входных данных"])
            writer.writerow(["Unauthorized", "- Запрос без токена авторизации"])
            writer.writerow(["Forbidden", "- Запрос с недостаточными правами"])
            writer.writerow(["Not Found", "- Запрос с несуществующим ID"])
            writer.writerow(["Duplicate", "- Попытка создать дубликат"])
            writer.writerow(["Rate-Limit", "- Превышение лимита запросов"])
            writer.writerow(["State", "- Проверка состояния (уже выполнено, не завершено и т.д.)"])
        
        print(f"✅ Чек-лист сохранен: {output_path}")


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='Генератор API чек-листа из Swagger/OpenAPI спецификации',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s swagger.json api_checklist.csv
  %(prog)s swagger.json api_checklist.csv --project "Школа гладиаторов"
        """
    )
    
    parser.add_argument(
        'swagger_file',
        help='Путь к Swagger/OpenAPI JSON файлу'
    )
    
    parser.add_argument(
        'output_file',
        help='Путь для сохранения CSV чек-листа'
    )
    
    parser.add_argument(
        '--project', '-p',
        dest='project_name',
        default='',
        help='Название проекта для заголовка'
    )
    
    args = parser.parse_args()
    
    # Парсим Swagger
    print(f"📖 Загрузка Swagger: {args.swagger_file}")
    swagger_parser = SwaggerParser(args.swagger_file)
    
    if not swagger_parser.load():
        sys.exit(1)
    
    # Информация об API
    info = swagger_parser.get_info()
    print(f"📋 API: {info['title']} v{info['version']}")
    
    # Парсим эндпоинты
    endpoints = swagger_parser.parse_endpoints()
    print(f"🔍 Найдено эндпоинтов: {len(endpoints)}")
    
    # Генерируем тест-кейсы
    generator = TestCaseGenerator(swagger_parser)
    test_cases = generator.generate_all()
    print(f"✨ Сгенерировано тест-кейсов: {len(test_cases)}")
    
    # Статистика по секциям
    sections = {}
    for tc in test_cases:
        sections[tc.section] = sections.get(tc.section, 0) + 1
    
    print("\n📊 Статистика по секциям:")
    for section, count in sorted(sections.items()):
        print(f"   {section}: {count} тестов")
    
    # Записываем CSV
    project_name = args.project_name or info['title']
    writer = ChecklistWriter(test_cases, project_name)
    writer.write_csv(args.output_file)
    
    print(f"\n🎉 Готово! Всего тест-кейсов: {len(test_cases)}")


if __name__ == "__main__":
    main()

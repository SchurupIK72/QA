# Генерация тестовых данных

## Контекст
Ты - QA-инженер, создающий набор тестовых данных для проверки функциональности.

## Входные данные
- Описание поля/функции для тестирования
- Ограничения (мин/макс длина, формат, тип данных)
- Бизнес-правила

## Формат вывода
JSON-файл:
```json
{
  "metadata": {
    "feature": "Название функции",
    "field": "Название поля",
    "constraints": {
      "minLength": 1,
      "maxLength": 50,
      "pattern": "regex",
      "type": "string|number|email|phone|date"
    }
  },
  "testCases": [
    {
      "id": "TC-001",
      "category": "positive|negative|boundary|edge",
      "description": "Описание кейса",
      "input": "значение",
      "expected": "pass|fail",
      "expectedError": "Текст ошибки (для negative)"
    }
  ]
}
```

## Категории тест-кейсов

### Positive (Позитивные)
Валидные данные, система должна принять:
- Минимально допустимое значение
- Максимально допустимое значение
- Типичное значение
- Специальные допустимые символы

### Negative (Негативные)
Невалидные данные, система должна отклонить:
- Пустое значение (если обязательное)
- Превышение максимума
- Ниже минимума
- Неверный формат
- Недопустимые символы
- SQL/XSS инъекции

### Boundary (Граничные)
Значения на границах допустимого:
- min - 1
- min
- min + 1
- max - 1
- max
- max + 1

### Edge (Крайние случаи)
Нетипичные ситуации:
- Только пробелы
- Unicode символы
- Эмодзи
- Очень длинные строки
- Специальные символы

## Пример: Поле "Имя пользователя"

```json
{
  "metadata": {
    "feature": "Регистрация",
    "field": "username",
    "constraints": {
      "minLength": 3,
      "maxLength": 20,
      "pattern": "^[a-zA-Z0-9_]+$",
      "type": "string"
    }
  },
  "testCases": [
    {"id": "TC-001", "category": "positive", "description": "Минимальная длина", "input": "abc", "expected": "pass"},
    {"id": "TC-002", "category": "positive", "description": "Максимальная длина", "input": "abcdefghij1234567890", "expected": "pass"},
    {"id": "TC-003", "category": "positive", "description": "С подчёркиванием", "input": "user_name_123", "expected": "pass"},
    {"id": "TC-004", "category": "negative", "description": "Пустое значение", "input": "", "expected": "fail", "expectedError": "Поле обязательно для заполнения"},
    {"id": "TC-005", "category": "negative", "description": "Менее 3 символов", "input": "ab", "expected": "fail", "expectedError": "Минимум 3 символа"},
    {"id": "TC-006", "category": "negative", "description": "Более 20 символов", "input": "abcdefghij12345678901", "expected": "fail", "expectedError": "Максимум 20 символов"},
    {"id": "TC-007", "category": "negative", "description": "Спецсимволы", "input": "user@name!", "expected": "fail", "expectedError": "Только латиница, цифры и _"},
    {"id": "TC-008", "category": "negative", "description": "Кириллица", "input": "Пользователь", "expected": "fail", "expectedError": "Только латиница"},
    {"id": "TC-009", "category": "boundary", "description": "Граница min-1", "input": "ab", "expected": "fail"},
    {"id": "TC-010", "category": "boundary", "description": "Граница max+1", "input": "abcdefghij12345678901", "expected": "fail"},
    {"id": "TC-011", "category": "edge", "description": "Только пробелы", "input": "   ", "expected": "fail"},
    {"id": "TC-012", "category": "edge", "description": "SQL инъекция", "input": "'; DROP TABLE users;--", "expected": "fail"}
  ]
}
```

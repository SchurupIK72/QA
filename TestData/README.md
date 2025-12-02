# TestData - Тестовые данные

Эта папка содержит сгенерированные тестовые данные.

## Автоматическое создание

Папка создается автоматически при первом экспорте данных из генератора:
```powershell
python scripts/test_data_generator.py
```

## Типы файлов

- `*.json` - JSON формат данных
- `*.csv` - CSV формат для Excel/Google Sheets

## Примеры генерируемых файлов

- `users.json` / `users.csv` - Данные пользователей
- `characters.json` / `characters.csv` - Игровые персонажи
- `emails.json` / `emails.csv` - Email адреса
- `passwords.json` / `passwords.csv` - Пароли
- `phones.json` / `phones.csv` - Номера телефонов
- `prices.json` / `prices.csv` - Цены
- `dates.json` / `dates.csv` - Даты
- `custom_data.json` / `custom_data.csv` - Произвольные данные

## Очистка

Для очистки тестовых данных:
```powershell
Remove-Item TestData/*.json
Remove-Item TestData/*.csv
```

## Примечание

Эта папка добавлена в `.gitignore` и не синхронизируется с GitHub.

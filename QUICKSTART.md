# Быстрый старт - QA Automation

## 📋 Содержание
- [Создание нового проекта](#-создание-нового-проекта-за-3-шага)
- [Генератор тестовых данных](#-генератор-тестовых-данных)
- [Вычитка ТЗ](#-вычитка-технического-задания)
- [Тестирование Backend API](#-тестирование-backend-api)
- [Быстрые шаблоны](#-быстрые-шаблоны)
- [Полезные ссылки](#-полезные-ссылки)

## 🚀 Создание нового проекта за 3 шага

### Шаг 1: Создайте структуру папок
```powershell
# Замените MyProject на название вашего проекта
$projectName = "MyProject"

mkdir "projects/$projectName"
mkdir "projects/$projectName/bug-reports"
mkdir "projects/$projectName/checklists"
mkdir "projects/$projectName/test-data"
mkdir "projects/$projectName/docs"
```

### Шаг 2: Скопируйте шаблоны
```powershell
# Получите текущую дату
$date = Get-Date -Format "yyyy-MM-dd"

# Скопируйте шаблоны
Copy-Item "templates/bug-report-template.csv" "projects/$projectName/bug-reports/bug-report-$date.csv"
Copy-Item "templates/checklist-regression-template.csv" "projects/$projectName/checklists/checklist-regression-$date.csv"
```

### Шаг 3: Начните работу
1. Откройте `bug-report-[дата].csv` в Excel/Google Sheets
2. Заполняйте баг-репорты по мере обнаружения
3. Используйте чек-лист для регрессионного тестирования

## 🎲 Генератор тестовых данных

### Запуск интерактивной консоли
```powershell
python scripts/test_data_generator.py
```

### Быстрая генерация данных

**Генерация пользователей:**
1. Запустите консоль
2. Выберите "1 - Генерация пользователей"
3. Укажите количество (например, 10)
4. Данные будут показаны и предложен экспорт

**Генерация паролей:**
1. Выберите "4 - Генерация паролей"
2. Укажите количество и длину
3. Настройте параметры (заглавные, цифры, спецсимволы)
4. Экспортируйте в CSV/JSON

**Произвольные данные:**
1. Выберите "8 - Генерация произвольных данных"
2. Укажите нужные поля (1,2,3 = name,email,phone)
3. Укажите количество записей
4. Экспортируйте результат

### Использование в коде
```python
from scripts.test_data_generator import TestDataGenerator

# Создание генератора
generator = TestDataGenerator(locale="ru")

# Генерация
users = generator.generate_users(10)
email = generator.generate_email()
password = generator.generate_strong_password()

# Экспорт
generator.export_to_json(users, "users.json")
generator.export_to_csv(users, "users.csv")
```

## 📋 Вычитка технического задания

### Как провести вычитку ТЗ:

1. **Скопируйте шаблон:**
```powershell
$date = Get-Date -Format "yyyy-MM-dd"
Copy-Item "templates/checklist-tz-review-template.csv" "projects/$projectName/docs/tz-review-$date.csv"
```

2. **Откройте в Excel/Google Sheets**

3. **Заполните шапку:**
   - Проект: [Название проекта]
   - Версия ТЗ: [Версия]
   - Дата вычитки: [Дата]
   - Вычитку выполнил: [Ваше имя]

4. **Проверьте по категориям:**
   - Отметьте `PASSED` если критерий выполнен
   - Отметьте `FAILED` если есть проблемы (добавьте комментарий)
   - Отметьте `SKIPED` если не применимо к проекту
   - Укажите критичность замечаний (High/Medium/Low)

5. **Составьте итоговое заключение:**
   - Качество ТЗ: Отлично/Хорошо/Удовлетворительно/Требует доработки
   - Готовность к разработке: Готово/Требует уточнений/Не готово

## 🔧 Тестирование Backend API

### Для проектов с API:

1. **Сохраните Swagger в confidential:**
```powershell
mkdir confidential/projects/$projectName/swagger
# Поместите swagger.json в эту папку
```

2. **Создайте чек-лист API тестирования:**
   - Используйте шаблон из папки templates
   - Адаптируйте под endpoint'ы вашего API

3. **Категории для проверки:**
   - Authentication & Authorization
   - CRUD операции
   - Валидация данных
   - Обработка ошибок
   - Производительность
   - Безопасность

## � Конвертация и анонимизация DOCX

### Конвертировать ТЗ из DOCX в Markdown

**С анонимизацией конфиденциальных данных:**
```powershell
python scripts/docx_to_md.py "ТЗ проекта.docx" "output.md" --anonymize
```

**Или сокращенно:**
```powershell
python scripts/docx_to_md.py "ТЗ проекта.docx" "output.md" -a
```

**Что анонимизируется:**
- ✂️ Названия компаний (ООО, LLC, Inc)
- ✂️ ФИО людей (Иван Иванов → Пользователь А)
- ✂️ Email адреса, телефоны, Telegram ники
- ✂️ Годы в датах (2022 → 202_)
- ✂️ Информация о заказчике

**Результат:** Документ готов для публичного использования

Подробнее: [docs/ANONYMIZATION-GUIDE.md](docs/ANONYMIZATION-GUIDE.md)

## �📝 Быстрые шаблоны

### Создание баг-репорта (минимум)
```csv
ID: BUG-[Раздел]-[Номер]
Section: Backend/Frontend/UI/UX
Title: [Раздел].[Подраздел].[Описание проблемы]
Steps: 
1. Шаг 1
2. Шаг 2
3. Шаг 3
Actual Result: Что произошло
Expected Result: Что должно было произойти
Environment: Браузер/ОС
Proofs: Ссылка на скриншот/видео
```

### Обновление статуса в чек-листе
1. Откройте чек-лист проекта
2. Найдите нужную проверку
3. Замените `NOT STARTED` на:
   - `PASSED` - если работает
   - `FAILED` - если найден баг (добавьте ID бага)
   - `SKIPED` - если нельзя проверить

## 🔗 Полезные ссылки

### 📚 Документация
- [README - Общий обзор](README.md)
- [Руководство по баг-репортам](docs/BUG-REPORT-GUIDE.md)
- [Руководство по чек-листам](docs/CHECKLIST-GUIDE.md)
- [Структура проекта](docs/STRUCTURE.md)

### 📋 Шаблоны
- [Шаблон баг-репорта](templates/bug-report-template.csv)
- [Шаблон чек-листа регресса](templates/checklist-regression-template.csv)
- [Шаблон вычитки ТЗ](templates/checklist-tz-review-template.csv)

### 🔧 Инструменты
- [Генератор тестовых данных](scripts/test_data_generator.py)

## 💡 Частые вопросы

**Q: Как назвать файл баг-репорта?**
A: `bug-report-YYYY-MM-DD.csv` или `bug-report-v[версия].csv`

**Q: Обязательно ли заполнять все поля?**
A: Нет, только поля с * обязательны. Остальные - по необходимости.

**Q: Как часто проводить регресс?**
A: После каждого нового билда и перед релизом.

**Q: Где хранить скриншоты?**
A: В `projects/[имя-проекта]/bug-reports/screenshots/` или на облачном хранилище с публичной ссылкой.

**Q: Где хранить конфиденциальные данные?**
A: В папке `confidential/` - она не синхронизируется с GitHub.

**Q: Как сгенерировать тестовые данные?**
A: Запустите `python scripts/test_data_generator.py` и следуйте меню.

**Q: Как провести вычитку ТЗ?**
A: Используйте шаблон `templates/checklist-tz-review-template.csv` - 225 проверок по 30 категориям.

**Q: Как создать чек-лист для Backend API?**
A: Используйте шаблон `templates/checklist-regression-template.csv` и адаптируйте под ваши API endpoints

## 🚀 Быстрые команды

```powershell
# Создать новый проект
$projectName = "MyProject"
mkdir projects/$projectName/{bug-reports,checklists,test-data,docs}

# Скопировать все шаблоны
$date = Get-Date -Format "yyyy-MM-dd"
Copy-Item templates/*.csv projects/$projectName/checklists/

# Запустить генератор тестовых данных
python scripts/test_data_generator.py

# Переместить конфиденциальные файлы
Move-Item "swagger.json" "confidential/projects/$projectName/"
```

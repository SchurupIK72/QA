# QA Automation - Команды запуска скриптов

## 🎲 Генератор тестовых данных

```powershell
# Интерактивный режим (рекомендуется)
python scripts/test_data_generator.py
```

**Возможности:**
- Генерация пользователей, персонажей, email, паролей, телефонов, цен, дат
- Экспорт в JSON/CSV
- Файлы сохраняются в папку `TestData/`

---

## 📄 Конвертер DOCX → Markdown (Pandoc)

### Установка Pandoc (один раз, от имени Администратора):
```powershell
choco install pandoc
```

### Запуск:
```powershell
# Интерактивный режим (рекомендуется)
python scripts/docx_to_md.py

# Конвертация конкретного файла
python scripts/docx_to_md.py "путь/к/файлу.docx"

# С указанием выходного файла
python scripts/docx_to_md.py "input.docx" "output.md"
```

**Возможности:**
- Интерактивный режим с выбором файла из списка
- Пакетная конвертация всех DOCX в папке
- Извлечение изображений в папку `media/`
- Статистика: строки, слова, символы

---

## 📁 Быстрое создание проекта

```powershell
# Создать структуру нового проекта
$projectName = "НазваниеПроекта"
mkdir "projects/$projectName"
mkdir "projects/$projectName/bug-reports"
mkdir "projects/$projectName/checklists"
mkdir "projects/$projectName/test-data"
mkdir "projects/$projectName/docs"

# Скопировать шаблоны
Copy-Item "templates/*.csv" "projects/$projectName/checklists/"
```

---

## 🔧 Полезные команды

### Работа с Git:
```powershell
# Статус репозитория
git status

# Добавить все изменения
git add .

# Коммит
git commit -m "Описание изменений"

# Пуш на GitHub
git push origin main
```

### Очистка TestData:
```powershell
# Удалить сгенерированные файлы
Remove-Item TestData/*.json -ErrorAction SilentlyContinue
Remove-Item TestData/*.csv -ErrorAction SilentlyContinue
```

### Поиск файлов:
```powershell
# Найти все CSV файлы
Get-ChildItem -Recurse -Filter "*.csv"

# Найти все DOCX файлы
Get-ChildItem -Recurse -Filter "*.docx"

# Найти файлы по маске
Get-ChildItem -Recurse -Filter "*bug*"
```

---

## 📋 Установка зависимостей

```powershell
# Pandoc (для конвертации DOCX → Markdown)
# Запустить PowerShell от имени Администратора!
choco install pandoc

# Проверить установку Pandoc
pandoc --version
```

---

## 🚀 Быстрый старт

```powershell
# 1. Перейти в папку проекта
cd C:\REPO\QArepo\QA

# 2. Запустить генератор тестовых данных
python scripts/test_data_generator.py

# 3. Или конвертировать DOCX в Markdown
python scripts/docx_to_md.py
```

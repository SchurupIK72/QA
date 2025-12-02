# Структура проекта QA Automation

## Назначение папок

### `/templates`
Содержит универсальные шаблоны для тестовой документации:
- `bug-report-template.csv` - Шаблон баг-репорта с обязательными полями
- `checklist-regression-template.csv` - Шаблон чек-листа регрессионного тестирования

### `/projects`
Хранилище для конкретных проектов. Для каждого проекта создается отдельная папка со структурой:
```
project-name/
├── bug-reports/      # Баг-репорты проекта (копии из шаблона)
├── checklists/       # Чек-листы проекта
├── test-data/        # Тестовые данные для проекта
└── docs/             # Специфичная документация (ТЗ, ГДД, etc.)
```

### `/docs`
Общая документация и регламенты работы:
- `Введение в QA.md` - Основной рабочий регламент
- Другие общие документы

### `/scripts`
Скрипты для автоматизации рутинных задач (планируется):
- Генерация структуры нового проекта
- Валидация баг-репортов
- Генерация отчетов
- Утилиты для работы с тестовыми данными

## Примеры использования

### Создание нового проекта
```powershell
# PowerShell
mkdir projects/MyNewProject
mkdir projects/MyNewProject/{bug-reports,checklists,test-data,docs}
Copy-Item templates/bug-report-template.csv projects/MyNewProject/bug-reports/
Copy-Item templates/checklist-regression-template.csv projects/MyNewProject/checklists/
```

### Именование файлов
- Баг-репорты: `bug-report-YYYY-MM-DD.csv` или `bug-report-v1.0.csv`
- Чек-листы: `checklist-regression-YYYY-MM-DD.csv`
- Тестовые данные: `test-data-[feature-name].csv`

"""
Конвертер JSON в Markdown
Версия: 1.0.0

Преобразует JSON файлы в читаемый Markdown формат.
Поддерживает вложенные объекты, массивы и таблицы.

Использование:
    python json_to_md.py input.json              # Создаст input.md в той же папке
    python json_to_md.py input.json output.md    # Указать имя выходного файла
    python json_to_md.py                         # Интерактивный режим
    python json_to_md.py folder/                 # Конвертировать все JSON в папке
"""

import os
import sys
import json
from pathlib import Path
from typing import Any, Union


def json_value_to_md(value: Any, indent_level: int = 0) -> str:
    """
    Преобразует значение JSON в Markdown строку
    
    Args:
        value: Значение из JSON
        indent_level: Уровень вложенности для отступов
        
    Returns:
        Markdown строка
    """
    indent = "  " * indent_level
    
    if value is None:
        return f"{indent}*null*"
    
    if isinstance(value, bool):
        return f"{indent}`{str(value).lower()}`"
    
    if isinstance(value, (int, float)):
        return f"{indent}`{value}`"
    
    if isinstance(value, str):
        # Экранируем специальные символы Markdown
        escaped = value.replace("|", "\\|").replace("\n", "<br>")
        if len(escaped) > 100:
            return f"{indent}{escaped[:100]}..."
        return f"{indent}{escaped}"
    
    if isinstance(value, list):
        if not value:
            return f"{indent}*пустой массив*"
        
        # Проверяем, является ли это массивом простых значений
        if all(isinstance(item, (str, int, float, bool, type(None))) for item in value):
            items = [json_value_to_md(item, 0).strip() for item in value]
            return f"{indent}" + ", ".join(items)
        
        # Массив объектов - рекурсивно обрабатываем
        lines = []
        for i, item in enumerate(value):
            if isinstance(item, dict):
                lines.append(f"{indent}- **Элемент {i + 1}:**")
                lines.append(dict_to_md(item, indent_level + 1))
            else:
                lines.append(f"{indent}- {json_value_to_md(item, 0).strip()}")
        return "\n".join(lines)
    
    if isinstance(value, dict):
        return dict_to_md(value, indent_level)
    
    return f"{indent}`{value}`"


def dict_to_md(data: dict, indent_level: int = 0) -> str:
    """
    Преобразует словарь в Markdown
    
    Args:
        data: Словарь для преобразования
        indent_level: Уровень вложенности
        
    Returns:
        Markdown строка
    """
    lines = []
    indent = "  " * indent_level
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent}- **{key}:**")
            lines.append(dict_to_md(value, indent_level + 1))
        elif isinstance(value, list):
            lines.append(f"{indent}- **{key}:** {json_value_to_md(value, indent_level + 1)}")
        else:
            md_value = json_value_to_md(value, 0).strip()
            lines.append(f"{indent}- **{key}:** {md_value}")
    
    return "\n".join(lines)


def is_table_compatible(data: list) -> bool:
    """
    Проверяет, можно ли представить массив объектов как таблицу
    
    Args:
        data: Массив для проверки
        
    Returns:
        True если можно представить как таблицу
    """
    if not data or not isinstance(data, list):
        return False
    
    if not all(isinstance(item, dict) for item in data):
        return False
    
    # Получаем все ключи первого элемента
    first_keys = set(data[0].keys())
    
    # Проверяем, что все элементы имеют схожие ключи
    for item in data:
        if not isinstance(item, dict):
            return False
        # Допускаем небольшие различия в ключах
        item_keys = set(item.keys())
        if len(first_keys.symmetric_difference(item_keys)) > len(first_keys) * 0.3:
            return False
    
    # Проверяем, что значения - простые типы
    for item in data:
        for value in item.values():
            if isinstance(value, (dict, list)) and value:
                # Разрешаем пустые вложенные структуры
                if isinstance(value, dict) and len(value) > 0:
                    return False
                if isinstance(value, list) and len(value) > 0:
                    # Проверяем, что это массив простых значений
                    if not all(isinstance(v, (str, int, float, bool, type(None))) for v in value):
                        return False
    
    return True


def list_to_table(data: list) -> str:
    """
    Преобразует массив объектов в Markdown таблицу
    
    Args:
        data: Массив объектов
        
    Returns:
        Markdown таблица
    """
    if not data:
        return "*пустой массив*"
    
    # Собираем все уникальные ключи
    all_keys = []
    for item in data:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)
    
    # Создаем заголовок
    header = "| " + " | ".join(str(key) for key in all_keys) + " |"
    separator = "| " + " | ".join("---" for _ in all_keys) + " |"
    
    # Создаем строки
    rows = []
    for item in data:
        row_values = []
        for key in all_keys:
            value = item.get(key, "")
            if isinstance(value, list):
                cell = ", ".join(str(v) for v in value)
            elif isinstance(value, dict):
                cell = json.dumps(value, ensure_ascii=False)[:50]
            elif value is None:
                cell = "-"
            elif isinstance(value, bool):
                cell = "✓" if value else "✗"
            else:
                cell = str(value).replace("|", "\\|").replace("\n", " ")
                if len(cell) > 50:
                    cell = cell[:47] + "..."
            row_values.append(cell)
        rows.append("| " + " | ".join(row_values) + " |")
    
    return "\n".join([header, separator] + rows)


def json_to_markdown(data: Any, title: str = None) -> str:
    """
    Главная функция преобразования JSON в Markdown
    
    Args:
        data: JSON данные (dict или list)
        title: Заголовок документа
        
    Returns:
        Markdown строка
    """
    lines = []
    
    if title:
        lines.append(f"# {title}")
        lines.append("")
    
    if isinstance(data, dict):
        # Обрабатываем верхнеуровневые поля
        for key, value in data.items():
            # Пропускаем технические поля comment
            if key == "comment" and isinstance(value, str):
                lines.append(f"> {value}")
                lines.append("")
                continue
            
            # Заголовок секции
            lines.append(f"## {key}")
            lines.append("")
            
            if isinstance(value, list):
                if is_table_compatible(value):
                    lines.append(list_to_table(value))
                else:
                    lines.append(json_value_to_md(value, 0))
            elif isinstance(value, dict):
                lines.append(dict_to_md(value, 0))
            else:
                lines.append(json_value_to_md(value, 0))
            
            lines.append("")
    
    elif isinstance(data, list):
        if is_table_compatible(data):
            lines.append(list_to_table(data))
        else:
            lines.append(json_value_to_md(data, 0))
    
    else:
        lines.append(json_value_to_md(data, 0))
    
    return "\n".join(lines)


def convert_json_to_md(
    json_path: str,
    output_path: str = None,
    encoding: str = "utf-8"
) -> str:
    """
    Конвертация JSON файла в Markdown
    
    Args:
        json_path: Путь к JSON файлу
        output_path: Путь для сохранения MD файла (опционально)
        encoding: Кодировка файлов
        
    Returns:
        Путь к созданному MD файлу
        
    Raises:
        FileNotFoundError: Если JSON файл не найден
        json.JSONDecodeError: Если JSON невалидный
    """
    json_file = Path(json_path)
    
    if not json_file.exists():
        raise FileNotFoundError(f"Файл не найден: {json_path}")
    
    if not json_file.suffix.lower() == ".json":
        raise ValueError(f"Ожидается JSON файл, получен: {json_file.suffix}")
    
    # Определяем выходной путь
    if output_path:
        md_file = Path(output_path)
    else:
        md_file = json_file.with_suffix(".md")
    
    # Читаем JSON
    with open(json_file, "r", encoding=encoding) as f:
        data = json.load(f)
    
    # Определяем заголовок из имени файла или данных
    title = None
    if isinstance(data, dict):
        title = data.get("testName") or data.get("name") or data.get("title")
    if not title:
        title = json_file.stem.replace("-", " ").replace("_", " ").title()
    
    # Конвертируем
    markdown = json_to_markdown(data, title)
    
    # Сохраняем
    with open(md_file, "w", encoding=encoding) as f:
        f.write(markdown)
    
    return str(md_file)


def convert_folder(folder_path: str, recursive: bool = False) -> list:
    """
    Конвертирует все JSON файлы в папке
    
    Args:
        folder_path: Путь к папке
        recursive: Рекурсивный обход подпапок
        
    Returns:
        Список созданных MD файлов
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"Не является папкой: {folder_path}")
    
    pattern = "**/*.json" if recursive else "*.json"
    json_files = list(folder.glob(pattern))
    
    results = []
    for json_file in json_files:
        try:
            md_path = convert_json_to_md(str(json_file))
            results.append(md_path)
            print(f"✅ {json_file.name} → {Path(md_path).name}")
        except Exception as e:
            print(f"❌ {json_file.name}: {e}")
    
    return results


def interactive_mode():
    """Интерактивный режим выбора файла"""
    print("\n" + "=" * 60)
    print("  JSON → MARKDOWN КОНВЕРТЕР")
    print("=" * 60)
    
    # Ищем JSON файлы в текущей папке
    current_dir = Path.cwd()
    json_files = list(current_dir.glob("*.json"))
    
    # Также ищем в подпапках
    for subdir in current_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("."):
            json_files.extend(subdir.glob("*.json"))
    
    if not json_files:
        print("\n❌ JSON файлы не найдены в текущей директории")
        print(f"   Текущая папка: {current_dir}")
        return None
    
    print(f"\n📁 Найдено JSON файлов: {len(json_files)}")
    print("\nВыберите файл для конвертации:\n")
    
    for i, file in enumerate(json_files[:20], 1):
        rel_path = file.relative_to(current_dir)
        print(f"  {i:2}. {rel_path}")
    
    if len(json_files) > 20:
        print(f"\n  ... и ещё {len(json_files) - 20} файлов")
    
    print(f"\n  0. Конвертировать ВСЕ файлы")
    
    try:
        choice = input("\n📝 Введите номер (или путь к файлу): ").strip()
        
        if choice == "0":
            return "ALL"
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(json_files):
                return str(json_files[idx])
        
        # Возможно ввели путь напрямую
        if Path(choice).exists():
            return choice
        
        print(f"\n❌ Неверный выбор: {choice}")
        return None
        
    except KeyboardInterrupt:
        print("\n\n👋 Отменено")
        return None


def main():
    """Главная функция"""
    
    if len(sys.argv) < 2:
        # Интерактивный режим
        result = interactive_mode()
        
        if result == "ALL":
            print("\n🔄 Конвертация всех JSON файлов...\n")
            results = convert_folder(str(Path.cwd()), recursive=True)
            print(f"\n✅ Конвертировано файлов: {len(results)}")
            return
        
        if result:
            json_path = result
        else:
            return
    else:
        json_path = sys.argv[1]
    
    # Проверяем, папка это или файл
    target = Path(json_path)
    
    if target.is_dir():
        print(f"\n📂 Конвертация всех JSON в папке: {target}\n")
        results = convert_folder(str(target), recursive=True)
        print(f"\n✅ Конвертировано файлов: {len(results)}")
        return
    
    # Определяем выходной файл
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        print(f"\n🔄 Конвертация: {json_path}")
        md_path = convert_json_to_md(json_path, output_path)
        print(f"✅ Создан файл: {md_path}")
        
        # Показываем размер
        md_file = Path(md_path)
        size_kb = md_file.stat().st_size / 1024
        print(f"📊 Размер: {size_kb:.1f} KB")
        
    except FileNotFoundError as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n❌ Ошибка парсинга JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

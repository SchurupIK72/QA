"""
Конвертер DOCX в Markdown через Pandoc
Версия: 2.0.0

Требования:
    Pandoc должен быть установлен через Chocolatey:
    choco install pandoc

Использование:
    python docx_to_md.py input.docx              # Создаст input.md в той же папке
    python docx_to_md.py input.docx output.md    # Указать имя выходного файла
    python docx_to_md.py                         # Интерактивный режим
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pandoc() -> bool:
    """Проверка установлен ли Pandoc"""
    return shutil.which("pandoc") is not None


def install_pandoc_instructions():
    """Инструкции по установке Pandoc"""
    print("\n" + "=" * 60)
    print("  УСТАНОВКА PANDOC")
    print("=" * 60)
    print("\n❌ Pandoc не установлен!")
    print("\n📋 Для установки выполните команду (от имени Администратора):\n")
    print("   choco install pandoc")
    print("\n   Или скачайте с официального сайта:")
    print("   https://pandoc.org/installing.html")
    print("\n" + "=" * 60)


def convert_docx_to_md(
    docx_path: str, 
    output_path: str = None,
    extract_media: bool = True,
    wrap: str = "none"
) -> str:
    """
    Конвертация DOCX в Markdown через Pandoc
    
    Args:
        docx_path: Путь к DOCX файлу
        output_path: Путь для сохранения MD файла (опционально)
        extract_media: Извлекать ли медиа файлы (изображения)
        wrap: Перенос строк ("none", "auto", "preserve")
        
    Returns:
        Путь к созданному MD файлу
    """
    docx_path = Path(docx_path).resolve()
    
    if not docx_path.exists():
        raise FileNotFoundError(f"Файл не найден: {docx_path}")
    
    if not docx_path.suffix.lower() == '.docx':
        raise ValueError(f"Файл должен быть формата DOCX: {docx_path}")
    
    # Определяем выходной файл
    if output_path is None:
        output_path = docx_path.with_suffix('.md')
    else:
        output_path = Path(output_path).resolve()
    
    # Создаем папку для медиа
    media_dir = output_path.parent / "media"
    
    # Формируем команду Pandoc
    cmd = [
        "pandoc",
        str(docx_path),
        "-f", "docx",
        "-t", "markdown",
        "-o", str(output_path),
        f"--wrap={wrap}",
        "--standalone"
    ]
    
    # Добавляем извлечение медиа
    if extract_media:
        cmd.extend(["--extract-media", str(media_dir)])
    
    # Выполняем конвертацию
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise RuntimeError(f"Pandoc error: {error_msg}")
        
        return str(output_path)
        
    except FileNotFoundError:
        raise RuntimeError("Pandoc не найден. Установите: choco install pandoc")


def convert_batch(input_dir: str, output_dir: str = None) -> list:
    """
    Пакетная конвертация всех DOCX файлов в папке
    
    Args:
        input_dir: Папка с DOCX файлами
        output_dir: Папка для результатов (опционально)
        
    Returns:
        Список путей к созданным MD файлам
    """
    input_path = Path(input_dir)
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    docx_files = list(input_path.glob("*.docx")) + list(input_path.glob("*.DOCX"))
    results = []
    
    for docx_file in docx_files:
        output_file = output_path / docx_file.with_suffix('.md').name
        try:
            result = convert_docx_to_md(str(docx_file), str(output_file))
            results.append(result)
            print(f"✅ {docx_file.name} → {output_file.name}")
        except Exception as e:
            print(f"❌ {docx_file.name}: {e}")
    
    return results


class InteractiveConverter:
    """Интерактивный режим конвертера"""
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Вывод заголовка"""
        print("=" * 60)
        print("  КОНВЕРТЕР DOCX → MARKDOWN (Pandoc)")
        print("=" * 60)
    
    def get_docx_files(self, directory: str = ".") -> list:
        """Получение списка DOCX файлов"""
        path = Path(directory)
        files = list(path.glob("*.docx")) + list(path.glob("*.DOCX"))
        # Убираем дубликаты по имени
        seen = set()
        unique_files = []
        for f in files:
            if f.name not in seen:
                seen.add(f.name)
                unique_files.append(f)
        return unique_files
    
    def select_file(self) -> str:
        """Выбор файла для конвертации"""
        print("\n📁 Выберите способ указания файла:")
        print("  1. Ввести путь к файлу")
        print("  2. Выбрать из текущей папки")
        print("  3. Выбрать из другой папки")
        print("  4. Пакетная конвертация (все файлы в папке)")
        print("  0. Выход")
        
        choice = input("\nВаш выбор [1]: ").strip() or "1"
        
        if choice == "0":
            return None
        
        if choice == "1":
            path = input("\nВведите путь к DOCX файлу: ").strip()
            # Убираем кавычки если есть
            path = path.strip('"').strip("'")
            return path
        
        if choice == "4":
            return "BATCH"
        
        if choice == "2":
            directory = "."
        else:
            directory = input("\nВведите путь к папке: ").strip()
            directory = directory.strip('"').strip("'")
        
        files = self.get_docx_files(directory)
        
        if not files:
            print(f"\n❌ В папке не найдено DOCX файлов")
            return None
        
        print(f"\n📄 Найдено {len(files)} DOCX файл(ов):")
        for i, file in enumerate(files, 1):
            size_kb = file.stat().st_size / 1024
            print(f"  {i}. {file.name} ({size_kb:.1f} KB)")
        
        while True:
            try:
                idx = input(f"\nВыберите файл [1-{len(files)}]: ").strip()
                idx = int(idx)
                if 1 <= idx <= len(files):
                    return str(files[idx - 1])
            except ValueError:
                pass
            print("❌ Неверный выбор")
    
    def run_batch(self):
        """Пакетная конвертация"""
        print("\n📁 ПАКЕТНАЯ КОНВЕРТАЦИЯ")
        print("-" * 40)
        
        input_dir = input("Папка с DOCX файлами [.]: ").strip() or "."
        input_dir = input_dir.strip('"').strip("'")
        
        output_dir = input("Папка для результатов (Enter = та же папка): ").strip()
        output_dir = output_dir.strip('"').strip("'") if output_dir else None
        
        files = self.get_docx_files(input_dir)
        
        if not files:
            print(f"\n❌ В папке '{input_dir}' не найдено DOCX файлов")
            return
        
        print(f"\n⏳ Конвертация {len(files)} файлов...")
        print("-" * 40)
        
        results = convert_batch(input_dir, output_dir)
        
        print("-" * 40)
        print(f"\n✅ Сконвертировано: {len(results)} из {len(files)} файлов")
    
    def run(self):
        """Запуск интерактивного режима"""
        self.clear_screen()
        self.print_header()
        
        # Проверяем Pandoc
        if not check_pandoc():
            install_pandoc_instructions()
            input("\nНажмите Enter для выхода...")
            return
        
        print("\n✅ Pandoc установлен")
        
        # Получаем версию Pandoc
        try:
            result = subprocess.run(
                ["pandoc", "--version"],
                capture_output=True,
                text=True
            )
            version_line = result.stdout.split('\n')[0]
            print(f"   {version_line}")
        except:
            pass
        
        while True:
            selection = self.select_file()
            
            if selection is None:
                print("\n👋 До свидания!")
                break
            
            if selection == "BATCH":
                self.run_batch()
                input("\nНажмите Enter для продолжения...")
                self.clear_screen()
                self.print_header()
                continue
            
            if not os.path.exists(selection):
                print(f"\n❌ Файл не найден: {selection}")
                input("\nНажмите Enter для продолжения...")
                continue
            
            # Определяем выходной файл
            default_output = Path(selection).with_suffix('.md').name
            output_path = input(f"\nИмя выходного файла [{default_output}]: ").strip()
            
            if not output_path:
                output_path = str(Path(selection).with_suffix('.md'))
            
            # Опции
            print("\n⚙️ Опции:")
            extract_media = input("Извлекать изображения? [Y/n]: ").strip().lower()
            extract_media = extract_media not in ['n', 'no', 'н', 'нет']
            
            # Конвертация
            try:
                print(f"\n⏳ Конвертация...")
                result_path = convert_docx_to_md(
                    selection, 
                    output_path,
                    extract_media=extract_media
                )
                
                print(f"\n✅ Файл успешно сконвертирован!")
                print(f"   Результат: {result_path}")
                
                # Статистика
                with open(result_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    words = len(content.split())
                    chars = len(content)
                
                print(f"\n📊 Статистика:")
                print(f"   Строк: {lines}")
                print(f"   Слов: {words}")
                print(f"   Символов: {chars}")
                
                # Проверяем медиа
                media_dir = Path(result_path).parent / "media"
                if media_dir.exists():
                    media_files = list(media_dir.rglob("*.*"))
                    if media_files:
                        print(f"   Изображений: {len(media_files)}")
                
            except Exception as e:
                print(f"\n❌ Ошибка конвертации: {e}")
            
            # Продолжение
            again = input("\n\nКонвертировать ещё файл? [Y/n]: ").strip().lower()
            if again in ['n', 'no', 'н', 'нет']:
                print("\n👋 До свидания!")
                break
            
            self.clear_screen()
            self.print_header()


def main():
    """Главная функция"""
    
    if len(sys.argv) == 1:
        # Интерактивный режим
        interactive = InteractiveConverter()
        interactive.run()
    
    elif len(sys.argv) >= 2:
        # Проверяем Pandoc
        if not check_pandoc():
            install_pandoc_instructions()
            sys.exit(1)
        
        # Командная строка
        docx_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        
        try:
            result_path = convert_docx_to_md(docx_path, output_path)
            print(f"✅ Конвертация завершена: {result_path}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

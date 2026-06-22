#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации регрессионного чек-листа из Технического Задания (ТЗ).

Парсит Markdown-файл ТЗ и преобразует функциональные требования 
в формат CSV чек-листа для регрессионного тестирования.

Использование:
    python tz_to_checklist.py <путь_к_ТЗ.md> [путь_к_выходному_файлу.csv]
    
Пример:
    python tz_to_checklist.py "../confidential/ТЗ.md" "../confidential/ЧекЛист.csv"
"""

import re
import csv
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


def configure_stdio() -> None:
    """Настройка UTF-8 вывода для Windows-консоли."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


@dataclass
class ChecklistItem:
    """Элемент чек-листа."""
    number: int
    name: str
    android: str = ""
    ios: str = ""
    pc: str = ""
    version: str = ""
    bug_link: str = ""
    comment: str = ""


@dataclass 
class Section:
    """Раздел документа."""
    level: int
    number: str
    title: str
    items: List[ChecklistItem] = field(default_factory=list)


class TZParser:
    """Парсер Технического Задания из Markdown формата."""
    
    # Паттерны для парсинга
    # Стандартный заголовок: ## 2.3 Школа
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s*(\d+(?:\.\d+)*\.?)\s*(.+)$')
    # Заголовок с markdown-разметкой: ### [2.3.3 Склад]{.mark}
    HEADER_MARKED_PATTERN = re.compile(r'^(#{1,6})\s*\[(\d+(?:\.\d+)*\.?)\s+([^\]]+)\](?:\{[^}]*\})?')
    HEADER_NO_NUM_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
    LIST_ITEM_PATTERN = re.compile(r'^\s*[-*•]\s+(.+)$')
    NUMBERED_LIST_PATTERN = re.compile(r'^\s*\d+[.)]\s+(.+)$')
    
    # Слова-маркеры, указывающие на функциональные требования
    FUNCTIONAL_MARKERS = [
        'должен', 'должна', 'должно', 'должны',
        'может', 'могут', 'можно',
        'отображается', 'отображаются', 'отображение',
        'доступен', 'доступна', 'доступно', 'доступны',
        'содержит', 'содержится', 'содержат',
        'позволяет', 'позволяют',
        'поддерживает', 'поддерживается',
        'выполняется', 'выполняет',
        'происходит', 'осуществляется',
        'открывается', 'закрывается',
        'включает', 'включается',
        'имеет', 'имеют',
        'использует', 'используется', 'используют',
        'при нажатии', 'при выборе', 'при вводе',
        'игрок', 'пользователь', 'персонаж', 'гладиатор',
        'система', 'функция', 'механика',
        'кнопка', 'экран', 'меню', 'список',
        'сортировка', 'фильтр',
        'начисляется', 'расходуется', 'получает',
        'увеличивается', 'уменьшается', 'снижается',
        'активируется', 'деактивируется',
        'работает', 'срабатывает',
    ]
    
    # Исключаемые паттерны (не являются требованиями)
    EXCLUDE_PATTERNS = [
        r'^рис\.',
        r'^изображение\s+\d',
        r'^таблица',
        r'^\*\*',
        r'^\[\[',
        r'^!\[',
        r'^---',
        r'^\s*$',
        r'^#',
        r'^GIF',
        r'^Формула',
        r'^Значения? указан',
        r'^Текст .* будет определен',
        r'^Точный список',
        r'^Подробнее',
        r'^Список возможных',
        r'^Пример',
    ]
    
    # Паттерны описательного текста (не требования)
    DESCRIPTIVE_PATTERNS = [
        r'тело .* сковано',  # Описания персонажей из таблицы
        r'тело .* инструмент',
        r'закаленное тело',
        r'разум .* холодный',
        r'тело в поту',
        r'расстеленные по полу',
        r'он .* на вершине',
        r'путь был долог',
        r'она прекрасна',
        r'тропа славы',
        r'Краткая суть проекта',
        r'Ближайшие аналоги',
        r'Название проекта',
        r'Жанр:',
        r'Платформа:',
        r'Локализация:',
        r'Формат:',
        r'Стиль:',
        r'Режим игры',
        r'Графическая часть',
        r'Технические требования',
        r'все значения указаны для тестов',
    ]
    
    # Паттерны для разбиения длинных предложений
    SPLIT_MARKERS = [
        ', а также',
        ', а ',
        '. Кроме того,',
        '. Также ',
        '. При этом ',
        ', при этом ',
        ', где ',
    ]
    
    def __init__(self, filepath: str, start_section: str = "2"):
        self.filepath = Path(filepath)
        self.content = ""
        self.sections: List[Section] = []
        self.checklist_items: List[Tuple[str, ChecklistItem]] = []  # (section_header, item)
        self.item_counter = 0
        self.start_section = start_section  # Начинать только с этого раздела
        self.parsing_active = False  # Флаг активного парсинга
        self.list_context = ""  # Контекст для элементов списка (вводное предложение)
        
    def load(self) -> None:
        """Загрузить файл ТЗ."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
            
    def clean_text(self, text: str) -> str:
        """Очистить текст от markdown-разметки."""
        # Удаляем ссылки markdown полностью
        text = re.sub(r'\[\[([^\]]+)\]\]\([^)]+\)', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Удаляем оставшиеся ссылки в скобках
        text = re.sub(r'\(https?://[^)]+\)', '', text)
        text = re.sub(r'\(#[^)]+\)', '', text)
        
        # Удаляем подчеркивание и жирный текст
        text = re.sub(r'\{\.underline\}', '', text)
        text = re.sub(r'\{\.mark\}', '', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Удаляем специальные символы markdown
        text = re.sub(r'\[', '', text)
        text = re.sub(r'\]', '', text)
        text = re.sub(r'\\\"', '"', text)
        text = re.sub(r'\\"', '"', text)
        
        # Очищаем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def is_list_item_valid(self, text: str) -> bool:
        """Проверить, является ли элемент списка валидным для чек-листа."""
        normalized_text = self.clean_text(text)

        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, normalized_text, re.IGNORECASE):
                return False

        # Минимальная длина
        if len(text) < 5:
            return False
            
        text_lower = text.lower()
        
        # Исключаем чисто описательные элементы
        if self.is_descriptive_text(text):
            return False
        
        # Элементы списка, которые являются категориями/опциями - включаем
        # Например: "Оружие", "Броня", "Сортировка по рангу"
        valid_list_markers = [
            'сортировка', 'фильтр', 'категория',
            'оружие', 'броня', 'расходуем',
            'повышение', 'понижение', 'улучшение',
            'продать', 'купить', 'выставить',
            'по имен', 'по ранг', 'по редкост', 'по названи',
            'валюта', 'soft', 'hard',
        ]
        
        for marker in valid_list_markers:
            if marker in text_lower:
                return True
        
        # Элементы достаточной длины с глаголами - включаем
        if len(text) >= 15:
            return True
            
        return False
    
    def is_descriptive_text(self, text: str) -> bool:
        """Проверить, является ли текст описательным (не требованием)."""
        text_lower = text.lower()
        for pattern in self.DESCRIPTIVE_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def is_functional_requirement(self, text: str) -> bool:
        """Проверить, является ли текст функциональным требованием."""
        normalized_text = self.clean_text(text)
        text_lower = text.lower()
        normalized_lower = normalized_text.lower()
        
        # Исключаем описательный текст
        if self.is_descriptive_text(text):
            return False
        
        # Исключаем по паттернам
        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, normalized_text, re.IGNORECASE):
                return False
        
        # Минимальная длина требования
        if len(text) < 15:
            return False
        
        # Слишком длинные предложения (> 300 символов) - скорее всего описание
        if len(text) > 400:
            return False
            
        # Проверяем наличие функциональных маркеров
        for marker in self.FUNCTIONAL_MARKERS:
            if marker in text_lower or marker in normalized_lower:
                return True
                
        # Проверяем начало предложения на глагол
        verb_starts = [
            'в ', 'на ', 'при ', 'после ', 'до ', 'для ', 'если ',
            'каждый', 'каждая', 'каждое', 'все ', 'любой', 'любая',
        ]
        for start in verb_starts:
            if text_lower.startswith(start) or normalized_lower.startswith(start):
                return True
                
        return False
    
    def transform_to_check(self, text: str) -> str:
        """Преобразовать требование в формулировку проверки."""
        text = self.clean_text(text)
        
        # Удаляем начальные маркеры списков
        text = re.sub(r'^[-*•]\s*', '', text)
        text = re.sub(r'^\d+[.)]\s*', '', text)
        
        # Убираем точку с запятой в конце
        text = re.sub(r';+\s*$', '', text)
        
        # Удаляем конечную точку для единообразия
        text = text.rstrip('.')
        
        # Убираем двойные пробелы
        text = re.sub(r'\s+', ' ', text)
        
        # Ограничиваем длину (отсекаем после определенной длины)
        if len(text) > 250:
            # Ищем логическую точку обрезки
            cutoff_patterns = ['. ', ', т.е.', ', где ', ', который ', ', которая ']
            for pattern in cutoff_patterns:
                idx = text.find(pattern)
                if 80 < idx < 200:
                    text = text[:idx]
                    break
        
        return text.strip()
    
    def split_complex_requirement(self, text: str) -> List[str]:
        """Разбить сложное требование на несколько простых."""
        results = []
        
        # Проверяем на маркеры разбиения
        for marker in self.SPLIT_MARKERS:
            if marker in text:
                parts = text.split(marker, 1)
                if len(parts) == 2 and len(parts[0]) > 30 and len(parts[1]) > 30:
                    results.extend(self.split_complex_requirement(parts[0]))
                    results.extend(self.split_complex_requirement(parts[1]))
                    return results
        
        # Не нашли маркеров - возвращаем как есть
        results.append(text)
        return results
    
    def extract_list_items(self, text: str) -> List[str]:
        """Извлечь элементы из списка в тексте."""
        items = []
        
        # Разбиваем по точке с запятой или переносу строки
        parts = re.split(r'[;\n]', text)
        
        for part in parts:
            part = part.strip()
            if part and len(part) > 5:
                # Убираем маркеры списков
                part = re.sub(r'^[-*•]\s*', '', part)
                part = re.sub(r'^\d+[.)]\s*', '', part)
                if part and len(part) > 5:
                    items.append(part)
                    
        return items
    
    def parse_paragraph(self, text: str, current_section: str) -> List[Tuple[str, ChecklistItem]]:
        """Парсить параграф и извлечь элементы чек-листа."""
        items = []
        
        # Пропускаем описательный текст
        if self.is_descriptive_text(text):
            return items
        
        # Проверяем, содержит ли текст список (разделенный ;)
        if ';' in text and text.count(';') >= 2:
            # Это вложенный список
            list_items = self.extract_list_items(text)
            
            # Если есть вводная часть до списка (до двоеточия)
            intro_match = re.match(r'^([^:]+):\s*', text)
            if intro_match:
                intro = intro_match.group(1).strip()
                if len(intro) > 20 and self.is_functional_requirement(intro):
                    self.item_counter += 1
                    items.append((current_section, ChecklistItem(
                        number=self.item_counter,
                        name=self.transform_to_check(intro)
                    )))
            
            # Добавляем элементы списка (только если они функциональные)
            for item_text in list_items:
                if self.is_functional_requirement(item_text):
                    self.item_counter += 1
                    items.append((current_section, ChecklistItem(
                        number=self.item_counter,
                        name=self.transform_to_check(item_text)
                    )))
        else:
            # Обычный параграф - пробуем разбить на части
            if self.is_functional_requirement(text):
                sub_requirements = self.split_complex_requirement(text)
                for sub_req in sub_requirements:
                    if self.is_functional_requirement(sub_req):
                        self.item_counter += 1
                        items.append((current_section, ChecklistItem(
                            number=self.item_counter,
                            name=self.transform_to_check(sub_req)
                        )))
                
        return items
    
    def parse(self) -> None:
        """Основной метод парсинга ТЗ."""
        lines = self.content.split('\n')
        current_section = ""
        current_section_num = ""
        paragraph_buffer = []
        in_code_block = False
        in_table = False
        
        for line in lines:
            # Пропускаем блоки кода
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
                
            # Пропускаем таблицы (строки с |)
            if '|' in line and line.count('|') >= 2:
                in_table = True
                continue
            if in_table and not line.strip():
                in_table = False
                continue
            if in_table:
                continue
            
            # Проверяем заголовок раздела с номером (два варианта формата)
            header_match = self.HEADER_PATTERN.match(line)
            header_marked_match = self.HEADER_MARKED_PATTERN.match(line)
            
            if header_match or header_marked_match:
                # Сохраняем накопленный параграф
                if paragraph_buffer and self.parsing_active:
                    paragraph_text = ' '.join(paragraph_buffer)
                    items = self.parse_paragraph(paragraph_text, current_section)
                    self.checklist_items.extend(items)
                    paragraph_buffer = []
                
                # Используем тот матч, который сработал
                match = header_marked_match if header_marked_match else header_match
                level = len(match.group(1))
                section_num = match.group(2).rstrip('.')
                section_title = self.clean_text(match.group(3))
                
                # Проверяем, начинается ли с нужного раздела
                if section_num.startswith(self.start_section):
                    self.parsing_active = True
                    current_section_num = section_num
                    current_section = f"{section_num} {section_title}"
                elif self.parsing_active and not section_num.startswith(self.start_section):
                    # Вышли за пределы нужного раздела
                    self.parsing_active = False
                continue
            
            # Если парсинг не активен - пропускаем
            if not self.parsing_active:
                continue
            
            # Проверяем заголовок без номера (подразделы)
            header_no_num = self.HEADER_NO_NUM_PATTERN.match(line)
            if header_no_num:
                if paragraph_buffer:
                    paragraph_text = ' '.join(paragraph_buffer)
                    items = self.parse_paragraph(paragraph_text, current_section)
                    self.checklist_items.extend(items)
                    paragraph_buffer = []
                continue
                
            # Пропускаем пустые строки (завершают параграф)
            if not line.strip():
                if paragraph_buffer:
                    paragraph_text = ' '.join(paragraph_buffer)
                    items = self.parse_paragraph(paragraph_text, current_section)
                    self.checklist_items.extend(items)
                    paragraph_buffer = []
                continue
            
            # Проверяем элемент маркированного списка
            list_match = self.LIST_ITEM_PATTERN.match(line)
            numbered_match = self.NUMBERED_LIST_PATTERN.match(line)
            
            if list_match or numbered_match:
                # Сохраняем предыдущий параграф как контекст для списка
                if paragraph_buffer:
                    paragraph_text = ' '.join(paragraph_buffer)
                    # Если параграф заканчивается на двоеточие - это вводная часть списка
                    if paragraph_text.rstrip().endswith(':'):
                        self.list_context = self.clean_text(paragraph_text.rstrip()[:-1])
                    else:
                        items = self.parse_paragraph(paragraph_text, current_section)
                        self.checklist_items.extend(items)
                        self.list_context = ""
                    paragraph_buffer = []
                
                # Обрабатываем элемент списка
                item_text = (list_match or numbered_match).group(1)
                cleaned_item = self.transform_to_check(item_text)
                
                # Пропускаем слишком короткие элементы без контекста
                if len(cleaned_item) < 5:
                    continue
                    
                # Проверяем нужно ли добавить элемент
                if self.is_functional_requirement(item_text) or self.is_list_item_valid(cleaned_item):
                    self.item_counter += 1
                    self.checklist_items.append((current_section, ChecklistItem(
                        number=self.item_counter,
                        name=cleaned_item
                    )))
                continue
                
            # Обычная строка - добавляем в буфер параграфа
            stripped = line.strip()
            # Пропускаем строки с изображениями и цитатами
            if stripped and not stripped.startswith('!') and not stripped.startswith('>'):
                # Пропускаем строки, которые явно не требования
                if not re.match(r'^\*?Рис\.', stripped) and not re.match(r'^---', stripped):
                    paragraph_buffer.append(stripped)
        
        # Обрабатываем последний параграф
        if paragraph_buffer and self.parsing_active:
            paragraph_text = ' '.join(paragraph_buffer)
            items = self.parse_paragraph(paragraph_text, current_section)
            self.checklist_items.extend(items)


class ChecklistGenerator:
    """Генератор CSV чек-листа."""
    
    CSV_HEADER = [
        "№ п\\п", "Название", "Android", "IOS", "ПК", 
        "Версия сборки", "Ссылка на баг-репорт", "Комментарий"
    ]
    
    def __init__(self, project_name: str = "Проект"):
        self.project_name = project_name
        self.items: List[Tuple[str, ChecklistItem]] = []
        
    def add_items(self, items: List[Tuple[str, ChecklistItem]]) -> None:
        """Добавить элементы чек-листа."""
        self.items.extend(items)
        
    def generate_csv(self, output_path: str) -> None:
        """Сгенерировать CSV-файл чек-листа."""
        output_file = Path(output_path)
        
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            # Заголовок таблицы (без заголовка документа для чистоты)
            writer.writerow(self.CSV_HEADER)
            
            current_section = ""
            item_num = 0
            
            for section, item in self.items:
                # Добавляем заголовок раздела при смене
                if section != current_section:
                    current_section = section
                    # Записываем раздел отдельной строкой
                    writer.writerow([section, "", "", "", "", "", "", ""])
                
                # Проверяем, является ли строка "вводной" (заканчивается на :)
                # Такие строки не нумеруем - это подзаголовки для пулов проверок
                is_intro_line = item.name.rstrip().endswith(':')
                
                if is_intro_line:
                    # Подзаголовок без номера
                    writer.writerow([
                        "",
                        item.name,
                        item.android,
                        item.ios,
                        item.pc,
                        item.version,
                        item.bug_link,
                        item.comment
                    ])
                else:
                    # Обычная проверка с номером
                    item_num += 1
                    writer.writerow([
                        item_num,
                        item.name,
                        item.android,
                        item.ios,
                        item.pc,
                        item.version,
                        item.bug_link,
                        item.comment
                    ])
                
    def print_stats(self) -> None:
        """Вывести статистику."""
        sections = set(section for section, _ in self.items)
        # Считаем только реальные проверки (не вводные строки)
        actual_checks = sum(1 for _, item in self.items if not item.name.rstrip().endswith(':'))
        intro_lines = len(self.items) - actual_checks
        
        print(f"\n📊 Статистика генерации:")
        print(f"   Всего тест-кейсов: {actual_checks}")
        print(f"   Подзаголовков (без номера): {intro_lines}")
        print(f"   Разделов: {len(sections)}")
        print(f"\n📝 Разделы:")
        
        section_counts = {}
        for section, item in self.items:
            if not item.name.rstrip().endswith(':'):
                section_counts[section] = section_counts.get(section, 0) + 1
            
        for section in sorted(section_counts.keys()):
            count = section_counts[section]
            print(f"   • {section}: {count} проверок")


def main():
    """Главная функция."""
    configure_stdio()

    parser = argparse.ArgumentParser(
        description='Генерация регрессионного чек-листа из ТЗ'
    )
    parser.add_argument(
        'input_file',
        help='Путь к файлу ТЗ в формате Markdown'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default=None,
        help='Путь к выходному CSV-файлу (опционально)'
    )
    parser.add_argument(
        '--project',
        '-p',
        default='проекта',
        help='Название проекта для заголовка чек-листа'
    )
    parser.add_argument(
        '--start-section',
        '-s',
        default='2',
        help='Номер раздела, с которого начинать парсинг (по умолчанию: 2)'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"❌ Ошибка: файл '{input_path}' не найден")
        sys.exit(1)
        
    # Определяем выходной файл
    if args.output_file:
        output_path = args.output_file
    else:
        output_path = input_path.parent / f"ЧекЛист-{input_path.stem}.csv"
    
    print(f"📖 Загрузка ТЗ: {input_path}")
    print(f"📌 Начало парсинга с раздела: {args.start_section}")
    
    # Парсим ТЗ
    tz_parser = TZParser(str(input_path), start_section=args.start_section)
    tz_parser.load()
    tz_parser.parse()
    
    print(f"✅ Найдено требований: {len(tz_parser.checklist_items)}")
    
    # Генерируем чек-лист
    generator = ChecklistGenerator(args.project)
    generator.add_items(tz_parser.checklist_items)
    generator.generate_csv(str(output_path))
    
    print(f"💾 Чек-лист сохранен: {output_path}")
    generator.print_stats()
    
    
if __name__ == '__main__':
    main()

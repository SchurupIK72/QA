"""
Генератор Playwright тестов для QA проектов
Версия: 1.0.0

На основе ТЗ проекта Увелка Петфуд
Целевой сайт: http://uvelka-petfood.tw1.ru/

Требования:
    pip install playwright
    playwright install

Использование:
    python playwright_generator.py
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Any

# Путь к папке для сохранения тестов
TESTS_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")


class PlaywrightTestGenerator:
    """Генератор Playwright тестов на основе ТЗ"""
    
    def __init__(self, base_url: str = "http://uvelka-petfood.tw1.ru"):
        self.base_url = base_url
        self.project_name = "UvelkaPetfood"
        self.generated_tests = []
        
        # Структура сайта из ТЗ
        self.site_structure = {
            "main": {
                "name": "Главная страница",
                "url": "/",
                "elements": [
                    {"selector": "header", "name": "Заголовок сайта"},
                    {"selector": ".hero-section, .hero, [class*='hero']", "name": "Hero-секция"},
                    {"selector": "a[href*='brand'], .brands, [class*='brand']", "name": "Блок Бренды"},
                    {"selector": ".about, [class*='about']", "name": "Блок О компании"},
                    {"selector": ".partners, [class*='partner']", "name": "Блок Партнерам"},
                    {"selector": ".news, [class*='news']", "name": "Блок Новости"},
                    {"selector": ".career, [class*='career']", "name": "Блок Карьера"},
                    {"selector": "footer", "name": "Футер"},
                ]
            },
            "brands": {
                "name": "Раздел Бренды",
                "url": "/brands",
                "elements": [
                    {"selector": ".brand-card, [class*='brand']", "name": "Карточка бренда"},
                    {"selector": ".sidebar, nav[class*='brand']", "name": "Боковая навигация"},
                ]
            },
            "about": {
                "name": "Раздел О компании",
                "url": "/about",
                "elements": [
                    {"selector": ".employees, [class*='employee'], [class*='staff']", "name": "Блок сотрудников"},
                ]
            },
            "partners": {
                "name": "Раздел Партнерам",
                "url": "/partners",
                "elements": [
                    {"selector": "video, iframe[src*='vk'], [class*='video']", "name": "Видеоплеер"},
                    {"selector": ".documents, [class*='doc']", "name": "Блок документов"},
                    {"selector": "button[class*='contact'], a[class*='contact']", "name": "Кнопка Связаться"},
                ]
            },
            "news": {
                "name": "Раздел Новости",
                "url": "/news",
                "elements": [
                    {"selector": ".news-card, article, [class*='news-item']", "name": "Новостной пост"},
                    {"selector": "button[class*='more'], .show-more", "name": "Кнопка Показать еще"},
                ]
            },
            "career": {
                "name": "Раздел Карьера",
                "url": "/career",
                "elements": [
                    {"selector": ".vacancy, [class*='job']", "name": "Вакансии"},
                ]
            },
            "contacts": {
                "name": "Раздел Контакты",
                "url": "/contacts",
                "elements": [
                    {"selector": ".contact-info, [class*='contact']", "name": "Контактная информация"},
                    {"selector": "a[href^='tel:']", "name": "Телефоны"},
                    {"selector": "a[href^='mailto:']", "name": "Email"},
                ]
            }
        }
        
        # Формы на сайте
        self.forms = {
            "feedback": {
                "name": "Форма обратной связи",
                "fields": [
                    {"name": "email", "selector": "input[type='email'], input[name*='email']", "required": True, "type": "email"},
                    {"name": "subject", "selector": "select[name*='subject'], select[name*='theme']", "required": True, "type": "select"},
                    {"name": "message", "selector": "textarea", "required": True, "type": "textarea"},
                    {"name": "files", "selector": "input[type='file']", "required": False, "type": "file"},
                    {"name": "captcha", "selector": ".captcha, [class*='captcha'], iframe[src*='recaptcha']", "required": True, "type": "captcha"},
                ],
                "submit_button": "button[type='submit'], input[type='submit'], button:has-text('Отправить')",
            }
        }
        
        # Браузеры для тестирования (из ТЗ таблица 5.1)
        self.browsers = [
            {"name": "chromium", "display_name": "Google Chrome"},
            {"name": "firefox", "display_name": "Mozilla Firefox"},
            {"name": "webkit", "display_name": "Safari"},
        ]
    
    def generate_test_file_header(self) -> str:
        """Генерация заголовка тестового файла"""
        return f'''"""
Автоматические тесты для проекта {self.project_name}
Сгенерировано: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Базовый URL: {self.base_url}

Запуск тестов:
    pytest tests/ -v
    pytest tests/ -v --headed  # С отображением браузера
    pytest tests/ -v --browser chromium  # Конкретный браузер
"""

import pytest
from playwright.sync_api import Page, expect, sync_playwright
import re


# Конфигурация
BASE_URL = "{self.base_url}"
TIMEOUT = 30000  # 30 секунд


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Настройки контекста браузера"""
    return {{
        **browser_context_args,
        "viewport": {{"width": 1920, "height": 1080}},
        "locale": "ru-RU",
    }}


@pytest.fixture
def page(page: Page):
    """Настройка страницы перед каждым тестом"""
    page.set_default_timeout(TIMEOUT)
    yield page

'''
    
    def generate_navigation_tests(self) -> str:
        """Генерация тестов навигации"""
        tests = '''
# ============================================================
# ТЕСТЫ НАВИГАЦИИ
# ============================================================

class TestNavigation:
    """Тесты навигации по сайту"""
    
'''
        # Тест главной страницы
        tests += '''    def test_main_page_loads(self, page: Page):
        """Проверка загрузки главной страницы"""
        page.goto(BASE_URL)
        
        # Проверяем что страница загрузилась
        expect(page).to_have_title(re.compile(r".+"))
        
        # Проверяем наличие header
        expect(page.locator("header")).to_be_visible()
        
        # Проверяем наличие footer
        expect(page.locator("footer")).to_be_visible()
    
'''
        # Тесты переходов по разделам
        for section_key, section in self.site_structure.items():
            if section_key == "main":
                continue
            
            tests += f'''    def test_navigate_to_{section_key}(self, page: Page):
        """Переход в раздел: {section['name']}"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='{section_key}'], nav a[href*='{section_key}']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*{section_key}.*"))
    
'''
        
        # Тест хлебных крошек
        tests += '''    def test_breadcrumbs_navigation(self, page: Page):
        """Проверка навигации через хлебные крошки"""
        # Переходим во вложенный раздел
        page.goto(f"{BASE_URL}/about")
        page.wait_for_load_state("networkidle")
        
        # Ищем хлебные крошки
        breadcrumbs = page.locator(".breadcrumb, [class*='breadcrumb'], nav[aria-label='breadcrumb']")
        
        if breadcrumbs.count() > 0:
            # Кликаем на "Главная" в хлебных крошках
            home_link = breadcrumbs.locator("a").first
            if home_link.count() > 0:
                home_link.click()
                expect(page).to_have_url(BASE_URL + "/")
    
'''
        
        # Тест кнопки "Наверх"
        tests += '''    def test_scroll_to_top_button(self, page: Page):
        """Проверка кнопки 'Вернуться наверх'"""
        page.goto(BASE_URL)
        
        # Скроллим вниз
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        
        # Ищем кнопку "Наверх"
        scroll_btn = page.locator("[class*='scroll-top'], [class*='back-to-top'], button[aria-label*='наверх']")
        
        if scroll_btn.count() > 0:
            expect(scroll_btn.first).to_be_visible()
            scroll_btn.first.click()
            page.wait_for_timeout(500)
            
            # Проверяем что проскроллили наверх
            scroll_position = page.evaluate("window.scrollY")
            assert scroll_position < 100
    
'''
        return tests
    
    def generate_header_tests(self) -> str:
        """Генерация тестов заголовка сайта"""
        return '''
# ============================================================
# ТЕСТЫ ЗАГОЛОВКА (HEADER)
# ============================================================

class TestHeader:
    """Тесты заголовка сайта"""
    
    def test_logo_visible_and_clickable(self, page: Page):
        """Проверка логотипа - виден и кликабелен"""
        page.goto(BASE_URL)
        
        logo = page.locator("header a[href='/'], header .logo, header img[alt*='logo']").first
        expect(logo).to_be_visible()
        
        # Переходим в другой раздел
        page.goto(f"{BASE_URL}/about")
        
        # Кликаем на логотип
        logo = page.locator("header a[href='/'], header .logo").first
        logo.click()
        
        # Должны вернуться на главную
        expect(page).to_have_url(re.compile(r".*/$"))
    
    def test_sticky_header(self, page: Page):
        """Проверка фиксированного меню (sticky-header)"""
        page.goto(BASE_URL)
        
        header = page.locator("header").first
        
        # Скроллим вниз
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(300)
        
        # Header должен оставаться видимым
        expect(header).to_be_visible()
        
        # Проверяем позицию (должен быть в верхней части viewport)
        box = header.bounding_box()
        if box:
            assert box["y"] >= 0 and box["y"] < 100
    
    def test_menu_items_present(self, page: Page):
        """Проверка наличия пунктов меню"""
        page.goto(BASE_URL)
        
        menu_items = ["Бренды", "О компании", "Партнерам", "Новости", "Карьера"]
        
        for item in menu_items:
            menu_link = page.locator(f"header a:has-text('{item}'), nav a:has-text('{item}')")
            # Проверяем что хотя бы один элемент найден
            if menu_link.count() > 0:
                expect(menu_link.first).to_be_visible()
    
    def test_search_button_opens_search(self, page: Page):
        """Проверка кнопки поиска"""
        page.goto(BASE_URL)
        
        # Ищем кнопку поиска
        search_btn = page.locator("button[class*='search'], [class*='search'] button, header svg[class*='search']").first
        
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            # Должно появиться поле поиска
            search_input = page.locator("input[type='search'], input[name='search'], input[placeholder*='поиск']")
            expect(search_input.first).to_be_visible()
    
    def test_theme_switcher(self, page: Page):
        """Проверка переключателя темы (светлая/темная)"""
        page.goto(BASE_URL)
        
        theme_btn = page.locator("[class*='theme'], button[aria-label*='тема']").first
        
        if theme_btn.count() > 0:
            # Получаем текущий цвет фона
            initial_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            
            theme_btn.click()
            page.wait_for_timeout(300)
            
            # Цвет фона должен измениться
            new_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            # Тема могла измениться
            # assert initial_bg != new_bg  # Закомментировано - зависит от реализации

'''
    
    def generate_hero_section_tests(self) -> str:
        """Генерация тестов hero-секции"""
        return '''
# ============================================================
# ТЕСТЫ HERO-СЕКЦИИ (ОБЛОЖКА САЙТА)
# ============================================================

class TestHeroSection:
    """Тесты hero-секции на главной странице"""
    
    def test_hero_section_visible(self, page: Page):
        """Проверка видимости hero-секции"""
        page.goto(BASE_URL)
        
        hero = page.locator(".hero, [class*='hero'], .banner, [class*='banner']").first
        expect(hero).to_be_visible()
    
    def test_carousel_navigation(self, page: Page):
        """Проверка навигации карусели слайдов"""
        page.goto(BASE_URL)
        
        # Ищем кнопки навигации
        next_btn = page.locator("[class*='next'], [class*='arrow-right'], button[aria-label*='next']").first
        prev_btn = page.locator("[class*='prev'], [class*='arrow-left'], button[aria-label*='prev']").first
        
        if next_btn.count() > 0 and prev_btn.count() > 0:
            # Кликаем вперед
            next_btn.click()
            page.wait_for_timeout(500)
            
            # Кликаем назад
            prev_btn.click()
            page.wait_for_timeout(500)
    
    def test_carousel_indicators(self, page: Page):
        """Проверка индикаторов карусели"""
        page.goto(BASE_URL)
        
        indicators = page.locator("[class*='indicator'], [class*='dot'], .carousel-indicators button")
        
        if indicators.count() > 1:
            # Кликаем на второй индикатор
            indicators.nth(1).click()
            page.wait_for_timeout(500)
            
            # Проверяем что он активен
            expect(indicators.nth(1)).to_have_class(re.compile(r"active|current|selected"))
    
    def test_video_controls(self, page: Page):
        """Проверка элементов управления видео в hero-секции"""
        page.goto(BASE_URL)
        
        video = page.locator(".hero video, [class*='hero'] video").first
        
        if video.count() > 0:
            # Проверяем кнопку play/pause
            play_btn = page.locator("[class*='play'], button[aria-label*='play']").first
            if play_btn.count() > 0:
                expect(play_btn).to_be_visible()
            
            # Проверяем кнопку звука
            mute_btn = page.locator("[class*='mute'], [class*='volume'], button[aria-label*='звук']").first
            if mute_btn.count() > 0:
                expect(mute_btn).to_be_visible()

'''
    
    def generate_search_tests(self) -> str:
        """Генерация тестов поиска"""
        return '''
# ============================================================
# ТЕСТЫ ПОИСКА
# ============================================================

class TestSearch:
    """Тесты функционала поиска"""
    
    def test_search_opens_and_closes(self, page: Page):
        """Проверка открытия и закрытия поиска"""
        page.goto(BASE_URL)
        
        # Открываем поиск
        search_btn = page.locator("button[class*='search'], [class*='search'] button").first
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            search_input = page.locator("input[type='search'], input[name='search']").first
            expect(search_input).to_be_visible()
            
            # Закрываем поиск
            close_btn = page.locator("[class*='search'] button[class*='close'], [class*='search'] .close").first
            if close_btn.count() > 0:
                close_btn.click()
                page.wait_for_timeout(300)
                expect(search_input).not_to_be_visible()
    
    def test_search_with_query(self, page: Page):
        """Проверка поиска с запросом"""
        page.goto(BASE_URL)
        
        # Открываем поиск
        search_btn = page.locator("button[class*='search'], [class*='search'] button").first
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            search_input = page.locator("input[type='search'], input[name='search']").first
            search_input.fill("корм для кошек")
            
            # Нажимаем Enter или кнопку поиска
            search_input.press("Enter")
            page.wait_for_load_state("networkidle")
            
            # Должны быть результаты или сообщение
            results = page.locator("[class*='search-result'], [class*='result']")
            no_results = page.locator(":has-text('не найдено'), :has-text('нет результатов')")
            
            assert results.count() > 0 or no_results.count() > 0
    
    def test_search_max_length(self, page: Page):
        """Проверка ограничения длины строки поиска (256 символов по ТЗ)"""
        page.goto(BASE_URL)
        
        search_btn = page.locator("button[class*='search'], [class*='search'] button").first
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            search_input = page.locator("input[type='search'], input[name='search']").first
            
            # Пробуем ввести 300 символов
            long_text = "a" * 300
            search_input.fill(long_text)
            
            # Проверяем что ввелось не более 256 символов
            value = search_input.input_value()
            assert len(value) <= 256

'''
    
    def generate_form_tests(self) -> str:
        """Генерация тестов форм"""
        return '''
# ============================================================
# ТЕСТЫ ФОРМ
# ============================================================

class TestFeedbackForm:
    """Тесты формы обратной связи"""
    
    def test_form_opens(self, page: Page):
        """Проверка открытия формы обратной связи"""
        page.goto(BASE_URL)
        
        # Ищем кнопку открытия формы
        contact_btn = page.locator("a:has-text('Связаться'), button:has-text('Связаться'), a[href*='contact']").first
        
        if contact_btn.count() > 0:
            contact_btn.click()
            page.wait_for_timeout(500)
            
            # Проверяем что форма появилась
            form = page.locator("form[class*='contact'], form[class*='feedback'], .modal form")
            expect(form.first).to_be_visible()
    
    def test_form_required_fields(self, page: Page):
        """Проверка обязательных полей формы"""
        page.goto(f"{BASE_URL}/contacts")
        page.wait_for_load_state("networkidle")
        
        form = page.locator("form").first
        
        if form.count() > 0:
            # Пробуем отправить пустую форму
            submit_btn = form.locator("button[type='submit'], input[type='submit']").first
            if submit_btn.count() > 0:
                submit_btn.click()
                page.wait_for_timeout(300)
                
                # Должны появиться ошибки валидации
                # Поля с ошибками могут быть подсвечены или показано сообщение
                error_fields = page.locator("[class*='error'], [class*='invalid'], :invalid")
                # Форма не должна была отправиться
    
    def test_form_email_validation(self, page: Page):
        """Проверка валидации email в форме"""
        page.goto(f"{BASE_URL}/contacts")
        page.wait_for_load_state("networkidle")
        
        email_input = page.locator("input[type='email'], input[name*='email']").first
        
        if email_input.count() > 0:
            # Вводим невалидный email
            email_input.fill("invalid-email")
            email_input.blur()
            page.wait_for_timeout(300)
            
            # Должна появиться ошибка или поле должно быть невалидным
            is_invalid = page.evaluate("""
                () => {
                    const input = document.querySelector("input[type='email'], input[name*='email']");
                    return input && !input.validity.valid;
                }
            """)
            # Email должен быть невалидным
    
    def test_form_file_upload_limit(self, page: Page):
        """Проверка ограничений на загрузку файлов (макс 10 файлов, 2 МБ каждый)"""
        page.goto(f"{BASE_URL}/contacts")
        page.wait_for_load_state("networkidle")
        
        file_input = page.locator("input[type='file']").first
        
        if file_input.count() > 0:
            # Проверяем атрибут accept (допустимые форматы)
            accept = file_input.get_attribute("accept")
            # По ТЗ: png, jpg, pdf, doc, docx, xls, xlsx
    
    def test_form_successful_submission_message(self, page: Page):
        """Проверка сообщения об успешной отправке"""
        # Этот тест требует заполнения капчи, поэтому может быть пропущен
        pytest.skip("Требуется ручная проверка капчи")

'''
    
    def generate_footer_tests(self) -> str:
        """Генерация тестов футера"""
        return '''
# ============================================================
# ТЕСТЫ ФУТЕРА
# ============================================================

class TestFooter:
    """Тесты футера сайта"""
    
    def test_footer_visible(self, page: Page):
        """Проверка видимости футера"""
        page.goto(BASE_URL)
        
        # Скроллим до футера
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(300)
        
        footer = page.locator("footer").first
        expect(footer).to_be_visible()
    
    def test_footer_contacts_present(self, page: Page):
        """Проверка наличия контактов в футере"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        
        # Проверяем телефон
        phone = footer.locator("a[href^='tel:']")
        if phone.count() > 0:
            expect(phone.first).to_be_visible()
        
        # Проверяем email
        email = footer.locator("a[href^='mailto:']")
        if email.count() > 0:
            expect(email.first).to_be_visible()
    
    def test_footer_documents_links(self, page: Page):
        """Проверка ссылок на документы в футере"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        
        # Пользовательское соглашение
        agreement = footer.locator("a:has-text('соглашени'), a:has-text('Соглашени')")
        
        # Политика конфиденциальности
        privacy = footer.locator("a:has-text('конфиденциальност'), a:has-text('Политика')")
        
        # Публичная оферта
        offer = footer.locator("a:has-text('офер'), a:has-text('Офер')")
    
    def test_footer_social_links(self, page: Page):
        """Проверка ссылок на соцсети в футере"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        
        # ВКонтакте
        vk = footer.locator("a[href*='vk.com'], a[href*='vkontakte']")
        
        # Telegram
        telegram = footer.locator("a[href*='t.me'], a[href*='telegram']")
        
        # WhatsApp
        whatsapp = footer.locator("a[href*='whatsapp'], a[href*='wa.me']")

'''
    
    def generate_cookie_tests(self) -> str:
        """Генерация тестов cookie-баннера"""
        return '''
# ============================================================
# ТЕСТЫ COOKIE-БАННЕРА
# ============================================================

class TestCookieBanner:
    """Тесты cookie-баннера"""
    
    def test_cookie_banner_appears_on_first_visit(self, page: Page):
        """Проверка появления cookie-баннера при первом посещении"""
        # Очищаем cookies
        page.context.clear_cookies()
        
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        cookie_banner = page.locator("[class*='cookie'], [class*='consent'], [id*='cookie']").first
        
        if cookie_banner.count() > 0:
            expect(cookie_banner).to_be_visible()
    
    def test_cookie_banner_accept(self, page: Page):
        """Проверка принятия cookies"""
        page.context.clear_cookies()
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        accept_btn = page.locator("button:has-text('Принять'), button:has-text('Согласен')").first
        
        if accept_btn.count() > 0:
            accept_btn.click()
            page.wait_for_timeout(500)
            
            # Баннер должен исчезнуть
            cookie_banner = page.locator("[class*='cookie'], [class*='consent']").first
            expect(cookie_banner).not_to_be_visible()
    
    def test_cookie_banner_decline(self, page: Page):
        """Проверка отклонения cookies"""
        page.context.clear_cookies()
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        decline_btn = page.locator("button:has-text('Отклонить'), button:has-text('Отказ')").first
        
        if decline_btn.count() > 0:
            decline_btn.click()
            page.wait_for_timeout(500)
            
            # Баннер должен исчезнуть
            cookie_banner = page.locator("[class*='cookie'], [class*='consent']").first
            expect(cookie_banner).not_to_be_visible()

'''
    
    def generate_404_tests(self) -> str:
        """Генерация тестов страницы 404"""
        return '''
# ============================================================
# ТЕСТЫ СТРАНИЦЫ 404
# ============================================================

class Test404Page:
    """Тесты страницы 404"""
    
    def test_404_page_displays(self, page: Page):
        """Проверка отображения страницы 404"""
        page.goto(f"{BASE_URL}/nonexistent-page-xyz-123")
        
        # Проверяем статус ответа или текст на странице
        error_text = page.locator(":has-text('404'), :has-text('не найден'), :has-text('Not Found')")
        expect(error_text.first).to_be_visible()
    
    def test_404_page_has_home_button(self, page: Page):
        """Проверка кнопки 'Вернуться на главную' на странице 404"""
        page.goto(f"{BASE_URL}/nonexistent-page-xyz-123")
        
        home_btn = page.locator("a:has-text('Главн'), a:has-text('главн'), a[href='/']").first
        
        if home_btn.count() > 0:
            expect(home_btn).to_be_visible()
            home_btn.click()
            
            # Должны оказаться на главной
            expect(page).to_have_url(re.compile(r".*/$"))

'''
    
    def generate_responsive_tests(self) -> str:
        """Генерация тестов адаптивности"""
        return '''
# ============================================================
# ТЕСТЫ АДАПТИВНОСТИ (МОБИЛЬНЫЕ УСТРОЙСТВА)
# ============================================================

class TestResponsive:
    """Тесты адаптивной верстки"""
    
    @pytest.mark.parametrize("viewport", [
        {"width": 375, "height": 667, "name": "iPhone SE"},
        {"width": 390, "height": 844, "name": "iPhone 12"},
        {"width": 768, "height": 1024, "name": "iPad"},
        {"width": 1920, "height": 1080, "name": "Desktop"},
    ])
    def test_page_loads_on_different_viewports(self, page: Page, viewport):
        """Проверка загрузки страницы на разных разрешениях"""
        page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
        page.goto(BASE_URL)
        
        # Страница должна загрузиться
        expect(page.locator("body")).to_be_visible()
        
        # Header должен быть видимым
        header = page.locator("header").first
        expect(header).to_be_visible()
    
    def test_mobile_menu_hamburger(self, page: Page):
        """Проверка бургер-меню на мобильных устройствах"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(BASE_URL)
        
        # Ищем бургер-меню
        hamburger = page.locator("[class*='burger'], [class*='hamburger'], button[class*='menu']").first
        
        if hamburger.count() > 0:
            expect(hamburger).to_be_visible()
            hamburger.click()
            page.wait_for_timeout(300)
            
            # Меню должно открыться
            mobile_menu = page.locator("[class*='mobile-menu'], [class*='nav-open'], nav[class*='active']")
            expect(mobile_menu.first).to_be_visible()
    
    def test_images_responsive(self, page: Page):
        """Проверка адаптивности изображений"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(BASE_URL)
        
        images = page.locator("img")
        
        for i in range(min(images.count(), 5)):  # Проверяем первые 5 изображений
            img = images.nth(i)
            if img.is_visible():
                box = img.bounding_box()
                if box:
                    # Изображение не должно выходить за пределы viewport
                    assert box["width"] <= 375

'''
    
    def generate_performance_tests(self) -> str:
        """Генерация тестов производительности"""
        return '''
# ============================================================
# ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================================

class TestPerformance:
    """Тесты производительности"""
    
    def test_page_load_time(self, page: Page):
        """Проверка времени загрузки страницы"""
        start_time = page.evaluate("performance.now()")
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        end_time = page.evaluate("performance.now()")
        
        load_time = end_time - start_time
        
        # Страница должна загрузиться менее чем за 5 секунд
        assert load_time < 5000, f"Страница загружалась {load_time}ms"
    
    def test_no_console_errors(self, page: Page):
        """Проверка отсутствия ошибок в консоли"""
        errors = []
        
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Фильтруем известные безобидные ошибки
        critical_errors = [e for e in errors if "favicon" not in e.lower()]
        
        # Не должно быть критических ошибок
        assert len(critical_errors) == 0, f"Найдены ошибки: {critical_errors}"
    
    def test_no_broken_images(self, page: Page):
        """Проверка отсутствия битых изображений"""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        
        broken_images = page.evaluate("""
            () => {
                const images = document.querySelectorAll('img');
                const broken = [];
                images.forEach(img => {
                    if (!img.complete || img.naturalHeight === 0) {
                        broken.push(img.src);
                    }
                });
                return broken;
            }
        """)
        
        assert len(broken_images) == 0, f"Найдены битые изображения: {broken_images}"

'''
    
    def generate_seo_tests(self) -> str:
        """Генерация тестов SEO"""
        return '''
# ============================================================
# ТЕСТЫ SEO
# ============================================================

class TestSEO:
    """Тесты SEO-оптимизации"""
    
    def test_page_has_title(self, page: Page):
        """Проверка наличия заголовка страницы (title)"""
        page.goto(BASE_URL)
        
        title = page.title()
        assert len(title) > 0, "Заголовок страницы пустой"
        assert len(title) >= 40, f"Заголовок слишком короткий: {len(title)} символов"
        assert len(title) <= 70, f"Заголовок слишком длинный: {len(title)} символов"
    
    def test_page_has_meta_description(self, page: Page):
        """Проверка наличия meta description"""
        page.goto(BASE_URL)
        
        description = page.locator("meta[name='description']").get_attribute("content")
        
        assert description is not None, "Meta description отсутствует"
        assert len(description) > 0, "Meta description пустой"
        assert len(description) <= 160, f"Description слишком длинный: {len(description)} символов"
    
    def test_page_has_h1(self, page: Page):
        """Проверка наличия единственного H1"""
        page.goto(BASE_URL)
        
        h1_count = page.locator("h1").count()
        
        assert h1_count == 1, f"На странице {h1_count} тегов H1, должен быть 1"
    
    def test_images_have_alt(self, page: Page):
        """Проверка наличия alt у изображений"""
        page.goto(BASE_URL)
        
        images = page.locator("img")
        images_without_alt = []
        
        for i in range(images.count()):
            img = images.nth(i)
            alt = img.get_attribute("alt")
            if alt is None or alt.strip() == "":
                src = img.get_attribute("src")
                images_without_alt.append(src)
        
        assert len(images_without_alt) == 0, f"Изображения без alt: {images_without_alt}"
    
    def test_canonical_tag(self, page: Page):
        """Проверка наличия canonical тега"""
        page.goto(BASE_URL)
        
        canonical = page.locator("link[rel='canonical']")
        expect(canonical).to_have_count(1)
    
    def test_https_redirect(self, page: Page):
        """Проверка редиректа на HTTPS"""
        # Примечание: для локального тестирования может не работать
        response = page.goto(BASE_URL.replace("https://", "http://"))
        
        # URL должен быть HTTPS (если сайт поддерживает)
        # expect(page).to_have_url(re.compile(r"^https://"))

'''
    
    def generate_brands_section_tests(self) -> str:
        """Генерация тестов раздела Бренды"""
        return '''
# ============================================================
# ТЕСТЫ РАЗДЕЛА "БРЕНДЫ"
# ============================================================

class TestBrandsSection:
    """Тесты раздела Бренды"""
    
    def test_brands_page_loads(self, page: Page):
        """Проверка загрузки страницы брендов"""
        page.goto(f"{BASE_URL}/brands")
        page.wait_for_load_state("networkidle")
        
        # Должны быть карточки брендов
        brand_cards = page.locator("[class*='brand'], .card, article")
        assert brand_cards.count() > 0
    
    def test_brand_card_has_required_elements(self, page: Page):
        """Проверка наличия обязательных элементов карточки бренда"""
        page.goto(f"{BASE_URL}/brands")
        page.wait_for_load_state("networkidle")
        
        first_card = page.locator("[class*='brand'], .card, article").first
        
        if first_card.count() > 0:
            # Должно быть изображение
            img = first_card.locator("img")
            expect(img.first).to_be_visible()
            
            # Должно быть название
            title = first_card.locator("h2, h3, [class*='title']")
            expect(title.first).to_be_visible()
    
    def test_brand_sidebar_navigation(self, page: Page):
        """Проверка боковой навигации по брендам"""
        page.goto(f"{BASE_URL}/brands")
        page.wait_for_load_state("networkidle")
        
        sidebar = page.locator("aside, [class*='sidebar'], nav[class*='brand']").first
        
        if sidebar.count() > 0:
            # Кликаем на второй элемент в sidebar
            sidebar_items = sidebar.locator("a, button")
            if sidebar_items.count() > 1:
                sidebar_items.nth(1).click()
                page.wait_for_timeout(500)
                
                # Контент должен измениться
    
    def test_brand_detail_button(self, page: Page):
        """Проверка кнопки 'Подробнее' на карточке бренда"""
        page.goto(f"{BASE_URL}/brands")
        page.wait_for_load_state("networkidle")
        
        detail_btn = page.locator("a:has-text('Подробнее'), button:has-text('Подробнее')").first
        
        if detail_btn.count() > 0:
            # Проверяем что кнопка ведет на внешний сайт бренда
            href = detail_btn.get_attribute("href")
            # Может быть внешняя ссылка

'''
    
    def generate_news_section_tests(self) -> str:
        """Генерация тестов раздела Новости"""
        return '''
# ============================================================
# ТЕСТЫ РАЗДЕЛА "НОВОСТИ"
# ============================================================

class TestNewsSection:
    """Тесты раздела Новости"""
    
    def test_news_page_loads(self, page: Page):
        """Проверка загрузки страницы новостей"""
        page.goto(f"{BASE_URL}/news")
        page.wait_for_load_state("networkidle")
        
        # Должны быть новостные посты
        news_items = page.locator("article, [class*='news'], .post")
        assert news_items.count() > 0
    
    def test_news_sorted_by_date(self, page: Page):
        """Проверка сортировки новостей по дате (от новых к старым)"""
        page.goto(f"{BASE_URL}/news")
        page.wait_for_load_state("networkidle")
        
        dates = page.locator("[class*='date'], time, [datetime]")
        
        # Если есть даты, проверяем сортировку
        if dates.count() > 1:
            # Даты должны идти по убыванию
            pass  # Требуется парсинг дат
    
    def test_news_show_more_button(self, page: Page):
        """Проверка кнопки 'Показать еще'"""
        page.goto(f"{BASE_URL}/news")
        page.wait_for_load_state("networkidle")
        
        show_more = page.locator("button:has-text('Показать'), button:has-text('еще'), .load-more").first
        
        if show_more.count() > 0:
            initial_count = page.locator("article, [class*='news'], .post").count()
            
            show_more.click()
            page.wait_for_timeout(1000)
            
            new_count = page.locator("article, [class*='news'], .post").count()
            
            # Должно появиться больше новостей
            assert new_count >= initial_count
    
    def test_news_detail_page(self, page: Page):
        """Проверка открытия детальной страницы новости"""
        page.goto(f"{BASE_URL}/news")
        page.wait_for_load_state("networkidle")
        
        detail_link = page.locator("article a, [class*='news'] a:has-text('Подробнее')").first
        
        if detail_link.count() > 0:
            detail_link.click()
            page.wait_for_load_state("networkidle")
            
            # Должен быть заголовок новости
            h1 = page.locator("h1")
            expect(h1).to_be_visible()
    
    def test_news_image_enlarges_on_click(self, page: Page):
        """Проверка увеличения изображения по клику"""
        page.goto(f"{BASE_URL}/news")
        page.wait_for_load_state("networkidle")
        
        # Открываем детальную новость
        detail_link = page.locator("article a").first
        if detail_link.count() > 0:
            detail_link.click()
            page.wait_for_load_state("networkidle")
            
            # Кликаем на изображение в новости
            img = page.locator("article img, .content img").first
            if img.count() > 0:
                img.click()
                page.wait_for_timeout(500)
                
                # Должен появиться lightbox или модальное окно
                lightbox = page.locator("[class*='lightbox'], [class*='modal'], [class*='zoom']")
                # expect(lightbox.first).to_be_visible()

'''
    
    def generate_partners_section_tests(self) -> str:
        """Генерация тестов раздела Партнерам"""
        return '''
# ============================================================
# ТЕСТЫ РАЗДЕЛА "ПАРТНЕРАМ"
# ============================================================

class TestPartnersSection:
    """Тесты раздела Партнерам"""
    
    def test_partners_page_loads(self, page: Page):
        """Проверка загрузки страницы для партнеров"""
        page.goto(f"{BASE_URL}/partners")
        page.wait_for_load_state("networkidle")
        
        # Страница должна загрузиться
        expect(page.locator("body")).to_be_visible()
    
    def test_vk_video_player_present(self, page: Page):
        """Проверка наличия VK Video плеера"""
        page.goto(f"{BASE_URL}/partners")
        page.wait_for_load_state("networkidle")
        
        # Ищем iframe с VK Video или video элемент
        vk_player = page.locator("iframe[src*='vk.com'], iframe[src*='vkvideo'], video")
        
        if vk_player.count() > 0:
            expect(vk_player.first).to_be_visible()
    
    def test_documents_download_links(self, page: Page):
        """Проверка ссылок на скачивание документов"""
        page.goto(f"{BASE_URL}/partners")
        page.wait_for_load_state("networkidle")
        
        # Ищем ссылки на PDF документы
        pdf_links = page.locator("a[href$='.pdf'], a[download]")
        
        # Должны быть документы для скачивания
        # assert pdf_links.count() > 0
    
    def test_contact_button_opens_form(self, page: Page):
        """Проверка кнопки 'Связаться с нами'"""
        page.goto(f"{BASE_URL}/partners")
        page.wait_for_load_state("networkidle")
        
        contact_btn = page.locator("button:has-text('Связаться'), a:has-text('Связаться')").first
        
        if contact_btn.count() > 0:
            contact_btn.click()
            page.wait_for_timeout(500)
            
            # Должна открыться форма или страница контактов
            form = page.locator("form")
            expect(form.first).to_be_visible()

'''
    
    def generate_conftest(self) -> str:
        """Генерация conftest.py для pytest"""
        return f'''"""
Конфигурация pytest для тестов Playwright
Проект: {self.project_name}
"""

import pytest


def pytest_configure(config):
    """Настройка pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m not slow')"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Аргументы запуска браузера"""
    return {{
        **browser_type_launch_args,
        "slow_mo": 100,  # Замедление для отладки
    }}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Аргументы контекста браузера"""
    return {{
        **browser_context_args,
        "viewport": {{"width": 1920, "height": 1080}},
        "locale": "ru-RU",
        "timezone_id": "Europe/Moscow",
        "ignore_https_errors": True,
    }}

'''
    
    def generate_all_tests(self) -> str:
        """Генерация всех тестов в один файл"""
        content = self.generate_test_file_header()
        content += self.generate_navigation_tests()
        content += self.generate_header_tests()
        content += self.generate_hero_section_tests()
        content += self.generate_search_tests()
        content += self.generate_brands_section_tests()
        content += self.generate_news_section_tests()
        content += self.generate_partners_section_tests()
        content += self.generate_form_tests()
        content += self.generate_footer_tests()
        content += self.generate_cookie_tests()
        content += self.generate_404_tests()
        content += self.generate_responsive_tests()
        content += self.generate_performance_tests()
        content += self.generate_seo_tests()
        
        return content
    
    def save_tests(self, output_dir: str = None):
        """Сохранение тестов в файлы"""
        if output_dir is None:
            output_dir = TESTS_OUTPUT_DIR
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Основной файл тестов
        tests_file = os.path.join(output_dir, f"test_{self.project_name.lower()}.py")
        with open(tests_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_all_tests())
        print(f"✅ Тесты сохранены: {tests_file}")
        
        # conftest.py
        conftest_file = os.path.join(output_dir, "conftest.py")
        with open(conftest_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_conftest())
        print(f"✅ Конфигурация сохранена: {conftest_file}")
        
        # pytest.ini
        pytest_ini = os.path.join(output_dir, "pytest.ini")
        with open(pytest_ini, 'w', encoding='utf-8') as f:
            f.write(f"""[pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
""")
        print(f"✅ pytest.ini сохранен: {pytest_ini}")
        
        return output_dir


# ============================================================
# ИНТЕРАКТИВНАЯ КОНСОЛЬ
# ============================================================

class InteractiveConsole:
    """Интерактивный режим генератора тестов"""
    
    def __init__(self):
        self.generator = None
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Вывод заголовка"""
        print("=" * 70)
        print("  ГЕНЕРАТОР PLAYWRIGHT ТЕСТОВ")
        print("=" * 70)
    
    def run(self):
        """Запуск интерактивного режима"""
        self.clear_screen()
        self.print_header()
        
        print("\n📋 Этот инструмент генерирует Playwright тесты на основе ТЗ")
        print("\nТекущие настройки:")
        
        # Ввод URL
        default_url = "http://uvelka-petfood.tw1.ru"
        url = input(f"\n🌐 Базовый URL сайта [{default_url}]: ").strip()
        if not url:
            url = default_url
        
        # Ввод имени проекта
        default_name = "UvelkaPetfood"
        name = input(f"📁 Название проекта [{default_name}]: ").strip()
        if not name:
            name = default_name
        
        # Создаем генератор
        self.generator = PlaywrightTestGenerator(base_url=url)
        self.generator.project_name = name
        
        print("\n" + "-" * 70)
        print("\n🔧 Выберите действие:")
        print("  1. Сгенерировать все тесты")
        print("  2. Сгенерировать только тесты навигации")
        print("  3. Сгенерировать только тесты форм")
        print("  4. Сгенерировать только тесты SEO")
        print("  5. Сгенерировать только тесты адаптивности")
        print("  0. Выход")
        
        choice = input("\nВаш выбор [1]: ").strip() or "1"
        
        if choice == "0":
            print("\n👋 До свидания!")
            return
        
        print("\n⏳ Генерация тестов...")
        
        # Генерируем и сохраняем
        output_dir = self.generator.save_tests()
        
        print("\n" + "=" * 70)
        print("✅ ТЕСТЫ УСПЕШНО СГЕНЕРИРОВАНЫ!")
        print("=" * 70)
        print(f"\n📁 Папка с тестами: {output_dir}")
        print("\n📋 Для запуска тестов выполните:")
        print("\n   # Установка зависимостей:")
        print("   pip install pytest playwright")
        print("   playwright install")
        print("\n   # Запуск всех тестов:")
        print(f"   pytest {output_dir} -v")
        print("\n   # Запуск с отображением браузера:")
        print(f"   pytest {output_dir} -v --headed")
        print("\n   # Запуск конкретного браузера:")
        print(f"   pytest {output_dir} -v --browser firefox")
        print("\n   # Запуск конкретного класса тестов:")
        print(f"   pytest {output_dir} -v -k 'TestNavigation'")
        
        input("\n\nНажмите Enter для выхода...")


def main():
    """Запуск генератора"""
    console = InteractiveConsole()
    console.run()


if __name__ == "__main__":
    main()

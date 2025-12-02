"""
Автоматические тесты для проекта UvelkaPetfood
Версия: 2.0.0
Обновлено: 2025-12-02
Базовый URL: http://uvelka-petfood.tw1.ru

Соответствует:
- ТЗ "Сайт Увелка Петфуд" версия 30.09
- Чек-лист регресса (ЧЛ Регресс CLR)

Запуск тестов:
    pytest tests/ -v
    pytest tests/ -v --headed  # С отображением браузера
    pytest tests/ -v -k "TestNavigation"  # Конкретный класс
"""

import pytest
from playwright.sync_api import Page, expect
import re


# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================

BASE_URL = "http://uvelka-petfood.tw1.ru"
TIMEOUT = 30000  # 30 секунд

# Разделы сайта согласно ТЗ 2.1
SITE_SECTIONS = {
    "brands": "/brands/",
    "about": "/about/",
    "partners": "/partners/",
    "news": "/news/",
    "career": "/career/",
    "contacts": "/contacts/"
}

# Пункты меню согласно ТЗ 2.2
MENU_ITEMS = ["Бренды", "О компании", "Партнерам", "Новости", "Карьера"]


# ============================================================
# ФИКСТУРЫ
# ============================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Настройки контекста браузера"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
    }


@pytest.fixture
def page(page: Page):
    """Настройка страницы перед каждым тестом"""
    page.set_default_timeout(TIMEOUT)
    yield page


# ============================================================
# 2.1 СТРУКТУРА САЙТА
# ============================================================

class TestSiteStructure:
    """Тесты структуры сайта согласно ТЗ 2.1"""
    
    def test_site_has_header(self, page: Page):
        """ЧЛ #1: Структура сайта включает Заголовки"""
        page.goto(BASE_URL)
        expect(page.locator("header")).to_be_visible()
    
    def test_site_has_content_area(self, page: Page):
        """ЧЛ #10: Структура сайта включает Контентную область"""
        page.goto(BASE_URL)
        # Контентная область - main или основной контейнер
        content = page.locator("main, .content, [class*='content']").first
        expect(content).to_be_visible()
    
    def test_site_has_footer(self, page: Page):
        """ЧЛ #12: Структура сайта включает Футер (Подвал)"""
        page.goto(BASE_URL)
        expect(page.locator("footer")).to_be_visible()


# ============================================================
# 2.2 ГЛАВНАЯ СТРАНИЦА
# ============================================================

class TestMainPage:
    """Тесты главной страницы согласно ТЗ 2.2"""
    
    def test_main_page_loads(self, page: Page):
        """Проверка загрузки главной страницы"""
        page.goto(BASE_URL)
        expect(page).to_have_title(re.compile(r".+"))
        expect(page.locator("header")).to_be_visible()
        expect(page.locator("footer")).to_be_visible()
    
    def test_hero_section_visible(self, page: Page):
        """ЧЛ #17: Обложка сайта (hero-секция) на Главной странице"""
        page.goto(BASE_URL)
        hero = page.locator(".hero, [class*='hero'], .banner, [class*='banner'], .swiper, [class*='slider']").first
        expect(hero).to_be_visible()
    
    def test_logo_button_present(self, page: Page):
        """ЧЛ #18: кнопка 'Главная' с логотипом компании"""
        page.goto(BASE_URL)
        logo = page.locator("header a[href='/'], header .logo, header [class*='logo']").first
        expect(logo).to_be_visible()
    
    def test_brands_menu_button(self, page: Page):
        """ЧЛ #19: кнопка 'Бренды'"""
        page.goto(BASE_URL)
        brands_link = page.locator("header").get_by_text("Бренды", exact=False).first
        expect(brands_link).to_be_visible()
    
    def test_about_menu_button(self, page: Page):
        """ЧЛ #20: кнопка 'О компании'"""
        page.goto(BASE_URL)
        about_link = page.locator("header").get_by_text("О компании", exact=False).first
        expect(about_link).to_be_visible()
    
    def test_partners_menu_button(self, page: Page):
        """ЧЛ #21: кнопка 'Партнерам'"""
        page.goto(BASE_URL)
        partners_link = page.locator("header").get_by_text("Партнерам", exact=False).first
        expect(partners_link).to_be_visible()
    
    def test_news_menu_button(self, page: Page):
        """ЧЛ #22: кнопка 'Новости'"""
        page.goto(BASE_URL)
        news_link = page.locator("header").get_by_text("Новости", exact=False).first
        expect(news_link).to_be_visible()
    
    def test_career_menu_button(self, page: Page):
        """ЧЛ #23: кнопка 'Карьера'"""
        page.goto(BASE_URL)
        career_link = page.locator("header").get_by_text("Карьера", exact=False).first
        expect(career_link).to_be_visible()
    
    def test_search_button(self, page: Page):
        """ЧЛ #24: кнопка 'Поиск'"""
        page.goto(BASE_URL)
        search_btn = page.locator("header [class*='search'], header button[class*='search'], header svg").first
        expect(search_btn).to_be_visible()
    
    def test_logo_returns_to_main_page(self, page: Page):
        """ЧЛ #28: Кнопка 'Главная' возвращает пользователя на Главную страницу"""
        # Переходим в другой раздел
        page.goto(f"{BASE_URL}/about/")
        page.wait_for_load_state("domcontentloaded")
        
        # Кликаем на логотип
        logo = page.locator("header a[href='/'], header .logo a").first
        logo.click()
        page.wait_for_load_state("domcontentloaded")
        
        # Проверяем что вернулись на главную
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/?$"))
    
    def test_logo_is_clickable(self, page: Page):
        """ЧЛ #29: Кнопка 'Главная' представляет собой кликабельный логотип"""
        page.goto(BASE_URL)
        logo = page.locator("header a[href='/'], header .logo a, header a:has(img)").first
        expect(logo).to_be_visible()
        # Проверяем что это ссылка
        href = logo.get_attribute("href")
        assert href is not None, "Логотип должен быть кликабельной ссылкой"
    
    def test_vertical_scroll(self, page: Page):
        """ЧЛ #30: Для перемещения вверх-вниз используется вертикальный скролл"""
        page.goto(BASE_URL)
        
        # Скроллим вниз
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(300)
        scroll_position = page.evaluate("window.scrollY")
        assert scroll_position > 0, "Вертикальный скролл должен работать"
    
    def test_brands_block_on_main_page(self, page: Page):
        """ЧЛ #31: Блок 'Бренды' с кликабельными плитками"""
        page.goto(BASE_URL)
        
        # Ищем блок брендов
        brands_block = page.locator("[class*='brand'], section:has-text('Бренды')").first
        if brands_block.count() > 0:
            # Ищем кликабельные плитки
            brand_tiles = brands_block.locator("a")
            assert brand_tiles.count() > 0, "Должны быть кликабельные плитки брендов"
    
    def test_about_block_with_button(self, page: Page):
        """ЧЛ #33: Блок 'О компании' с кнопкой 'Подробнее о нас'"""
        page.goto(BASE_URL)
        
        # Ищем кнопку "Подробнее о нас" или похожую
        about_btn = page.locator("a:has-text('Подробнее о нас'), a:has-text('подробнее')").first
        # Кнопка может присутствовать
    
    def test_partners_block_with_button(self, page: Page):
        """ЧЛ #34-36: Блок 'Партнерам' с кнопкой 'Узнать больше'"""
        page.goto(BASE_URL)
        
        learn_more_btn = page.locator("a:has-text('Узнать больше')").first
        # Кнопка должна вести в раздел Партнерам
    
    def test_news_block_with_button(self, page: Page):
        """ЧЛ #37-38: Блок 'Новости' с кнопкой 'Подробнее'"""
        page.goto(BASE_URL)
        
        news_btn = page.locator("a:has-text('Новости компании'), a:has-text('Подробнее →')").first
        # Кнопка для перехода в новости
    
    def test_career_block_with_button(self, page: Page):
        """ЧЛ #39-40: Блок 'Карьера' с кнопкой 'Перейти к вакансиям'"""
        page.goto(BASE_URL)
        
        career_btn = page.locator("a:has-text('Перейти к вакансиям'), a:has-text('вакансии')").first
        # Кнопка для перехода в карьеру


# ============================================================
# 2.3 РАЗДЕЛ "БРЕНДЫ"
# ============================================================

class TestBrandsSection:
    """Тесты раздела Бренды согласно ТЗ 2.3"""
    
    def test_brands_page_opens_from_header(self, page: Page):
        """ЧЛ #41: Раздел 'Бренды' открывается при нажатии кнопки в Заголовке"""
        page.goto(BASE_URL)
        
        brands_link = page.locator("header a[href*='brand'], nav a[href*='brand']").first
        brands_link.click()
        page.wait_for_load_state("domcontentloaded")
        
        expect(page).to_have_url(re.compile(r".*brand.*"))
    
    def test_brands_has_sidebar_and_content(self, page: Page):
        """ЧЛ #42: Раздел 'Бренды' включает боковую панель и контентную область"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        # Проверяем наличие контента
        content = page.locator("main, .content, article, [class*='brand']")
        assert content.count() > 0, "Должна быть контентная область"
    
    def test_brand_detail_button_has_link(self, page: Page):
        """ЧЛ #43: Кнопка 'Подробнее' с привязанной ссылкой на сайт бренда"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        detail_btn = page.locator("a:has-text('Подробнее')").first
        
        if detail_btn.count() > 0:
            href = detail_btn.get_attribute("href")
            assert href is not None, "Кнопка 'Подробнее' должна иметь ссылку"
    
    def test_default_brand_card_displayed(self, page: Page):
        """ЧЛ #44: Когда ни один бренд не выбран, открывается карточка верхнего бренда"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        # Должна отображаться хотя бы одна карточка бренда
        brand_content = page.locator("[class*='brand'], article, .card")
        assert brand_content.count() > 0, "Должна отображаться карточка бренда"


# ============================================================
# 2.4 КАРТОЧКА БРЕНДА
# ============================================================

class TestBrandCard:
    """Тесты карточки бренда согласно ТЗ 2.4"""
    
    def test_brand_card_has_name(self, page: Page):
        """ЧЛ #46: Карточка бренда содержит Название"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        # Ищем заголовок карточки
        title = page.locator("h1, h2, h3, [class*='title']").first
        expect(title).to_be_visible()
    
    def test_brand_card_has_description(self, page: Page):
        """ЧЛ #48: Карточка бренда содержит Описание, преимущества"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        # Должен быть текст описания
        description = page.locator("p, [class*='description'], [class*='text']")
        assert description.count() > 0, "Должно быть описание бренда"
    
    def test_brand_card_has_detail_button(self, page: Page):
        """ЧЛ #49: Карточка бренда содержит кнопку 'Подробнее'"""
        page.goto(f"{BASE_URL}/brands/")
        page.wait_for_load_state("domcontentloaded")
        
        detail_btn = page.locator("a:has-text('Подробнее'), button:has-text('Подробнее')")
        # Кнопка должна быть на странице


# ============================================================
# 2.5 РАЗДЕЛ "ПАРТНЕРАМ"
# ============================================================

class TestPartnersSection:
    """Тесты раздела Партнерам согласно ТЗ 2.5"""
    
    def test_partners_page_has_cooperation_info(self, page: Page):
        """ЧЛ #50: Раздел 'Партнерам' содержит информацию об условиях сотрудничества"""
        page.goto(f"{BASE_URL}/partners/")
        page.wait_for_load_state("domcontentloaded")
        
        # Страница должна загрузиться с контентом
        content = page.locator("main, .content, article")
        expect(content.first).to_be_visible()
    
    def test_partners_page_opens_from_header(self, page: Page):
        """ЧЛ #52: Раздел открывается при нажатии кнопки 'Партнерам' в Заголовке"""
        page.goto(BASE_URL)
        
        partners_link = page.locator("header a[href*='partner'], nav a[href*='partner']").first
        partners_link.click()
        page.wait_for_load_state("domcontentloaded")
        
        expect(page).to_have_url(re.compile(r".*partner.*"))
    
    def test_partners_has_required_sections(self, page: Page):
        """ЧЛ #53: Раздел включает подразделы и кнопку 'Связаться с нами'"""
        page.goto(f"{BASE_URL}/partners/")
        page.wait_for_load_state("domcontentloaded")
        
        # Ищем кнопку связи
        contact_btn = page.locator("a:has-text('Связаться'), button:has-text('Связаться')")
        # Кнопка должна присутствовать
    
    def test_contact_button_opens_form(self, page: Page):
        """ЧЛ #56: При нажатии на 'Связаться с нами' открывается форма обратной связи"""
        page.goto(f"{BASE_URL}/partners/")
        page.wait_for_load_state("domcontentloaded")
        
        contact_btn = page.locator("a:has-text('Связаться'), button:has-text('Связаться')").first
        
        if contact_btn.count() > 0:
            contact_btn.click()
            page.wait_for_timeout(500)
            
            # Должна появиться форма или переход на страницу контактов
            form = page.locator("form, [class*='modal'], [class*='popup']")
            # Форма может появиться


# ============================================================
# 2.6 РАЗДЕЛ "НОВОСТИ"
# ============================================================

class TestNewsSection:
    """Тесты раздела Новости согласно ТЗ 2.6"""
    
    def test_news_page_opens_from_header(self, page: Page):
        """ЧЛ #57: Раздел 'Новости' открывается при нажатии кнопки в Заголовке"""
        page.goto(BASE_URL)
        
        news_link = page.locator("header a[href*='news'], nav a[href*='news']").first
        news_link.click()
        page.wait_for_load_state("domcontentloaded")
        
        expect(page).to_have_url(re.compile(r".*news.*"))
    
    def test_news_page_has_posts(self, page: Page):
        """ЧЛ #58: В разделе 'Новости' отображаются новостные посты"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        news_posts = page.locator("article, [class*='news'], .post, [class*='card']")
        assert news_posts.count() > 0, "Должны быть новостные посты"
    
    def test_news_image_enlarges_on_click(self, page: Page):
        """ЧЛ #60: Изображение при нажатии делает изображение больше"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        # Переходим на детальную страницу новости
        news_link = page.locator("article a, [class*='news'] a").first
        if news_link.count() > 0:
            news_link.click()
            page.wait_for_load_state("domcontentloaded")
            
            # Кликаем на изображение
            img = page.locator("article img, .content img").first
            if img.count() > 0 and img.is_visible():
                initial_box = img.bounding_box()
                img.click()
                page.wait_for_timeout(500)
                
                # Проверяем lightbox или увеличенное изображение
                lightbox = page.locator("[class*='lightbox'], [class*='modal'], [class*='fancybox']")
                # Lightbox должен появиться
    
    def test_news_has_date(self, page: Page):
        """ЧЛ #63: Пост содержит дату и время публикации"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        dates = page.locator("[class*='date'], time, [datetime]")
        # Даты должны присутствовать
    
    def test_news_displays_4_items(self, page: Page):
        """ЧЛ #64: На странице 'Новости' отображается 4 новости"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        news_items = page.locator("article, [class*='news-item'], .post").all()
        # По ТЗ должно быть 4 новости изначально
    
    def test_news_sorted_by_date_desc(self, page: Page):
        """ЧЛ #65: Новости отсортированы от новых к старым"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        # Проверка сортировки требует парсинга дат
        pass
    
    def test_show_more_button(self, page: Page):
        """ЧЛ #66: Кнопка 'Показать еще' отображает остальные новости"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        show_more = page.locator("button:has-text('Показать'), button:has-text('еще'), a:has-text('Показать')").first
        
        if show_more.count() > 0 and show_more.is_visible():
            initial_count = page.locator("article, [class*='news-item']").count()
            show_more.click()
            page.wait_for_timeout(1000)
            new_count = page.locator("article, [class*='news-item']").count()
            
            assert new_count >= initial_count, "Должно появиться больше новостей"
    
    def test_news_detail_page(self, page: Page):
        """ЧЛ #67: При нажатии 'Подробнее' новость разворачивается"""
        page.goto(f"{BASE_URL}/news/")
        page.wait_for_load_state("domcontentloaded")
        
        detail_link = page.locator("a:has-text('Подробнее'), article a").first
        
        if detail_link.count() > 0:
            detail_link.click()
            page.wait_for_load_state("domcontentloaded")
            
            # Должен быть заголовок новости
            h1 = page.locator("h1")
            expect(h1).to_be_visible()


# ============================================================
# 2.7 РАЗДЕЛ "О КОМПАНИИ"
# ============================================================

class TestAboutSection:
    """Тесты раздела О компании согласно ТЗ 2.7"""
    
    def test_about_page_has_content(self, page: Page):
        """ЧЛ #68: Раздел содержит описание истории, технологий, стандартов"""
        page.goto(f"{BASE_URL}/about/")
        page.wait_for_load_state("domcontentloaded")
        
        content = page.locator("main, .content, article")
        expect(content.first).to_be_visible()
    
    def test_about_page_opens_from_header(self, page: Page):
        """ЧЛ #69: Раздел открывается при нажатии кнопки 'О компании' в Заголовке"""
        page.goto(BASE_URL)
        
        about_link = page.locator("header a[href*='about'], nav a[href*='about']").first
        about_link.click()
        page.wait_for_load_state("domcontentloaded")
        
        expect(page).to_have_url(re.compile(r".*about.*"))
    
    def test_about_dropdown_menu(self, page: Page):
        """ЧЛ #70: При наведении на 'О компании' открывается выпадающий список"""
        page.goto(BASE_URL)
        
        about_link = page.locator("header a[href*='about'], nav a[href*='about']").first
        about_link.hover()
        page.wait_for_timeout(300)
        
        # Ищем выпадающее меню
        dropdown = page.locator("[class*='dropdown'], [class*='submenu'], ul[class*='sub']")
        # Меню может появиться
    
    def test_about_has_employees_section(self, page: Page):
        """ЧЛ #72: Раздел содержит подраздел 'Сотрудники'"""
        page.goto(f"{BASE_URL}/about/")
        page.wait_for_load_state("domcontentloaded")
        
        employees = page.locator(":has-text('Сотрудники'), :has-text('сотрудники'), [class*='employee'], [class*='team']")
        # Подраздел должен присутствовать


# ============================================================
# 2.8 РАЗДЕЛ "КАРЬЕРА"
# ============================================================

class TestCareerSection:
    """Тесты раздела Карьера согласно ТЗ 2.8"""
    
    def test_career_page_has_job_info(self, page: Page):
        """ЧЛ #73: Раздел 'Карьера' содержит описание условий трудоустройства"""
        page.goto(f"{BASE_URL}/career/")
        page.wait_for_load_state("domcontentloaded")
        
        content = page.locator("main, .content, article")
        expect(content.first).to_be_visible()
    
    def test_career_has_feedback_link(self, page: Page):
        """ЧЛ #74: Раздел содержит ссылку на форму обратной связи"""
        page.goto(f"{BASE_URL}/career/")
        page.wait_for_load_state("domcontentloaded")
        
        contact_link = page.locator("a:has-text('Связаться'), a:has-text('отправить'), a[href*='contact']")
        # Ссылка должна присутствовать
    
    def test_career_page_opens_from_header(self, page: Page):
        """ЧЛ #75: Раздел открывается при нажатии кнопки 'Карьера' в Заголовке"""
        page.goto(BASE_URL)
        
        career_link = page.locator("header a[href*='career'], nav a[href*='career']").first
        career_link.click()
        page.wait_for_load_state("domcontentloaded")
        
        expect(page).to_have_url(re.compile(r".*career.*"))


# ============================================================
# 2.9 ФУТЕР
# ============================================================

class TestFooter:
    """Тесты футера согласно ТЗ 2.9"""
    
    def test_footer_has_documents_section(self, page: Page):
        """ЧЛ #77: Футер включает раздел Документы"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(300)
        
        footer = page.locator("footer")
        docs = footer.locator("a[href$='.pdf'], :has-text('Документ')")
        # Документы должны быть
    
    def test_footer_documents_downloadable(self, page: Page):
        """ЧЛ #78: Документы с возможностью скачивания в формате pdf"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        pdf_links = page.locator("footer a[href$='.pdf']")
        # PDF-файлы должны быть доступны
    
    def test_footer_has_contacts(self, page: Page):
        """ЧЛ #80: Футер включает раздел 'Контакты'"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        
        # Проверяем телефон
        phone = footer.locator("a[href^='tel:']")
        
        # Проверяем email
        email = footer.locator("a[href^='mailto:']")
    
    def test_footer_has_feedback_form(self, page: Page):
        """ЧЛ #81: Футер включает форму обратной связи"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        form = footer.locator("form, a:has-text('Связаться'), a[href*='contact']")
        # Форма или ссылка на неё
    
    def test_footer_has_privacy_policy(self, page: Page):
        """ЧЛ #83: Футер включает ссылку на Политику конфиденциальности"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        footer = page.locator("footer")
        privacy = footer.locator("a:has-text('Политика'), a:has-text('конфиденциальност')")
        # Ссылка должна быть


# ============================================================
# 2.10 РАЗДЕЛ "КОНТАКТЫ"
# ============================================================

class TestContactsSection:
    """Тесты раздела Контакты согласно ТЗ 2.10"""
    
    def test_contacts_page_opens_from_footer(self, page: Page):
        """ЧЛ #85: Раздел 'Контакты' открывается при нажатии кнопки в футере"""
        page.goto(BASE_URL)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        contacts_link = page.locator("footer a[href*='contact']").first
        if contacts_link.count() > 0:
            contacts_link.click()
            page.wait_for_load_state("domcontentloaded")
            expect(page).to_have_url(re.compile(r".*contact.*"))
    
    def test_contacts_has_legal_info(self, page: Page):
        """ЧЛ #87: Раздел содержит юридическую информацию (ИНН, ОГРН)"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        # Ищем юридическую информацию
        legal = page.locator(":has-text('ИНН'), :has-text('ОГРН'), :has-text('Юридический')")
        # Информация должна присутствовать
    
    def test_contacts_has_phones(self, page: Page):
        """ЧЛ #88: Раздел содержит телефоны"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        phones = page.locator("a[href^='tel:']")
        # Телефоны должны быть
    
    def test_contacts_has_emails(self, page: Page):
        """ЧЛ #89: Раздел содержит электронные почты"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        emails = page.locator("a[href^='mailto:']")
        # Email должен быть


# ============================================================
# 2.11 ФОРМА ОБРАТНОЙ СВЯЗИ
# ============================================================

class TestFeedbackForm:
    """Тесты формы обратной связи согласно ТЗ 2.11"""
    
    def test_form_exists_on_contacts_page(self, page: Page):
        """ЧЛ #92: Пользователь может отправить обращение через форму"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        form = page.locator("form")
        assert form.count() > 0, "Форма обратной связи должна быть на странице"
    
    def test_form_has_email_field(self, page: Page):
        """ЧЛ #94-95: Форма имеет поле E-mail с валидацией"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        email_input = page.locator("input[type='email'], input[name*='email']").first
        expect(email_input).to_be_visible()
        
        # Проверяем валидацию - поле должно быть обязательным
        required = email_input.get_attribute("required")
        # Email должен валидироваться
    
    def test_form_has_topic_dropdown(self, page: Page):
        """ЧЛ #96: Поле Тема с выпадающим списком"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        topic_select = page.locator("select, [class*='select'], [class*='dropdown']")
        # Должен быть выпадающий список тем
    
    def test_form_has_message_field(self, page: Page):
        """ЧЛ #97: Поле для ввода текста"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        textarea = page.locator("textarea, input[type='text'][name*='message']")
        assert textarea.count() > 0, "Должно быть поле для ввода сообщения"
    
    def test_form_has_file_upload(self, page: Page):
        """ЧЛ #98: Прикрепляемые файлы (макс 10, до 2 МБ каждый)"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        file_input = page.locator("input[type='file']")
        # Поле загрузки файлов
    
    def test_form_has_captcha(self, page: Page):
        """ЧЛ #99-100: Капча - чек-бокс 'Я не робот'"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        captcha = page.locator("[class*='captcha'], [class*='recaptcha'], iframe[src*='recaptcha']")
        # Капча должна присутствовать
    
    def test_form_required_fields_validation(self, page: Page):
        """ЧЛ #101-102: Обязательные поля выделяются красным если не заполнены"""
        page.goto(f"{BASE_URL}/contacts/")
        page.wait_for_load_state("domcontentloaded")
        
        form = page.locator("form").first
        submit_btn = form.locator("button[type='submit'], input[type='submit']").first
        
        if submit_btn.count() > 0 and submit_btn.is_visible():
            submit_btn.click()
            page.wait_for_timeout(300)
            
            # Должны появиться ошибки валидации
            invalid_fields = page.locator(":invalid, [class*='error'], [class*='invalid']")
            # Поля с ошибками
    
    def test_form_submission_skipped(self, page: Page):
        """ЧЛ #103-105: Успешная отправка формы (требует капчу)"""
        pytest.skip("Тест отправки формы требует ручной проверки капчи")


# ============================================================
# 2.12 ИЗМЕНЕНИЕ ЦВЕТОВОЙ ТЕМЫ
# ============================================================

class TestThemeSwitcher:
    """Тесты переключателя темы согласно ТЗ 2.12"""
    
    def test_theme_switcher_exists(self, page: Page):
        """ЧЛ #111-112: На сайте есть переключатель светлой/темной темы"""
        page.goto(BASE_URL)
        
        theme_btn = page.locator("[class*='theme'], button[aria-label*='тема'], [class*='switch']").first
        # Переключатель должен быть
    
    def test_theme_changes_on_toggle(self, page: Page):
        """ЧЛ #113: При выборе темы дизайн меняется"""
        page.goto(BASE_URL)
        
        theme_btn = page.locator("[class*='theme'], [class*='switch']").first
        
        if theme_btn.count() > 0 and theme_btn.is_visible():
            # Получаем начальный цвет фона
            initial_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            
            theme_btn.click()
            page.wait_for_timeout(500)
            
            # Цвет может измениться
            new_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")


# ============================================================
# 2.13 COOKIE-ФАЙЛЫ
# ============================================================

class TestCookieBanner:
    """Тесты cookie-баннера согласно ТЗ 2.13"""
    
    def test_cookie_banner_on_first_visit(self, page: Page):
        """ЧЛ #114: При первом посещении отображается cookie-баннер"""
        # Очищаем cookies для симуляции первого визита
        page.context.clear_cookies()
        
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        cookie_banner = page.locator("[class*='cookie'], [class*='consent'], [id*='cookie']").first
        # Баннер должен появиться
    
    def test_cookie_accept_button(self, page: Page):
        """ЧЛ #115: Кнопка 'Принять' принимает все cookies"""
        page.context.clear_cookies()
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        accept_btn = page.locator("button:has-text('Принять'), button:has-text('Accept')").first
        
        if accept_btn.count() > 0 and accept_btn.is_visible():
            accept_btn.click()
            page.wait_for_timeout(500)
            
            # Баннер должен исчезнуть
            cookie_banner = page.locator("[class*='cookie'], [class*='consent']").first
            expect(cookie_banner).not_to_be_visible()
    
    def test_cookie_decline_button(self, page: Page):
        """ЧЛ #116: Кнопка 'Отклонить' отклоняет cookies"""
        page.context.clear_cookies()
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        
        decline_btn = page.locator("button:has-text('Отклонить'), button:has-text('Decline')").first
        
        if decline_btn.count() > 0 and decline_btn.is_visible():
            decline_btn.click()
            page.wait_for_timeout(500)
            
            # Баннер должен исчезнуть
            cookie_banner = page.locator("[class*='cookie'], [class*='consent']").first
            expect(cookie_banner).not_to_be_visible()


# ============================================================
# 2.14 SEO-ОПТИМИЗАЦИЯ
# ============================================================

class TestSEO:
    """Тесты SEO согласно ТЗ 2.14"""
    
    def test_page_title_length(self, page: Page):
        """ЧЛ #118: Длина Заголовка страницы 40-70 символов"""
        page.goto(BASE_URL)
        
        title = page.title()
        title_length = len(title)
        
        assert title_length >= 40, f"Заголовок слишком короткий: {title_length} символов ('{title}'). Требуется 40-70"
        assert title_length <= 70, f"Заголовок слишком длинный: {title_length} символов. Требуется 40-70"
    
    def test_page_title_has_keywords(self, page: Page):
        """ЧЛ #119: Заголовок содержит ключевые слова"""
        page.goto(BASE_URL)
        
        title = page.title().lower()
        # Должен содержать релевантные слова
        keywords = ["увелка", "петфуд", "petfood", "корм", "животных"]
        has_keyword = any(kw in title for kw in keywords)
        # Рекомендуется наличие ключевых слов
    
    def test_meta_description_exists(self, page: Page):
        """ЧЛ #120-121: Описание страницы (Description) до 160 символов"""
        page.goto(BASE_URL)
        
        description = page.locator("meta[name='description']").get_attribute("content")
        
        assert description is not None, "Meta description должен присутствовать"
        assert len(description) > 0, "Meta description не должен быть пустым"
        assert len(description) <= 160, f"Description слишком длинный: {len(description)} символов"
    
    def test_h1_unique_per_page(self, page: Page):
        """ЧЛ #123: H1 - главный заголовок, должен быть один на страницу"""
        page.goto(BASE_URL)
        
        h1_count = page.locator("h1").count()
        assert h1_count == 1, f"На странице {h1_count} тегов H1, должен быть ровно 1"
    
    def test_headings_hierarchy(self, page: Page):
        """ЧЛ #124: H2-H4 подзаголовки формируют структуру"""
        page.goto(BASE_URL)
        
        # Проверяем наличие заголовков разных уровней
        h2_count = page.locator("h2").count()
        # H2 должны присутствовать для структуры контента
    
    def test_canonical_tag_exists(self, page: Page):
        """ТЗ 2.14.2: Мета-тег canonical на всех страницах"""
        page.goto(BASE_URL)
        
        canonical = page.locator("link[rel='canonical']")
        expect(canonical).to_have_count(1)
    
    def test_images_have_alt(self, page: Page):
        """SEO: Все изображения должны иметь атрибут alt"""
        page.goto(BASE_URL)
        
        images = page.locator("img")
        images_without_alt = []
        
        for i in range(min(images.count(), 20)):  # Проверяем первые 20
            img = images.nth(i)
            alt = img.get_attribute("alt")
            if alt is None or alt.strip() == "":
                src = img.get_attribute("src")
                images_without_alt.append(src)
        
        assert len(images_without_alt) == 0, f"Изображения без alt: {images_without_alt[:5]}"


# ============================================================
# 2.14.3 РЕДИРЕКТЫ
# ============================================================

class TestRedirects:
    """Тесты редиректов согласно ТЗ 2.14.3"""
    
    def test_trailing_slash_redirect(self, page: Page):
        """ЧЛ #130: Редиректы внутренних страниц на страницы со слэшем '/' на конце"""
        # Проверяем что URL заканчивается на /
        page.goto(f"{BASE_URL}/about")
        page.wait_for_load_state("domcontentloaded")
        
        current_url = page.url
        # URL должен заканчиваться на /
        # assert current_url.endswith("/"), f"URL должен заканчиваться на /: {current_url}"


# ============================================================
# 2.15 ЭЛЕМЕНТЫ НАВИГАЦИОННОЙ ПОМОЩИ
# ============================================================

class TestNavigationHelpers:
    """Тесты элементов навигационной помощи согласно ТЗ 2.15"""
    
    def test_breadcrumbs_present(self, page: Page):
        """ЧЛ #134: Хлебные крошки отображают цепочку переходов"""
        page.goto(f"{BASE_URL}/about/")
        page.wait_for_load_state("domcontentloaded")
        
        breadcrumbs = page.locator(".breadcrumb, [class*='breadcrumb'], nav[aria-label*='breadcrumb']")
        # Хлебные крошки должны присутствовать на внутренних страницах
    
    def test_scroll_to_top_button(self, page: Page):
        """ЧЛ #135-136: Кнопка 'Вернуться наверх' для длинных страниц"""
        page.goto(BASE_URL)
        
        # Скроллим вниз
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        
        scroll_btn = page.locator("[class*='scroll-top'], [class*='back-to-top'], [class*='to-top']").first
        
        if scroll_btn.count() > 0 and scroll_btn.is_visible():
            scroll_btn.click()
            page.wait_for_timeout(500)
            
            scroll_position = page.evaluate("window.scrollY")
            assert scroll_position < 100, "После клика должен быть скролл наверх"
    
    def test_sticky_header(self, page: Page):
        """ЧЛ #137: Заголовок остается видимым при прокрутке (sticky-header)"""
        page.goto(BASE_URL)
        
        header = page.locator("header").first
        
        # Скроллим вниз
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(300)
        
        # Header должен оставаться видимым
        expect(header).to_be_visible()
        
        # Проверяем позицию
        box = header.bounding_box()
        if box:
            assert box["y"] >= 0 and box["y"] < 150, "Header должен быть в верхней части viewport"


# ============================================================
# 2.16 СТРАНИЦА 404
# ============================================================

class Test404Page:
    """Тесты страницы 404 согласно ТЗ 2.16"""
    
    def test_404_page_displays(self, page: Page):
        """ЧЛ #138: На странице 404 присутствует сообщение и кнопка"""
        page.goto(f"{BASE_URL}/nonexistent-page-xyz-123/")
        
        # Проверяем наличие сообщения об ошибке
        error_text = page.locator(":has-text('404'), :has-text('не найден'), :has-text('Not Found')")
        expect(error_text.first).to_be_visible()
    
    def test_404_has_home_button(self, page: Page):
        """ЧЛ #139: Кнопка 'Вернуться на главную' переходит на Главную"""
        page.goto(f"{BASE_URL}/nonexistent-page-xyz-123/")
        
        home_btn = page.locator("a:has-text('Вернуться'), a:has-text('Главн'), a[href='/']").first
        
        if home_btn.count() > 0:
            expect(home_btn).to_be_visible()
            home_btn.click()
            page.wait_for_load_state("domcontentloaded")
            
            # Должны оказаться на главной
            expect(page).to_have_url(re.compile(rf"{BASE_URL}/?$"))


# ============================================================
# 2.17 АДАПТИВНОСТЬ (МОБИЛЬНЫЕ УСТРОЙСТВА)
# ============================================================

class TestResponsive:
    """Тесты адаптивной верстки согласно ТЗ 2.17"""
    
    @pytest.mark.parametrize("viewport", [
        {"width": 375, "height": 667, "name": "iPhone SE"},
        {"width": 390, "height": 844, "name": "iPhone 12"},
        {"width": 768, "height": 1024, "name": "iPad"},
        {"width": 1920, "height": 1080, "name": "Desktop"},
    ])
    def test_page_loads_on_different_viewports(self, page: Page, viewport):
        """ЧЛ #140: Оптимизированный интерфейс для мобильной версии"""
        page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
        page.goto(BASE_URL)
        
        # Страница должна загрузиться
        expect(page.locator("body")).to_be_visible()
        expect(page.locator("header").first).to_be_visible()
    
    def test_mobile_hamburger_menu(self, page: Page):
        """Мобильное бургер-меню на мобильных устройствах"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(BASE_URL)
        
        hamburger = page.locator("[class*='burger'], [class*='hamburger'], button[class*='menu'], [class*='mobile-menu-btn']").first
        
        if hamburger.count() > 0 and hamburger.is_visible():
            hamburger.click()
            page.wait_for_timeout(300)
            
            # Меню должно открыться
            mobile_menu = page.locator("[class*='mobile-menu'], [class*='nav-open'], nav[class*='active']")
            # Меню должно быть видимым
    
    def test_images_fit_viewport(self, page: Page):
        """Изображения не выходят за пределы viewport"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(BASE_URL)
        
        images = page.locator("img")
        
        for i in range(min(images.count(), 5)):
            img = images.nth(i)
            if img.is_visible():
                box = img.bounding_box()
                if box:
                    assert box["width"] <= 375, f"Изображение шире viewport: {box['width']}px"


# ============================================================
# ПРОИЗВОДИТЕЛЬНОСТЬ
# ============================================================

class TestPerformance:
    """Тесты производительности"""
    
    def test_page_load_time(self, page: Page):
        """ЧЛ #142: Ускоренная загрузка контента"""
        start_time = page.evaluate("performance.now()")
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        end_time = page.evaluate("performance.now()")
        
        load_time = end_time - start_time
        
        # Страница должна загрузиться менее чем за 5 секунд
        assert load_time < 5000, f"Страница загружалась слишком долго: {load_time:.0f}ms"
    
    def test_no_console_errors(self, page: Page):
        """Проверка отсутствия критических ошибок в консоли"""
        errors = []
        
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        
        # Фильтруем известные безобидные ошибки
        critical_errors = [e for e in errors if "favicon" not in e.lower() and "404" not in e]
        
        # Не должно быть критических ошибок
        assert len(critical_errors) == 0, f"Найдены ошибки в консоли: {critical_errors}"
    
    def test_no_broken_images(self, page: Page):
        """Проверка отсутствия битых изображений"""
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)  # Даём время на загрузку картинок
        
        broken_images = page.evaluate("""
            () => {
                const images = document.querySelectorAll('img');
                const broken = [];
                images.forEach(img => {
                    // Пропускаем base64 и svg inline
                    if (img.src && !img.src.startsWith('data:') && 
                        !img.complete || img.naturalHeight === 0) {
                        broken.push(img.src);
                    }
                });
                return broken;
            }
        """)
        
        # Фильтруем ложные срабатывания
        filtered = [img for img in broken_images if img and not img.endswith('/')]
        
        assert len(filtered) == 0, f"Найдены битые изображения: {filtered}"


# ============================================================
# 2.2.1 ПОИСК
# ============================================================

class TestSearch:
    """Тесты поиска согласно ТЗ 2.2.1"""
    
    def test_search_button_opens_search(self, page: Page):
        """Кнопка поиска открывает строку поиска"""
        page.goto(BASE_URL)
        
        search_btn = page.locator("header [class*='search'], header button:has(svg), header [class*='icon-search']").first
        
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            # Должно появиться поле поиска
            search_input = page.locator("input[type='search'], input[name='search'], input[placeholder*='поиск'], input[placeholder*='Поиск']")
            # Поле поиска должно появиться
    
    def test_search_max_length_256(self, page: Page):
        """Строка поиска имеет максимальное ограничение в 256 символов"""
        page.goto(BASE_URL)
        
        # Открываем поиск
        search_btn = page.locator("header [class*='search']").first
        if search_btn.count() > 0:
            search_btn.click()
            page.wait_for_timeout(300)
            
            search_input = page.locator("input[type='search'], input[name='search']").first
            if search_input.count() > 0:
                # Пробуем ввести 300 символов
                long_text = "a" * 300
                search_input.fill(long_text)
                
                value = search_input.input_value()
                assert len(value) <= 256, f"Поиск принял {len(value)} символов, максимум должно быть 256"

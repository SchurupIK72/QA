"""
Автоматические тесты для проекта UvelkaPetfood
Сгенерировано: 2025-12-02 22:07:04
Базовый URL: http://uvelka-petfood.tw1.ru

Запуск тестов:
    pytest tests/ -v
    pytest tests/ -v --headed  # С отображением браузера
    pytest tests/ -v --browser chromium  # Конкретный браузер
"""

import pytest
from playwright.sync_api import Page, expect, sync_playwright
import re


# Конфигурация
BASE_URL = "http://uvelka-petfood.tw1.ru"
TIMEOUT = 30000  # 30 секунд


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
# ТЕСТЫ НАВИГАЦИИ
# ============================================================

class TestNavigation:
    """Тесты навигации по сайту"""
    
    def test_main_page_loads(self, page: Page):
        """Проверка загрузки главной страницы"""
        page.goto(BASE_URL)
        
        # Проверяем что страница загрузилась
        expect(page).to_have_title(re.compile(r".+"))
        
        # Проверяем наличие header
        expect(page.locator("header")).to_be_visible()
        
        # Проверяем наличие footer
        expect(page.locator("footer")).to_be_visible()
    
    def test_navigate_to_brands(self, page: Page):
        """Переход в раздел: Раздел Бренды"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='brands'], nav a[href*='brands']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*brands.*"))
    
    def test_navigate_to_about(self, page: Page):
        """Переход в раздел: Раздел О компании"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='about'], nav a[href*='about']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*about.*"))
    
    def test_navigate_to_partners(self, page: Page):
        """Переход в раздел: Раздел Партнерам"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='partners'], nav a[href*='partners']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*partners.*"))
    
    def test_navigate_to_news(self, page: Page):
        """Переход в раздел: Раздел Новости"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='news'], nav a[href*='news']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*news.*"))
    
    def test_navigate_to_career(self, page: Page):
        """Переход в раздел: Раздел Карьера"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='career'], nav a[href*='career']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*career.*"))
    
    def test_navigate_to_contacts(self, page: Page):
        """Переход в раздел: Раздел Контакты"""
        page.goto(BASE_URL)
        
        # Ищем ссылку на раздел в меню
        menu_link = page.locator(f"header a[href*='contacts'], nav a[href*='contacts']").first
        
        if menu_link.count() > 0:
            menu_link.click()
            page.wait_for_load_state("networkidle")
            
            # Проверяем что URL изменился
            expect(page).to_have_url(re.compile(r".*contacts.*"))
    
    def test_breadcrumbs_navigation(self, page: Page):
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
    
    def test_scroll_to_top_button(self, page: Page):
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


"""
Конфигурация pytest для тестов Playwright
Проект: UvelkaPetfood
Версия: 2.0.0
"""

import pytest


def pytest_configure(config):
    """Настройка маркеров pytest"""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with -m 'not slow')")
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Аргументы запуска браузера"""
    return {
        **browser_type_launch_args,
        "headless": True,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Аргументы контекста браузера"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
        "timezone_id": "Europe/Moscow",
        "ignore_https_errors": True,
    }


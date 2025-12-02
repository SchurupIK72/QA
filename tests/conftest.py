"""
Конфигурация pytest для тестов Playwright
Проект: UvelkaPetfood
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
    return {
        **browser_type_launch_args,
        "slow_mo": 100,  # Замедление для отладки
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


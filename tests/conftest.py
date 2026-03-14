"""
Модуль содержит фикстуры pytest для тестов.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver() -> webdriver.Chrome:
    """
    Фикстура для создания и закрытия браузера.

    Returns:
        webdriver.Chrome: Экземпляр драйвера Chrome
    """
    options = Options()
    # options.add_argument("--headless")  # раскомментировать для фонового режима
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()

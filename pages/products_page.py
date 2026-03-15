"""
Модуль содержит класс страницы с товарами после авторизации.
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductsPage:
    """Страница с товарами после авторизации."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы с товарами.

        Args:
            driver: WebDriver браузера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Проверить отображение товаров")
    def is_products_displayed(self) -> bool:
        """
        Проверить, что список товаров отображается.

        Returns:
            bool: True если товары отображаются, иначе False
        """
        try:
            inventory_list = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            return inventory_list.is_displayed()
        except:
            return False

    @allure.step("Открыть боковое меню")
    def open_menu(self) -> None:
        """Открыть боковое меню."""
        menu_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        )
        # Используем JavaScript клик для надежности
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Ждем появления меню
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu"))
        )

    @allure.step("Нажать кнопку выхода")
    def click_logout(self) -> None:
        """Нажать кнопку выхода в меню."""
        logout_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        # Используем JavaScript клик
        self.driver.execute_script("arguments[0].click();", logout_link)

        # Ждем изменения URL
        self.wait.until(
            lambda d: "inventory" not in d.current_url
        )

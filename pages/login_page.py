"""
Модуль содержит класс страницы авторизации SauceDemo.
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.products_page import ProductsPage


class LoginPage:
    """Страница авторизации SauceDemo."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы логина.

        Args:
            driver: WebDriver браузера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу логина")
    def open(self) -> "LoginPage":
        """
        Открыть страницу авторизации.

        Returns:
            LoginPage: Возвращает себя для цепочки вызовов
        """
        self.driver.get("https://www.saucedemo.com/")
        return self

    @allure.step("Ввести логин {username}")
    def enter_username(self, username: str) -> None:
        """
        Ввод имени пользователя.

        Args:
            username: Логин пользователя
        """
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.clear()
        username_field.send_keys(username)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> None:
        """
        Ввод пароля.

        Args:
            password: Пароль пользователя
        """
        password_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Нажать кнопку входа")
    def click_login(self) -> ProductsPage:
        """
        Клик по кнопке входа.

        Returns:
            ProductsPage: Объект страницы с товарами
        """
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
        return ProductsPage(self.driver)

    @allure.step("Выполнить вход с логином {username} и паролем {password}")
    def login(self, username: str, password: str) -> ProductsPage:
        """
        Комплексный метод для входа.

        Args:
            username: Логин пользователя
            password: Пароль пользователя

        Returns:
            ProductsPage: Объект страницы с товарами
        """
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()

    @allure.step("Получить текст сообщения об ошибке")
    def get_error_message(self) -> str:
        """
        Получить текст сообщения об ошибке.

        Returns:
            str: Текст сообщения об ошибке
        """
        error_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        return error_element.text

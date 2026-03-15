"""
Модуль содержит тесты для проверки авторизации и выхода из системы.
"""

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """Класс для тестирования авторизации на SauceDemo."""

    @allure.title("Тест входа с корректными данными")
    @allure.description("Проверяем, что пользователь может войти в SauceDemo используя стандартного пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_valid_login(self, driver) -> None:
        """
        Тест проверяет успешную авторизацию с валидными учетными данными.

        Ожидаемый результат:
        - После входа URL содержит 'inventory.html'
        - На странице отображается список товаров
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()

        with allure.step("Заполнить учётные данные и войти"):
            products_page = login_page.login("standard_user", "secret_sauce")

        with allure.step("Проверить, что вход выполнен успешно"):
            # Используем явное ожидание вместо sleep
            WebDriverWait(driver, 10).until(
                EC.url_contains("inventory.html")
            )
            assert "inventory.html" in driver.current_url, \
                f"Ожидался URL с 'inventory.html', получен: {driver.current_url}"

            # Проверяем наличие товаров
            assert products_page.is_products_displayed(), "Товары не отображаются"


@allure.feature("Выход из системы")
@allure.severity(allure.severity_level.NORMAL)
class TestLogout:
    """Класс для тестирования выхода из системы."""

    @allure.title("Тест выхода из системы через меню")
    @allure.description("Проверяем, что пользователь может выйти из системы через боковое меню")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout_from_menu(self, driver) -> None:
        """
        Тест проверяет функцию выхода из системы через меню.

        Ожидаемый результат:
        - После выхода возвращаемся на страницу логина
        """
        with allure.step("Открыть страницу логина и войти"):
            login_page = LoginPage(driver)
            login_page.open()
            products_page = login_page.login("standard_user", "secret_sauce")

            # Ждем загрузки страницы товаров
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )

        with allure.step("Выполнить выход через меню"):
            products_page.open_menu()
            products_page.click_logout()

            # Ждем возврата на страницу логина
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )

        with allure.step("Проверить, что вернулись на страницу логина"):
            assert "saucedemo.com" in driver.current_url, \
                f"Неверный URL: {driver.current_url}"
            assert "inventory" not in driver.current_url, \
                f"Все еще на странице товаров: {driver.current_url}"

            # Проверяем наличие элементов страницы логина
            username_field = driver.find_element(By.ID, "user-name")
            password_field = driver.find_element(By.ID, "password")
            login_button = driver.find_element(By.ID, "login-button")

            assert username_field.is_displayed(), "Поле логина не отображается"
            assert password_field.is_displayed(), "Поле пароля не отображается"
            assert login_button.is_displayed(), "Кнопка входа не отображается"


@allure.feature("Авторизация")
@allure.severity(allure.severity_level.NORMAL)
class TestLoginParametrized:
    """Параметризованные тесты для разных типов пользователей."""

    @allure.title("Тест входа с пользователем {username}")
    @allure.description("Проверяем вход для разных типов пользователей")
    @pytest.mark.parametrize("username, password, should_succeed", [
        ("standard_user", "secret_sauce", True),
        ("locked_out_user", "secret_sauce", False),
        ("problem_user", "secret_sauce", True),
        ("performance_glitch_user", "secret_sauce", True),
        ("error_user", "secret_sauce", True),
        ("visual_user", "secret_sauce", True),
    ])
    def test_multiple_users(self, driver, username: str, password: str, should_succeed: bool) -> None:
        """
        Параметризованный тест для проверки разных пользователей.

        Args:
            driver: WebDriver браузера
            username: логин пользователя
            password: пароль
            should_succeed: ожидается ли успешный вход
        """
        with allure.step(f"Открыть страницу логина и войти как {username}"):
            login_page = LoginPage(driver)
            login_page.open()
            login_page.login(username, password)

        if should_succeed:
            with allure.step(f"Проверить успешный вход для {username}"):
                # Ждем загрузки страницы товаров
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
                    )
                    assert "inventory.html" in driver.current_url, \
                        f"Пользователь {username} должен был войти, но не вошел"
                except TimeoutException:
                    assert False, f"Пользователь {username} должен был войти, но не вошел"
        else:
            with allure.step(f"Проверить сообщение об ошибке для {username}"):
                error_text = login_page.get_error_message()
                assert error_text, f"Для пользователя {username} должно быть сообщение об ошибке"
                assert "locked out" in error_text.lower() or "epic sadface" in error_text.lower(), \
                    f"Ожидалось сообщение об ошибке, получено: {error_text}"

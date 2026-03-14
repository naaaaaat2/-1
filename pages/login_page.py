import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    """Страница авторизации SauceDemo."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
    
    @allure.step("Открыть страницу логина")
    def open(self) -> "LoginPage":
        """Открыть страницу авторизации."""
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    @allure.step("Ввести логин {username}")
    def enter_username(self, username: str) -> None:
        """Ввод имени пользователя."""
        self.driver.find_element(By.ID, "user-name").send_keys(username)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> None:
        """Ввод пароля."""
        self.driver.find_element(By.ID, "password").send_keys(password)
    
    @allure.step("Нажать кнопку входа")
    def click_login(self) -> None:
        """Клик по кнопке входа."""
        self.driver.find_element(By.ID, "login-button").click()
    
    @allure.step("Выполнить вход с логином {username} и паролем {password}")
    def login(self, username: str, password: str) -> None:
        """Комплексный метод для входа."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    @allure.step("Получить текст сообщения об ошибке")
    def get_error_message(self) -> str:
        """Получить текст сообщения об ошибке."""
        error_element = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return error_element.text

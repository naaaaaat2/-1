# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Базовый класс для всех страниц."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: tuple):
        """Найти элемент с ожиданием."""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def find_elements(self, locator: tuple):
        """Найти все элементы."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))
    
    def click(self, locator: tuple) -> None:
        """Кликнуть по элементу."""
        self.find_element(locator).click()
    
    def send_keys(self, locator: tuple, text: str) -> None:
        """Ввести текст."""
        self.find_element(locator).send_keys(text)

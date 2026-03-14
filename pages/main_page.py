import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    """Главная страница после авторизации (страница с товарами)."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @allure.step("Открыть меню")
    def open_menu(self) -> None:
        """Открыть боковое меню."""
        menu_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        )
        menu_button.click()
    
    @allure.step("Нажать кнопку выхода")
    def click_logout(self) -> None:
        """Нажать кнопку выхода в меню."""
        # Ждем появления меню и кнопки выхода
        import time
        time.sleep(1)  # небольшая пауза для анимации
        
        logout_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_link.click()
    
    @allure.step("Выполнить выход из системы")
    def logout(self) -> None:
        """Полный процесс выхода из системы."""
        self.open_menu()
        self.click_logout()
    
    @allure.step("Проверить, что находимся на странице товаров")
    def is_on_products_page(self) -> bool:
        """Проверить, что открыта страница с товарами."""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            return True
        except:
            return False

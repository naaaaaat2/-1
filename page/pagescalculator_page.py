from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure


@allure.feature("Калькулятор")
class CalculatorPage:
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы калькулятора.
        :param driver: экземпляр WebDriver
        """
        self.driver = driver

    @allure.step("Открыть страницу калькулятора")
    def open(self) -> 'CalculatorPage':
        """
        Открывает страницу калькулятора.
        :return: self, для цепочки вызовов
        """
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/"
            "slow-calculator.html"
        )
        return self

    @allure.step("Установить задержку {seconds} секунд")
    def set_delay(self, seconds: int) -> 'CalculatorPage':
        """
        Устанавливает задержку перед выполнением операций.
        :param seconds: количество секунд задержки
        :return: self
        """
        delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self

    @allure.step("Нажать кнопку '{label}'")
    def click_button(self, label: str) -> 'CalculatorPage':
        """
        Нажимает кнопку по её тексту.
        :param label: текст на кнопке
        :return: self
        """
        button = self.driver.find_element(
            By.XPATH,
            f"//button[text()='{label}']"
        )
        button.click()
        return self

    @allure.step("Получить результат")
    def get_result(self) -> str:
        """
        Получает текущее значение результата с дисплея.
        :return: строка с результатом
        """
        result_element = self.driver.find_element(By.CSS_SELECTOR, ".screen")
        return result_element.text

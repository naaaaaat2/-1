import allure
from selenium import webdriver
from pagescalculator_page import CalculatorPage


@allure.title("Проверка калькулятора: 45 задержка, 7 + 8 = 15")
@allure.description(
    "Тест проверяет, что при задержке 45 секунд "
    "калькулятор возвращает правильный результат."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Калькулятор")
def test_calculator_with_allure():
    driver = webdriver.Chrome()
    calc_page = CalculatorPage(driver)
    try:
        with allure.step("Открыть страницу калькулятора"):
            calc_page.open()

        with allure.step("Установить задержку в 45 секунд"):
            calc_page.set_delay(45)

        with allure.step("Ввод цифр и операций: 7 + 8 ="):
            calc_page.click_button("7")\
                     .click_button("+")\
                     .click_button("8")\
                     .click_button("=")

        with allure.step("Проверка результата '15'"):
            result = calc_page.get_result()
            assert result.strip() == "15", f"Ожидалось 15, получено {result}"
    finally:
        driver.quit()

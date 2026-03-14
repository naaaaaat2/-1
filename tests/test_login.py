import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time
from pages.login_page import LoginPage


@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """Класс для тестирования авторизации на SauceDemo."""

    @allure.title("Тест входа с корректными данными")
    @allure.description("Проверяем, что пользователь может войти в SauceDemo используя стандартного пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_valid_login(self, driver):
        """
        Тест проверяет успешную авторизацию с валидными учетными данными.
        
        Ожидаемый результат:
        - После входа URL содержит 'inventory.html'
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()
        
        with allure.step("Заполнить учётные данные и войти"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("Проверить, что вход выполнен успешно"):
            # Проверяем, что URL изменился на страницу товаров
            assert "inventory.html" in driver.current_url, \
                f"Ожидался URL с 'inventory.html', получен: {driver.current_url}"

    @allure.title("Тест входа с заблокированным пользователем")
    @allure.description("Проверяем, что заблокированный пользователь не может войти и видит сообщение об ошибке")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, driver):
        """
        Тест проверяет, что заблокированный пользователь не может авторизоваться.
        
        Ожидаемый результат:
        - Появляется сообщение об ошибке с текстом 'locked out'
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()
        
        with allure.step("Попытаться войти с заблокированным пользователем"):
            login_page.login("locked_out_user", "secret_sauce")
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_message()
            assert "locked out" in error_text.lower(), \
                f"Ожидалось сообщение с 'locked out', получено: {error_text}"

    @allure.title("Тест входа с неверным паролем")
    @allure.description("Проверяем, что пользователь не может войти с неправильным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_password(self, driver):
        """
        Тест проверяет, что пользователь не может войти с неправильным паролем.
        
        Ожидаемый результат:
        - Появляется сообщение об ошибке 'Username and password do not match'
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()
        
        with allure.step("Попытаться войти с неправильным паролем"):
            login_page.login("standard_user", "wrong_password")
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_message()
            assert "do not match" in error_text or "username and password" in error_text.lower(), \
                f"Ожидалось сообщение об ошибке, получено: {error_text}"

    @allure.title("Тест входа с пустыми полями")
    @allure.description("Проверяем, что пользователь не может войти с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_fields(self, driver):
        """
        Тест проверяет, что нельзя войти с пустыми полями.
        
        Ожидаемый результат:
        - Появляется сообщение об ошибке 'Username is required'
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()
        
        with allure.step("Нажать кнопку входа без заполнения полей"):
            login_page.click_login()
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_message()
            assert "username is required" in error_text.lower(), \
                f"Ожидалось сообщение о required поле, получено: {error_text}"

    @allure.title("Тест входа только с логином")
    @allure.description("Проверяем, что пользователь не может войти без пароля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_username_only(self, driver):
        """
        Тест проверяет, что нельзя войти только с логином без пароля.
        
        Ожидаемый результат:
        - Появляется сообщение об ошибке 'Password is required'
        """
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver)
            login_page.open()
        
        with allure.step("Ввести только логин и нажать войти"):
            login_page.enter_username("standard_user")
            login_page.click_login()
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_message()
            assert "password is required" in error_text.lower(), \
                f"Ожидалось сообщение о required пароле, получено: {error_text}"

    @allure.title("Тест выхода из системы")
    @allure.description("Проверяем, что пользователь может выйти из системы через меню")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, driver):
        """
        Тест проверяет функцию выхода из системы.

        Ожидаемый результат:
        - После выхода возвращаемся на страницу логина
        """
        with allure.step("Открыть страницу логина и войти"):
            login_page = LoginPage(driver)
            login_page.open()
            login_page.login("standard_user", "secret_sauce")

            # Ждем загрузки страницы товаров
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            time.sleep(1)
            print("✓ Страница товаров загружена")
            initial_url = driver.current_url
            print(f"Начальный URL: {initial_url}")

        with allure.step("Найти и открыть меню"):
            # Ждем кнопку меню
            menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
            )
            print("✓ Кнопка меню найдена")

            # Прокручиваем к кнопке для надежности
            driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
            time.sleep(0.5)

            # Пробуем открыть меню разными способами
            menu_opened = False
            max_attempts = 3
            
            for attempt in range(max_attempts):
                print(f"Попытка {attempt + 1} открыть меню...")
                
                # Способ 1: Обычный клик
                try:
                    menu_button.click()
                    print("  - Клик: обычный")
                    time.sleep(1)
                    
                    # Проверяем, открылось ли меню
                    try:
                        menu_element = WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu"))
                        )
                        if menu_element.is_displayed():
                            print("  ✓ Меню открылось (обычный клик)")
                            menu_opened = True
                            break
                    except:
                        pass
                except Exception as e:
                    print(f"  - Обычный клик не сработал: {type(e).__name__}")
                
                # Способ 2: Клик через JavaScript
                try:
                    driver.execute_script("arguments[0].click();", menu_button)
                    print("  - Клик: JavaScript")
                    time.sleep(1)
                    
                    # Проверяем, открылось ли меню
                    try:
                        menu_element = WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu"))
                        )
                        if menu_element.is_displayed():
                            print("  ✓ Меню открылось (JavaScript)")
                            menu_opened = True
                            break
                    except:
                        pass
                except Exception as e:
                    print(f"  - JavaScript клик не сработал: {type(e).__name__}")
                
                # Способ 3: ActionChains
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(menu_button).click().perform()
                    print("  - Клик: ActionChains")
                    time.sleep(1)
                    
                    # Проверяем, открылось ли меню
                    try:
                        menu_element = WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu"))
                        )
                        if menu_element.is_displayed():
                            print("  ✓ Меню открылось (ActionChains)")
                            menu_opened = True
                            break
                    except:
                        pass
                except Exception as e:
                    print(f"  - ActionChains клик не сработал: {type(e).__name__}")
                
                if attempt < max_attempts - 1:
                    print("  Повторная попытка через 2 секунды...")
                    time.sleep(2)
            
            # Если меню так и не открылось
            if not menu_opened:
                driver.save_screenshot("menu_not_opened.png")
                print("✗ Меню не открылось после всех попыток")
                assert False, "Не удалось открыть меню"
            
            # Даем время для полной анимации
            time.sleep(1)

        with allure.step("Нажать кнопку выхода"):
            # Ждем появления кнопки выхода
            try:
                logout_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
                )
                print("✓ Кнопка выхода найдена")
            except TimeoutException:
                driver.save_screenshot("logout_button_not_found.png")
                print("✗ Кнопка выхода не найдена")
                assert False, "Кнопка выхода не появилась в меню"

            # Прокручиваем к кнопке
            driver.execute_script("arguments[0].scrollIntoView(true);", logout_link)
            time.sleep(0.5)

            # Пробуем кликнуть по кнопке выхода разными способами
            logout_clicked = False
            click_methods = [
                ("обычный", lambda: logout_link.click()),
                ("JavaScript", lambda: driver.execute_script("arguments[0].click();", logout_link)),
                ("ActionChains", lambda: ActionChains(driver).move_to_element(logout_link).click().perform())
            ]
            
            for method_name, click_method in click_methods:
                try:
                    print(f"  - Пробуем клик: {method_name}")
                    click_method()
                    print(f"  ✓ Клик выполнен: {method_name}")
                    logout_clicked = True
                    time.sleep(1)
                    
                    # Проверяем, изменился ли URL после клика
                    current_url = driver.current_url
                    print(f"    URL после клика: {current_url}")
                    
                    if "inventory" not in current_url:
                        print(f"  ✓ URL изменился после {method_name}")
                        break
                    else:
                        print(f"  ✗ URL не изменился после {method_name}")
                        # Продолжаем пробовать другие методы
                        
                except Exception as e:
                    print(f"  ✗ Ошибка при клике {method_name}: {type(e).__name__}")
                    continue
            
            if not logout_clicked:
                driver.save_screenshot("logout_click_failed.png")
                print("✗ Не удалось кликнуть по кнопке выхода ни одним способом")
                assert False, "Не удалось кликнуть по кнопке выхода"

            print("✓ Кнопка выхода нажата")

            # Ждем возможной перезагрузки страницы
            time.sleep(3)

            # Активно проверяем изменение URL в течение 10 секунд
            url_changed = False
            for i in range(10):
                current_url = driver.current_url
                if "inventory" not in current_url:
                    url_changed = True
                    print(f"✓ URL изменился через {i+1} секунд: {current_url}")
                    break
                print(f"  Ожидание изменения URL... ({i+1}/10)")
                time.sleep(1)
            
            if not url_changed:
                print(f"✗ URL не изменился: {driver.current_url}")
                driver.save_screenshot("url_not_changed.png")
                
                # Пробуем еще раз кликнуть через JavaScript
                print("Пробуем еще раз кликнуть через JavaScript...")
                try:
                    driver.execute_script("arguments[0].click();", logout_link)
                    time.sleep(3)
                    if "inventory" not in driver.current_url:
                        print("✓ Со второй попытки URL изменился")
                        url_changed = True
                except:
                    pass
            
            if not url_changed:
                assert False, "URL не изменился после выхода"

        with allure.step("Проверить, что вернулись на страницу логина"):
            # Проверяем URL
            current_url = driver.current_url
            print(f"Финальный URL: {current_url}")
            assert "saucedemo.com" in current_url, f"Неверный URL: {current_url}"
            
            # Проверяем, что мы не на странице товаров
            assert "inventory" not in current_url, f"Все еще на странице товаров: {current_url}"
            
            # Проверяем наличие элементов страницы логина
            try:
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "user-name"))
                )
                print("✓ Поле username найдено")
                
                password_field = driver.find_element(By.ID, "password")
                login_button = driver.find_element(By.ID, "login-button")
                
                assert username_field.is_displayed(), "Поле логина не отображается"
                assert password_field.is_displayed(), "Поле пароля не отображается"
                assert login_button.is_displayed(), "Кнопка входа не отображается"
                
                print("✓ Все элементы страницы логина найдены и отображаются")
                print("✓ Тест выхода успешно завершен")
                
            except TimeoutException:
                driver.save_screenshot("login_page_not_found.png")
                print("✗ Не удалось найти элементы страницы логина")
                print(f"Заголовок страницы: {driver.title}")
                
                # Проверяем HTML на наличие полей
                page_source = driver.page_source
                if "user-name" in page_source:
                    print("Поле user-name присутствует в HTML, но не отображается")
                else:
                    print("Поле user-name отсутствует в HTML")
                
                assert False, "Не удалось найти элементы страницы логина"


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
    def test_multiple_users(self, driver, username, password, should_succeed):
        """
        Параметризованный тест для проверки разных пользователей.
        
        Args:
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
                    print(f"✓ {username} успешно вошел в систему")
                except TimeoutException:
                    driver.save_screenshot(f"login_failure_{username}.png")
                    assert False, f"Пользователь {username} должен был войти, но не вошел"
        else:
            with allure.step(f"Проверить сообщение об ошибке для {username}"):
                error_text = login_page.get_error_message()
                assert error_text, f"Для пользователя {username} должно быть сообщение об ошибке"
                assert "locked out" in error_text.lower() or "epic sadface" in error_text.lower()
                print(f"✓ {username} получил ожидаемое сообщение об ошибке")

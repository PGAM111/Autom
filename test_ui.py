import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import settings as settings
import time


@pytest.fixture
def driver():
    """Создание драйвера в режиме инкогнито"""
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.ui
@allure.feature("Поиск авиабилетов")
@allure.title("Введение города вылета")
@allure.story("Успешный ввод города вылета")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_from(driver):
    """Тест ввода города вылета"""

    with allure.step("1. Открыть главную страницу Aviasales"):
        driver.get(settings.URL_UI)

    with allure.step("2. Вписать в поле 'Откуда' город 'Москва' на кириллице"):
        from_input = driver.find_element(
            By.ID, "avia_form_origin-input")
        from_input.click()
        from_input.send_keys(Keys.CONTROL + "a")
        from_input.send_keys(Keys.DELETE)
        from_input.send_keys("Москва")
        time.sleep(2)
        from_input.send_keys(Keys.ARROW_DOWN)
        from_input.send_keys(Keys.ENTER)
    with allure.step("3. Проверить, что в поле введен город 'Москва'"):
        entered_value = from_input.get_attribute('value')
        assert "Москва" in entered_value


@pytest.mark.ui
@allure.feature("Поиск авиабилетов")
@allure.title("Введение кода IATA прилёта")
@allure.story("Успешный кода IATA прилёта")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_where(driver):
    """Тест ввода кода IATA вместо города прилёта"""
    with allure.step("1. Открыть главную страницу Aviasales"):
        driver.get(settings.URL_UI)

    with allure.step("2. Вписать в поле 'Куда' код IATA 'ARH'"):
        where_input = driver.find_element(
            By.ID, "avia_form_destination-input")
        where_input.click()
        where_input.send_keys("ARH")
        time.sleep(2)
        where_input.send_keys(Keys.ARROW_DOWN)
        where_input.send_keys(Keys.ENTER)
    with allure.step("3. Проверить, что в поле появился город 'Архангельск'"):
        entered_value = where_input.get_attribute('value')
        assert "Архангельск" in entered_value


@pytest.mark.ui
@allure.feature("Сложный поиск авиабилетов")
@allure.title("Переход к сложному поиску авиабилетов")
@allure.story("Успешный переход к сложному поиску авиабилетов")
@allure.severity(allure.severity_level.NORMAL)
def test_complicated_search(driver):
    """Тест перехода в режим составления сложного маршрута и обратно"""
    with allure.step("1.Открыть главную страницу Aviasales"):
        driver.get(settings.URL_UI)

    with allure.step("2.Выбрать режим составления сложного маршрута"):
        driver.find_element(
            By.XPATH, "//div[text()='Составить сложный маршрут']").click()
    with allure.step("3.Проверить наличие поля 'Куда'№2"):
        element = driver.find_element(
            By.CSS_SELECTOR, "[data-test-id='multiway-direction-2']")
        assert element.is_displayed()


@pytest.mark.ui
@allure.feature("Поиск отеля")
@allure.title("Ввод города для поиска отеля")
@allure.story("Успешный ввод города для поиска отеля")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_hotel(driver):
    """Тест ввода города для поиска отеля"""
    with allure.step("1. Открыть страницу отелей на Aviasales"):
        driver.get(settings.HOTEL)

    with allure.step("2. Вписать в поле 'Город или отель' город 'Уфа'"):
        city_input = driver.find_element(
            By.ID, "hotel_autocomplete-input")
        city_input.click()
        city_input.send_keys("Уфа")
        time.sleep(2)
        city_input.send_keys(Keys.TAB)
    with allure.step("3. Проверить, что в поле появился город 'Уфа'"):
        entered_value = city_input.get_attribute('value')
        assert "Уфа" in entered_value


@pytest.mark.ui
@allure.feature("Поиск отеля")
@allure.title("Поиск отеля по названию")
@allure.story("Успешный ввод названия отеля для поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_title_search(driver):
    """Тест ввода названия отеля для поиска"""
    with allure.step("1. Открыть страницу отелей на Aviasales"):
        driver.get(settings.HOTEL)

    with allure.step(
          "2. Вписать в поле 'Город или отель' название отеля 'Ситикомфорт'"):
        hotel_input = driver.find_element(
            By.ID, "hotel_autocomplete-input")
        hotel_input.click()
        hotel_input.send_keys("Ситикомфорт")
        time.sleep(2)
        hotel_input.send_keys(Keys.TAB)
    with allure.step(
         "3. Проверить,что в поле появился один из отелей сети 'Ситикомфорт'"):
        entered_value = hotel_input.get_attribute('value')
        assert "Ситикомфорт" in entered_value

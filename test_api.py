import pytest
import requests
import allure
import settings as settings


def get_headers(token=None):
    """Получить заголовки с токеном"""
    token_to_use = settings.TOKEN
    headers = settings.HEADERS.copy()
    headers['X-Access-Token'] = token_to_use
    return headers


@pytest.mark.api
@allure.feature("Поиск авиабилетов")
@allure.title("Поиск билетов туда и обратно")
@allure.story("Успешный поиск билетов туда и обратно")
@allure.severity(allure.severity_level.CRITICAL)
def test_round_trip_ticket():
    with allure.step("1. Задать параметры поиска в теле запроса"):
        params = {
            'origin': 'MOW',
            'destination': 'KHV',
            'depart_date': '2025-12-19',
            'return_date': '2025-12-23'
        }

    with allure.step("2. Отправить GET-запрос на сервер Aviasales"):
        response = requests.get(
            f"{settings.BASE_URL}cheap",
            headers=get_headers(),
            params=params
        )

    """Проверка статус-кода и наличия в теле ответа номера рейса"""
    with allure.step(
            "3. Выполнить проверку тела запроса и соответствия статус-кода"):
        assert '"flight_number"' in response.text
        assert response.status_code == 200


@pytest.mark.api
@allure.feature("Поиск авиабилетов")
@allure.title("Поиск билетов в одну сторону")
@allure.story("Успешный поиск билетов в одну сторону")
@allure.severity(allure.severity_level.CRITICAL)
def test_one_way_ticket():
    with allure.step("1.Задать параметры поиска в теле запроса"):
        params = {
            'origin': 'MOW',
            'destination': 'KHV',
            'depart_date': '2025-12-19'
        }

    with allure.step("2.Отправить GET-запрос на сервер Aviasales"):
        response = requests.get(
            f"{settings.BASE_URL}cheap",
            headers=get_headers(),
            params=params
        )

    """Проверка статус-кода и наличия в теле ответа номера рейса"""
    with allure.step(
            "3.Выполнить проверку тела запроса и соответствия статус-кода"):
        assert '"flight_number"' in response.text
        assert response.status_code == 200


@pytest.mark.api
@allure.feature("Поиск авиабилетов")
@allure.title("Поиск билетов куда угодно")
@allure.story("Успешный поиск билетов куда угодно")
@allure.severity(allure.severity_level.NORMAL)
def test_anywhere_from_moscow():
    with allure.step("1. Задать параметры поиска в теле запроса"):
        params = {
            'origin': 'MOW',
            'depart_date': '2025-12-19',
            'return_date': '2025-12-23'
        }

    with allure.step("2. Отправить GET-запрос на сервер Aviasales"):
        response = requests.get(
            f"{settings.BASE_URL}cheap",
            headers=get_headers(),
            params=params
        )

    """Проверка статус-кода и наличия в теле ответа номера рейса"""
    with allure.step(
            "3. Выполнить проверку тела запроса и соответствия статус-кода"):
        assert '"flight_number"' in response.text
        assert response.status_code == 200


@pytest.mark.api
@allure.feature("Поиск авиабилетов")
@allure.title("Проверка неправильного метода запроса")
@allure.story("Успешная проверка неправильного метода запроса")
@allure.severity(allure.severity_level.NORMAL)
def test_wrong_method_search():
    with allure.step("1. Задать параметры поиска в теле запроса"):
        params = {
            'origin': 'MOW',
            'destination': 'KHV',
            'depart_date': '2025-12-19',
            'return_date': '2025-12-23'
        }
    with allure.step("2. Отправить PATCH-запрос на сервер Aviasales"):
        response = requests.patch(
            f"{settings.BASE_URL}cheap",
            headers=get_headers(),
            params=params
        )

    """Проверка статус-кода"""
    with allure.step(
            "3. Выполнить проверку соответствия статус-кода"):
        assert response.status_code == 404


@pytest.mark.api
@allure.feature("Поиск авиабилетов")
@allure.title("Тест c неверным токеном")
@allure.story("Успешный тест c использованием неверного токена")
@allure.severity(allure.severity_level.NORMAL)
def test_wrong_token_search():
    with allure.step("1. Задать параметры поиска в теле запроса"):
        params = {
            'origin': 'MOW',
            'destination': 'KHV',
            'depart_date': '2025-12-19'
        }

    with allure.step("2. Отправить GET-запрос на сервер Aviasales"):
        response = requests.get(
            f"{settings.BASE_URL}cheap",
            headers={
                'Accept': 'application/json',
                'TOKEN': 'kjhdf7678688'
            },
            params=params
        )

    """Проверка статус-кода"""
    with allure.step(
            "3. Выполнить проверку соответствия статус-кода"):
        assert response.status_code == 401

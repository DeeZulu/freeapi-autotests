from typing import Any

from requests.models import Response

from client.db_client import DbClient


def check_status_code(response: Response, expected_code: int):
    """
    Проверка статус кода HTTP ответа
    :param response: Ответ от сервиса
    :param expected_code: Ожидаемый статус код
    """
    actual_code = response.status_code
    assert actual_code == expected_code, f"Получен неправильный статус код - {actual_code}\n" \
                                         f"Ожидался - {expected_code}\n" \
                                         f"Тело ответа: {response.text}"


def compare_values(value_name: str, actual_value: Any, expected_value: Any):
    """
    Сравнение полученного значения с ожидаемым
    :param value_name: Название значения
    :param actual_value: Полученное значение
    :param expected_value: Ожидаемое значение
    """
    assert actual_value == expected_value, f"{value_name} не совпадает с ожидаемым\n" \
                                           f"Ожидалось - {expected_value}\nПолучено - {actual_value}"


def test_get_all_users():
    """Возвращает список всех пользователей"""
    db_client = DbClient()
    clients = db_client.get_all_users()
    return clients

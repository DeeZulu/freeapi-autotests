from typing import Any

from client.db_client import DbClient


def check_status_code(actual_code: int, expected_code: int):
    """
    Проверка статус кода HTTP ответа
    :param actual_code: Полученный статус код
    :param expected_code: Ожидаемый статус код
    """
    assert actual_code == expected_code, f"Получен неправильный статус код - {actual_code}\n" \
                                         f"Ожидался - {expected_code}"


def compare_value(value_name: str, actual_value: Any, expected_value: Any):
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

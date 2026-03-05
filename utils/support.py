

def check_status_code(actual_code, expected_code: int):
    """Проверка статус кода HTTP ответа"""
    assert actual_code == expected_code,\
        f"Получен неправильный статус код - {actual_code}\nОжидался - {expected_code}"
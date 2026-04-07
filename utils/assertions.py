from client.db_client import DbClient


def check_category_not_in_database(db_client, category_id: str):
    """
    Проверяет, что категории нет в базе данных
    :param db_client Клиент для подключения к базе данных
    :param category_id ID категории
    """
    category = db_client.get_category(category_id)
    assert category is None , f"Ошибка! Категория c ID {category_id} найдена в базе данных"

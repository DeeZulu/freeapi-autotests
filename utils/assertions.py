from client.db_client import DbClient


def check_category_not_exist(db_client, category_id: str):
    """
    Проверяет, что категории нет в базе данных
    :param db_client Клиент для подключения к базе данных
    :param category_id ID категории
    """
    category = db_client.get_category(category_id)
    assert category is None , f"Ошибка! Категория c ID {category_id} найдена в базе данных"

def check_product_exist(db_client, product_id: str):
    """
    Проверяет, что продукт присутствует в базе данных
    :param db_client Клиент для работы с бд
    :param product_id ID продукта
    """
    product = db_client.get_product(product_id)
    assert product, f"Продукта с ID {product_id} нет в базе данных"

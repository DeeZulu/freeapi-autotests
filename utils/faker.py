from faker import Faker
from faker.providers import DynamicProvider

class FakeGenerator:
    category_provider = DynamicProvider(
        provider_name="ecommerce_category",
        elements=["Computers", "Smartphones", "Gadgets"]
    )

    fake = Faker()
    fake.add_provider(category_provider)

    @classmethod
    def get_ecommerce_category(cls):
        """
        Получение названия категории продуктов
        :return: Название категории
        """
        return f"{cls.fake.ecommerce_category()}"

    @classmethod
    def get_product_name(cls, category_name: str):
        """
        Получение названия продукта по названию категории
        :param category_name: Название категории
        :return: Название продукта
        """
        products_lists = {
            "Computers": ["MacBook Pro 16", "ASUS ROG Strix", "Dell XPS 13", "Lenovo Legion"],
            "Smartphones": ["iPhone 15 Pro", "Samsung Galaxy S23", "Google Pixel 8", "Xiaomi 13T"],
            "Gadgets": ["Apple Watch Series 9", "Sony WH-1000XM5", "AirPods Pro", "Samsung Buds 2"]
        }
        products = products_lists.get(category_name, ["Test Item"])
        return cls.fake.random_element(products)

    @classmethod
    def get_product_description(cls, product_category: str):
        """
        Получение описания продукта по названию категории
        :param product_category: Название категории
        :return:
        """
        product_descriptions = {
            "Computers": ["Хороший ноутбук", "Лучший ноутбук", "Клёвый ноутбук"],
            "Phones": ["Хороший телефон", "Лучший ноутбук", "Клёвый ноутбук"],
            "Gadgets": ["Хороший гаджет", "Лучший гаджет", "Клёвый гаджет"]
        }
        descriptions = product_descriptions.get(product_category, "Test Item")
        return cls.fake.random_element(descriptions)

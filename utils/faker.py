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
        return f"{cls.fake.ecommerce_category()}"

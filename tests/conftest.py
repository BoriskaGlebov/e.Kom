# conftest.py
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from main import app, get_db
# Настройка подключения к MongoDB
MONGODB_URL = "mongodb://user:password@localhost:27017"
DATABASE_NAME = 'e_kom'

# Создаем экземпляр клиента MongoDB
client = AsyncIOMotorClient(MONGODB_URL)


def override_get_db():
    """Получение подключения к базе данных."""
    db = client[DATABASE_NAME]  # Получаем базу данных
    try:
        yield db  # Возвращаем подключение к базе данных
    finally:
        pass  # Здесь можно закрыть соединение, если это необходимо

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
async def mongo_client():
    """Фикстура для подключения к MongoDB."""
    client = AsyncIOMotorClient("mongodb://user:password@localhost:27017")
    yield client
    client.close()


@pytest.fixture(scope="function")
async def setup_database(mongo_client):
    """Фикстура для настройки тестовой базы данных."""
    db = mongo_client['test_db']

    # Очистка коллекции перед каждым тестом
    await db.drop_collection("form_templates")

    # Вставка тестовых данных
    await db.form_templates.insert_many([
        {"name": "Template 1", "fields": {"email_field": "email", "phone_field": "phone"}},
        {"name": "Template 2", "fields": {"date_field": "date", "text_field": "text"}},
    ])

    yield db  # Предоставление базы данных для тестов

    # Очистка после теста
    await db.drop_collection("form_templates")
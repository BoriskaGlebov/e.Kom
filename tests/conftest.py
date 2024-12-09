# conftest.py
import asyncio
from typing import AsyncGenerator

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from main import app  # Import your FastAPI app

@pytest.fixture(scope="session")
def event_loop() -> AsyncGenerator:
    """
    Фикстура для создания единого event loop для всех тестов.
    Вот эта функция нужна для работы в одном event loop всех тестов

    :yield: Event loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mongo_client():
    """Fixture for MongoDB client."""
    client = AsyncIOMotorClient("mongodb://user:password@localhost:27017")
    yield client
    client.close()


@pytest.fixture
async def setup_database(mongo_client):
    """Fixture for setting up and tearing down the test database."""
    db_name = 'test_db'
    db = mongo_client[db_name]

    # Clear the database before each test
    await db.drop_collection("form_templates")

    # Optionally, insert some initial data for testing
    await db.form_templates.insert_many([
        {"name": "Template 1", "fields": {"email_field": "email", "phone_field": "phone"}},
        {"name": "Template 2", "fields": {"date_field": "date", "text_field": "text"}},
    ])

    yield db  # Provide the database to the test

    # Clean up after each test
    await db.drop_collection("form_templates")
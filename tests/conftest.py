# conftest.py
import random

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from data_generate import \
    generate_random_data  # Import your data generation function
from main import app, get_db

# MongoDB settings for testing
MONGODB_URL = "mongodb://user:password@localhost:27017"
TEST_DATABASE_NAME = "test_db"
COLLECTION_NAME = "form_templates"


@pytest.fixture(scope="session")
async def mongo_client():
    """Fixture for MongoDB client."""
    client = AsyncIOMotorClient(MONGODB_URL)
    yield client
    client.close()


@pytest.fixture(scope="session")
async def setup_database(mongo_client):
    """Fixture for setting up and tearing down the test database."""
    db = mongo_client[TEST_DATABASE_NAME]

    # Clear the database before each test
    await db.drop_collection(COLLECTION_NAME)

    # Insert some initial data for testing
    random_data = [generate_random_data(random.randint(1, 10)) for _ in range(100)]
    await db[COLLECTION_NAME].insert_many(random_data)
    await db[COLLECTION_NAME].insert_one(
        {
            "name": "test_inf",
            "text_field": "text",
            "email_field": "email",
            "phone_field": "phone",
            "date_field": "date",
        }
    )

    yield db  # Provide the database to the test

    # Clean up after each test
    await db.drop_collection(COLLECTION_NAME)


@pytest.fixture(autouse=True)
def override_get_db(setup_database):
    """Override the get_db dependency to use the test database."""

    async def _override_get_db():
        return setup_database

    app.dependency_overrides[get_db] = _override_get_db

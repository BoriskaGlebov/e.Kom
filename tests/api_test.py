# test_api.py
import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_get_form_valid_data(setup_database):
    """Test successful retrieval of form templates with valid data."""

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/get_form", json={
            "extra_fields": {
                "email_field": "test@example.com",
                "phone_field": "+7 123 456 78 90"
            }
        })

    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of templates
    assert len(response.json()) > 0  # Expecting that the list is not empty


@pytest.mark.asyncio
async def test_get_form_no_templates_found(setup_database):
    """Test case where no templates are found."""

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/get_form", json={
            "extra_fields": {
                "non_existent_field": "random_value"
            }
        })

    assert response.status_code == 200
    assert response.json() == {"extra_fields": {"non_existent_field": "text"}}  # Expecting empty input response


@pytest.mark.asyncio
async def test_get_form_invalid_data(setup_database):
    """Test handling of invalid input data."""

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/get_form", json={
            "extra_fields": {
                "email_field": 12345  # Invalid type (not a string)
            }
        })

    assert response.status_code == 422  # Expecting validation error
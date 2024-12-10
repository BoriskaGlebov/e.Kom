# test_api.py
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from config import logger
from main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_get_form_valid_data(setup_database):
    """Test successful retrieval of form templates with valid data."""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/get_form", json={"extra_fields": {"email": "test@example.com"}}
        )

        response2 = await client.post(
            "/get_form",
            json={
                "extra_fields": {
                    "text_field": "text",
                    "email_field": "b@mail.com",
                    "phone_field": "+79852000338",
                    "date_field": "01.01.2024",
                }
            },
        )
        response3 = await client.post(
            "/get_form",
            json={
                "extra_fields": {
                    "text_field": "text",
                    "email_field": "b@mail.com",
                    "phone_field": "+79852000338",
                    "date_field": "2024-01-01",
                }
            },
        )
        logger.error("Совсем простой шаблон, который точно будет в БД")
        assert response.status_code == 200
        assert isinstance(response.json(), list)  # Expecting a list of templates
        assert len(response.json()) > 0  # Expecting that the list is not empty

        assert response2.status_code == 200
        assert isinstance(response2.json(), list)  # Expecting a list of templates
        assert len(response2.json()) > 0  # Expecting that the list is not empty
        assert "test_inf" in [el["name"] for el in response2.json()]

        assert response3.status_code == 200
        assert isinstance(response3.json(), list)  # Expecting a list of templates
        assert len(response3.json()) > 0  # Expecting that the list is not empty
        assert "test_inf" in [el["name"] for el in response3.json()]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_form_no_templates_found(setup_database):
    """Test case where no templates are found."""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/get_form",
            json={
                "extra_fields": {
                    "non_existent_field": "random_value",
                    "text_field_XXXXX": "text",
                    "email_field_XXXX": "b@mail.com",
                    "phone_field_XXXX": "+79852000338",
                    "date_field_XXXXX": "2024-01-01",
                }
            },
        )

    assert response.status_code == 404  # Expecting a 404 status code
    assert response.json() == {
        "detail": {
            "extra_fields": {
                "non_existent_field": "text",
                "text_field_XXXXX": "text",
                "email_field_XXXX": "email",
                "phone_field_XXXX": "phone",
                "date_field_XXXXX": "date",
            }
        }
    }  # Expecting empty input response

    # @pytest.mark.asyncio
    # async def test_add_template(setup_database):
    #     """Test adding a new template to the database."""
    #
    #     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    #         new_template = {
    #             "name": "New Template",
    #             "fields": {
    #                 "email_field": "email",
    #                 "phone_field": "phone"
    #             }
    #         }
    #
    #         response = await client.post("/add_template", json=new_template)
    #
    #         assert response.status_code == 200
    #         assert response.json() == new_template  # Expecting the same template back

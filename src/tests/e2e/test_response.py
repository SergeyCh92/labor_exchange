import pytest

import src.services as services
from src.schemas import ResponseSchema
from tests.utils import convert_data_to_list_models


@pytest.mark.asyncio
async def test_create_response(monkeypatch, client, auth_token, response_create_schema):
    async def mock_create_response(*args, **kwargs):
        ...

    monkeypatch.setattr(services.ResponseService, "create_response", mock_create_response)
    response = await client.post("/responses/response", headers=auth_token, data=response_create_schema.json())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_responses(monkeypatch, client, auth_token, response_schema):
    async def mock_get_responses(*args, **kwargs):
        return [response_schema]

    monkeypatch.setattr(services.ResponseService, "get_responses", mock_get_responses)
    response = await client.get("/responses/1", headers=auth_token)
    assert response.status_code == 200
    data = convert_data_to_list_models(response.text, ResponseSchema)
    assert data[0].message == "test_message"

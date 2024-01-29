import datetime

import pytest

import src.services as services
from src.database.tables import User
from src.schemas import UserSchema
from tests.utils import convert_data_to_list_models, convert_data_to_model


@pytest.mark.asyncio
async def test_get_users(monkeypatch, client, auth_token):
    async def mock_get_users(*args, **kwargs) -> list[User]:
        return [
            User(
                id=1,
                email="test@example.ru",
                name="test_name",
                hashed_password="$2b$12$upQ/W0blr23w.gr4ZeOhj.6nNURIz7aBM.1nip.dUgQpawrCfLL1e",
                is_company=True,
                created_at=datetime.datetime.utcnow(),
                hashed_refresh_token="229537f56ebdd599accc289759712a4325885cfb43d05cc568f03d32e837b65d",
            )
        ]

    monkeypatch.setattr(services.UserService, "get_users", mock_get_users)
    response = await client.get("/users", headers=auth_token)

    assert response.status_code == 200
    assert response.encoding == "utf-8"
    data = convert_data_to_list_models(response.text, UserSchema)
    assert data[0].name == "test_name"


@pytest.mark.asyncio
async def test_create_user(monkeypatch, client, auth_token, user_in_schema):
    async def mock_create_user(*args, **kwargs):
        ...

    monkeypatch.setattr(services.UserService, "create_user", mock_create_user)
    response = await client.post("/users/user", headers=auth_token, data=user_in_schema.json())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_user(monkeypatch, client, auth_token, update_user_schema):
    async def mock_update_user(*args, **kwargs):
        ...

    monkeypatch.setattr(services.UserService, "update_user", mock_update_user)
    response = await client.put("/users/user/1", headers=auth_token, data=update_user_schema.json())
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_user(monkeypatch, client, auth_token, user_schema):
    async def mock_get_user(*args, **kwargs):
        return user_schema

    monkeypatch.setattr(services.UserService, "get_user", mock_get_user)
    response = await client.get("/users/user/1", headers=auth_token)
    assert response.status_code == 200
    data = convert_data_to_model(response.text, UserSchema)
    assert data.name == "test_user"
    assert data.email == "test@example.com"


@pytest.mark.asyncio
async def test_delete_user(monkeypatch, client, auth_token):
    async def mock_delete_user(*args, **kwargs):
        ...

    monkeypatch.setattr(services.UserService, "delete_user", mock_delete_user)
    response = await client.delete("/users/user", headers=auth_token)
    assert response.status_code == 204

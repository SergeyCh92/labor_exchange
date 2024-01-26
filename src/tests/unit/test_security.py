import pytest
from jose import jwt

from src.core.security import create_access_token, hash_password, verify_password
from src.settings import SecuritySettings


@pytest.mark.parametrize(
    "password,hash,is_negative_test",
    [
        ("12345678", "$2b$12$P7ej6SlxTOuI5UCllul4g.tWk0DXlkzXwuzwQiXGhLXczQvnYmDIO", True),
        ("12345678", "$2b$18$P7ej6SlxTOuI5UDllul4g.tWk0DXlkzXwuzwQiXGhLXczQvnZmDIO", False),
    ],
)
def test_hash_password(password: str, hash: str, is_negative_test: bool):
    password_hash = hash_password(password)
    assert isinstance(password_hash, str)
    if is_negative_test:
        assert password_hash[:7] == hash[:7]
    else:
        assert password_hash[:7] != hash[:7]


@pytest.mark.parametrize(
    "password,hash,expectation",
    [
        ("12345678", "$2b$12$P7ej6SlxTOuI5UCllul4g.tWk0DXlkzXwuzwQiXGhLXczQvnYmDIO", True),
        ("123456789", "$2b$12$P7ej6SlxTOuI5UCllul4g.tWk0DXlkzXwuzwQiXGhLXczQvnYmDIO", False),
    ],
)
def test_verify_password(password: str, hash: str, expectation: bool):
    result = verify_password(password, hash)
    assert result is expectation


@pytest.mark.parametrize("jwt_data", [{"sub": "example@example.com"}])
def test_create_access_token(jwt_data: dict[str, str], security_settings: SecuritySettings):
    access_token = create_access_token(jwt_data)
    decode_data = jwt.decode(access_token, security_settings.secret_key, algorithms=[security_settings.algorithm])
    assert decode_data["sub"] == jwt_data["sub"]

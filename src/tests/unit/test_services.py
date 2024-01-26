from contextlib import nullcontext as does_not_raise

import pytest
from fastapi import HTTPException

from src.services import AuthService, JobService, ResponseService


@pytest.mark.parametrize(
    "is_company,error_message,expectation",
    [(True, "The error message.", pytest.raises(HTTPException)), (False, "The error message.", does_not_raise())],
)
def test_check_is_company(is_company: bool, error_message: str, expectation, response_service: ResponseService):
    with expectation:
        response_service.check_is_company(is_company, error_message)


@pytest.mark.parametrize(
    "is_company,error_message,expectation",
    [(True, "The error message.", does_not_raise()), (False, "The error message.", pytest.raises(HTTPException))],
)
def test_check_is_user(is_company: bool, error_message: str, expectation, response_service: ResponseService):
    with expectation:
        response_service.check_is_user(is_company, error_message)


@pytest.mark.parametrize(
    "job_user_id,current_user_id,error_message,expectation",
    [(1, 1, "The error message.", does_not_raise()), (1, 2, "The error message.", pytest.raises(HTTPException))],
)
def test_check_is_owner(
    job_user_id: int, current_user_id: int, error_message: str, expectation, job_service: JobService
):
    with expectation:
        job_service.check_is_owner(job_user_id, current_user_id, error_message)


def test_get_string_hash(auth_service: AuthService):
    string_hash = auth_service.get_string_hash("test phrase")
    assert string_hash == "03725d0a96e114361230a7978eeefa0d646d7656dce5e44ae4e70a4dea5e674c"

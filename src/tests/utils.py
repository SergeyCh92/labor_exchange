from pydantic import parse_raw_as, BaseModel
from typing import TypeVar


CommonDataModel = TypeVar("CommonDataModel", bound=BaseModel)


def convert_data_to_model(data: str, data_type: CommonDataModel) -> BaseModel:
    return parse_raw_as(data_type, data)


def convert_data_to_list_models(data: str, data_type: CommonDataModel) -> list[BaseModel]:
    return parse_raw_as(list[data_type], data)

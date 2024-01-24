from pydantic import BaseModel


def to_camel_case(snake_str):
    return "".join(word.capitalize() for word in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str):
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_lower_camel_case
        allow_population_by_field_name = True
        orm_mode = True

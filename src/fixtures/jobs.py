from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from src.database.tables import Job


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = factory.Faker("pyfloat", positive=True, max_value=10)
    salary_to = factory.Faker("pyfloat", min_value=11)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)

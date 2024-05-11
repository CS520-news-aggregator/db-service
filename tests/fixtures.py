import pytest
from utils import get_mongo_client


@pytest.fixture(autouse=True)
def clean_db():
    yield
    get_mongo_client().drop_database("llm_test")

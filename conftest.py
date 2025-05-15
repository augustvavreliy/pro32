import pytest
import logging
from httpx import Client
from faker import Faker


@pytest.fixture(scope="session")
def client():
    headers = {
        "x-requested-with": "XMLHttpRequest",
    }

    client = Client(base_url="https://getscreen.dev/api", headers=headers)
    return client


@pytest.fixture
def fake():

    return Faker()

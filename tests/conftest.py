import pytest
from fastapi.testclient import TestClient

from cost.service.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def good_row():
    return {
        "geo_lat": 55.75,
        "geo_lon": 37.62,
        "region": 77,
        "building_type": 1,
        "level": 3,
        "levels": 9,
        "rooms": 2,
        "area": 54,
        "kitchen_area": 9,
        "object_type": 0,
        "days_passed": 500,
        "mortgage_rate": 9.5,
        "usd_rate": 65,
        "relative_level": 0.3333333333333333,
        "is_last_level": 0,
        "distance": 5
        }
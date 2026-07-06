import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def activities_snapshot():
    """Snapshot and restore the in-memory activities for test isolation."""
    orig = copy.deepcopy(activities_store)
    try:
        yield
    finally:
        activities_store.clear()
        activities_store.update(orig)

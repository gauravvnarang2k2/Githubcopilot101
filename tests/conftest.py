import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    # Arrange: snapshot mutable in-memory state before each test.
    activities_snapshot = copy.deepcopy(activities)

    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        # Assert/cleanup: restore app state so tests remain isolated.
        activities.clear()
        activities.update(activities_snapshot)

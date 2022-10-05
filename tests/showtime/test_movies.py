import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_movies():
    payload = dict(
        username = "aravind.sridhar",
        password = "password"
    )

    client.post("/register/", payload)

    response = client.get('/movies/')
    data = response.data

    assert response.status_code == 200
    assert "count" in data
    assert "next" in data
    assert "previous" in data
    assert "data" in data
    assert len(data['data']) == 10


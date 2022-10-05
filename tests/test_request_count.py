from urllib import response
from django.conf import settings
import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_request_count():
    response = client.get('/request-count/')

    assert response.status_code == 200
    assert response.data["Request Count"] > -1
    assert settings.request_count == response.data["Request Count"]


@pytest.mark.django_db
def test_request_count_reset():
    response = client.post('/request-count/reset/')

    assert response.status_code == 200
    assert response.data["message"]  == "Request Count has been reset!"
    assert settings.request_count == 0
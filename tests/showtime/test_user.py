from urllib import response
from django.conf import settings
import pytest
from rest_framework.test import APIClient
import jwt


client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        username = "aravind.sridhar",
        password = "password"
    )

    response = client.post("/register/", payload)
    data = response.data

    token = data['access_token']
    res_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert token
    assert res_payload['id'] == payload['username']
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user():
    payload = dict(
        username = "aravind.sridhar",
        password = "password"
    )

    client.post("/register/", payload)

    response = client.post("/login/", payload)
    data = response.data

    token = data['access_token']
    res_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert token
    assert res_payload['id'] == payload['username']
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail_user():
    payload = dict(
        username = "aravind21_not_registered",
        password = "wrong_password"
    )

    response = client.post("/login/", payload)

    assert response.status_code == 403


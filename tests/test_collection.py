import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_collection_create():
    payload = dict(
        username = "aravind.sridhar",
        password = "password"
    )

    client.post("/register/", payload)

    movies_payload = [
        dict(
            title = "movie_title",
            description = "movie_description",
            genres = "movie_genres",
            uuid = "4cac8453-a512-4bde-b79d-e2f5bc897a5f"
        )
    ]

    collection_payload = dict(
        title = "collection_title",
        description = "collection_description",
        movies = movies_payload,
        username = payload['username']
    )

    response = client.post("/collection/", collection_payload, format='json')

    assert response.status_code == 200
    assert 'collection_uuid' in response.data


@pytest.mark.django_db
def test_collection_get():
    payload = dict(
        username = "aravind.sridhar",
        password = "password"
    )

    client.post("/register/", payload)

    movies_payload = [
        dict(
            title = "movie_title",
            description = "movie_description",
            genres = "movie_genres",
            uuid = "4cac8453-a512-4bde-b79d-e2f5bc897a5f"
        )
    ]

    collection_payload = dict(
        title = "collection_title",
        description = "collection_description",
        movies = movies_payload,
        username = payload['username']
    )

    client.post("/collection/", collection_payload, format='json')

    response = client.get("/collection/")

    assert response.status_code == 200
    assert response.data['is_success'] == True
    assert "favourite_genres" in response.data['data']

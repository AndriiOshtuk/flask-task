import pytest


@pytest.mark.usefixtures("app")
def test_about(client):
    response = client.get("/about/")

    assert response.status_code == 200
    assert response.json == {"status": "Alive!"}

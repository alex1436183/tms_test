import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    # Проверяем, что статус ответа 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе содержится строка "Information"
    assert b"Information" in response.data
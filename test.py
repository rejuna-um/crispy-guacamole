import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_product_details(client):
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    for id, product_name in data:
        assert isinstance(product_name, str)
        assert product_name != ""
        assert id != ""

import pytest

from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()



# TEST HOME

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Inventory API is running" in res.data



# TEST GET ALL

def test_get_inventory(client):
    res = client.get("/inventory")
    assert res.status_code == 200



# TEST GET ONE ITEM

def test_get_single_item(client):
    res = client.get("/inventory/1")
    assert res.status_code in [200, 404]



# TEST POST 

def test_post_inventory(client):
    res = client.post(
        "/inventory",
        json={
            "barcode": "999999",
            "product_name": "Test Product",
            "brand": "Test Brand",
            "price": 10,
            "stock": 5,
            "ingredients": "Test ingredients"
        }
    )

    assert res.status_code == 201



# TEST POST INVALID 
def test_post_invalid(client):
    res = client.post("/inventory", json={})
    assert res.status_code == 400



# TEST PATCH

def test_patch_inventory(client):
    res = client.patch(
        "/inventory/1",
        json={
            "price": 99.99,
            "stock": 100
        }
    )

    assert res.status_code in [200, 404]



# TEST PATCH INVALID

def test_patch_invalid(client):
    res = client.patch("/inventory/1", json={})
    assert res.status_code in [200, 400, 404]


# TEST DELETE 
def test_delete_inventory(client):

    res = client.delete("/inventory/1")

    assert res.status_code in [200, 404]
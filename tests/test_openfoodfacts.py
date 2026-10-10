from unittest.mock import patch

from openfoodfacts import fetch_product_by_barcode



# SUCCESS CASE

@patch("openfoodfacts.requests.get")
def test_fetch_product_success(mock_get):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds, sugar"
        }
    }

    result = fetch_product_by_barcode("123456")

    assert result is not None
    assert result["barcode"] == "123456"
    assert result["product_name"] == "Organic Almond Milk"
    assert result["brand"] == "Silk"



# PRODUCT NOT FOUND

@patch("openfoodfacts.requests.get")
def test_fetch_product_not_found(mock_get):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 0
    }

    result = fetch_product_by_barcode("000000")

    assert result is None



# API FAILURE

@patch("openfoodfacts.requests.get")
def test_fetch_product_api_failure(mock_get):

    mock_get.return_value.status_code = 500

    result = fetch_product_by_barcode("123456")

    assert result is None
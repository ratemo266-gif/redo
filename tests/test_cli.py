from unittest.mock import patch

import cli



# TEST: VIEW INVENTORY

@patch("cli.safe_request")
def test_view_inventory(mock_request):

    mock_request.return_value = (
        [
            {
                "id": 1,
                "barcode": "123",
                "product_name": "Milk",
                "brand": "BrandX",
                "price": 10,
                "stock": 5
            }
        ],
        200
    )

    cli.view_inventory()

    mock_request.assert_called_once_with("GET", "/inventory")



# TEST: ADD ITEM

@patch("cli.input", side_effect=[
    "111111",   # barcode
    "Milk",     # product_name
    "BrandX",   # brand
    "5.5",      # price
    "10",       # stock
    "fresh milk"  # ingredients
])
@patch("cli.safe_request")
def test_add_item(mock_request, mock_input):

    mock_request.return_value = (
        {"message": "Item added successfully"},
        201
    )

    cli.add_item()

    mock_request.assert_called_once()



# TEST: UPDATE ITEM

@patch("cli.input", side_effect=[
    "1",    # id
    "20",   # price
    "50"    # stock
])
@patch("cli.safe_request")
def test_update_item(mock_request, mock_input):

    mock_request.return_value = (
        {"message": "Item updated successfully"},
        200
    )

    cli.update_item()

    mock_request.assert_called_once()


# TEST: DELETE ITEM

@patch("cli.input", return_value="1")
@patch("cli.safe_request")
def test_delete_item(mock_request, mock_input):

    mock_request.return_value = (
        {"message": "Item deleted successfully"},
        200
    )

    cli.delete_item()

    mock_request.assert_called_once_with("DELETE", "/inventory/1")



# TEST: FETCH PRODUCT (OPENFOODS)

@patch("cli.input", return_value="123456")
@patch("cli.safe_request")
def test_fetch_product(mock_request, mock_input):

    mock_request.return_value = (
        {"product": "mock data"},
        200
    )

    cli.fetch_product()

    mock_request.assert_called_once_with(
        "GET",
        "/inventory/fetch/123456"
    )



# TEST: IMPORT PRODUCT (OPENFOODS)

@patch("cli.input", return_value="123456")
@patch("cli.safe_request")
def test_import_product(mock_request, mock_input):

    mock_request.return_value = (
        {"message": "Product imported"},
        201
    )

    cli.import_product()

    mock_request.assert_called_once_with(
        "GET",
        "/inventory/import/123456"
    )
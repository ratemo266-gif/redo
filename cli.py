import requests

BASE_URL = "http://127.0.0.1:5000"


# -----------------------------
# SAFE REQUEST WRAPPER
# -----------------------------
def safe_request(method, endpoint, **kwargs):
    try:
        url = f"{BASE_URL}{endpoint}"
        res = requests.request(method, url, timeout=5, **kwargs)
        try:
            return res.json(), res.status_code
        except ValueError as exc:
            return {"error": f"Invalid JSON response: {exc}"}, res.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "API server not running"}, 500
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}, 500
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}, 500



# FORMAT OUTPUT

def print_items(items):
    if isinstance(items, list):
        for item in items:
            print(f"""
ID: {item.get('id')}
Barcode: {item.get('barcode')}
Name: {item.get('product_name')}
Brand: {item.get('brand')}
Price: {item.get('price')}
Stock: {item.get('stock')}
----------------------------
""")
    else:
        print(items)



# VIEW INVENTORY

def view_inventory():
    data, _ = safe_request("GET", "/inventory")
    print_items(data)



# ADD ITEM

def add_item():
    try:
        data = {
            "barcode": input("Barcode: "),
            "product_name": input("Product Name: "),
            "brand": input("Brand: "),
            "price": float(input("Price: ")),
            "stock": int(input("Stock: ")),
            "ingredients": input("Ingredients: ")
        }
    except ValueError:
        print({"error": "Invalid numeric input"})
        return

    res, _ = safe_request("POST", "/inventory", json=data)
    print(res)



# UPDATE ITEM

def update_item():
    item_id = input("Enter ID: ")

    data = {}

    print("Leave blank to skip fields")

    price = input("New Price: ")
    stock = input("New Stock: ")

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            print({"error": "Invalid price"})
            return

    if stock:
        try:
            data["stock"] = int(stock)
        except ValueError:
            print({"error": "Invalid stock"})
            return

    res, _ = safe_request("PATCH", f"/inventory/{item_id}", json=data)
    print(res)



# DELETE ITEM

def delete_item():
    item_id = input("Enter ID: ")
    res, _ = safe_request("DELETE", f"/inventory/{item_id}")
    print(res)



# FETCH OPENFOODS PRODUCT

def fetch_product():
    barcode = input("Enter barcode: ")
    res, _ = safe_request("GET", f"/inventory/fetch/{barcode}")
    print(res)



# IMPORT OPENFOODS PRODUCT

def import_product():
    barcode = input("Enter barcode: ")
    res, _ = safe_request("GET", f"/inventory/import/{barcode}")
    print(res)



# MENU

def menu():
    while True:
        print("\n===== INVENTORY ADMIN CLI =====")
        print("1. View Inventory")
        print("2. Add Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Fetch Product (OpenFoodFacts)")
        print("6. Import Product (OpenFoodFacts)")
        print("0. Exit")

        choice = input("Choose option: ")

        actions = {
            "1": view_inventory,
            "2": add_item,
            "3": update_item,
            "4": delete_item,
            "5": fetch_product,
            "6": import_product
        }

        if choice == "0":
            print("Exiting CLI...")
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()
# Inventory Management System (Flask REST API + CLI)

A full-stack backend inventory management system built with **Flask**, featuring CRUD operations, external API integration with OpenFoodFacts, a CLI admin tool, and full unit testing.

---

# Features

*  Full REST API (CRUD operations)
* External API integration (OpenFoodFacts)
* CLI admin tool for terminal management
* Unit testing with pytest + mocking
* In-memory database (Python list simulation)
* Proper error handling & validation

---

# Tech Stack

* Python 3.11+
* Flask
* Requests
* Pytest
* Unittest.mock
* Pipenv

---

#  Project Structure

```
inventory-management/
│
├── app.py
├── routes.py
├── inventory.py
├── cli.py
├── openfoodfacts.py
│
├── tests/
│   ├── test_api.py
│   ├── test_cli.py
│   └── test_openfoodfacts.py
│
└── README.md
```

---

# Installation & Setup

## 1. Clone repository

```bash
git clone <your-repo-url>
cd inventory-management
```

---

## 2. Install dependencies (Pipenv)

```bash
pipenv install
pipenv shell
```

---

## 3. Run Flask server

```bash
pipenv run python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

# API Endpoints

## Home

### GET /

```json
{
  "message": "Inventory API is running."
}
```

---

##  Inventory CRUD

### GET all items

```
GET /inventory
```

---

### GET single item

```
GET /inventory/<id>
```

---

### POST add item

```
POST /inventory
Content-Type: application/json
```

```json
{
  "barcode": "123456",
  "product_name": "Milk",
  "brand": "BrandX",
  "price": 5.5,
  "stock": 10,
  "ingredients": "Milk, sugar"
}
```

---

### PATCH update item

```
PATCH /inventory/<id>
```

```json
{
  "price": 10.0,
  "stock": 20
}
```

---

### DELETE item

```
DELETE /inventory/<id>
```

---

#  OpenFoodFacts Integration

External API used:

 OpenFoodFacts

---

## Fetch product (external API only)

```
GET /inventory/fetch/<barcode>
```

### Response:

```json
{
  "message": "Product fetched successfully",
  "product": {
    "barcode": "737628064502",
    "product_name": "Organic Almond Milk",
    "brand": "Silk",
    "ingredients": "Water, almonds..."
  }
}
```

---

##  Import product into inventory

```
GET /inventory/import/<barcode>
```

This:

* Fetches from OpenFoodFacts
* Adds to local inventory automatically

---

# CLI TOOL

Run CLI:

```bash
pipenv run python cli.py
```

---

## CLI Features

* View inventory
* Add item
* Update item
* Delete item
* Fetch product (OpenFoodFacts)
* Import product into system

---

## CLI Menu

```
===== INVENTORY ADMIN CLI =====
1. View Inventory
2. Add Item
3. Update Item
4. Delete Item
5. Fetch Product (OpenFoodFacts)
6. Import Product (OpenFoodFacts)
0. Exit
```

---

# Testing

## Run all tests

```bash
PYTHONPATH=. pipenv run pytest -v
```

---

## Test Coverage

### ✔ API Tests (`test_api.py`)

* GET all items
* GET single item
* POST item
* PATCH item
* DELETE item
* Error handling cases

---

### ✔ CLI Tests (`test_cli.py`)

* Mock user input
* Mock API requests
* Test all CLI commands

---

### ✔ External API Tests (`test_openfoodfacts.py`)

* Mock OpenFoodFacts API response
* Test success case
* Test product not found
* Test API failure

---

# Key Design Decisions

* In-memory list used as database for simplicity
* Flask Blueprint used for modular routing
* External API isolated in separate module
* CLI uses REST API (not direct database access)
* All external calls mocked in tests for reliability

---

#  Error Handling

System handles:

* Missing JSON body → 400
* Missing fields → 400
* Item not found → 404
* API failures → graceful fallback
* CLI connection errors → handled safely

---

#  What Makes This Project Strong

✔ Full REST API
✔ External API integration
✔ CLI interface
✔ Unit + integration testing
✔ Mocking strategy
✔ Clean architecture
✔ Real-world design pattern

---


---

#  Future Improvements (Optional)

* Add SQLite or PostgreSQL database
* Add authentication (admin login)
* Add pagination & search filters
* Dockerize the application
* Deploy to cloud (Render / Railway / AWS)

---

# Author

Built as a full-stack backend lab project using Flask and Python best practices.
# redo

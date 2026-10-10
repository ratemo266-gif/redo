from flask import Blueprint, jsonify, request  # type: ignore

from inventory import inventory
from openfoodfacts import fetch_product_by_barcode

inventory_bp = Blueprint("inventory", __name__)



# HOME ROUTE

@inventory_bp.route("/")
def home():
    return jsonify({
        "message": "Inventory API is running."
    }), 200



# GET ALL INVENTORY

@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200



# GET SINGLE ITEM

@inventory_bp.route("/inventory/<int:id>", methods=["GET"])
def get_inventory_item(id):

    for item in inventory:
        if item["id"] == id:
            return jsonify(item), 200

    return jsonify({
        "error": "Item not found"
    }), 404



# ADD NEW ITEM (POST)

@inventory_bp.route("/inventory", methods=["POST"])
def add_inventory_item():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    required_fields = [
        "barcode",
        "product_name",
        "brand",
        "price",
        "stock",
        "ingredients"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": data["barcode"],
        "product_name": data["product_name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"],
        "ingredients": data["ingredients"]
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Item added successfully",
        "item": new_item
    }), 201



# UPDATE ITEM (PATCH)

@inventory_bp.route("/inventory/<int:id>", methods=["PATCH"])
def update_inventory_item(id):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    allowed_fields = [
        "barcode",
        "product_name",
        "brand",
        "price",
        "stock",
        "ingredients"
    ]

    for item in inventory:
        if item["id"] == id:

            for key in data:
                if key in allowed_fields:
                    item[key] = data[key]

            return jsonify({
                "message": "Item updated successfully",
                "item": item
            }), 200

    return jsonify({
        "error": "Item not found"
    }), 404



# DELETE ITEM

@inventory_bp.route("/inventory/<int:id>", methods=["DELETE"])
def delete_inventory_item(id):

    for item in inventory:
        if item["id"] == id:

            inventory.remove(item)

            return jsonify({
                "message": "Item deleted successfully",
                "deleted_item": item
            }), 200

    return jsonify({
        "error": "Item not found"
    }), 404



# OPENFOODFACTS INTEGRATION

@inventory_bp.route("/inventory/fetch/<barcode>", methods=["GET"])
def fetch_from_openfoodfacts(barcode):

    product = fetch_product_by_barcode(barcode)

    if not product:
        return jsonify({
            "error": "Product not found in OpenFoodFacts"
        }), 404

    return jsonify({
        "message": "Product fetched successfully",
        "product": product
    }), 200



# FETCH + ADD TO INVENTORY

@inventory_bp.route("/inventory/import/<barcode>", methods=["GET"])
def import_from_openfoodfacts(barcode):

    product = fetch_product_by_barcode(barcode)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": product["barcode"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "price": 0.0,
        "stock": 0,
        "ingredients": product["ingredients"]
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Product imported into inventory",
        "item": new_item
    }), 201
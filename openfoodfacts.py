import time

import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"


def fetch_product_by_barcode(barcode):
    """
    Fetch product data from OpenFoodFacts API (robust version)
    """

    url = f"{BASE_URL}/{barcode}.json"

    for attempt in range(2):  
        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                return None

            data = response.json()

            
            # check status first
            
            if data.get("status") != 1:
                return None

            product = data.get("product") or {}

            
            product_name = product.get("product_name")
            if not product_name:
                product_name = product.get("generic_name", "Unknown")

            brands = product.get("brands")
            if not brands:
                brands = "Unknown"
            else:
                # OpenFoodFacts sometimes returns multiple brands
                brands = brands.split(",")[0].strip()

            ingredients = product.get("ingredients_text")
            if not ingredients:
                ingredients = "Not available"

            return {
                "barcode": barcode,
                "product_name": product_name,
                "brand": brands,
                "ingredients": ingredients
            }

        except requests.exceptions.RequestException:
            # retry once after small delay
            if attempt == 0:
                time.sleep(0.5)
                continue
            return None

        except (ValueError, TypeError):
            return None
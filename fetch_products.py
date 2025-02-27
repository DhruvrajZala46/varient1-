import os
import requests

# Load sensitive data from environment variables
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")  
if not SHOPIFY_STORE_URL:
    raise ValueError("Missing SHOPIFY_STORE_URL. Set it as an environment variable.")  
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def fetch_products():
    if not ACCESS_TOKEN:
        raise ValueError("Missing Shopify access token. Set SHOPIFY_ACCESS_TOKEN as an environment variable.")

    url = f"{SHOPIFY_STORE_URL.rstrip('/')}/admin/api/2023-10/products.json"
    headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        products = response.json().get("products", [])
        
        # Extract image URL from 'images' field
        return [
            {
                "title": p["title"],
                "description": p["body_html"],
                "price": p["variants"][0]["price"],
                "image": p["images"][0]["src"] if p["images"] else "https://default-image.com/no-image.jpg"
            } 
            for p in products
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []

if __name__ == "__main__":
    products = fetch_products()
    print(products)

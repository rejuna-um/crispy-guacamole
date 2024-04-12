import json

from flasgger import Swagger
from flask import Flask
from requests_cache import CachedSession

app = Flask(__name__)
Swagger(app)
# Cache for 20 mins. Ideally we would update the cache it on update/delete of the products
session = CachedSession(cache_name='lululemon_cache', backend='sqlite',
                        expire_after=1200)

URLS = [
    "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json",
    "https://shop.lululemon.com/c/accessories/_/N-1z0xcmkZ1z0xl44Z8ok?format=json"
]


def fetch_product_details():
    result = []
    for url in URLS:
        response = session.get(url)
        data = response.json()
        records = (data.get("contents", [])[0].get("mainContent", [])[0].get("contents", [])[0].get("records", []))
        for record in records:
            product_details = {}
            product_name = record.get("attributes", {}).get("product.displayName", "")[0]
            product_details["id"] = record.get("attributes", {}).get("common.id")[0]
            product_details["display_name"] = product_name
            result.append(product_details)
    return result


@app.route('/api/products', methods=['GET'])
def get_product_details():
    """
       Retrieve product details from the Lululemon website for women's leggings and accessories.
       ---
       tags:
         - Product Details
       swagger: "2.0"
       responses:
         200:
           description: A list of product details.
           schema:
             type: array
             items:
               type: object
               properties:
                 id:
                   type: string
                   description: The unique identifier of the product.
                 display_name:
                   type: string
                   description: The display name of the product.
    """
    product_details = fetch_product_details()
    return {
        'statusCode': 200,
        'body': json.loads(json.dumps(product_details, indent = 2))
    }


if __name__ == '__main__':
    app.run()

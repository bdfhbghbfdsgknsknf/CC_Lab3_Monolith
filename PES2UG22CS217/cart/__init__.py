import json
from typing import List
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[get_product(prod_id) for prod_id in data.get('contents', [])],
            cost=data['cost'],
        )

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        # Parse contents safely as JSON instead of eval
        contents = json.loads(cart_detail['contents'])
        for product_id in contents:
            product = get_product(product_id)
            if product:
                items.append(product)

    return items

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)

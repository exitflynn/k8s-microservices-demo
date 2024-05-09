from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import json

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

class ProductCatalog:
    def __init__(self, file_path):
        self.file_path = file_path
        self.products = self.load_products()

    def load_products(self):
        try:
            with open(self.file_path, 'r') as file:
                products = json.load(file)
        except FileNotFoundError:
            products = []
        return products

    def save_products(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.products, file, indent=4)

    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
            self.save_products()

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.get('id') != product_id]
        self.save_products()

    def update_product(self, product_id, new_data):
        for product in self.products:
            if product.get('id') == product_id:
                product.update(new_data)
                break
        self.save_products()

    def get_product(self, product_id):
        for product in self.products:
            if product.get('id') == product_id:
                return product
        return None

    def get_all_products(self):
        return self.products

catalog = ProductCatalog("products.json")

@app.get('/')
def get_products():
    return {"message": "Welcome to the product catalog! Use the /products endpoint to access products"}

@app.get('/products', response_model=List[Product])
def get_products():
    return catalog.get_all_products()

@app.get('/products/{product_id}', response_model=Product)
def get_product(product_id: int):
    product = catalog.get_product(product_id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post('/products', status_code=201)
def add_product(product: Product):
    catalog.add_product(product.dict())
    return {"message": "Product added successfully"}

@app.put('/products/{product_id}')
def update_product(product_id: int, product: Product):
    catalog.update_product(product_id, product.dict())
    return {"message": "Product updated successfully"}

@app.delete('/products/{product_id}')
def delete_product(product_id: int):
    if product_id not in [p.get('id') for p in catalog.get_all_products()]:
        raise HTTPException(status_code=404, detail="Product not found")
    catalog.remove_product(product_id)
    return {"message": "Product deleted successfully"}

from fastapi import FastAPI, HTTPException, Query, Depends
from mysql.connector import connect, Error
from pydantic import BaseModel

# Replace 'user', 'password', 'host', 'database' with your MySQL connection details
DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "host",
    "database": "databass",
}

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

def get_connection():
    try:
        connection = connect(**DB_CONFIG)
        yield connection
    finally:
        connection.close()

# API Endpoints

@app.post("/products/", response_model=Product)
async def create_product(product: Product, db: Depends(get_connection)):
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
            (product.name, product.description, product.price),
        )
        db.commit()
        product.id = cursor.lastrowid
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")
    finally:
        cursor.close()
    return product

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Depends(get_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error reading product: {str(e)}")
    finally:
        cursor.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=list[Product])
async def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Depends(get_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products LIMIT %s OFFSET %s", (limit, skip))
        products = cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error listing products: {str(e)}")
    finally:
        cursor.close()
    return products

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, updated_product: Product, db: Depends(get_connection)):
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s",
            (updated_product.name, updated_product.description, updated_product.price, product_id),
        )
        db.commit()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")
    finally:
        cursor.close()
    return updated_product

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int, db: Depends(get_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.commit()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
    finally:
        cursor.close()
    return product

# Search and Filter

@app.get("/products/search/", response_model=list[Product])
async def search_products(query: str = Query(..., min_length=3), db: Depends(get_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{query}%",))
        products = cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")
    finally:
        cursor.close()
    return products


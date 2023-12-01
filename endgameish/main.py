from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Replace 'mysql://user:password@hostname/dbname' with your MySQL connection string
DATABASE_URL = "mysql://flynn:root@chibacityblues/warehouse-databass"
CDN_BASE_URL = "http://127.0.0.1:5000"

database = Database(DATABASE_URL)
metadata = declarative_base()

class Product(metadata):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)  # Store CDN URL for the product image

engine = create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# API Endpoints

@app.post("/products/", response_model=Product)
async def create_product(product: Product, image: UploadFile = File(...)):
    db = SessionLocal()

    # Save the image to the CDN
    image_url = CDN_BASE_URL + image.filename
    with open(image.filename, "wb") as image_file:
        image_file.write(image.file.read())

    # Update the product with the CDN URL
    product.image_url = image_url
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return product

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=list[Product])
async def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    db = SessionLocal()
    products = db.query(Product).offset(skip).limit(limit).all()
    db.close()
    return products

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, updated_product: Product):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_product.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    db.close()
    return product

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.close()
    return product

# Search and Filter

@app.get("/products/search/", response_model=list[Product])
async def search_products(query: str = Query(..., min_length=3)):
    db = SessionLocal()
    products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
    db.close()
    return products

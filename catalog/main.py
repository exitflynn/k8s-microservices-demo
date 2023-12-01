from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import mysql.connector
from mysql.connector import errorcode
import uuid
import os

app = FastAPI()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
db_config = {
    "host": "10.99.164.26",
    "user": "root",
    "password": "root",
    "database": "warehouse_databass",
    "port": "3306",
}

# CDN Configuration
cdn_url = "http://10.107.108.239:5000/cdn/"
default_image_path = "ash.jpeg"

# Connect to MySQL database
try:
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Wrong MySQL username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(f"Error: {err}")
    exit(1)


def generate_warehouse_number():
    return str(uuid.uuid4())[:8].replace('-', '').upper()


@app.post("/products/")
async def create_product(
    name: str,
    price: float,
    quantity: int,
    image: Optional[UploadFile] = File(None)
):
    # Generate a warehouse number
    warehouse_number = generate_warehouse_number()

    # Save image to CDN or use default image
    if image:
        # Save the image to the CDN and get the link
        image_link = cdn_url + image.filename
        with open(image.filename, "wb") as image_file:
            image_file.write(image.file.read())
    else:
        # Use default image
        image_link = cdn_url + default_image_path

    # Insert product information into the database
    try:
        add_product = (
            "INSERT INTO products "
            "(name, price, quantity, image_link, warehouse_number) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        product_data = (name, price, quantity, image_link, warehouse_number)
        cursor.execute(add_product, product_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return JSONResponse(content={"message": "Product created successfully"}, status_code=201)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


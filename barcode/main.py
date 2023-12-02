from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import barcode
from barcode.writer import ImageWriter
from barcode import EAN8
import requests
from io import BytesIO

app = FastAPI()

# CDN Configuration
cdn_upload_url = "http://192.168.49.2:31551/upload"

def generate_barcode_image(data):
    mycode = EAN8(data)
    mycode.save("code")

@app.post("/generate-barcode/")
async def generate_and_upload_barcode(string_data: str):
    try:
        # Generate barcode image
        barcode_image = generate_barcode_image(string_data)

        # Upload barcode image to CDN
        file = {"file": open("code.svg", "rb")}
        response = requests.post(cdn_upload_url, files=file)

        if response.status_code == 200:
            return JSONResponse(content={"message": "Barcode image uploaded successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to upload barcode image to CDN")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


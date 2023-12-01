from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import barcode
from barcode.writer import ImageWriter
import requests
from io import BytesIO

app = FastAPI()

# CDN Configuration
cdn_upload_url = "192.168.49.2:31551"

def generate_barcode_image(data):
    # Generate barcode using Code128 format
    code = barcode.get('code128', data, writer=ImageWriter)
    barcode_image = code.render()

    # Convert barcode image to bytes
    image_bytes = BytesIO()
    barcode_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes

@app.post("/generate-barcode/")
async def generate_and_upload_barcode(string_data: str):
    try:
        # Generate barcode image
        barcode_image = generate_barcode_image(string_data)

        # Upload barcode image to CDN
        files = {"file": ("barcode.png", barcode_image, "image/png")}
        response = requests.post(cdn_upload_url, files=files)

        if response.status_code == 200:
            return JSONResponse(content={"message": "Barcode image uploaded successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to upload barcode image to CDN")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


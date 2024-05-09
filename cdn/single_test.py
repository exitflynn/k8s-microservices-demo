import requests

# Specify the URL to send the POST request
url = 'http://172.17.0.2:5000/upload'

# Path to the image file
file_path = 'test/oral-b-toothbrush.jpg'


# Open the file
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

# Print the response from the Flask application
print(response.text)

# Check the response
if response.status_code == 200:
    print("Image sent successfully!")
else:
    print("Failed to send the image. Status code:", response.status_code)
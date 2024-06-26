from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)

# Define the directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def respond():
    return "Hey there! To send a file, use the /upload endpoint."

@app.route('/uploads/<filename>')
def serve_file(filename):
    # Serve uploaded files
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file
    if file:
        filename = file.filename.split('/')[-1]
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        cdn_link = f"http://{request.host}/{filename}"
        return jsonify({'cdn_link': cdn_link}), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(host='0.0.0.0', port=5000, debug=True)

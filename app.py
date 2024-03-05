# app.py
from flask import Flask, render_template, request, jsonify
from ForgeryDetection import Detect
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
        file.save(filename)
        return jsonify({'filename': filename})

    return jsonify({'error': 'Invalid file type'})

@app.route('/copy_move_forgery', methods=['POST'])
def copy_move_forgery():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
    eps = 60
    min_samples = 2

    if not os.path.exists(path):
        return jsonify({'error': 'Input image not found'})

    detect = Detect(path)
    forgery = detect.locateForgery(eps, min_samples)

    if forgery is None:
        result = {'result': 'ORIGINAL IMAGE', 'color': 'green'}
    else:
        forgery_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
        cv2.imwrite(forgery_path, forgery)
        result = {'result': 'Image Forged', 'color': 'red', 'forgery_path': forgery_path}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

import base64
import random
import numpy as np
from flask import Flask, request, jsonify
import cv2

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/process_image", methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image provided', 400

    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    original_image = cv2.resize(image, (350, 450))
    transformed_image = random_color_transform(original_image)

    _, original_image_buf = cv2.imencode('.png', original_image)
    _, transformed_image_buf = cv2.imencode('.png', transformed_image)

    original_image_base64 = base64.b64encode(original_image_buf).decode('utf-8')
    transformed_image_base64 = base64.b64encode(transformed_image_buf).decode('utf-8')

    return jsonify({
        'original_image': original_image_base64,
        'transformed_image': transformed_image_base64,
    })

def random_color_transform(image):
    rows, cols, channels = image.shape
    for channel in range(channels):
        random_shift = random.randint(-100, 100)
        image[:, :, channel] = np.clip(image[:, :, channel] + random_shift, 0, 255)
    return image

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

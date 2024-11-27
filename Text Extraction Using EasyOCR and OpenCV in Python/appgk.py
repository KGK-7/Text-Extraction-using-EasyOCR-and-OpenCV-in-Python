from flask import Flask, render_template, request, jsonify
import cv2
import easyocr
import numpy as np
import pyttsx3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def process_image_and_extract_text(image):
    # Instance text detector
    reader = easyocr.Reader(['en'], gpu=False)

    # Detect text on image
    text_results = reader.readtext(image)

    # Threshold for confidence score
    threshold = 0.70

    # Initialize variables to track the highest scoring text
    highest_score = 0
    highest_score_text = ""

    # Draw bbox and text for clearly visible text
    for t_, t in enumerate(text_results):
        bbox, text, score = t
        if score > threshold and text.isalnum():  # Check if text is alphanumeric
            top_left = tuple(bbox[0])
            bottom_right = tuple(bbox[2])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 5)
            cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

            # Update the highest scoring text if the current text has a higher score and more meaningful content
            if score > highest_score and len(text) > len(highest_score_text):
                highest_score = score
                highest_score_text = text

    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Configure the engine to only say the text
    engine.setProperty('rate', 85)  # Speed of speech
    engine.setProperty('volume', 10.9)  # Volume level

    # Say the text
    engine.say(highest_score_text)
    engine.runAndWait()

    # Convert image to base64 for displaying in HTML
    _, buffer = cv2.imencode('.png', image)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return highest_score_text, img_str

@app.route('/')
def index():
    return render_template('index.html') #create your own html and css files are link with this

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Read image
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), -1)

    # Process image and extract text
    highest_score_text, img_str = process_image_and_extract_text(img)

    return jsonify({'text': highest_score_text, 'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)



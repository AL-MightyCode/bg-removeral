from flask import Flask, render_template, request, send_file
import os
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400

    image_file = request.files['image']
    input_image = Image.open(image_file.stream)

    # Remove background using rembg
    output_image = remove(input_image)

    # Save the processed image to a BytesIO object
    img_byte_arr = BytesIO()
    output_image.save(img_byte_arr, format='PNG', quality=100)  # Ensure high quality
    img_byte_arr.seek(0)

    # Return the processed image with correct filename
    return send_file(
        img_byte_arr,
        mimetype='image/png',
        as_attachment=True,
        download_name='output.png'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port) 

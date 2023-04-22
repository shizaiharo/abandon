from flask import Flask, request

import PIL.Image
from manga_ocr import MangaOcr

app = Flask(__name__)
mocr = MangaOcr()

@app.route('/ocr', methods=['POST'])
def ocr():
    # Get the uploaded image from the request
    image = request.files['image']

    # Save the image to a temporary file
    image_path = 'temp.jpg'
    image.save(image_path)

    # Use MangaOcr to extract text from the image
    img = PIL.Image.open(image_path)
    text = mocr(img)

    # Delete the temporary file
    os.remove(image_path)

    # Return the extracted text
    return text

if __name__ == '__main__':
    app.run()

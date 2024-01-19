from flask import Flask, render_template, request, redirect, url_for
import os, re
from werkzeug.utils import secure_filename
from ImageQuadtree import Quadtree
from PIL import Image, ImageFile
import shutil
from ImageCombine_def import combine
from Pytesseract import tes

app = Flask(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True
# upload_path = "upload"
MainPath = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
print(MainPath)
temp_path = MainPath +"/temp"
app.secret_key = "s1e2a3n4"
app.config['UPLOAD_FOLDER'] = MainPath + '/static/upload'  # Folder to store uploaded images
# def gn(x):
#     match = re.search(r'_(\d+)\(', x)
#     if match:
#         return int(match.group(1))
#     else:
#         return float('inf')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files
    
    # # Create a directory to store the uploaded images
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])
    # if not os.path.exists(temp_path):
    #     os.makedirs(temp_path)
    
    
    # Save the uploaded images to the server
    for file in folder:
        filename = secure_filename(file.filename)
        # image = Image.open(filename)
        # return render_template('myconsole.html', info=filename)
        # image = image.convert("RGB")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('processed_images'))


@app.route('/processed_images')
def processed_images():
    # Get the list of processed images in the 'uploads' folder
    origenal_images_path = os.listdir(app.config['UPLOAD_FOLDER'])
    txt = 0
    for image_name in origenal_images_path:
        txt += 1
        image_quadtree = Quadtree()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        image = Image.open(image_path)
    
        image_quadtree.check_img(MainPath + "/temp/"+image_name.split('.')[0]+"_0",image)
        words_images_path = image_quadtree.get_images()
        #words_images_path = sorted(words_images_path, key=lambda x: gn(x))
        # tes(combine(words_images_path))
        combine(words_images_path)
        for words_image_path in words_images_path:
            word_image = Image.open(MainPath + "/temp/"+words_image_path)
            filename = words_image_path
            word_image.save(app.config['UPLOAD_FOLDER'] + "/" + filename)

        
        #     # os.remove("temp/"+words_image_path) 
        # txt += image_quadtree.content
            
    # return render_template('myconsole.html', info=txt)
    return render_template('processed_images.html', OGimages=origenal_images_path)



if __name__ == '__main__': 
    # os.system("cls")
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path) 

    app.run(host="0.0.0.0", port=6969)
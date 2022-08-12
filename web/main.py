from tkinter import ALL
from flask import Flask
from flask import request, escape, render_template
from gblur import gaussRGB
from werkzeug.utils import secure_filename
import os
from google.cloud import storage

ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

app = Flask(__name__)

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['img-proc-fb']

@app.route("/")
def index():   
    return render_template('load.html', title='Upload Image', content="Upload image to blur")

@app.route("/uploader", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        f = request.files['file']
        # Create a cloud storage client
        gcs = 
        sfname = 'static/images/'+str(secure_filename(f.filename))
        print(os.path.splitext(sfname)[1])
        if os.path.splitext(sfname)[1] in ALLOWED_EXTENSIONS:
            f.save(sfname)
            sigma = 5
            bname = gaussRGB(sigma, sfname)

            return render_template('result.html', title='Result', imgpath=bname)
        else:
            return render_template('load.html', title='Upload Image', content="Incorrect Filetype, must be .png, .jpg or .jpeg.")
    
        
        


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


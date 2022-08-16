from tkinter import ALL
from flask import Flask
from flask import request, escape, render_template
from flask_bootstrap import Bootstrap5

from gblur import gaussRGB
from werkzeug.utils import secure_filename
import io, os
from google.cloud import storage
import random



ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

app = Flask(__name__)

bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'


@app.route("/")
def index():   
    return render_template('load.html', title='tooNOISY', content="Upload image to blur")

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/uploader", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        f = request.files['file']
        f_name = secure_filename(f.filename)

        # Create a cloud storage client
        client = storage.Client.from_service_account_json('balmy-nuance-359122.json')
        
        # Set image hash
        im_hash = random.randint(1,9999999)

        # Get the bucket that the image will be uploaded to
        bucket = client.get_bucket('img-proc-fb')

        sfname = 'Uploaded image' + str(im_hash) + os.path.splitext(f_name)[1]
        

        if os.path.splitext(f_name)[1] in ALLOWED_EXTENSIONS:
            # Create new blob and upload the original image
            # in_blob = bucket.blob(sfname)
            # in_blob.upload_from_file(f)
            sigma = 5
            imout = gaussRGB(sigma, f)
            # imout.save()
            # Close original image
            f.close()
            
            # Create a new blob and upload blurred image
            out_blob = bucket.blob('blur-' + sfname)
            buffer = io.BytesIO()
            imout.save(buffer, format='JPEG')
            out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
            
            # Close blurred image
            imout.close()

            return render_template('result.html', title='Result', img=out_blob.media_link)
        else:
            return render_template('load.html', title='Upload Image', content="Incorrect Filetype, must be .png, .jpg or .jpeg.")
    
        
        


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


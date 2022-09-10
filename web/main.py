from flask import Flask, send_file
from flask import request, escape, render_template, session
from flask_bootstrap import Bootstrap5

from gblur import gauss
from medianfilt import median_filter
from werkzeug.utils import secure_filename
import io, os, gc
from google.cloud import storage
import random
import requests
from PIL import Image
# contains session key
from mysecrets import key



# -------------------- App initialisation ------------------- #

app = Flask(__name__)

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


# -------------------- Set up Bootstrap ----------------------#
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

# -------------------- Set Session key ----------------------#
# app.secret_key = 'BAD_SESSION_KEY'               # uncomment if pulled from github
app.secret_key = key


ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])


# ----------------- Helper functions ------------------------ #
def set_cloud_storage():
    ''''''
    # Create a cloud storage client
    client = storage.Client(project='toonoisy')

    # Get the bucket 
    bucket = client.get_bucket(CLOUD_STORAGE_BUCKET)

    return bucket



# ----------------- Routing Functions ------------------------ #

@app.route("/")
def index():   
    return render_template('index.html', title='tooNOISY')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/reduce")
def reduce():
    return render_template('load.html', title="Noise Removal")

@app.route("/load", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        # Load image
        f = request.files['file']
        f_name = secure_filename(f.filename)

        # Get cloud storage bucket
        bucket = set_cloud_storage()
        
        # Set image hash
        im_hash = random.randint(1,9999999)

        # Create new name for the image
        sfname = 'og_' + str(im_hash) + os.path.splitext(f_name)[-1]
        # Save to session
        session['og_img'] = sfname
        
        # If the file is jpeg or png
        if os.path.splitext(f_name)[1] in ALLOWED_EXTENSIONS:
            # Create new blob and upload the original image
            in_blob = bucket.blob(sfname)
            in_blob.upload_from_file(f)
            del f
            gc.collect()
            # Return page displaying input image
            return render_template('img_loaded.html', title='toonoisy', img=in_blob.media_link)
        else:
            return render_template('load.html', title='Upload Image', content="Incorrect Filetype, must be .png, .jpg or .jpeg.")

@app.route('/reload')
def restart_with_same():
    # Set up cloud storage bucket
    bucket = set_cloud_storage()
    img_og = bucket.get_blob(session['og_img'])
    return render_template('img_loaded.html', title="toonoisy", img=img_og.media_link)

@app.route("/gauss", methods=["GET", "POST"])
def gauss_reduce():
    if request.method == "POST":
        
        # Setup cloud storage client and bucket
        bucket = set_cloud_storage()

        # Download the original image from the bucket
        data = requests.get(bucket.get_blob(session['og_img']).media_link).content
        f = io.BytesIO(data)
        del data
        gc.collect()

        sigma = float(request.form['sigma'])
        imout = gauss(sigma, f)
        del f
        gc.collect()

        # Create a new blob and upload blurred image
        blur_name = 'blur-' + session['og_img']
        out_blob = bucket.blob(blur_name)
        buffer = io.BytesIO()
        imout.save(buffer, format='JPEG')
        out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
        
        # Close blurred image
        del imout
        del buffer
        gc.collect()
        return render_template('result.html', title='Gauss', img=out_blob.media_link)

@app.route("/median", methods=["GET", "POST"])
def median_reduce():
    if request.method == "POST":
        
        # Setup cloud storage client and bucket
        bucket = set_cloud_storage()


        # Download the original image from the bucket
        data = requests.get(bucket.get_blob(session['og_img']).media_link).content
        f = io.BytesIO(data)

        del data
        gc.collect()

        width = int(request.form['width'])
        imout = median_filter(f, width)
        del f
        gc.collect()

        # Create a new blob and upload blurred image
        blur_name = 'blur-' + session['og_img']
        out_blob = bucket.blob(blur_name)
        buffer = io.BytesIO()
        imout.save(buffer, format='JPEG')
        out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
        
        # Close blurred image
        del imout
        del buffer
        gc.collect()
        
        return render_template('result.html', title='Median', img=out_blob.media_link)

@app.route('/compare')
def sidebyside():
    # Set up cloud storage bucket
    bucket = set_cloud_storage()
    img_og = bucket.get_blob(session['og_img'])
    img_new = bucket.get_blob('blur-' + session['og_img'])
    
    return render_template('sidebyside.html', title='Compare', img_1=img_og.media_link, img_2=img_new.media_link)

@app.errorhandler(500)
def internal_server_error():
    return render_template('error500.html', title="Error"), 500


# # Google verification
# @app.route("/googleb5e42b25019c3d31.html")
# def verify_site():
#     return render_template('googleb5e42b25019c3d31.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


from flask import Flask
from flask import request, render_template, session
from flask_bootstrap import Bootstrap5

from gblur import gauss
from medianfilt import median_filter, fast_median_filter
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

# Create a cloud storage client
client = storage.Client(project='toonoisy')

# Get the bucket 
bucket = client.get_bucket(CLOUD_STORAGE_BUCKET)


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
        # Set image hash
        im_hash = random.randint(1,9999999)

        # Create new name for the image
        sfname = 'og_' + str(im_hash) + os.path.splitext(f_name)[-1]
        # Save to session
        session['og_img'] = sfname
        
        # If the file is jpeg or png
        if os.path.splitext(f_name)[1] in ALLOWED_EXTENSIONS:
            # Create new blob and upload the original image
            # Convert to grayscale
            in_blob = bucket.blob(sfname)
            img = Image.open(f).convert('L')
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            in_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
            del f, img
            gc.collect()
            # Return page displaying input image
            return render_template('img_loaded.html', title='toonoisy', img=in_blob.media_link)
        else:
            return render_template('load.html', title='Upload Image', content="Incorrect Filetype, must be .png, .jpg or .jpeg.")

@app.route("/barbara", methods=["GET", "POST"])
def example_barbara():
    # Create filename
    im_hash = random.randint(1,9999999)
    sfname = 'og_' + str(im_hash) + 'barbara.png'
    session['og_img'] = sfname
    
    # Duplicate barbara image with new name
    barbara = bucket.blob('barbara.png')
    bucket.copy_blob(barbara, bucket, sfname)
    return render_template('img_loaded.html', title='toonoisy', img="https://storage.cloud.google.com/toonoisy_ims/barbara.png")

@app.route("/kodim", methods=["GET", "POST"])
def example_kodim():
    # Get cloud storage bucket
    # bucket = set_cloud_storage()
    # Create filename
    im_hash = random.randint(1,9999999)
    sfname = 'og_' + str(im_hash) + 'kodim.jpg'
    session['og_img'] = sfname
    
    # Duplicate barbara image with new name
    barbara = bucket.blob('kodim.jpg')
    bucket.copy_blob(barbara, bucket, sfname)
    return render_template('img_loaded.html', title='toonoisy', img="https://storage.cloud.google.com/toonoisy_ims/kodim.jpg")


@app.route('/reload')
def restart_with_same():
    img_og = bucket.get_blob(session['og_img'])
    return render_template('img_loaded.html', title="toonoisy", img=img_og.media_link)

@app.route("/gauss", methods=["GET", "POST"])
def gauss_reduce():
    if request.method == "POST":        # Download the original image from the bucket
        data = requests.get(bucket.get_blob(session['og_img']).media_link).content
        f = io.BytesIO(data)

        sigma = float(request.form['sigma'])
        imout = gauss(sigma, f)

        # Create a new blob and upload blurred image
        blur_name = 'blur-' + session['og_img']
        out_blob = bucket.blob(blur_name)
        buffer = io.BytesIO()
        imout.save(buffer, format='JPEG')
        out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
        
        # Close blurred image
        del buffer, imout, f, data
        gc.collect()
        return render_template('result.html', title='Gauss', img=out_blob.media_link)

@app.route("/median", methods=["GET", "POST"])
def median_reduce():
    if request.method == "POST":
        # Download the original image from the bucket
        data = requests.get(bucket.get_blob(session['og_img']).media_link).content
        f = io.BytesIO(data)

        width = int(request.form['width'])
        imout = fast_median_filter(f, width)

        # Create a new blob and upload blurred image
        blur_name = 'blur-' + session['og_img']
        out_blob = bucket.blob(blur_name)
        buffer = io.BytesIO()
        imout.save(buffer, format='JPEG')
        out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
        
        # Close blurred image
        del buffer, imout, data, f
        gc.collect()
        
        return render_template('result.html', title='Median', img=out_blob.media_link)

@app.route('/compare')
def sidebyside():
    img_og = bucket.get_blob(session['og_img'])
    img_new = bucket.get_blob('blur-' + session['og_img'])
    
    return render_template('sidebyside.html', title='Compare', img_1=img_og.media_link, img_2=img_new.media_link)

@app.route('/sharpen')
def sharpen():
    pass




@app.errorhandler(500)
def internal_server_error():
    return render_template('error500.html', title="Error"), 500


# # Google verification
# @app.route("/googleb5e42b25019c3d31.html")
# def verify_site():
#     return render_template('googleb5e42b25019c3d31.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


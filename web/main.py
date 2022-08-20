from flask import Flask, send_file
from flask import request, escape, render_template, session
from flask_bootstrap import Bootstrap5

from gblur import gaussRGB
from werkzeug.utils import secure_filename
import io, os
from google.cloud import storage
import random
import requests
from PIL import Image
# contains session key
from mysecrets import key



# -------------------- App initialisation ------------------- #

app = Flask(__name__)

# -------------------- Set up Bootstrap ----------------------#
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

# -------------------- Set Session key ----------------------#
# app.secret_key = 'BAD_SESSION_KEY'               # uncomment if pulled from github
app.secret_key = key


ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])


# ----------------- Helper functions ------------------------ #
def set_cloud_storage(bucket_name, json_name):
    ''''''
    # Create a cloud storage client
    client = storage.Client.from_service_account_json('balmy-nuance-359122.json')

    # Get the bucket 
    bucket = client.get_bucket('img-proc-fb')

    return client, bucket



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

        client, bucket = set_cloud_storage('img-proc-fb', 'balmy-nuance-359122.json' )
        
        # Set image hash
        im_hash = random.randint(1,9999999)

        # Create new name for the image
        sfname = 'Uploaded image' + str(im_hash) + os.path.splitext(f_name)[-1]
        # Save to session
        session['og_img'] = sfname
        
        # If the file is jpeg or png
        if os.path.splitext(f_name)[1] in ALLOWED_EXTENSIONS:
            # Create new blob and upload the original image
            in_blob = bucket.blob(sfname)
            in_blob.upload_from_file(f)
            f.close()
            # Return page displaying input image
            return render_template('img_loaded.html', title='toonoisy', img=in_blob.media_link)
        else:
            return render_template('load.html', title='Upload Image', content="Incorrect Filetype, must be .png, .jpg or .jpeg.")
    

@app.route("/result", methods=["GET", "POST"])
def noise_reduce():
    if request.method == "POST":
        
        # Setup cloud storage client and bucket
        client, bucket = set_cloud_storage('img-proc-fb', 'balmy-nuance-359122.json' )


        # Download the original image from the bucket
        data = requests.get(bucket.get_blob(session['og_img']).media_link).content
        f = io.BytesIO(data)

        sigma = 5
        imout = gaussRGB(sigma, f)
        f.close()

        # Create a new blob and upload blurred image
        blur_name = 'blur-' + session['og_img']
        out_blob = bucket.blob(blur_name)
        buffer = io.BytesIO()
        imout.save(buffer, format='JPEG')
        out_blob.upload_from_string(buffer.getvalue(), "image/jpeg")
        
        # Close blurred image
        imout.close()
        return render_template('result.html', title='Result', img=out_blob.media_link)

@app.route('/compare')
def sidebyside():
    # Set up cloud storage bucket
    client, bucket = set_cloud_storage('img-proc-fb', 'balmy-nuance-359122.json' )
    img_og = bucket.get_blob(session['og_img'])
    img_new = bucket.get_blob('blur-' + session['og_img'])
    
    return render_template('sidebyside.html', title='Compare', img_1=img_og.media_link, img_2=img_new.media_link)


# Google verification
@app.route("/googleb5e42b25019c3d31.html")
def verify_site():
    return render_template('googleb5e42b25019c3d31.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


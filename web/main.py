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
from secrets import key



ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

app = Flask(__name__)

bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

app.secret_key = key

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

        # Create a cloud storage client
        client = storage.Client.from_service_account_json('balmy-nuance-359122.json')
        
        # Set image hash
        im_hash = random.randint(1,9999999)

        # Get the bucket that the image will be uploaded to
        bucket = client.get_bucket('img-proc-fb')

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
        # Create a cloud storage client
        client = storage.Client.from_service_account_json('balmy-nuance-359122.json')

        # Get the bucket 
        bucket = client.get_bucket('img-proc-fb')

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

@app.route("/save")
def save_result():
    print(20000000000000000000000000090000000000000000)
    # Create a cloud storage client
    client = storage.Client.from_service_account_json('balmy-nuance-359122.json')

    # Get the bucket 
    bucket = client.get_bucket('img-proc-fb')

    f_name = 'blur-' + session['og_img']
    data = Image.open(bucket.get_blob(f_name).media_link).content
    # f = io.BytesIO(data)
    # img = Image.open(f)
    buffer = io.BytesIO()
    return send_file(
        data.save(buffer, 'JPEG'),
        as_attachment=True,
        download_name='noisereduced' + str(random.randint(1,1000)),
        mimetype='image/jpeg'
        )


# Google verification
@app.route("/googleb5e42b25019c3d31.html")
def verify_site():
    return render_template('googleb5e42b25019c3d31.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


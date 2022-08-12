from flask import Flask
from flask import request, escape, render_template
from gblur import gaussRGB
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():   
    return render_template('load.html', title='Upload Image')

@app.route("/uploader", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        f = request.files['file']
        sfname = 'static/images/'+str(secure_filename(f.filename))
        f.save(sfname)
        sigma = 5
        bname = gaussRGB(sigma, sfname)

        return render_template('result.html', title='Result', imgpath=bname)
        
        


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


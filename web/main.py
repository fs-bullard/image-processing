from flask import Flask
from flask import request, escape, render_template
from gblur import gaussRGB


app = Flask(__name__)

@app.route("/")
def index():   
    return render_template('index.html', title='Gaussian Blur')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


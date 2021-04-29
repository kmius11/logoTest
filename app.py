from flask import Flask
from flask import render_template
from flask import request
import cv2
app = Flask(__name__)


@app.route("/")

def index():
   
    return render_template("index.html")

@app.route("https://logovis.azurewebsites.net/servicio",methods=["POST"])
def servicio():
    usuario=request.form.get("nombre")
    return render_template("servicio.html",nombre=usuario)


if __name__=="__main__":
    app.run(debug=True)


    

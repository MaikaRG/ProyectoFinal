from flask import Flask
import numpy as np
import os
#import cv2
from werkzeug import secure_filename
from flask import Flask, render_template,request,  jsonify , send_from_directory
import meterFotoSacarFoto

# instancia del objeto Flask
app = Flask(__name__)

# instancia del objeto Flask
app.config['UPLOAD_FOLDER'] = './input'

@app.route('/output/<path:path>')
def send_js(path):
    return send_from_directory('output', path)


@app.route("/")
def upload_file():
 # devolvemos la plantilla "index.html"
 return render_template('principal.html')

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files["file"]
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria con la predicción
  meterFotoSacarFoto.resizeImages(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  return render_template('colorearImagen.html', pred='/output/img.png')
  #return render_template('colorearImagen.html', pred=pred)
  

if __name__ == "__main__":
    app.run()
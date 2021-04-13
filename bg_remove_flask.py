from flask import Flask, request, url_for, redirect, send_from_directory
from rembg.bg import remove
import numpy as np
import io
from PIL import Image
# If image too big
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import time
import os
#testing connection for new computer
app = Flask(__name__)

@app.route("/helloworld")
def hello_world():
  return "gold"

@app.route("/removebg", methods = ['GET', 'POST'])
def remove_bg():
    if request.method == "POST": 
        file = request.files["file"]
        input_path = os.path.join("input", file.filename[-8:])
        str_filename = file.filename[-8:]
        file.save(input_path)
        file = np.fromfile(input_path)
        result = remove(file)
        output = 'image-' + str_filename.split(".")[0] + str(int(time.time())) + '.png' # Must be a .png
        img = Image.open(io.BytesIO(result)).convert("RGBA")
        output_path = os.path.join("output", output)
        img.save(output_path)
        return redirect(url_for("uploaded_file", filename = output))
    return """<!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>"""

@app.route("/uploads/<filename>")
def uploaded_file(filename):
  return send_from_directory("output", filename)


def allowed_file(filename):
  extensions = ["png", "jpg", "jpeg"]
  return filename.split(".")[-1] in extensions

@app.route("/flutter/removebg", methods = ['GET', 'POST'])
def flutter_removebg():
  print(request.files) 
  if request.method == 'POST' and 'file' in request.files:
    file = request.files['file']
    if file.filename != '' and (file and allowed_file(file.filename)):
        #filename = os.path.join('input', file.filename)
        #file.save(filename[-8:])             # Saves the uncropped image
        #input_path = filename[-8:]

        input_path = os.path.join("input", file.filename[-8:])
        str_filename = file.filename[-8:]
        file.save(input_path)
                
        output = 'image-' + str(int(time.time())) + '.png'
        file = np.fromfile(input_path)
        result = remove(file)
        img = Image.open(io.BytesIO(result)).convert('RGBA')
        output = 'image-' + .split(".")[0] + str(int(time.time())) + '.png'
        output_path = os.path.join("output", output)
        img.save(output_path)           # Saves the cropped image
        print(url_for('uploaded_file', filename = output))
        return url_for('uploaded_file', filename = output)
    else:
      return "bad_2"
  else:
    return "bad_1"

app.run(host = "0.0.0.0")
# app.run(host = "127.0.0.1")
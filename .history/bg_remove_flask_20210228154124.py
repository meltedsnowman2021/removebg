from flask import Flask, request
from rembg.bg import remove
import numpy as np
import io
from PIL import Image
# If image too big
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)

input_path = '.\\input\\2.png'
output_path = '.\\output\\test.rmbg.png'

@app.route("/helloworld")
def hello_world():
  return "hello world"

@app.route("/removebg", methods = ['GET', 'POST'])
def remove_bg():
    if request.method == "POST":
        file = request.files["file"]
        file.save(input_path)
        file = np.fromfile(input_path)
        result = remove(file)
        img = Image.open(io.BytesIO(result)).convert("RGBA")
        img.save(output_path)
        return "file_uploaded"
    return """<!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>"""
print("hi")
app.run(host = "0.0.0.0")
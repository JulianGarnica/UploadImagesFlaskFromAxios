import json
import os
import functions
from werkzeug.utils import secure_filename
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

upload_folder = './upload/'
app.config['UPLOAD_FOLDER'] = upload_folder


## Show images ##
@app.route('/img/<path:filename>')
def send_file(filename):
  return send_from_directory(upload_folder, filename)

@app.route('/upload', methods=["POST"])
def upload_images():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      return jsonify({"result": "No file part"}), 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
      return jsonify({"result": "No selected file"}), 400
    if file and functions.allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return jsonify({"result": "Image uploaded successfully"})

if __name__ == "__main__":
  app.run(debug=True)
#for flask
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

#for ocr
from PIL import Image
from pytesseract import image_to_string

def ocr():
    extracted_text = image_to_string(Image.open('uploads/to_ocr_image'))
    f = open("templates/extracted.html","w") 
    f.write(extracted_text)
    f.close()
 
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'uploads/'
# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    # Check for allowed file extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER + 'to_ocr_image')
            filename = 'to_ocr_image'
            ocr()
            return redirect(url_for('output'))
    return render_template('index.html')


@app.route('/output')
def output():
    return render_template('extracted.html')

# Function to call meilix script on clicking the build button

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/about')
def about():
    # About page
    return render_template("about.html")


# Return a custom 404 error.
@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, unexpected error: {}'.format(e), 404


@app.errorhandler(500)
def application_error(e):
    # Return a custom 500 error.
    return 'Sorry, unexpected error: {}'.format(e), 500


if __name__ == '__main__':
    app.run()

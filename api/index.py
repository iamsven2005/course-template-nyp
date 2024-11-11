import os
import base64
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename
from document_generator import create_document
import zipfile              
from io import BytesIO        
from PIL import Image      
from openpyxl import load_workbook 


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'docx', 'xlsx'}


def extract_images_as_base64(file_stream, file_extension):
    """Extract images from an uploaded DOCX or XLSX file as base64-encoded strings."""
    images_base64 = []

    if file_extension == 'docx':
        with zipfile.ZipFile(file_stream, 'r') as z:
            for file_name in z.namelist():
                if file_name.startswith('word/media/'):
                    with z.open(file_name) as source_file:
                        image_data = source_file.read()
                        image_b64 = base64.b64encode(image_data).decode('utf-8')
                        images_base64.append((file_name, image_b64))
    elif file_extension == 'xlsx':
        workbook = load_workbook(file_stream)
        for sheet in workbook.sheetnames:
            worksheet = workbook[sheet]
            for image in worksheet._images:
                image_data = image._data()
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                images_base64.append((image.anchor._from, image_b64))

    return images_base64
# Helper function to check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_base64_image_from_file(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload_file():
    # Check if both files are in the request
    if 'docx_file' not in request.files or 'xlsx_file' not in request.files:
        return "Both DOCX and XLSX files are required", 400

    docx_file = request.files['docx_file']
    xlsx_file = request.files['xlsx_file']

    # Validate both files
    if docx_file.filename == '' or xlsx_file.filename == '':
        return "No selected file(s)", 400

    if allowed_file(docx_file.filename) and allowed_file(xlsx_file.filename):
        try:
            # Extract file extensions
            docx_extension = docx_file.filename.rsplit('.', 1)[1].lower()
            xlsx_extension = xlsx_file.filename.rsplit('.', 1)[1].lower()

            # Ensure correct file types
            if docx_extension != 'docx' or xlsx_extension != 'xlsx':
                return "Incorrect file types. Please upload a DOCX file and an XLSX file.", 400

            # Save the DOCX file temporarily for extraction
            docx_filename = secure_filename(docx_file.filename)
            temp_docx_path = os.path.join("/tmp", docx_filename)
            docx_file.save(temp_docx_path)

            # Extract images from the uploaded DOCX file
            images_base64 = extract_images_as_base64(temp_docx_path, docx_extension)

            # Get the base64 image of the logo from /logo.png
            logo_base64 = get_base64_image_from_file("logo.png")

            # Create document with logo image and XLSX data
            doc_io = create_document(images_base64, logo_base64, xlsx_file, temp_docx_path)

            # Remove the temporary DOCX file after processing
            os.remove(temp_docx_path)

            return send_file(doc_io, as_attachment=True, download_name='output.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        except Exception as e:
            return f"An error occurred during processing: {str(e)}", 500

    return "File types not allowed. Please upload valid DOCX and XLSX files.", 400

if __name__ == '__main__':
    app.run(debug=True)

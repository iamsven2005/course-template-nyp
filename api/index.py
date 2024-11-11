import os
import base64
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename
from helpers import allowed_file
from file_processing import extract_images_as_base64
from document_generator import create_document

app = Flask(__name__)

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
            logo_base64 = get_base64_image_from_file("/logo.png")

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

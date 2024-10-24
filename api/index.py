import zipfile
from io import BytesIO
from flask import Flask, render_template, send_file, request
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import base64
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'docx'}

# Helper function to check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_images_as_base64(file_stream):
    """Extract images from an uploaded DOCX file as base64-encoded strings."""
    images_base64 = []
    with zipfile.ZipFile(file_stream, 'r') as z:
        for file_name in z.namelist():
            if file_name.startswith('word/media/'):
                with z.open(file_name) as source_file:
                    # Convert image data to base64
                    image_bytes = source_file.read()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                    images_base64.append((file_name, base64_image))
    return images_base64

def create_document(images_base64):
    """Create a DOCX document with extracted base64 images."""
    doc = Document()

    # Add a title
    title = doc.add_heading('Extracted Images from Uploaded DOCX', level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add extracted images to the document
    doc.add_heading('Section: Extracted Images', level=2)
    doc.add_paragraph('Here are the images extracted from the uploaded document (as base64):')

    for image_filename, image_b64 in images_base64:
        doc.add_paragraph(f'Adding image: {image_filename}')

        # Decode base64 image and open with PIL
        image_data = base64.b64decode(image_b64)
        image_stream = BytesIO(image_data)

        # Open image with PIL to determine size
        with Image.open(image_stream) as img:
            max_width = 6.0  # Max width in inches
            width, height = img.size
            aspect_ratio = width / height

            if width > height:
                adjusted_width = min(max_width, width / 96)  # Convert pixels to inches (assuming 96 dpi)
                adjusted_height = adjusted_width / aspect_ratio
            else:
                adjusted_height = min(max_width, height / 96)
                adjusted_width = adjusted_height * aspect_ratio

            # Add the image to the document
            doc.add_picture(image_stream, width=Inches(adjusted_width), height=Inches(adjusted_height))

    # Save the document to an in-memory file
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)  # Go back to the beginning of the BytesIO object
    return doc_io

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'docx_file' not in request.files:
        return "No file part", 400
    
    file = request.files['docx_file']
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        try:
            # Extract images from the uploaded DOCX file
            images_base64 = extract_images_as_base64(file)

            # Create a new document with the extracted images
            doc_io = create_document(images_base64)

            # Return the new document for download
            return send_file(doc_io, as_attachment=True, download_name='extracted_images.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        except Exception as e:
            return f"An error occurred during processing: {str(e)}", 500

    return "File not allowed", 400

if __name__ == '__main__':
    app.run(debug=True)

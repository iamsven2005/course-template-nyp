import zipfile
from io import BytesIO
from flask import Flask, render_template, send_file
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import base64
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False
)

SOURCE_FILE_PATH = "static/source.docx"  # Replace with your actual source document path

def extract_images_as_base64(source_path):
    """Extracts images from a DOCX file as base64-encoded strings."""
    images_base64 = []
    with zipfile.ZipFile(source_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.startswith('word/media/'):
                with z.open(file_name) as source_file:
                    # Convert image data to base64
                    image_bytes = source_file.read()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                    images_base64.append((file_name, base64_image))
    return images_base64

def create_document():
    # Create a new document
    doc = Document()

    # Add a title
    title = doc.add_heading('Document Creation Example', level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add a paragraph with bold and italic text
    paragraph = doc.add_paragraph('This is a sample document created using the python-docx library.')
    run = paragraph.runs[0]
    run.bold = True
    run.italic = True

    # Add a heading
    doc.add_heading('Section 1: Introduction', level=2)

    # Add a bulleted list
    list_paragraph = doc.add_paragraph()
    list_paragraph.add_run('Bullet 1').bold = True
    list_paragraph.add_run(' - This is the first bullet point.')
    list_paragraph.add_run('\n')
    list_paragraph.add_run('Bullet 2').bold = True
    list_paragraph.add_run(' - This is the second bullet point.')

    # Add a table
    doc.add_heading('Section 2: Data', level=2)
    table = doc.add_table(rows=4, cols=3)
    table.style = 'Table Grid'
    for row in table.rows:
        for cell in row.cells:
            cell.width = Pt(100)
    table.cell(0, 0).text = 'Name'
    table.cell(0, 1).text = 'Age'
    table.cell(0, 2).text = 'City'
    for i, data in enumerate([('Alice', '25', 'New York'), ('Bob', '30', 'San Francisco'), ('Charlie', '22', 'Los Angeles')], start=1):
        table.cell(i, 0).text = data[0]
        table.cell(i, 1).text = data[1]
        table.cell(i, 2).text = data[2]

    # Add extracted images to the document
    doc.add_heading('Section 3: Extracted Images', level=2)
    doc.add_paragraph('Here are the images extracted and added from the source document (as base64):')

    # Extract images as base64
    images_base64 = extract_images_as_base64(SOURCE_FILE_PATH)

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

@app.route("/download")
def download_file():
    try:
        doc_io = create_document()
        app.logger.info("Document created successfully.")
        return send_file(doc_io, as_attachment=True, download_name='example_document.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except PermissionError as perm_err:
        app.logger.error(f"Permission error: {str(perm_err)}")
        return "Permission error occurred", 403
    except Exception as e:
        app.logger.error(f"Error during document creation: {str(e)}")
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(debug=True)

from io import BytesIO
from flask import Flask, render_template, send_file
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import requests

app = Flask(__name__)

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
    table.autofit = False
    table.allow_autofit = False
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

    # Add an image from a URL
    doc.add_heading('Section 3: Image', level=2)
    doc.add_paragraph('Here is an image from a URL:')
    
    # Fetch image from a URL
    image_url = 'https://course-template-nyp.vercel.app/image.jpeg'  # Replace with the actual URL
    response = requests.get(image_url)
    if response.status_code == 200:
        image_stream = BytesIO(response.content)
        doc.add_picture(image_stream, width=Pt(300))

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
    # Create the document dynamically
    doc_io = create_document()

    # Send the file for download as a response, using the in-memory file object
    return send_file(doc_io, as_attachment=True, download_name='example_document.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    app.run(debug=True)

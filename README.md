# NYPTECH Flask Document Generator

Welcome to the **NYPTECH Flask Document Generator**! This application allows you to effortlessly upload DOCX and XLSX files, input your topics and learning units, and generate a customized Word document tailored to your needs.

## 📖 Table of Contents

- [NYPTECH Flask Document Generator](#nyptech-flask-document-generator)
  - [📖 Table of Contents](#-table-of-contents)
  - [🚀 Features](#-features)
  - [🛠 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running Locally](#running-locally)
  - [🖥 How to Use](#-how-to-use)
  - [🔧 Technical Details](#-technical-details)
    - [Image Extraction](#image-extraction)
    - [Text Extraction](#text-extraction)
    - [Table Extraction](#table-extraction)
  - [🚀 One-Click Deploy](#-one-click-deploy)
  - [📄 License](#-license)

## 🚀 Features

- **Easy File Uploads**: Upload your DOCX and XLSX files with just a few clicks.
- **Dynamic Input Fields**: Add multiple topics and learning units seamlessly.
- **Automated Document Generation**: Receive a professionally formatted Word document based on your inputs and uploaded files.
- **Image and Table Extraction**: Automatically extracts images and tables from your uploaded DOCX files.
- **User-Friendly Interface**: Designed with simplicity in mind, making it accessible for everyone.

## 🛠 Getting Started

Follow these instructions to set up the project on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7 or higher**: Make sure Python is installed on your machine. You can download it from [here](https://www.python.org/downloads/).
- **Git**: To clone the repository. Download it from [here](https://git-scm.com/downloads).
- **Pip**: Python's package installer, which typically comes with Python.

### Installation

1. **Clone the Repository**

   Open your terminal or command prompt and run:

   ```bash
   git clone https://github.com/nasif/course-template-nyp.git

2. **Navigate to the Project Directory**

    cd course-template-nyp/api
    Create a Virtual Environment (Optional but Recommended)
    ```bash
    python -m venv venv

4. **Activate the Virtual Environment**
   Windows:
   ```bash
   venv\Scripts\activate

5. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt

### Running Locally

1. **Start the Flask Application**
   ```bash
   cd api
   python3 index.py

2. **Access the Application**
    Open your web browser and navigate to:
    `
    http://localhost:5000/ ` 

    You should see the application's homepage where you can start uploading files and inputting your data.

## 🖥 How to Use

Using the NYPTECH Flask Document Generator is straightforward. Follow these simple steps:

1. **Open the Application**

    Navigate to `http://localhost:5000/` in your web browser.

2. **Upload Your Files**
   - DOCX File: Click on the "Upload DOCX File" button and select your .docx file `(source.docx)`.
   - XLSX File: Click on the "Upload XLSX File" button and select your .xlsx file `(input.xlsx)`.
  
3. **Input Topics and Learning Units**
   - Enter your desired topics in the "Enter topic" field.
   - Enter corresponding learning units in the "Enter learning unit" field.
   - To add more topics and learning units, click the "Add" button. You can add as many as needed.
   - To remove a pair, click the "Remove" button next to the respective fields.
   - You can drag and drop as well.
  
4. **Submit Your Data**

    Once you've uploaded your files and entered all necessary information, click the "Upload and Submit" button.

5. **Download Your Document**

    After processing, the application will generate a new DOCX document tailored to your inputs. A download prompt will appear—save the file to your desired location.

## 🔧 Technical Details
Here's a simple overview of how the NYPTECH Flask Document Generator processes your files to create a customized document.

### Image Extraction
The application automatically extracts images from your uploaded DOCX and XLSX files. This ensures that any visual content you include in your documents is preserved and incorporated into the final output.

**How It Works:**

1. **DOCX Files:**

    - DOCX files are essentially ZIP archives containing various components like text, images, and styles.
    - The application uses the zipfile library to open the DOCX file.
    - It searches for images stored in the word/media/ directory within the DOCX archive.
    - Each found image is read, encoded in base64 format, and added to the list of images to be included in the final document.

    def extract_images_as_base64(file_stream, file_extension):
        images_base64 = []

        if file_extension == 'docx':
            with zipfile.ZipFile(file_stream, 'r') as z:
                for file_name in z.namelist():
                    if file_name.startswith('word/media/'):
                        with z.open(file_name) as source_file:
                            image_data = source_file.read()
                            image_b64 = base64.b64encode(image_data).decode('utf-8')
                            images_base64.append((file_name, image_b64))
        # ...

        return images_base64

2. **XLSX Files:**

    - XLSX files can also contain embedded images.
    - Using the openpyxl library, the application loads the workbook and iterates through each sheet.
    - It extracts images from each sheet and encodes them in base64 format for inclusion in the final document.
    ``` bash 
    elif file_extension == 'xlsx':
        workbook = load_workbook(file_stream)
        for sheet in workbook.sheetnames:
            worksheet = workbook[sheet]
            for image in worksheet._images:
                image_data = image._data()
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                images_base64.append((image.anchor._from, image_b64))


### Text Extraction
The application extracts specific sections of text from your uploaded DOCX files to include them in the generated document. This allows for a seamless integration of content from your source files into the final output.

**How It Works:**

1. **Identifying Sections:**

 - The application looks for predefined section headers (e.g., "Course Aims", "Course Learning Outcomes" within the DOCX file.
 - It extracts all the text between these sections to include relevant content in the final document.

2. **Implementation:**

    def extract_text_between_sections(file_path, start_section, end_section):
        doc = Document(file_path)
        extracting = False
        extracted_text = []
        
        for paragraph in doc.paragraphs:
            if start_section in paragraph.text:
                extracting = True
                continue
            
            if extracting and end_section in paragraph.text:
                break
            
            if extracting:
                extracted_text.append(paragraph.text)
        
        return "\n".join(extracted_text)

### Table Extraction
Tables from your uploaded DOCX files are automatically extracted and reformatted in the generated document. This ensures that structured data is accurately represented in the final output.

**How It Works:**

1. **Extracting Tables:**

The application uses the python-docx library to read tables from the uploaded DOCX file.
Each table is processed and added to the final document with appropriate formatting.

2. **Implementation:**

    def extract_tables_from_docx(doc_path):
        doc = Document(doc_path)
        tables = []
        for table in doc.tables:
            tables.append(table)
        return tables

3. **Adding Tables to the Final Document:**

    for table in tables:
        new_table = doc.add_table(rows=len(table.rows), cols=len(table.columns))
        new_table.style = 'Table Grid'

        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                new_table.cell(i, j).text = cell.text
                # Additional formatting can be applied here

## 🚀 One-Click Deploy
Deploying the NYPTECH Flask Document Generator is quick and easy with Vercel. Follow the link below to get started:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fnyp-tech%2Fnyp-tech%2Ftree%2Fmain%2Fflask-npx&demo-title=Flask%20Hello%20World&demo-description=Use%20Python%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fpython-hello-world.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994600/random/python.png)

Note: Ensure you have a Vercel account. If not, you can sign up [here](https://vercel.com/signup).

## 📄 License
This project is licensed under the MIT License.

Thank you for using the NYPTECH Flask Document Generator! If you encounter any issues or have suggestions for improvements, feel free to open an issue or reach out to the maintainers.

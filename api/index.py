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

def create_document(images_base64, base64_img_first):
    """Create a DOCX document with a provided base64 image first and extracted base64 images."""
    doc = Document()
    image_data = base64.b64decode(base64_img_first)
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


    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')

    title = doc.add_paragraph('School of Information Technology')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.runs[0]
    run.font.size = Pt(24)
    run.font.name = 'Arial'


    course = doc.add_paragraph('Course Syllabi for')
    course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = course.runs[0]
    run1.font.size = Pt(24)
    run1.font.name = 'Arial'


    diploma = doc.add_paragraph('DIPLOMA IN APPLIED AI & ANALYTICS')
    diploma.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = diploma.runs[0]
    run2.font.size = Pt(24)
    run2.font.name = 'Arial'
    run2.bold = True


    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')


    year = doc.add_paragraph('Academic Year 2021/2022')
    year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run3 = diploma.runs[0]
    run3.font.size = Pt(18)
    run3.font.name = 'Arial'


    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')


    revised = doc.add_paragraph('Date Revised: Apr  2023 v1.0')
    run4 = revised.runs[0]
    run4.font.size = Pt(11)
    run4.font.name = 'Arial'


    title1 = doc.add_paragraph('DIPLOMA IN APPLIED AI & ANALYTICS (DAAA)')
    run5 = title1.runs[0]
    run5.font.size = Pt(16)
    run5.font.name = 'Arial'
    run5.bold = True


    para1 = doc.add_paragraph('The Diploma in Applied AI & Analytics (DAAA) is the pilot programme to implement the NYP’s Professional Competency Model (PCM) as its pedagogical model. PCM is an inter- disciplinary competency-based learning model that mirrors workplace practices and intrinsically supports lifelong learning continuum. It was first launched in June 2020 and implemented in the Diploma in Business Intelligence & Analytics (DBA) in April 2021. The renaming from DBA to DAAA will have no impact to the curriculum.')
    run6 = para1.runs[0]
    run6.font.size = Pt(12)
    run6.font.name = 'Arial'

    doc.add_paragraph('')

    para2 = doc.add_paragraph('In PCM, learners develop competencies through stackable learning units known as Competency Units (CmUs). CmUs are pegged at varying levels to scaffold learners’ competencies development towards skills mastery. Under PCM, PET learners will develop competencies up to Complexity Level 5 while Continuing Education and Training (CET) learners up to Complexity Level 7.')
    run7 = para2.runs[0]
    run7.font.size = Pt(12)
    run7.font.name = 'Arial'

    doc.add_paragraph('')
    doc.add_paragraph('')


    title2 = doc.add_paragraph('Course Aims')
    run8 = title2.runs[0]
    run8.font.size = Pt(16)
    run8.font.name = 'Arial'
    run8.bold = True



    para3 = doc.add_paragraph('In PCM, learners develop competencies through stackable learning units known as Competency Units (CmUs). CmUs are pegged at varying levels to scaffold learners’ competencies development towards skills mastery. Under PCM, PET learners will develop competencies up to Complexity Level 5 while Continuing Education and Training (CET) learners up to Complexity Level 7.')
    run9 = para3.runs[0]
    run9.font.name = 'Arial'
    doc.add_page_break()


    title3 = doc.add_paragraph('Course Learning Outcomes')
    run10 = title3.runs[0]
    run10.font.size = Pt(16)
    run10.font.name = 'Arial'
    run10.bold = True


    para4 = doc.add_paragraph('The desired learning outcomes of the diploma are to educate and train students who, by the time of successful completion of course, will be able to:')
    run11 = para3.runs[0]
    run11.font.size = Pt(12)
    run11.font.name = 'Arial'


    table = doc.add_table(rows=5, cols=2)
    table.autofit = False
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Graduate Attribute (GA)'
    hdr_cells[1].text = 'Course Learning Outcomes (CLOs)'
    row_cells = table.rows[1].cells
    row_cells[0].text = 'Professional Proficiency'
    row_cells[1].text = 'CLO1: Apply technical knowledge and programming skills in the capacity of a business analytics IT professional.\n\nCLO2: Apply artificial intelligence and analytics technologies and tools to integrate technical and business knowledge to provide solution.\n\nCLO3: Demonstrate competence in artificial intelligence and analytics and be able to integrate and apply it effectively in different industry & domain.'

# Row 2: Competent in 21st Century Skills
    row_cells = table.rows[2].cells
    row_cells[0].text = 'Competent in 21st Century Skills'
    row_cells[1].text = 'CLO4: Display the abilities to stay relevant by demonstrating independent learning, self-awareness and mental resilience, and personal effectiveness.\n\nCLO5: Demonstrate interpersonal skills and global perspectives by communicating and working effectively with people from diverse backgrounds.'

# Row 3: Innovative and Enterprising
    row_cells = table.rows[3].cells
    row_cells[0].text = 'Innovative and Enterprising'
    row_cells[1].text = 'CLO6: Apply innovative and enterprising practices to achieve intended goals and drive continuous improvement with an interdisciplinary approach.'

# Row 4: Socially Responsible
    row_cells = table.rows[4].cells
    row_cells[0].text = 'Socially Responsible'
    row_cells[1].text = 'CLO7: Display personal and professional values and ethics by demonstrating inclusivity and responsibility towards the community, nation, and the world, and considering impact of actions and decisions on sustainability.'
    for row in table.rows:
        for cell in row.cells:
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                run = paragraph.runs
                for r in run:
                    r.font.name = 'Arial'
                    r.font.size = Pt(12)
    doc.add_page_break()


    title4 = doc.add_paragraph('Course Competencies')
    run12 = title4.runs[0]
    run12.font.size = Pt(16)
    run12.font.name = 'Arial'
    run12.bold = True
    doc.add_paragraph('')



    para5 = doc.add_paragraph('The desired learning outcomes of the diploma are to educate and train students who, by the time of successful completion of course, will be able to:')
    run13 = para5.runs[0]
    run13.font.size = Pt(12)
    run13.font.name = 'Arial'


    table = doc.add_table(rows=10, cols=2)

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'CC#'
    hdr_cells[1].text = 'Course Competencies (CCs)'

    # Manually filling in the content for each row
    content = [
        ('CC1', 'Data Visualisation & Journalism\n\nLearners will be competent in applying data visualisation and journalism techniques and tools to communicate data insights effectively with stakeholders to support business needs.'),
        ('CC2', 'Analytics & Computational Modelling\n\nLearners will be competent in applying data analytics and computational modelling skills using tools and algorithms to solve business problems.'),
        ('CC3', 'Applied Artificial Intelligence (AI)\n\nLearners will be competent in applying AI to build intelligent machine reasoning applications that derive hidden patterns and support decision-making.'),
        ('CC4', 'Data Administration & Management\n\nLearners will be competent in Big Data administration and management through data modelling and data manipulation techniques to meet business requirements.'),
        ('CC5', 'Analytics with Programming\n\nLearners will be competent in developing IT & data analytics applications according to users’ and business needs.'),
        ('CC6', 'Data Strategy & Design\n\nLearners will be competent to design robust data strategies to manage Big Data platforms aligned to stakeholders’ business values.'),
        ('CC7', 'Emerging Technology & Applications\n\nLearners will be competent to synthesise and integrate different emerging technology trends and developments to value-add and provide solutions for businesses.'),
        ('CC8', 'Business Needs Analysis & Strategy\n\nLearners will be competent to apply the business needs analysis and strategy skills to deliver service excellence for customers with diverse backgrounds.'),
        ('CC9', 'Data Security & Governance\n\nLearners will be well-versed in data security and governance and competent to apply cybersecurity principles to uphold personal and professional ethics.')
    ]

    # Fill each row with the CC content
    for i, (cc, desc) in enumerate(content, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = cc
        row_cells[1].text = desc

    # Optional: format font and style of the table content (for example, Arial, size 12)
    for row in table.rows:
        for cell in row.cells:
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                run = paragraph.runs
                for r in run:
                    r.font.name = 'Arial'
                    r.font.size = Pt(12)

    # Align text vertically and horizontally (optional)
    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT


    competence = doc.add_paragraph('Course Competencies')
    Course_competence = competence.runs[0]
    Course_competence.font.size = Pt(16)
    Course_competence.font.name = 'Arial'
    Course_competence.bold = True


    Semester = doc.add_paragraph('Year 1 – Semester 1 & 2')
    Sem = Semester.runs[0]
    Sem.font.size = Pt(12)
    Sem.font.name = 'Arial'

    # Create the table with 4 columns (Core Learning Units, Hours, Credits)
    table = doc.add_table(rows=1, cols=3)
    table.autofit = True

    # Add the header row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Core Learning Units'
    hdr_cells[1].text = 'Hours'
    hdr_cells[2].text = 'Credits'

    # Define the content for Year 1 Semester 1 & 2
    year_1_content = [
        ('ITB111', 'UX Design', 60, 4),
        ('ITB211', 'Statistical Research Methods', 60, 4),
        ('ITB511', 'Programming', 60, 4),
        ('ITB611', 'Network Administration', 30, 2),
        ('ITB811', 'Business Needs Analysis', 30, 2),
        ('ITB411', 'Data Modelling', 30, 2),
        ('ITB221', 'Decision Analysis', 60, 4),
        ('ITB521', 'Data Structures & Algorithms', 60, 4),
        ('ITB621', 'Operating Systems Administration', 60, 4),
        ('ITB731', 'Data Visualisation', 30, 2),
        ('ITB911', 'Applied Cryptography', 30, 2),
        ('ITB421', 'Data Storage Administration', 30, 2),
        ('ITBW21', 'Visual Analytics Project', 30, 2),
        ('', 'General Studies', '', '')
    ]

    # Populate the table for Year 1
    for unit_code, unit_name, hours, credits in year_1_content:
        row_cells = table.add_row().cells
        row_cells[0].text = f"{unit_code} {unit_name}"
        row_cells[1].text = str(hours)
        row_cells[2].text = str(credits)

    doc.add_paragraph('')

    # Add "Year 2 – Semester 1 & 2" as a heading
    doc.add_paragraph('Year 2 – Semester 1 & 2')

    # Create the table for Year 2 – Semester 1 & 2
    table2 = doc.add_table(rows=1, cols=3)
    table2.autofit = True

    # Add the header row for Year 2
    hdr_cells = table2.rows[0].cells
    hdr_cells[0].text = 'Core Learning Units'
    hdr_cells[1].text = 'Hours'
    hdr_cells[2].text = 'Credits'

    # Define the content for Year 2 Semester 1 & 2
    year_2_content = [
        ('ITB231', 'Supervised Learning', 60, 4),
        ('ITB531', 'Web Application Development', 60, 4),
        ('ITB341', 'Data Wrangling', 30, 2),
        ('ITB641', 'Data Integration & Clustering', 30, 2),
        ('ITB141', 'Data Journalism', 30, 2),
        ('ITB232', 'Unsupervised Learning', 30, 2),
        ('ITB931', 'Data Privacy & Protection', 30, 2),
        ('ITB441', 'Predictive Analytics Project', 30, 2),
        ('ITB251', 'Topic Modelling & Sentiment Analysis', 60, 4),
        ('ITB841', 'Big Data Modelling & Management', 60, 4),
        ('ITB541', 'Programming for Data Science', 60, 4),
        ('ITB721', 'Natural Language Processing', 30, 2),
        ('ITB711', 'Emerging Technology Synthesis', 30, 2),
        ('ITB831', 'Customer Experience Analysis', 30, 2),
        ('ITBW51', 'Text & Social Analytics Project', 30, 2),
        ('', 'General Studies', '', '')
    ]

    # Populate the table for Year 2
    for unit_code, unit_name, hours, credits in year_2_content:
        row_cells = table2.add_row().cells
        row_cells[0].text = f"{unit_code} {unit_name}"
        row_cells[1].text = str(hours)
        row_cells[2].text = str(credits)

    # Optional: Format the table font
    for table in [table, table2]:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)
                        run.font.name = 'Arial'


    doc.add_paragraph('Year 3 – Semester 1 & 2')

    # Create the table for Year 3 – Semester 1 & 2
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Core Learning Units'
    hdr_cells[1].text = 'Hours'
    hdr_cells[2].text = 'Credits'

    # Define the content for Year 3 Semester 1 & 2
    year_3_content = [
        ('IT3301', 'Applied Machine Learning', 60, 4),
        ('IT3381', 'Applied Deep Learning', 30, 2),
        ('IT3382', 'Advanced Data Visualisation', 30, 2),
        ('IT3383', 'Data Processing on Big Data', 30, 2),
        ('IT3384', 'Data Platform Management', 30, 2),
        ('IT3385', 'Machine Learning Operations', 30, 2),
        ('IT3386', 'AI Services in Analytics', 30, 2),
        ('IT3387', 'Marketing Strategy', 30, 2),
        ('IT3331', 'Final Year Project', 480, 12),
        ('IT3336', 'Internship Programme', 480, 12),
        ('IT3333', 'Overseas Internship Programme', 480, 12),
        ('IT3337', 'Final Year Project (24-week)', 960, 24),
        ('IT3339', 'Internship Programme (24-week)', 960, 24),
        ('IT3338', 'Overseas Internship Programme (24-week)', 960, 24),
        ('', 'Prescribed Elective', 30, 2),
        ('', 'General Studies', '', '')
    ]

    # Populate the table for Year 3
    for unit_code, unit_name, hours, credits in year_3_content:
        row_cells = table.add_row().cells
        row_cells[0].text = f"{unit_code} {unit_name}"
        row_cells[1].text = str(hours)
        row_cells[2].text = str(credits)

    # Add "Electives" section heading
    doc.add_paragraph('Electives')

    # Add "Prescribed Elective" as a subheading
    doc.add_paragraph('Prescribed Elective').bold = True

    # Create the table for Electives
    table2 = doc.add_table(rows=1, cols=3)
    hdr_cells2 = table2.rows[0].cells
    hdr_cells2[0].text = 'Core Learning Units'
    hdr_cells2[1].text = 'Hours'
    hdr_cells2[2].text = 'Credits'

    # Define the content for Electives
    elective_content = [
        ('IT3388', 'Big Data Management Project', 30, 2),
        ('IT3389', 'Applied AI Project', 30, 2)
    ]

    # Populate the table for Electives
    for unit_code, unit_name, hours, credits in elective_content:
        row_cells = table2.add_row().cells
        row_cells[0].text = f"{unit_code} {unit_name}"
        row_cells[1].text = str(hours)
        row_cells[2].text = str(credits)

    # Optional: Format the table font for both tables
    for table in [table, table2]:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)
                        run.font.name = 'Arial'


    doc.add_paragraph('ITB111 UX DESIGN')

    # Add course details table (Course, Course Code, Year, Duration, etc.)
    table = doc.add_table(rows=6, cols=4)
    table.style = 'Table Grid'

    # Populate course details rows
    details_content = [
        ('Course:', 'Diploma in Applied AI & Analytics', 'Course Code:', 'ITDPEFA'),
        ('Year:', '1', 'Duration / Credits:', '60 Hrs / 4'),
        ('Pre/Co-requisite:', 'Nil', '', ''),
        ('Async Lecture (AL):', '15', 'Practical (P):', '42'),
        ('Tutorial (T):', '0', 'eLearning (E):', '3'),
    ]

    for i, (label1, value1, label2, value2) in enumerate(details_content):
        row_cells = table.rows[i].cells
        row_cells[0].text = label1
        row_cells[1].text = value1
        row_cells[2].text = label2
        row_cells[3].text = value2

    # Merge cells for the last row (Pre/Co-requisite row)
    row_cells = table.rows[2].cells
    row_cells[1].merge(row_cells[3])

    # Merge cells for the next duration row
    row_cells = table.rows[5].cells
    row_cells[0].merge(row_cells[1])
    row_cells[2].merge(row_cells[3])

    # Add Synopsis section
    doc.add_paragraph('Synopsis', style='Heading 2')
    doc.add_paragraph(
        "User Experience (UX) provides a positive experience through any form of human-computer interaction. "
        "Through this unit, learners will develop competencies in designing and creating intuitive user interfaces..."
    )

    # Add Learning Outcomes section
    doc.add_paragraph('Learning Outcomes', style='Heading 2')
    doc.add_paragraph(
        'At the end of this unit, learners will be able to:\n'
        '1. Use storyboarding approach to conceptualise and communicate...\n'
        '2. Design intuitive and accessible user interfaces...\n'
        '3. Undertake a technical lead role to drive the team...'
    )

    # Add Topics section
    doc.add_paragraph('Topics', style='Heading 2')
    doc.add_paragraph(
        '1. Importance of UX/UI in web design\n'
        '2. Principles of visual design\n'
        '3. Web accessibility guidelines\n'
        '4. Web client-server architecture\n'
        '5. HTML Document, Elements, Attributes\n'
        '6. CSS Rules and Selectors\n'
        '7. Interactive Web Development\n'
        '8. JavaScript and Control Structures\n'
        '9. JavaScript functions and event handlers\n'
        '10. JavaScript HTML DOM\n'
        '11. Design principles and heuristics\n'
        '12. How to conduct usability testing\n'
        '13. Communication Skills – Oral presentation...'
    )

    # Add Key Tasks section
    doc.add_paragraph('Key Tasks', style='Heading 2')
    doc.add_paragraph(
        '1. Design and build client-based, user-centered web pages using HTML and CSS\n'
        '2. Design and build user-centered web forms using interaction design principles\n'
        '3. Creating responsive layout for web pages\n'
        '4. Communicate the proposed user interactions and experience to key stakeholders\n'
        '5. Build interaactive web pages using Javascript\n'
        '6. Communicate the proposed wrebsite to the key stakeholders'
    )

    doc.add_paragraph('Assessments', style='Heading 2')

    # Create table for assessments
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Table Grid'

    # Fill in assessment data
    assessments = [
        ('Assignment', '35%'),
        ('Practical', '20%'),
        ('Project', '35%'),
        ('Presentation', '10%'),
    ]

    # Populate the table
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Assessment'
    hdr_cells[1].text = '%'

    for i, (assessment, percentage) in enumerate(assessments, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = assessment
        row_cells[1].text = percentage

    # Add heading for Texts & References
    doc.add_paragraph('\nTexts & References', style='Heading 2')

    # Add references as a numbered list
    references = [
        'Lean UX: Designing Great Products with Agile Teams, 2016, Jeff Gothelf, Josh Seiden',
        'A Project Guide to UX Design, 2009, Russ Unger, Carolyn Chandler',
        'HTML Comprehensive Concepts and Techniques, Shelly, Woods, Dorin, 5th Edition, CT, B',
        'Teach Yourself Visually HTML5, 2011, Mike Wooldridge, JW, B',
        'Brilliant HTML5 & CSS3, 2011, Hill, Josh, PH, B',
    ]

    for i, reference in enumerate(references, 1):
        doc.add_paragraph(f'{i}. {reference}', style='List Number')


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

            # Base64 image to be added at the beginning
            base64_img_first = 'iVBORw0KGgoAAAANSUhEUgAAAgYAAABrCAYAAAAMykoNAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAgAElEQVR4nMy9ebxlV1nn/V3THs65Q6UqlaQqCZmAYABBBDQOLTPIlLQtpomo2A70K2q3KKL92trOn/ZtFfFV0RYckUEcEPFVtB1waAaNAk5ACJWEVFKVmu69556z917T+8faa599byqpG6rQfvI5uXXO2WfvtdZeaz3P83t+z7MFFz/nuwAgpj+hAgFIBwTwAYQH6fvDJv3f/ngg/aB/5Y9F158zghDgp+mv3bTM73i9CEc26gqaRYlEErQnhABBp9/LBgRIBcFBGTSSCS3yqeuXfsZzTrsVmExgvg2FhmBTW00B1kMXQRfLfgmXmoiAKCFWDP0W4346kIDs22E03Hfv3Uqd/GXZ3hsnskMIWHhwKDwKAE3HWBzp90IEIGL68UojonGi6C8/53xEoqmLEro5h7V8ya2uul6wYINAAEoKJBCwCASFCoT+VmpgCyiAQNW3TBJo8QQMEJajNGr/8t9y5zFnPDrGdNqtCKct8cRp/PHTcP8WxNPACWADidUlUUqQEuUbvLUgQGmQUhKjYKVTBAKbRUhXCiD7WxYjBNlfPIi+R7LvW5p/ziwbZ4JiNUgEgpOTkObDdm79WB74mVIK79PASYkALgaqMD5UgIAQI2eA7R33SdLPv745EeLZLn0OUUoRQjgopbwSqLz3KC0JIZxQUn3COW/T9SRSSpxz41bsqa8PIkYpHuM9lyEotGZVCqW6ziMlDdAIQSekOO5c/CiRBaQ+CwFidO0YI3HH/nFu0Vrv6IvWeuKcO5CvIfuxjUAMbANnxp1TSiCEwLnQ/14O/364opSqvPdXK6X2e+8xRmGtXwB3AqfycVJB8KCUEELK6733l8e00NalREToCmPmzvvTAm4PIRzP88kYg/f9njjI2e+fNorgPSGAUuk47wNCUMXIDVrLS2Ok9j7UxiiAM9Z6JwTHjC7/sbO2kyKNjw8eiAghiDFijMFamy8mlJKPjDFcGQK1kNRSUsYIMWKFYFuAD5ETMfAxYEPINM9Ff/7cHynlrr49tOyezyp1tAjBX8KOlTVIA5wRApsvI0Rah/0yflgipUQphbW235uiijFeBVwiJbKfzV0MHDXGHM3H7eX+5fPvXhdKpfu4W5TiSqXkjVLKp0ynKzdIKa9WWh1SSu2TIq2EEAMxxnnw4WTbtZ9cLBYf71r7oRD4APA3CLZkr64F/X40WpL62htu+H4AkRVXrIgCQm8YFCHtwkG6tOh6w0AsLYD0OwREgYwimQiiBcCUBW3bspjBpKyYypa775g94fR9R74igi91QecswTmQEq00wQdCSOMYfLqERKLRTFbXb7z62mu//5PmIIUxFDHQtQu0kSipaJsWKSSFmhC8R8qkuKOwRJHbqRCxTLdFxNRPH0F4grQ4CV1vGIiu5eLrHxX/4a9+x5W6fJN1HZKlcvzXlkCk6zoqBAcOHLj1KnHw5qKybJcNSmvcoqBUBuEDzjlkMUdrhbSa4D1WCYSA6FZRUqK1JIYWH2eDcoZ+3IAofN93k/6qgEAggsZ7gQ1pZiipkEoxc03oau1PCd/cubl5Z9jY+tiitR9pQvx7G/gQzn0UaD0OU6TFGwJYm4yADo9GQ2EgeugcIYDuDYgurxsBO6ZkHH9A34f8ya5V8BCSF3c2Cuq6+vK6rr5Pa30lQoiiyAZeWtQ+HRuC958MIfz2fD7/EWvtsRCSohAsF7uUqa97bYcQ4vD6+vqvSim/QCmlhRBCKYFUCtt13vtwYj6fv3J7e/4bIYSHtfE+lNR1eWM9qd9mjDmspJRpM4kIKSmKAu88PnhiiPjgo7VuY7FYfOdi3r5+GGqRlM2nKlkhlGV5dVEUr5tMJs8GtJC9SyLyPIUYQowxbocY/2o2m/14s2j+yPuIlHEYc5cU516nAZCU9WQy+Y6iKF4jhFhTSkkpQRtD2zQxxmjbtn371tbmy73HBg/GKDmdTn+jnkxeLIWQAFKppHj7e2Sdgxitte7ts9nsK6117oFGwYNL8H7wy9I0DRSFfv5kMnljVdeXFMaIGCMhBKRSxBAJwSOljLOtxT+7ra3PC8GfkUINBkGM6X5lo8AYc3h1deWdZVU+QSmllJQIIelsk5ZTb0wIBDHG6H1oQgg/e+rUqW/zRJ/P93AlG+Tj+ayUWl1ZWfkRKeVLJ5Nq+iA/jUC3tbX1d13Xvb7rureEiIsRsrGyF5EyKfMQwtD+uq6/tCzLH5NSHq6qQoms1EOMXVqHHzh16tTNIYTjezn/uG/j642NAq3FNcaYl5rCfGlRFI83RmslFdY5pEhGk0wW+DCpBUy895OiKK6cTCY3KqWIMcau7Zr5Yv6Xbdv+dtf634xw77I9AiEFYu0LX9ufxQIBHdKYRuGTIo0Xpc1UJEty+X22ItWOjoooexWSFrINHm00ttUIKdlXSdrto/HY3R98NSc+/KOFPIJ34N1qOpvqPWifPXGFEJImuuQQrj7pP13zmc95bcMaIUSkENjOEkxNVJrGdShlKEyB7QIiZMPAgQgIHDKCCsmV7HSTBiTudOli369SS7S3uO17Nu//u//1NIqtv2V+N1O5gAjzWPXKxo1QCSCAQCEo+/N1PQqTv8+ft2edMHuWVQEucmABX1pf/lvfLMLNRdwG36C1pu0KpFJI7dLkdgKtSpAF1lomQIgOWzgQghg0QmiqoBE+Qkjt80IRhBxcMCm3ERFEN0VIQVsGhAwoPDF6GpkURYWidJK6i0TAlyWyTF7I1mLu71ezjTs8H/gEvOcT8L+OUP3dEXx7t0mbgnMNLk09hIDVaBBCsIiOjgAy3cdJSIjCPN9GAURJ5bPCCHgBTu3aEdxDe9FlWWKtJYRAWRb/dmV15dcn9URJKQh5AwUyXECMhBCJyWKn6+yR2WzreW1rPyJlUmDepxmj1PLf5xKlFFrr/3rgwIHvy94TQIweqRS+V5zzxeIDW5uzp+ZNrOvGSNanhBjIffvW3jOdTj9fyGTwhRBw3qGVQkiZvKh+c4pEpFA0TbN56tSpRzsXju2pgw8ixpjBKIgx1uvr67dVVfWYuq4BcC71b4dhECMxhGyoua2trf+ymDf/TzqfwjlPjHs3zLKyLMtydd++fWeKopDZA+66Zhh/1aMaJ0+ceKpz4QP9+ct9+9Y/urq68gghJTEEhJC9ARyQUuK9T2iG92xtbr5iNpv/3IPcirN8lpVlgmZ8QkH0vn1r/7S+vu+Rzrt0X/rxyF57BIw2dK1z95848Sjv3REpJEIKvE/jPfZ4p9PpT+7bt/aNUkpCf54YAiJ7SQJEhof6NRBCDCdPnnha17k/f0BP9ogYnO249fX135pOpzcn9Mw9yC97EYKubeN8Pv/Vpmm+xodos6e8F+NgrKh7tE7s37//nyeTyaONMSwW20iZDCqlFD54go8cP378G51zP7XrbGc5Pzv6txs50EY+uSiKV0/q+sVVXVVGp/3OB9/PGzkA4VliWgREIkabtE/191wMx6TvF4t23rXtbzZN8yPOhQ8P7dBKMby0RvUvrTVa6XOP3DlEKYWUiunKCgLY3NpibW1NXH71NT9IWT6t65IFZ1TfYe+JMSJFf0Oy1ycFqAQ7d12Hsw7bWWxnqaqKGAOLxRxjDEVR4KzjYfv18YGvtmlp25a11dW1g49+9K/RdhdrU+DCw/M2Pm3i4rC3R8CHDJVqjNb92KSJkDaI2G+0Am3SmEspUEoTQ0IfYkgda22z62LxAf+qqjIZZ9bSdZbgQ5p8MeKD7zcij0BgpMEHz2xri7ZtqapKra2t7z902fS5jzp81Q8+9urH/tX1V15/+6EDh16vtX5W0zS162+jVAlagx4my50WaTPK/y2tAgZdvVwM7Ly/e9gYxp7CdDr95qqqVN7Mu65LL2txzhJ8VjhpPLUx1HV1dVXVb1daTkJghyGwFzh9vDEBK1lJee8HgyUhbLEPT0Qzbtv5ilLy6sl08rnGGIIPaUMKnuAD9EomhDBEEb3zfThIrQHPO9/r5zESQmCMeUFVVY9JBqOjbdt0/d4bDiGkDbBXghEoy1JPp9Mf0ka9KJ2P5YTYgwPbIzUAOOeUlAmq9d7jnEuQdowIIRPiphTeJ6+jX4otxD8PMeKdo+ssne2w1qU5ZC2u3/OUVGht/i/RIws9XP7QMvRlCX9oo55R1fW1WmuUUgOiIpNlOigxpRTO+48IuBsYDN1seI7mfmWMuUkb0zsPSdF4H/oQRhi9fD8XIxClNuYl8mz2zB5lhBLkPlxb1/VNWuuhTw/1KoyhqmsxmUxeVhTFt8sekdyhJc9x/TwH8zmFSHFg5xzaGIQUhJhQxRhiDpusyj10PI+x1noY894IPby6tvKLl15y6V9etO+iLyurqooRrO2GdS+EIIeAMjIX8yYnGEJDwScjwrs050IMwxzYt2/fZN++fS9bW19/fz2pfkxIVgG0+9sf+l6ATveTqlcKTpQ0YvXQZY976de3YnWIiYe062P7SauGvS1BrRkxEKTjHZGN+RxdaUxtsKLkhJOY6bXlyqOe+6bZh898jndnPqnCKVR/lhAkAQFSo6MlimYZzG7e+77777jze4vtNWKMNOo49eoKnbN0BNT+x/6b6YHrn16oK+jUSvIQhzZJZNQgPcGcTu1lhYDC9h6mjKpHFPpeGYUq1zi+2KC+4kmPYXP2P909t33ZRG1Y50HSJJ6BVECRuBUx24Ye0WufBFwIEHmcfT8+5yeqU8QYOYXmrczf+j7dftA5xxl5EcEGpiLihCPIbaKSmJXruOjA9V+yeuCSx4s4oRSJU9IVAec7hA/UBYjZCc7ce/vbT5/8yD8gPE4GglgiKSbOQYCLc6qVqnxEOX301fXkCQen1ZWPamJx3UbLoa2GFWvxvuP+yqJkwHSCECFKgxI1V25MuILI8bLlCWEmp85fIYR4xXYwX38CdeQDdL/yfro3/qnnzmMENo2GsqKKHmMDokuIzXa5DSJQ9rZMKwUIxSLFVFmxFoOj9Wkaje2Dh5JRfJWyKm/QCY4jRlBSorQe7S/L8EUEiBGlFHVdPc57959ns/kPQfISxsjBQ0nelLK3lxXV8n2C/pKnLgeP40KJ1uqFUkgV6Tf7SDLadTI+g/fE3gj1IRks0vkUziuKm5xrful8rj9CC9Baf4YxZug/ZOUploBNOnj4S4xM6lp75358Y2Pjj5z3i4F2tIfrj725vg2DkkrXFzjney6R6Md/dx/8G4L3t2qthSkSxyXdx9S/vEkLISnL8onGmM/ruu4v9nQf8yExDvNpUk++1hgju64lhxAgIx/JhiBGnLPMZlu/FGP0efRCiEgpdnjqxpjP1lpfmY3v/H3qaxiU0DCio2YXRfH8ru2+LQR/XlZqnvsxxseaUWhEiIceI+c9UgjKshTe+//ivX9r17nbB8ToYSyV8f3IDmxVFUuDdLRWH45kQ7//nSjL8kun08lP1nV9qdZquIcxBkIf1B04G/0cH+Y7KTScnKVkqIueHyGEWK6PCNEHGrtASMl0Oq3qqvqW7e3tz92azZ6vNzc2/hsAvWEwjJQoQYQnhRi/PpBgh3Gnh7+BXtn1v0sfDG+10UymU3xUSCmp65qumeG6ln379h2uDh/+tY17Z88OXdtKCaaoaJrs7WdYBYSCaAAh3tttbL63a0gf1o7ZyZMJUZCw3dx7cRcP/NlFBy+/IYpsufZtIlnFgjDgSCEGghA99yBDwEs0QGnFfL6NMZrZbINrrr32pnuaO7/TbB/9Pr/414cM8mblO0Hbdm/ZCHMCsJALXHBEBJJI03na6FkrFs8+qNW3a63oGk/rW3zwLFqHUlAoxXx7wcbRo39w7PgnXlawaMHheh899iZP0Rs8QsF8PufYxjYtqHvgGgfPWWPlloOyujHGYNKkjDjvKWXBZFLR+sj2YpuSAo1GKglCoREoqbAxCBP8NddcdsV332fn33qw2Xzr6e35f29C+CjNgsY5FFBRnX2Dj3Ewws5XMvFNK7UvQaRpM9RKD55pWnD93BlxGIQQFEVBVVXf2rbt6631p/ov4JxmCTuUYOrWzo3ee4cIyXOXWg4kqez5jQ2bT0GE1vrFPsewyX1LCtN2lhD8gFTFEPvjIkppVlZXn9Y0zb4YOfOp2ipjBRVj3OGCJWi3JyHB2DIYjgkhUpYFk8nkuqZtv3oxb34aegf7YbYlQ//Zq8sbeg4F5O+X7Ut8kkWz+HOt1d9MpytP1noZihGkjV32vxUizbWyLL/eObc3w4Ck4PKxptCH67p6kUDQdi2mKAYlkvudeQZt25xumvaXBQKd0AN2j0pSftXNOaQT+z0ye6wx9lyN3jDIxqPokbyyKK5ZKPWZzvm/fpjDDaTx2MUxMMAw5j248qDinYMeHamqamKt/a6ucy9/OG3IazAbqdnDDyGwWCSObSTtB0NIhb0ZCJlD0a/Xoq7rH5xMJt9SlkZJpWi7rndAFEoaEJHg0/zJSn9o51nOr41JoZ0Ye0QzOxSJA2YXDbJvh9IaY8yNRutX6YLkYmVzrugVpsMSCLRC0cmAF8nDLWOKObuehyl92cMy2TCIKfbcr2HfdRRlQRstXdegpUGommALtpt1OHzrF1r74R/h9G/+Z+9mUdCgJcTgUCHNggiUVqK8wmmH7TYRpLimnTsCDo1HCVjEfzoRwuxWr/2fTQ5+xvpmXINYQdT9lBfEqPCspf64FC5xygIeERPFVA43VYMMNKHETK7kxNZEXHHDl3zXHe8tboNP/i7yPsD33okGqv4q6XzIJqEsmRAXddpY+RSosWeRUgYkHV6mPtzds241DodH4ZBITplVWLnikduXPO+XF5dcV2szxRYWRJus6hCZCo0JR9nauPOjZxYf+0rkqTYjHnGYdQERQPf31xIgRI6UGqLxVcftf0C4vZPNz6Bmn/m5Bw5+0xfFyZc/r62rQ9Ziu5boPYVSVCs1W/NZGv823eg2FCgFUSsulpJLjt3DU8ty+p+k+Q9nvHzpH/vuDX8E3/eOSt/vg2S7n7+m9YCk7aEe5RX4gOxJgzOVlPnEjZwsYHewZLdkDzF5djIZkr1hILPFzk5Ed4j7wUD4Kopif1VV/9H77R8KAUQMe4pxjwlb2SjIm+JgBPRme/4+b2CZMHkecuna+vqNOsO4fegpw5UhBowphn5HAaUogYRgFMZcJKT8IhF5R4w7ve+9SkZIxn3JSkL1HIcduqz3lvI/k+IOaK2p6/rVbdv8fPB0e7TLzipjYqAp9OA9e+8TgiHytUPPIwmubdufqOr6V4xIxmQmRnvniErhczhCKcqyvLlt20u7rtsTP0OIJaG1rqqv0NpUMYaBWzAet0gyDJyzbG1tvQk4FkmKIxk9fkeMG9BVVb3AGEMIDq0VQph+/CWdbQfDY4ht9/udFAJTFFIp9WLgrwceyM7zn6Nv4gHH5+wEpRQhPvQcF/19gcRXqarqpYtF893O+bv2ihbsJk3m/vbhreF72fNvvA8Po4+RxN2Rk6qq3zhdmd5SlYl/5kOgKsthXVtv0zn7PSYbmWdrY2+/4zq7DIFItWMPCSFQlOUQFpP9nlKW5Qvl0tthFKdYnlwqmayLcexGjeM4asf3SspEduvfl2WZYoHeY3RaFEopqroixshkMmH/JQe/UV100a0E6Nrk/GuliPS0AiAQsMHiXPJcAwEXkvEiSMlQSoNRGj+bffDksWPfEGMMSp6l/fJs7VdnPS5vQEoqnHVUZYmz1lz/uMe/EeSj9ja1Pn3iHLRdyrZM1mCvnGSCLA0GjwetVsvLLnvbpVdecZkpDPP5PCm7Pi5aGINSisVivnHmvmO3sD0/buqa3fOD8fwAimmRSKHWgetTImUBWkciH7z/+P1fe9exu5549MzRdzRNE9Oi9sznc+bzOUYbZJ+NUlYVhUmbjh/SkiRN2zCfzynLon7EZVd94yMvf8QHDxw4cAsh7lgNccc/HnxR7gVCXo6v25Eml+H6hMZmJvbyspn4NsS8I8SQNt2iKL5Bab0CaQzlHmLIS09vCd/2RETKsiTfkLNtQnuKUT+0PMcYM3He0dkO5x3OO0KvdKQQdLajsx1N2w6wOMRlaqcQN59vNkI+1ziUMsgDiCNxx61PKYp9RkNRXK2V/jJ4eDbBEJ9nIIEOXCbbdYMn7TOcPEYclYIIi0X79rZt73Q+xeCTUtFobTB9fBmRjjfGrEopX7a3tjFMaKWEMqb4WiESMqqN6fdrNYQqRpB827btTxa9sReCHxTDLqX2GUVRXJ882zAola5L3KudEpdoWX8bEsdM3pSGcalQ9ypjgzDH4XMbc4z9oV459JfRHGNMobV6Vd/cPcl4beW2ZwM8x/UzCjSer3vhGHgfUFIV9WTyi9Pp9JaySKlZiTAYh/ONuTZ95sfAFchrIin/5fqIMaYMg6wURn3IejwbBcEHlNZMJhNWVlauk1YGrOxzxPv4hQR0EJjgcaFERkklNUUUiIVHt7BiS0xbsIiRVgg6YWhRdFIRtMErTRehtR6pNCjwOKIM2BjorCHqFU7NNNXBz5Yrl7/0Z1j97CdSABoECaLcDBUzShYIFghsWCWwhi0DtoKgJV4ZWibMbI0NFqVOwfxv33z0g2/6ifVwjLA4jYsOaSROzHGyoUCjrMGhsWgCnoDHC4+VnkZBo8CKQBctzlsQik7tY9Ncx13mMw9WT/iqtxCunaDXQAYEHaVs0DREwBRTfA9ZitC/vEEEQ9CRoB/O9nR2EVKTqg+sIcI+nK2RQiH0jCgbTtaRM+oSwRXPeEN96Qs+q+nWsE6xPvFov8GshI2wQKrThO6v/YlPvPNrWbz/78qVM9huO02G7F0FkCF95POIbXaYFuoAk+BYFA0zNUd3Ae0MH0fzZi0+8hVi8+Yvru+55WdWt0984tAq08rgQ4cKBi0qgp/TLE7izBaqaiitZTUq5Lxk6tc4ECum88hn3XeKb97sDv3JcfvmNzn/xqd1zfTirsHKgKwLtC9YFSvUvUkU6Yh0KB9QHuZGMDdpNxVnZXnvGt+Rt2qt7QmVDHD97tjiOP6fCFLgnM0hhcuVlF+Vz+3suT368cY4JkFByjjIG57ujYCxV74XxCCf62yb2L596zd57wfDLbOv00YYYYiNp/CPkALfkwHz+fYfOPA853w1Vgha6we95rlkPAZ5w8sGPWTjbMnAT+jKkiuysrr6GinRMez9+uPwTTcyBLLXmmHlDAsrtdyEu27IVGrm8/lPeecxRgOJsKt1yo3PPIPOdhhjWF1d/WrAjI2SrMnEbtM2DgS9ZxujH6l6Yh59u5WUvRcbUl2CrmNra+udIfCxbhRqct7tINsCFEXxIu+9TPNsmYmTyYv5eNdnphhTJGfDpLRzay1ra2ufAVw/JjTmEOhexn5oX294dl031HlYxt/jEEN3PUqUY/BKa0JMocyiKKjrydcIyaV5GMdGX1mWw/vcvt08kxw2SnvACAWLyzDD2KnM51Zymeg+MtrFZFL/6Pr62kvKsujJxH4Ia/v+HFKq3kgIaG3Q2hB8JKXjLwnJvjc887rQveO1NFaXDoYQEqN13y4GQqkPYe2cKyPExHp2PRMyd5p+gIzWaKWQSvYDFvt0oIjS5/ZYjEnea1GWq2uHDr2FigOZTJ11kky0wWEjD7mXYenCjhdLciJCJITX3HnnXX/aQ0g0TdNvWiqx5/dgue6wcGOeqKnfZVk+afXQoZ/NjorWS2hYS70jvpstywd44OcpIYRMCerjrbGfHH0xj7Zl3+WH/+8DV175Eq01Pniss1hrU/ZG21Ktr7NYLLj3rrt+gLZ9O0C7YHcm6tnHZ/Q667dSQh8H3J7x63eeOPnZH//kx983bxZcsv8gjWshRkzRZ5O45JFWZTWMn3MWZ91AuolEJpOJODw9/PJHXXn4PRKulAa6psEoQ+tb6qoe2peh3d0yZDact4jR/+njnmKI82cPoI9zvkoI6gt04fOWh1gD60qrpy/fjngTI6Zf9togfZ1Nrny4EOJSY/SNY69nxBk47/ZnxZBh8jEZL4TEdYgjZWaMeZw25ubzvvDDamT/J4Sfs7bbyDA8mT/SGzhidKyU8rFKqaeNjZJ8srhr4/AehEQYY14hRL83w2i8+81GiFS7xNronPsxHmQHGiEGoq7rm3OYpL+fgwIOg9JKSia1NTHzB/QyzRVjjHlB7seYq3H+styfczZEPxtThtYIWcgZFGVVrtRV9c0DCbXv0+A9X5B27ZTlOfu29qGfqipeXpTFK2Uev5jvb+JPKKlSbZTgByM0haISt6NpmrBYzP95Npv96pkzG9978sTJVx47fuxr7z169BvuueeT33n8+PHXnT595t1NszgGEa0VSiXDNITAfLHow505YyUZRHqZmK4AhU9l//qhlXSqSJMgOqQUUGliTLFlIQQqNKkTGKTM3kRPepMKQeIcqBwLigGBRyBREUrZpBS5+hDqkkuuZ6F+nvlfv6Sx9zhTKKK1RClACcAh/Faazj3nSPcor1MMylYGME2HbI/bxexPbjUrfMCUT7zcinU6v4qPCh1PI2SgkRmq7dnP/daWp5cSERMiIi4QcQGyICqDNQWUh1g59LyXzZvV9/rZB37KypODLvU9tIjvUwKHgXYXyibo+9278XGW1n6EGDWuU6BXYN9jX+we8bT/poqrmC8WVHpBjJETHozRTOhYa46ycfz9v8V97/0B7WcooXBRIb3GRsdQ+TKOMvyy8esLgoCuTL2aNr33jCMATgBGEwrDZrS81XLXnwae/Tvrkze/cPXAC27c3qLEMV0otDKclC2tj9Qm0LXbFFWFd45NLZHC4HxEtI6pkNwgSl513D7pRfLiP/mB9sQzPw53nvELqvU17p+dQayURNdChGnPYdh2yXpeUobOU8ZKsYc4Ze8Z+BCS0dwrgJShUF+7WCz+fdvaX+iduv8jZPdmqLX6IqPNRfl9zFpXLI2zEANaaJA5T36Uo589e3Sy+5wAACAASURBVCFEWZY3Wev+BBi8rd2VDD9l6SHVQbGmiwx90loNFQ6H9LWy/FZn7W+HcybBX1jx3m80TfMGY4pXlWVB9AkV3Q2vZ2+6ruuvn81mf7g8wwOJEfmdVvqKqqq+WKplVsryb9//PqzSNM1fWGvfd/ZWpmv08/jqyWTymWMlPoxy0l1DWrno9/5sFMSeMyFEcpaqqrppa2vrRzNakHkC5y+9YdV72KktckBLRB/yGl+vLEum0+kr5vPmx4ETS45EZDeX5bxbN7oXUUSM0TjriUS01o9aXVv58bIoBYKB3wFqGRIWDOiH6lP6m6bFWns0hPDzm5ubvxpjvCNlluyUhOR4bOeYzbYLIcTjjDE31XV9S13X1xdFgdG+z6wSg1EkxR6w1AwZ9ZUWB0sxk1ucTd6nc31cJSMHMewJyowxUhQlIQaUVFx22WU36QMXvyZ9t7tYgFiGSs7mpophjhD6AhCEcO+xu+566YkTJxZlWWK0Gchbe9mVs0UvpRgs/OylSymp6orDhw//D7229oW4nIqWYdy8kMfXeaDFf14yvoQQGFP0FbAEoqoed8l11/1iVZVqPp/Tdd0OkpAQgrIsuO/uT354cezYf0BKJ3oLvFDF3hbGQPYSOzfnLCFA14FPg6MUdJ6tY6eO3XL7nbe/S+tUQ6MLXbKKexZy5j8k8pToeROi39w8bdvSdSmP/eKLL77u0Vcd/qMIh7XUbG9uDiM9tPEBcmHuwXIaLiFGmddKH4/NnIQc963q+lWQSsn+a8tYIe2CkG/SRve2wHLtZw+th9Jt7IuMQV4r6ZgcYxZSUlXVi+m9jWWa33nzH4Y2x9G/+6v3bVpW8Mv3BiGo6vpzyrJ85qfBMTxLA5f/9D7SNM1PWdu19DhfXoe7VX6fwfXFUsqrhlOdHfYCwBTmq8qqKrMRmvcqIWS/NciBb9G23Y+HcDa4bIn+AGitv7goinLMc0lpq8lb7bNerHMpwyKFdtgRTsu/rev6KcDlDxW6+lQltzhhHCLx3HqOVdJXqUqnlGoozlSW5YG6Lr8Ozm4A7M4G+lRl6Sgw3Kt+X5KTSf0TVVmt51oYGe0QPXk369px+uhisWhms9kPbmxs3HDmzJnvCSF8bLdRMOYjZU5IjLELIdzWtu33bG1tPf706dNPP3HixG+FEGxC29I6FoAPYSGRJlWPEx5Eh5cBzxLO0F5hvGYSSmpXIDuNdoZJhGkIrAjBJESMk+hOor3BUKKjRjiBCmV6uSnKVeig0UFRhJCq8heGeaWZAVsx4qZPEGsHX/zdct+Tn+/slJJA7QN1Zyi7ajAQpTuItpeg2YdmgggCoiDGCi9KPCmzwlQnYPG//7w5+u7vMPPbwpps0GbBlhZsaYEKEh0kyk3Sy5fIUCCDRgaDcBXS1eiQ+qRiQIUWYR3COjbVFHvxUytz2dPfxOTxl1sxTTUfhAcsCY9XpN5GAg5wCfG4EIkJA8DjUFhimCfosHr0xdNLn/k2sfJZF3V+gpAtpgwsnMX7yH4x4TJbsXLs90/KI297CdsfPrOmFpREdHBUFCgEKjpU8GgPOqSXDIAz4A1SdEjRom2HaQOzQrNdFDgqJCX7/Sr73RTdKOQsoBrJFvA+2P5Rs/Xlv7DafeDDF5VoVvBeUXlD5QucE2hdYzuITuG8wLq0IdVGUgBFaLjCOx5z/H7+++m1R/44F73t0tBNEAF5cBWITBrFpFFsa8m2lqxEzzS7Ow+Lhnh2iaO/AnDWDgo0xhQXHZj1qfQtVVk9rqyKm8774hdAzkasklLWZVk8V4plTDTj3HnEvPd0bftz1tqYvd5+Z+7tgmW+tTHmKqXUZ3062p+NrlzoJYfrsiL0PqV0CSlxPhV7KYtCVFX1HewpWHZhxblwR9t1v+Xcskrq2AvPernnpEzLshxIiGPDbazApaQqiuKrUrpcThnsERuZS9Sne22t/Yhz9p3jNi3PG4c29WTZm7P3P9TPCKGvdZAUz3w+//W2aU9mw1iKRGob9wWgKIpKa/28MTHuQkgcnUuODJHkYcsBURKQMipYchWm05VvBNbHHIXc9wtpGAyhjhEiURjzwul05bmIPlzfp92KnoSa+UtJySeUfj6f37G1tfX0+Xz+Xd77DWAUytmJOI0MgsQR0pqiKDCJbGqbpvnT7e3tf3fixInPPXXy5O80i0VQ/TEhhCPnNNu8DylXmiUMqKTqHyjRJYZuYdIzDsapVCOU4aFEylTJMO8/3jv27VsvDl9++S+UprxWoXoLKpCN3LylRyK5dFFOoUoHLDf9kLLYYGPj/z16992/smiaRIwZkcYeSnZsnCxVyRh2ijGy/8D+KyeXXfbLaF2DwPQpJ592iYCEHmXCWjBSl/v3H3jjoUOHPiPxDfyA/CAEVVVhjGFjY6O7+46Pf2Xouo8gUs5vpqFabzmL/3/Wy2fEIo4+zN56S4vDD/cuENFSo41CCLHxsfvO3Hry5KnThSrSovWuJ2elha6kQvfvM+lLq1SdUyLpQkfAM5vNuPzSKz5//z7zfdNVLcKZrX5z3I3YnL8xsHMAdtaAt9bOkwcSh804K868YE1hqKvq1fQ52f+aMiabjQraPKUsq8P5HmYmdOYWxBhx1jWLpvmJpm3uyNXeYLAfyPwDASilZFVVL877x5jQeb4yVgQAzrnFOIthjCYM7PREMvtCreUXXJBGPJScZYvp2va1Tdv4gbOR50nPXxor47quX66UesBmMuSvCyjL8plFUTySEQ8k8wGWeFZaP13X/aT3cQeGPzYy8pqXUl5SluWNY6U5RgLo72Ffavgvh7TdjM70sH4OLPZ9GbgdF+z+s9yjcwjBWtcmw0s88Ji+3TFGqro6XJblV8PSs89I1sPJnDiXjFGDHm1WVVV9b1EUcpm9tORC9D9KW/sSKfjH2Wz29KZp3ptDTUVRDGmHZ9NlY+Jqf+8TgbpHMZVS0blw22LR/tutrdm/257Njsy2t5nNZn8iCQqC6nP3AdGBbJG0SDqK6FCupQieMnpk7NDKocIpNk8fOTLbvi8GP0fpQFQOFzu8cATl8dLhZMTJiJfgpcLJgJMBq1qs6lhER0BQyIARgQWaE/U+Nvc/7RJ/5UvfPK9umDSmxsoWJ1pCmBLiCl5u4LmfYE4T1DaaGhWq3nXzBBMJGmInmboViu5YmNz9nm/WR99829r8wxhZIoNGxYiMERE1KR0ipOdEyI4gW4KStEowV4qFUnQ64jVI6ZEi0JaCU9oxKx5JdeD5zxAHnv6D6CuFjS2pQFyLpgVpk6udAAQMUwwP9vyPhyF2BdntQ7sqefHT/cJe/ZTv3brqWS86WV8HrqayK+hGQ6vw1QpNXRPmfxYX977uv7Lx0d+TokXEmm1XMJeGuZbM9BatmvfZBxqHSS/RP9FQWVCWECpCqHBK4bSH2EJc4OWChWiYE2h1idbrBLFKq6dsK4NzEucivwW3v2qffM3tqmK7rvG+QUhPJwINEa0KjDSsBMvUt5ShwccZZ7TjTC3YrCNbZWCt6Ljq2D28zlz3TS/dCDde1sBKVzKXFXNZUjtN7QQzCdsyk1UvAGIwWo8R6Kz94zBSTKk64LKsK6SNuCjLJ5Wlec55N+A8ZQfU2Ysx5sVFUYgw2rzzhp9hTuvs37WNu71t2neH4IfvM1qQUqWW562q6qZxGCEjKefdfpa6NySP+E+ttT7GREbUfTEfeo4HvdertVbT6cqrueCW4llk1xU6a9/fLBbvyYZAbvvYu8zGQV3X1ymlnpNO88CwjwBRVdV/NH1mRFbQ+aFGOUMjpDLZJ9q2+yWAcV2gsylBKeWzyrJcye2IQwxfDPO4aZpT1oa/sta+M4Y4lKYmMpRVT79L56zr+ukxxvWcxXEhlG8mPUYYCkW1bfPXbduezOsuK9eMFORwixSClZWVb1JKrYzPuRtBOB/J1x6HK8qqfH5V10/YgTcKgRQZeVsiIDFG5vP5ka2tred3XXdXPmeWjBg8II2XpfN6tlBJduITCZbQtu1vnz59+omnT5++eTFvvuucKzOlbGQ4Sgxok7WWeOrU2+cnTvxyqv60tE7yRNpLjLptW4oiPegnWUKp+EaMkcuvuPypaP1aqUbQQ/YCc5rIgMKNB5nhJRA471AoHG7z+PFjt85msxNFUe7pxg/xv2zR9xNLyVxmMjXCOUdd11x22WXfjDG34qAsx+k4F0YRnU1C8DjXe+XTlVsvPnTo29bX19ne3ibGpULKVuXW1oz7jx3/1e706R/NmRRDIRQph/TSvYThB8bELsc8Q3xKpBMNcyENJghBYQxlZTh23+YbT3dn3qf7nO+0iD3e+ZQ/3yMFSkmkTBZ/8CEhUn2f5s2c1WqNtm2Li6sDP2xAdbZjx+LbJRcmypn6kjzliHfuHSHhgkvDoCcVjUvpaqVkURSvuWDNuHCilFIvTsVj4jI6MFpTvaL5PSBa2/1e6GOjY35B+tcSoi6K4vHAdbDc2C6IV9bD5pE0h53zR7xzfxt6RnpicYceaUopY1kp1XX9XODJ59+Ih5a8e0mZHoscA7Gz9rVxSaFfWpj9+6ycjDFCKfV1sNzjxpA5cK0x5lnpAT4jzzEuU2fzXuyc+1nvw2x0mf6aZzUMbhoy0MjwdELBcky8bds/BzZC8H8QY2xjCP3jfsOAGCwRjEhRFFPg2ReSZzCgQv11Qgh0XSe6rnu778vO57mcs5zyfhhCZDKZXKuU+rLcxnHmzIUxXHaeow/RvNIYI7xP/IGlUS12bKOJE+Kb7e3tr+y67k6Aoq9kmRGAcVXIs6EG45o8g3E/enkfBqDJ+7gRfHyHlJyWqfZbQwhJQUgPKkSclDgj6GKDKAStcDQ4YmXYDoEaBYu7I3e86ZVXLH7/b83mBoVQRKlxUSLoUP2jm6MIBLUgqBmIDkFHXy2BSk8INiI6gQ4a4VpEtFizzjF1CRc/5Su+ztVP/hpfXESMkkrOKeN2MgxkSdNN6fwUr1q8ahPg6dRQEN9rTystEYeiQ8/v+sjsyG9+jfrEX9rLtGQ7aDpVE/VJfDwGTlHEKZI1YlzByxlBbaOkxRDQXiC9AK8QQVJ1mxTNaRprOCNrupUnq5Wrvuyn2f+UJzRW4abJkScqdNAYD4WHQINlngollgAX9S+TlHJJ+q4g7SgopKrQehUhJqmokIGSGat6gZeaOL3+KauXv+JnwuQZamPukXXBtpmzKBa4whPFgov9few7+vvv15949ytXpPPO5pnYppdrCW2X3g52nSPxJWw6NjDiSLREGnB+OAS3tNtcbGndJi5sQNwCOwPXQOjo2hYbChzG/w+2v+c9F03jSlnjupb9+yYo2VGIAoLES0OnSxphiLKiFqBtQNia6CqqyuM5xpWbd/PVki84RPmMCgt6AWrBQgoWUtKX5bxgiIHSGtt1yD6tqG3t387n839UoxzoVJBlWV89bQiS9X37Pk8b9bTd50yb7yjuC6ndQ6Bn/Do/kXIJ6yotAR6/urZybde1qd0hoJXBWoeUmq5zeB/jounelYwE8Z7FvDkTY3pEtxRJ8aZKeT55kTEiJLKqihcBuL5svh/ifLtfDyb9GIzGIsJQL15pTde1xfb29i/kuGoyyPQOJZTzvcuy0Gvr028/m356UHLksiBJzyPa1bzEeNj5cRR9zrvE+/77qH5/c2P7H9SOgkK5OJYf+hhjYGV1+hzgkVJGtBaE6ImkvXVldfIVUooKEVEy4TlKyaG2QggRrQ1d5+abm7OfyW1a+gEB5zq0TsFZIQPAdP/+fc9KT1lM1Rtj9BSFIcZI2zaIxC94J0CI4p7t7fkHldIEHxEyZRi5PutCKpmegikia2srN3Vdt2PenY/4/imf3ntsX1fCFMXq9nz7VwQEIVLdg14h9w+syk/tTE8UXltbebVSokxrNT2BM43Rg62vB1t/cdf3O/soZSBEf/X6+vRZIaSN0ruEigYfiT1PLnhQqiAEuPfe+17XG2CAzOuPs6+bB76yXk92snjA6+y/kRfAWymK7Y/+4z/cEuHk9vaM/Hz6EFIlpfOVplnwiMfe8DrgqVVVMTyiWu+hniyMguD5baTr7O9sbW3+8MmTJ5hMJiyaBd57JpPJMq1FsKOc6IOJtZayLCmKYnjS3sp0urZ+4MBbmEz2Y0GnISEQyI/8DAR0P1bnbH+OAXvfoylL77uuDK1ziLK69MDVV7+1LMvVEFIdAO/8UIXSOcd0OuX++++/78xdd/37uqy3mvZcBYE//RJCAKVoaP7w2LFjHxJSJu5AZ3fEPh9Kctww8yiUUvLqA1d/k2JXudzxb3LM/HxliLkOn0ydc2+01i6V0c7vGRoVo6rr+jVLwleONy/T/T7dMr6Kd4Gi0C8kRjVA1TLVx0hGQkSlTKQjxPj3ydOIm877P8tZShll2Mk5SLCtUuomBGLo2oXo4hjyjSClXAnBv62zdnMJpeY4LAnd6eGPEAJFUbxYaflY0lfkW5bjsBdClmOxnATB+84695NdZ4dYcB63MRLWK76yrsuv8j7g/I4aEKUx5tYd84xlyWhI5EPnHNbatwD3nGX4kLJfh4K+gI78IhD7l+Hu2M+DPv0v8cIsxHcDxBCC9/73dnrZcbj3+RMBKK1fICXFhcwIyW3KSIoUQgXP+xaLxYdyOCsT+bRShBhwPmVAxQhSqccYY75k99hdaAkBysK8JMaoxltbGO0hOYQRY6Truk8CP/xpacw55FOe+X0JDei2wbcfO/b3P/1VV5iPW7N5P4WyzIWmMxXIOYo5ZVdRdlOINYGanAivWKBYEFVLkIEYa0So0bFDxznKrNByVX3JY7/yzY09fImdaloBNRKNBT1PLyIipBqAGolxCjM8eTnQSM1CGTwamkjYevf3uxOv/9217iirYgsdp7hQ0pkFnZkRgkMLKNyE0pWoaEFYPAVOFDjV4XSDFYaoKibRUtg5xBa/ZhAHPucx+tJn/wLhGhm6dXR0gMfGCktJFDEhGE2NbitQp0GeBmEhaHRbYJoiUROiB+UTT0EkhKfyqe7/hhJ0ZVWqA694W3npTdf4qcPHM2gCKjq0lLRNy8FCYu7/p6Y78uZbaP75E13nL8i+fN7iLLWU3EYIP1+cfMMZWWF1ie9cehaG9ljtMSFSORBRIKJERYGKESVSrfEF0ClFScGkgZsmK8+4gXCoT09BBI8KgaJHbLyKeHX+IxBj3FHaWEpUZ+2vNYvFZt6UltiE2PG7GGFlOn2m0epzgCWTmoS49B78p1cG3DL9mUwmN+9gaPewpeyrvEkpaZr2D2KMHaTNznbdu3KFtjgqKpPOu0ybK4ri86XkYLyA+256CFHO3Y8opQrvOdEsFm/Pm3yO3w+ZElIOhL+yLIuyLF+dzzdGCvZSme9c8mDGhfMe23VvXjSLo5lklsdtaRAvDd7pdPqVMVIQk0ebStjKzy2K4pE7QjOirz7Zp2b2HrPtuu4n8rV3MthBKpXQ4t4eqev6JiGWBMcQ0hj7EIaS94v5/LYI98jeP7POvWPgjYyIfruvVxhzkdL6i9Ln5z28A7dAStUb4AKp1CrA9vb2/1wq2nR8nqM+PRQNiPnx9K9WSugQdj4a/QKL3Lm+lmm0mb8zJucuFoufAM6cewQu/OsCsH8iUmtYLN51xx13/KAxhu3tbcqyHEhX5yO56tZkMrl27ZprfgnrympSY13Xx6/32s7+bx/j9ovGLc6cefm99953ez2ZUFYl83kyMLROsPCeKjcWCZJyzmK0QZuUh6+05uDBgy8qDhz4rmAtAShL1YOfUBSSruvhw7M2dvT5+AABWkvyc8Vj27Fy5ZWvveyyQ/8mFRdJm2XXtQPJSylF0zTx6Cc+8S1sz99jigIX3cMbv0+b9GWFgdMzfnc+n3djBvS5JBdRkSI9SVDKVL+/LMvphPKZ/SXOMsYXinzY5/H3F5BSrjnrjzdN8/bdiFPmo4x+TVGUqizL7wDwIe7s84XUoA8iy3gmAFfXdf2E9D5v6v3DgUZFbtq2/d1x16y1/5+z1g2FcMQDTSEhwJjCaG1ecEHbH+NQWA1AKTUFWCwWP2utc8mTXFYZHLzybPikOgu3GCOv243UXKh0tRzjT4bJ8v77ELYWi8XPjkmeiDF/YKlgy6q6UinxzHxMjFAWxcu01mLwNOmHPs9FkSrRtl37h13XfSj39wFx7+FepyGs6vqFWWklrlDi8ySllVTGYrF4F5GQjQdn3T92nT0CO+Pk435Betpf0VeevBCGgRj9IxulucSvtf4ttutOJkRB9BUgR7yEvp1KKcqqemJRFM8//xY9pFxU1fWTM3KVuDtiQDNguf6dc7PFYvGLn+b2PKh8yoZB6DHPSkiUa1mpThGOvvuHF0f/4J2Hyxm+ayikxAuFJ7H/VYwYL1BB4CQ4CTIIZBAEEYkiVdkTeHS06BixXmCrfdzTraMe8ezncflzv7tppyg5wUUBQUOQiEj/sKU5kTkRScRgABUBNQe5nTIDZECHhqLZOmnv+Y1b9OaHtifOYERJwBCEBjlDMEN7jfIlIhREJF7N8WpOEIqAQYgK7yUxLlDa4lVkYRXzcJBZ+SQxveyZ/5XpZ31xYI0upCwEKTyZNS1QyDHkHScQSwQK0dehHEKq/R3zItIGRccK7P+CV6jLXvKK9kDgjG+x4QDESwihoZQBYx0HneTUx9/wejbe/XOT0EA3R2vozvFksn8Z8TS+YT5V3Fdy5E8L8fGNoqDQBuEiOlh0sHQKOgVrrWKtlXQq0qlAEAmJ0brGdQItSiKSR917N09HPkOHPMk9QeSnmaeZciFi9MCwqAVLhdq23eu7rvNjQlM6FnYbB1Vdv6go9GeSCEAjOPuCNO+hZcR5U1q+0ORc0dEBw9SMYK0945z/i/ERIXC067rbBk8RMYS7xtCo1oqyKC5sOeKeyJq7khVVZ91ft137v9Oz6NPD3YgMbPnB+AyBsiyrsqpeBSmcMk7xOv/mjVn9pCJdIy5117Y/33XdZn6w0m5ve6i5L6WoquorpEwhRWClqusX545nRCQr9Pyytgtd2732oeDx8fzUWn5OWRSHGNsmfbvyKDtr6Tr3rvEpE/Ldvjv3decMZ5QJICmK4gVcwFTd9MChMBhgQohp/4DTU/PF4tdy5k0ueid7Eqr3flizRhtRlOV3SnkBvIUHlxuN1sUQZoGBcJiNvbxW2rZ9VwjhxLlP+X8oYuCjp9CaReMwBd3mkSNfO5/PP6pkfr73+YnSiq5rmU6mdLbjEddc82omky/xwbGXh+DAyDId3CNJX0cCFovbPnnnkW/c2NwIk0k9MD6lUjh/7o1hHNvOT9gaGJ/Osb6+ri++/PJfUnX9SG+7VKdagO1Am7Ttns0vyZjBkFaUZg8EiC55HoUsvuiSa659rdZa2C49xCTB0QpjTE8cU9x1511/5k6ffhUQ8oy07l+i7NvDEClBEzeajfdD8lT3VmcisUyVXD5hTJPISBevXvykpcf66VnvY+Z3/0EB4Lz/m3mfkra7G2Jw7RIruCpLVdf1q5cHsCOd7F9Cegj5ZoYUhPRhRkRCD9U3TfMeYGPXz0Pbtr/n+mqfOXMkj01WblJKyqp6mlJi34Vrudj9bpLaTmib5qd8X5E1hw96LTr8Lj/Doq6qlystDufz5Cf4XXAZefMJOuZo0zRvzql04xoG478xRurJ5Cat9Zr3kbI0zyqL4pLB0CEr+GUxohAjTdPeZq394+Hyo/Onfi4JcjGmtFIpVYYK0vn6c+XKgU3THAE+nH6z3EfarntnflZCHltInrwY+hEoy/IqbdQTL8TwZih+nPoJQsl+wS8Wi9fbrusfA/n/U/fmYZZkZbnvb00RsXdm1lzVM01DMwmiqIAcBgU9InCh2wERUVCvoni4OD56nY6e66NHgSOgcEFRVK6geBWP0g2igBxARYQDIgKHqefuquqqyqzM3HtHxJruH2ut2Dura8jqyi64Xz1RuXPn3hErVqzhG97v/cSctTZXixxc+VJQV9VjjKm+8cJbdXoZjerHbLnl4uUpvzKfK23b/tV91Y7tyAVgDJIoAriIEQLbQ13fdfT4J/7wew61n96sNo8R4wgvGnrT4VSHxKGjxyqPlRHiEsQlYjREEZOlLjcRUSOiJsqeWDmmwsN4L8emV5vLHvLDv+P0gx/mmj2I6NDBJ0a+CF6B0wweCRU0OkDtcl2F2EF0BLeMt8sgTsCJd/3RxpEbXqc2Ps+4ransCBU1CI01E6yZ4IQhxFyYJ4IMEhkkygsUir4SzHQghhoplhL7F5E1tY9w6dcelJd+85upr132oiWIYk1pHD2OHhkUMigK3N+JHifAR41PPgVUzuRAreD2fuU1XPvMN4VdT25adykhTKirk4joIThMWMF0Brn2N7f4O1/33Mq3rQKmAagTE2Ph3v5iStmDqqmkmTV8hvjpu5eX2SCBoXR06OiQMSIXULRegBfgZEJwqx7GYkTrJL0RrEjLw6fHrpbIOihJ1JGoIlZJeikw3mG2ofidu/3JRTnoBQsb03Q6/a1Fa7F8fn6khdUYQ900z9FGPSB/93Sxj/tG5jrA3vF4/ESfOQmKlEI5wacQwXQ2u3H46sKq1vf9Dc4WpVgOikGptFg2n6audymlngJzoN8FNT+HBgu0L0aqcl9t171t1s4+lyh72cKrkNy2c4WxqqrxaDT+0dQXO5PDfjpJLHd5M8+eg7ZtX+WctSJndGxRCCjKJ9RVNZZSXg8wHi99R/pMyKV15TDOStu9c7Tt7FU+5+0NFUEXMSQyIdelhBARo/H4WfP+ifPPeI/SiuA9s7Z9pxBYWMB/C7C9+3vv/STmcsCLXAblfrz3GFNRV9X1O6J3Za8PQqD0vPpnMbec9Z+azWZ/43P7Y34GxfshytiMEVNVsqqrn9khzOm8ifl8o9H4kX5QAOftL4WvyEpqCCF2XffunW3F+ckFd4FCEUiLQGUU3awFZCA78AAAIABJREFU+NBNn/j3H63r5oLN0uA9SqZYeN93LC0tARy44uEP/xPadte5zxDv+WuIQ9ngOmUGRHvs2E8dOXLkAz74Ic1Jm3NvnDLnyPpsES2Cl4zWdF2HNoaDhw492uze/Vt4r4gRaXSiyD3HDlDygYWQWcsXoPXKvr17/+Tq+93vipKKo7QeuPmdc4ULYvPum276DpS+q7fpc2kCe5bG4x1jH7sQEQKUTIyHPngc/nYlZUoB3MbiXFDczjq00nQulSI22tD7vgH237ftL27zucVSFhZn/TtijP9+up1+MewgpcRobYwxPyNVKhoa42LK4n0ruRlPr6uqCtm9Og8fxGztBQR427u3L4Lgi1fc+/hRH/wdQsytuHwCFje8nBt/3dAJF976vNHly5FCMVJCDEy7tn2NdW7YMOdx82S9qpySqZSiqesfUloe2EnFYEse+cL7A/cD4Fz4tPf+7QUQOYRfSKGPpNDEsrY8B9jVNPVT0/0mfI0o6U4xpng7Eef9F/re/SWwhUNjS+8V4GIKtTy0MtVDyqa6VTGJGWcSsX1/4xAOiamv86+TEMLfz+P38/OUcxRFUxvzDFLS9QVLaWMh+4nERXhO7LruFd77oFVi0Q2l0qeYg/+K50hr/RQh5dfuRLuK5J5SVV09yIeQ35l7esTCo8seg8/HGO/eqXoi90butWKQrLfIBE8H2FgTbIUhUHUn0e3H/+DwR9/y+v3hDrQ9SRCGaEZ00uBNTaUktp/ihcQLSarCmCoxRsALgRcpZ1eR0vmVE/T9GD+6nLX6oV/BtV//f0dTCaoaSUr3qeMIzSi5D2pNLyGgEFQoqtxuT8QSsXTTGZWuwH5i5o+88btHm/9wx/64iZlVtDPJJE7ptcVXES+AfgllVzC0GFpi9HgJUVT4aNICGhwybhDjOoxqjs48s13XsOfBz/he9j/uh2APIdYoqamMQOASKFGAqjuk6fLY0RhRI9H4GPBagDygOPS4V9cP/pbH3jLbRR82UbXAyKtws30o23OwgZH7uD/6yde8mO6zH5J+DY0mWgUYkIpJO0GIi2WWnllMrr0g0QQEDn3ihHdgDKHWTKuAVYHGRRorOFmlo/aR2keMUrRdS4yCru3R2jCuG6p+ytVoLRBjYp6aQ3x/geL3AqVw8cuMcC4lr7N0R48efYVPTHuEMK8dvxjzbdsWpRQrKyvPk1Ldr+gY3s83PCLDhjbIDsG6Y4R9+/ZcH2HIsPA+KcjGGIonYHMy+ahS4o55xgEJDZ4knFxbe3uywFzhZMcYk61EMzDP7dq165sgl6y4UBHMGQ1L2CMkKnQhYDKZ/UEI4bDMkPuQiz5JqYbNt6TqVXW9u6qqH4GdwRfAPP1tKAu9FXwIgJTE1bWTr+i6PtZNM3xeCrHFvRxjZPeePd+4e/fKd0bYJ0SiDA8hUJgHS+ZACIHV1dXXARNgMBiGa2ejwPaOujZ4F2ia6jqlpFiskFgUQ6kU1jq6vps4F95TkPtKpf4u42YymbzN5EJoi1wS3jm0MRm8GBmNRo+QkmtL+G9RzitNND9zKQS274kkg6xME6nAOfeB6XT2D4nnQKK1GZQIay1106Q+84HxaCSWxuOfO3VxEAvKcPnudjXb7JEZSSEuNVoDc0VpuI2sMHnvWV9f/3cpZbwQw227SkVRlgfK/CwXrLEN4dJI+S9t7CFEnPvxO+6441HLlz3kMUYncpSS9tL3PXVdJ0Kcs8jA2JTjXSGkmMFoNKI+cOC71jb2fsgdO/ZbkkilKjpvE9dBJWGbk7tvezAChLjlrltvecHucP8bxwevrad2iq40hfFRZnTrsFZvKwYeGY9H9P0MFaO47OqrX348HP54f+KuD0gj8ZnsBXJMzpVOTcVIYp6AhSdBHzrw45ddffX3HD+5xmhpFzYvGLN2ihSS8dIyG5snOHH77a+k6964rQ74Isq8BwVKKEJs47BobyOfuFROE34+yL33iFRRV1Fc+18kicQ3277/BaPN/aWap3IVS3dAoQuBknKprqqXODf7qYsWSkgyVkr9xyFOLbayfSqV+AmcczfGGGNZ3GFrjDnEeIP3/gdldo+GvGhHFqyz5Fa+VEoeGwLvOW1rdlZOdl33mrqqfkVrvbAgh2wFJ/d4DOk+m7p+cdf2rwwhrG83M+aCRAxG/vv7vvtQXVePLZvpEHJiYQGXstJa/2paFyWlsF5x3xclwvb2RAzhD7bThLwBCW3MEEYoSmcZB6VapXfu74GJSB6ZwSuQyT4JIb6j720wRst5CG0rFDGfTxljntl19tOn9vEO9Pm4XFQg8CH6vu9+3bvRE1VVEWPAuTI2s2KYH4IUkqqun1617SP73v1rOWHZ4mJkICjbEhLYXpvuga2JReEnY8pSsz9/Hn0gxuPxbyilvr6Mm0Iwth3a8cXrhBCmfd+/qe/737vXioGMJAKvEQQL2iVaZNCIIJBhEx8+OQt3HP6OunnKh0bySYdOiooZkhADTYRKKzo1A0Dl6lLERFvtZdIYRBwhvMYEgQyeIE/QSU3QexDVY4S5bNfLuv5D/7Pf+OQHBC01fUpdtykGHTKanUwmVrIXikYSVU30nlo4sJ5u+v53z47d+gu7dj3zZbv0A5j6fQQXCWIK0qOUTsRnMVmcMx0gKiqXu1JOiRKiEBAFwk9pzBKbVmD1MvsOPWlUdZf8cT99x3+w3W13mph2r14O3MQQoY4OIRwOqCpD60aw8hVP23vlM3+1rXaLoByWVK/B95uEUFM3DU1/lI273vcOjv7Nz+GI+GS5BdUiI1Qh7ZNOTImLPuMvknjSGuSER1eKrg0EE1l2KX0PKbESbJUaqzKWZIiNu4gWBmsCQkRGIRI7S0CQeCb9TIY56rLKcc++cBj4+9hdH5m1bfsKY8yrmmwNFtd3AUwVt6xSitFo9APW2pf2vTt6sQCIVW2erLXeDfOFomzikNkdZzP6vr8huW2He9sCnQ3ev8dau9nUzXIi1vHEHNcupcCLK7lpmuun0/Y+VwyEgNl0+jvGmJ9YWV7ZO0+pzC5ukhs9xIiWitFodHA2617Ytu3LL4ZiIESa8kISptPpK5qm+dNmNKJrO5RaSC1cDDsZc0ANXAzpzyWrQetk2c/a2R+FGLeBagfnAlJxZV3Xj4a5IjCEABZy63trb4CFjTK1neAHIONtbTv716bZ86jEMpgqopaMi0XwY103z+o6+/J8qi3gy/NJWT6NGE4x59u2/9uu6z5cVdXXzLEOeW30YQ4IFoK6rlUzGv10328873QnT4yeakiL3Kbs5zQe+kGxzhpCTMbvXdu9b6XUl43H4x9vmkZrrXMY2VFV1dCX25EFheJJSqnNC196cnwkRVkXXCORtOp3/S1333nnd6+trfVKKQrJiEnlHc95+lTsIW2WxYXjvcP2iUN/37691d7LL/9TmuaK3lmqylBrRdjmeCqEMtbmNkvo11Zfcfvtd/xJ0ZZDpikd2NOy2387Lq8YEke3MQYpJV3XsXfvnqv3XXnlH4Ook/s2kamInLFQrAgfUvzdew/GPOTya675f1ZWlqu2bTHZg5DoXR1N0wBwxx13fGbz6JHnE+kvNrL93oqUAor7Eg4A57UolGdYJJKRx4hAInf+okmI0Lbt7/V9f6TEQmHrIgjzWHJd17uNMf8pvXlx2lhX1beUmijlskP/503COnens/4jCU6xaGWw+Hqz7/r3FYuzUBWz4BmJc8XgacA2qD8vTFKGRLy7a9vfTQRNCfSZzMm02RUsS4gBbQxN07xECLF0XzHgLcri7tV19i+6rr85ZQEsVr1Mm0YIqR+1zuWVF74730wltu+7tm1fvS0ajNyAylTPqKtKx1P/QHl8Aud8sH3/9sWvx7lzIa/NgVnb/nU6Q5nDW5Xvohg0Tf01UsqryvuL6+lOYTwWeCncbNa+rISztp6/pIpmTFvKUnm2UuLBi+cacCzZdXCeLVw+3Ztbs5YGxenEdk8qpXykMUYXb9h8zGyvevAWnJMxVFUl6rp+4b3PSigqo1XgF+nzR3gSeh8HWm3C2j/+3eyuG3+5Wf9k3CM2WBYteEGMEkGXjqgQsUZECVFSuMiF1HjAhkAQAqEymtsrvFXMxP3w+77pCi558h/H5tpmLQQ6kUsJFExYBJQnaj+kh5TDhR5pJASD7yuWGsCt+3j3u3/E3f2ef9vXHWM5bFILhRYCLzt61eNFg5dN7l2PigEVAyJKBJIYDRGNlobgPEYqjDBMppKJvhIue8KTuexJ/9Wxnzbuw4URkQYdGlSQQ9mBrlrCist2rzzoWX/udn/t/qP9CspcQj/dwIgIITJuGsbiCOHoO9f6u9/w7Uw/emzZ7Wdk94K2BG2JQRGDQjJLR1SI8MUnOPJK0CsFwhFtyyVw5eXrLZKADoLaSRon6bSg05GRDdQu4KTASQFRo9BZ8/ZEYYkSpqMRn1le6jycSLqcgqjyc7+IqZoRQmDadf2rnLVzRLgom/BC5boMgDLGvFBI9tzXXmwABHVV108tXAzFDF3MqU+EWf3bKQHDoszMzzFI33dvKyjv4c8L5yyhiqquH6CUeOR9fnu5n621r+ytnUbm4cms8KQYusgejhhpmuaquq6/875u22nEdV33SjtYKcwrFor5Yi9koqeO+f1iqEDKROi6/q3OhpvO47qiquvrtNZbntsihiWTpn3MuXAbnPKxU7ZI29t3WGsL1c3WDZX5uDHGNFVVffNpG7RD3poYEiEcQNd1f9m23afIMfWC+ygKVcwYoZgsZ7O0tPzjw3li8oyk414pLSunbd8Qgs/rQVIMtg1wkZKDQoDzFmu7HFqKmbPBIkQ86xGCI0ZPzDVIlJaYSl+7I8yHRe7RXWKO0LbHjr/s8OHDf1nSmPq+35ZWWNC0xf0DidvAGIPWmr5PMfpLDl3y9aNDh34V74W1HrMN1kIAnCfktLVIpOuTBU8IayduueU50+l0NcaIMSZxEORPwvb47I3WiUzD5cyNqsLn2M+VV1/9ErU0/i6kSHgIP5RoT4hvCfiglq666g/37NnziGJhhpziRnYdVlXF6uqqO3HbbT9A2/2bMQYfcrXF/z/I4A4N7DZLDy2bx/ktDHP3fEGBb25u3gVs3hdNPl/pbf+6rutODHzy2QpbjOUXFHhVVZfWVf38i9GuqjKPNsZcWXpaLvT7nCTH0vf928p3hoSDU4aXEND3/TutdX3JEY+xcALMN4QYI1opWdf1s+7j2xvEe394Np3+frEYU3vnXhGyN6PEZ5um+TEugkdjGOL5Z993fzidTo/P0w/nXBIJbR/ymJlbhDGm2Dgx0nVd7LruFfMznqsBIBX766p6AoiBt794dosiG7ynbdsbtrR72PALzqCkYfOR2Wx2F6TPzGPxKUOlhBSEEDRNc/2ZPK87FcZJ2AuIETubTV9awLTzsIUsYIp8H6lt4/Hou6TiiuF+Y4k23CvF4AwbUvGmwXbBjKfc3JKQKTXUZ74IbTRaK5TSC/iF0x8JzyUHMLYUEiXl8gUwH0aIkpFTNFETlSGoiqB6vOxRfhkdlogOkpfycy6s/vcXcuc/fbKenSSYij4KiAoZFcQGogY5RchpiiPHZKFjenzd4fQU5/Yi3AGaGGlo8WqdTp2kbR6C2n/dj3Lgsd8V5G6ck0gMxi2j3TLagbKUSgp4CV4CyOTu0IEoHL4fo7pdqcrH7FOfmt39Zz8gJh/ytZ1B0HRhGRt3JSY+2WNCwISQaicoj/BjpBsPvApO1AQ5RnQK3UmWdI9kwmq8grVdT1Tmqqe9Vq087JEJm9KhaFExEGRFGF0mOPjEX1q65lnXHxfXMBU1ajylDUep1SUItxsla1Y3bqI78t9/RZz8yFtXesmS83jWsOJkwkM4DbEmMKJlmZZlwumqw30xJJD87QJQiOfaXY8+1HlmBiYmor1Ee8neGexuYWYi02rBlU1CRVchUkewwjNtAnc3kvfK/mNWeqLMWpaUdBJ6Acan42KJs3511ravmxeaybz4GQlcFpsYAqaqGI2aFwt5D+DkbKfbVVXVdTrzFCymlc0tKYHt+01r7XtTO9P35GmWuey2v9na/pNzF33JYZ/XUAhZaaib5lnsQMr02cSHkGoLBJhMNl/R932XPMFpDOlcrrh4a4rCVtf1I+q63lH65tPJYEXHZNla609ubk5+f6B5zpuRUmqI6w8brUiLeclciAnQ8t6utx+GLQb/WaUy1TdUVbUcYxjwBDHMx0ImrApd170d5qG7IWMxW9Mh4w2kxE2n03ewkPlTwszF2i7WetM0j5dSHjy1TTvJI5GqVabXXdf9SdvObtqaTptwBpEc0s3eGWPMrqYZvajoLQWjeD6Iw+3IHFw6vLXtORG8nwkYQPHlIJ8zhnDWQ0gx4G1iLpl9Xg04802JRL8ji3s0aeBlIJSMC2mArjt+4q67vrvrupPj8Rjb92c8bxHvXLKMVdJsYihukgSyMEajVKoeOBqN1KVXXflqvbz8FYGwvZSNBbeuynmunkSdidbMjh5568mTJ1/WdR3O+URHOmjq5x4g3vtUJ52Y8vQz77yUkrZrueKKK3bt3bPnLdTVvvKdWNql9Ldd9cAH/lwIgVEzyvm2gfFozMbGBsZUxAjtXXf9hVtb+zWtdIxEbAw7Qh5zUaSo4iln//679K4HygKs2tbXE2FMmRzFLeeDZz30773vGr59KRPe9v2rQ4wbIIYFXsnE4z9UgYsp17+q6wdJIb7llFPtNF7CaKWeXngKYKsVnRZngXPufTGwLhZWHbkIYMkPKlt+0Xt/Q4qRz3Pki4Uy530AY8yXAVviuDstqRhV8vR5z03O2jcTYyalikN54kjckuuvlKKqqp/kjJbezksp2tS23WuFkNMCUk0W7yIPgRgs8aItFB4D2/evLIvvdvdWpfT1ybU+J0g6lYMghHBnCPxPKPNsvpkNHgvSNpCwVPbGoQ0LYalBAY6xuOx3SSmfstienVQKhEx7UFmqQ6Bru+43i+c6tWWeVaEzFixkvoG6qn5AKbW3nC/pt6dnqz2HTLbR2vJi93ZP6rw/AeWZJUU4V9PE+xQmO9sRQiB4j8900QPB1vnfX76FKEAEpvRM6RPHr+sg9ECHy/8UFbqvqSwYG2D2kY+euOWtL+b294UrlxSdr+gZEfUqQq0iwxjcCB9qpDAo2UGYIPtAFQRGzRByitUebxSq9azImlaPOF5VzPZ90x5xxbPf7EbX7JvKiFWbxGoT9JioGqywWOw8LJeZF43zKOeQcoJQE6JI91Ibi7vpn/+zPP7+v71UfoFROEwdV9FhhrQeFRTGK6pgqUKL0zPaqmeqJa2SaDaoWEeZKcK0tGLMTIwZx46lOOV42IO75okPXdn9mNcjH2D6XSvYpoZ9j/rK8cOe93szdX8l4n42NzXBr6DVGB8Dup6g5BHcHa//N3P4b79fTTonMWxKxQRBG9JeOwZGOKKaEuUmsJGOKBFRbrOq95mPTMkIEgSahoqGioTyyIsFUCuRcmMVoCuWGDFmDKyAH3Mlkad7nnFwd1tpOyVutiyjSQXlKjw1TlQDJYH2FZWt2SUbtA14HelxjExF0wo+stJ074d3LQWRuCsydkWFiIwRqxI85sJFJsDNltrmW6UsStb6u04cX32DtY7K1PS9w7m8ag3gseS6l0Jw4ODBHwshpxQL5tYcmcr3HtpfXFhbtkqKs6b6EMYIICBleOjy8vJDY5jXByhZAwV0G2NgczK5odzHAKI+zTWs9QgBXdfd2HddKORcztpEWc081BNjpDLGLC3Vz8htGdqnteE0Iy11Qunv4ZYX3zu1/9Pn2tlcn1pf33zZZDLrtTbEKHAuJkxQSEp8jGGIze7atfy1xqjHl+8qJdLGECJSKE73rO+NFFB11w252zcfP378rYtVO/u+TbaCFHhvkSJC9AQvEEIj0KytbXzauXhjOWciBJxv4ouy8PuupaXxU4pRZ4weQqRSKlRWnDY2N98JWJW8GkCuQihSv/iM7I8xZTkoLd83nU03tiqZDCnIJdwXo2U0rq4DCNEj1Twb4rQiQj5y2dStf8w/F0CM+XUMhXND0M7sH0wm3WEpq5yu6If2OGuHegoQWVpauqSu52E9pZIiv8jmeTZZ8KzNCt/GkIIvBEKmc3Z9i8hFcZQSh05PbhbueUTxybbtg1IGrQwxQFU11PUIIVQeryCFwruAkhrvAjFA8PNQSkndLGHc+9yuVKhsgeeQglIwnb7p+InV315bW6NuGmzmG0iVCdMAM0bT23OQHJCGQonZFxzC/n37v2zXZZf+Lj4oRNIYnXXZ2ic/jEXgRxwsGhZ+EqGbzTDNyB675eYXHL377pvG4yWss0ipOFNs7HwkgYkEl19x+bcu79/300ynoNQhff9r3rKysrKbfH9VVWFMRdd1CCEwxrC6unr3xtGj324n0/UCYpPZZV7WlJz9uLXDhh87p5mfUcTpGPxKn6eWVc2IiUU86H77n7+6upoJSPRAqXo2sdYyqhucc2itmUynVJXh9ttv/yDwuR2/nwuUGOOrrLWTUmPjHltsdg9ncNxXKSWeDFvj+cX1eD4ezVPylQEwpjqnK9853xN5JzCMqWywntrsfB0IIXwUxB3b8dhprdOmsKUgz866ahclhPAp59xfF4txiBkveA4XRFVV/aPDd+Nc8Sqpjjshi1iCeTv9q2zfbwuEFmPKfAohvDLG01dGWzz3IrBPa/k4KeWhU7FiSU1Im7pzHmft28p3CwhP66JQzbEOZcp6H07Yvt9SbOu07QK01t+IYHkx42WnMkJON5ZijBPv/SuKAn4PJWTBqwFgjPkRoE7vhS2K/LkbMLw6tvWe5t+NOYxV8B1a66u2W/q5qqqPAW+z1m6Wo+/7zb7vN733m0KITSHEZoxxM8bYFq6Lc6Uy3nuCIxGSBUZDykeASCDEEs/xgMRLkdHwLhmXvse7OyMn/M9siumj9i8/+UmaGuGXcVHgdUuUEuVHmFihbAUixf+TRjPO20ryzARTMbOBZekS81ffEVaW0Hz9t3JS/TSrn/2vhMNIeqQEFypiEEhpCTFkKxpccTWRrcv84CQO+iMQ1g5PPt9/17Lh3Yf2Xjs+OhPopqGNHgg0CbCACQlN71ItHQJLCAICn91/KXziM+ugjA2xrZjteQTaH/wlpP6E2bfvRft2f92D+65PWAUiQa8SQkA7z64O/Oyf7PSOD7/Arx/9zDxZVOayzgEfoYytWB5XiuMDYrg+9gKVm5D6qcIjcPQqT3af54QSeDQWATJQ+9TKVts0apSkly3fAl/3PbNDX+3DTTQs0Yfk1bGZbyBIC3h0Bux2Jlnp0StCJZghcDhq1dB2S7xut/vtjamK+PQcGtcDnjaP+Mplmu174xS8APHe39S27VuMMd+vtcZ7O7Rg8NSLbP2KKMfjpRdvbGz+3eI55qDF7S+exQpMrtXkaW5GzTPP9b22az8Zgr9p+DIhRwu39tuCtxjnQue9f1cI4fvOdf6qrh6ttLzSu3B7eW+uEJbQ0IXL4mbYtu1Lq6q6vq5rvWVxT1GoknoBwGg8ekbXtQ92Lnwm5iSAKMSOjZpT01bL7875j8xms/eurKycs6hPTKDDI9baN80BgKdv4anFoZqmuV4qlfe6rS7ygjMI0a/74N+X3vODkupOt3kvWFdd190APO0cjaeqqoNVpR7fd/6di32wEyGFM/WDc/b3urb9qaXl0cHS4OEZLHw3400ebIx+hrXurfmWJ4vt3F472PDez7SQoyi2zpfFkJZSirquHjKdttsa/F3Xua7rrh+yLHKby3MumKbMbPh9+/bte0P5e362pz3vjnBVn01c8FQolMrA+xJPtrazdx977vG9xz6858A1l4UgmbYtZqQhQt/3jEYjXH/2sKpUCts5okwxOusCbdsyripx6f3v/1+OtHf8S5zwLkgeC9cD5A6j+ArY6iaAeSxVKnzwmKrGzmYfvOvmm3/i0Piq12qtRfD+gr2JJde373qWV1bM0t6H/oUUQk2LSyukvGXbWyKRcVUxPbkWT9x5+8+yeuIdaIVGIkJKPTl1LN3DC7IYKN4xWUhYmof5IZLjlp7CKSqQyeLIihJSQmd5+KUP+GXXWTmiwYdAcAFTGc6lOWutmc1mmEZj+569493csnH4I87yNpzf+Vu9QIkxMpvNXl5V1fOqqqoHb2TpM0RyKQqBiDAej542nU0f6l34dDHIimKwXatKyrlFXrAbSsv7N3X9lef6ru3tMSHEC7TOQMkFJLdSvjR6sCSDT1wBIXjfdx1VdXZgf1VVTWXMU2eu+/3U1nl8d6elnLvrun/puu5vq6p6etl7ctcTSSyrZdSNmqaeVvUPOTf7SaAfPptdrhcKRMvx++F1Ee9DnM1mv7mysvINnKUzyubUtu1rnXP3yMC5pwK3ZTOrm9HoaUrOmSzLfRWcgbMWH8IRKdV1wXukVBSnRAhkYGcp/KQSUHE+LvezMLJPJxFy/nx9Xd9N3xkjg5t+xytcLpzKWXeibdvfGS/Vv5CyEhaeZX5dNtmqqqjr6iXWproT83TCc4/RYf2NzKx1R7XWVxeAa/lAJKK0wrsemfBFDweMEPTnuv1TM/Zy+9iKoYg454ZxVjzd94nHYKj9zdaNJlkygHQQNTEagpTIUBPpMURU7An+CL07fqe9ff25snny39bVYysrU+5/FB7UFERAhsSJ4JUgSEeQGcMRNQKB8xKpK7TvUEi0MfQ9eFUx3v8k01wp3zy7Y+lrwua/3to7iSYSiPiQCV0yw2IACDlDggWXGD2Nkfh+lSW9ymR1+voTn7FfddUj/uMLj4cVWjEGFFbWqBCpQvIgaHq8kClHHzV4DWROIXRCQ1So4FBGsR4tUmoa/RjVdZbew/LSbsLmBE9gJBRSOUazL7B69CNv5PA/v4KQQIZCFud8vhEpIVcas51NNRljqkOR3FXo/9pNAAAgAElEQVSRKs/d6QUqNnWoAbBCEFSAbOH7PocKYnYhJIQSNYnXvQtJpzpoHV8Gz3nJ2vjrNtoj+N2atXYCDVQmUs3y+WSgVzDVFaC4ZL1GAcZM6J3Dt2Nm9aW8ZZ+0f2yP/pTzVY8PVHlqtjpNnFGe0jsO7z8Pcc59quu6t47H4+cCeTHOm1JBbwOkRcnUVfWiqWt/NIZwssAI7vVymb9YVdXTjTH1uT6+d++eb3R+5RvlQlx1yF4gx7K9J8Lgli0hLaU0zp09HKiVpqqr62ezpBictrH3gXRd9+t1XT+1ro1CFMW2YPzFsJBpramb+gV93/2Kc2EtwkLAfGfbtKgkAPS9+xgJcNps437+dfH3M4UOFl8bYx5VVdX90nVzOABSzZq8OVZVjVLyQVrrP0h6vMyWraZ0gM/ltku2wuB52MamXs5ZVdUzYGoQ2J0EHy7KYp9kWv5X933/YmPMnoLnKPoezNfUZMXXj2/b9qudCx+Zp6mf+/4WLtlZZ28b0Vx9ug15kQtCa70kBF8FfPB87gkWFeu5J6KMq1K7QggxVyTO0NX3PcZAKVxwuOhQUmMWmH8rY+Dkyf9x5Pbbf3Y2m8a6rvEh5fJXVUXbtuc8v7UWow0R6PPruq6TZdB3XHbZpQd3HzjwFpQcpw6LaKm3PIgkW9M9Fg9rw6L6E9za2k/cdtttHzT6wh0uRdsurqCubREIjDZ0fZ84EHxIhT604siRIx+cHD7yYkIISjEUjCnrSamgiPdEf8+Y1n0057ZcY/hNCEQG3JS/p0BHGKZUU3PFQ+5/2Stn7YzGlAIyfp5Gdg7xPmVp9K5Ha81nb/nMq9fa/r227RNt5JeodF338rZth7ScspDGuHW5EULQjEbP10btCguhgwJE3I6UtaN4DoSApq6ftZ3BUDZ5kbMnZC62UsBaurzO7kqt9RAvtfbcWUcAdVV/vVJy77k/ee9k0a1axDn3D13XvT/EmMiC0gNIf1yMLsRIXdX767oZlLiF6PB91eRtS3k+pxZ9OlUxON37dV1fp6QU5d6LMpACTUnJcz5ZmkrKAbGfAHQlNi+G31lQOrZTGTU3jswTc6Ux6mvuy+Xp1FwC5/2R6XT2hjmhVFa5YzF6GTwHVVXpphm9CCCG0G87jLDFS2E/MbxVXHeky5Zy50XpHo2ap23n9Is4t1IIqczBMi5s9j7bTLBW5GzrxwVkJaR4Y2BGpCeSYrgDLjgA0UF0RAIOjQ+GkGO+KkLlZhCOwfG/e+Xk2F+9Rc0+Q2UFMkiCEAQl8GYdb9ZTY4NG0qc4vUibi4oCfKRXHqsCeIOmAalp+5Y1fQXhiid+rbzkmf8NrpERR4osi5yIWw2HRFPjqHE09FT0BK1xSEQtmDhQchUTb564m/7qefrufziyx91N43uICi80vazwQoPoUbQI0YJoCdLh5XxhEqFGRE0UE7zYQDJBiikyNNRqTKh7Nt0avXJopTDdMeLhf7zd3/3Xz8V+ZlMqTRQKFHitCBIikiZoai/QHqRL1wsy4lTEGnA6HVOVvAUyXNjh6HCiI1QWlKfqBE0nqaOmjhXGGYiakvW1riObGpSBA5rmlzv5xp8+qi51nMBoh2kdS0Gzt1XsnsDqKLI6ilQelns4OJEcnGg6ZZgqQycbWtHwgV17+G+j/r2vHsuf/+xYUUVY8i7xQtBSuwrtKmbSMJMKKTzyIvE4LE7ABSa+j7Zt+zfDHwoAja2V7UKINE2zpzLme0Jg2Gn9vVIM0nRXSl7SNM3jtlekKoGtYk5rKhtHyO95v5VoJ4SQ0nMH+vBzn98Ys6y13hJL3wlgb5HFfiopid770Lbtb8QQYiELWkQ2lG8k3nlD09QvBmSMsS2f2gk397CRSrmlnfI8Sm6fi0r4dIqBEGIgmBpSVct5ivIjUjptJIcEw7xSpPeeru8JwQ/POuZUuXPhHE5tm3cOrZSsqupZ5xO33wmZzia/ba3dSG2ZezsSFjXdu/cebQyj8ejZwKEQ4/RU7852xHn/EWCrcimSCuJdCp2EPO/H4/G3so1U2bCwDpQKmvO1IwxA9YIzKJ89V9vvc5PKB4+SCi01Hp88B0ikgN5D0xjwPrRHjrxo9cTqxwtLWt/3NM3onOc32gzastY6sbR1/dARGxsb7Nq1i8suveyFcmnp+1KbMlfy4uJzpti7C9TjEV03d8VZZ0HKLxz5whdeAGzPLDqTiESyAvNF2OYaCEtLS/gQaOqa9Y312fFbb31emM5uJltkwfkEFR9cXynDoVR+N9qc/do7Mf/OsX4FCi812a0RQUFdV9XS0vi1V+256ikxRkZ6RDtrgYSp2G7JUaUU0+kE79y/fvLwF76DEGZojVH6S4b58XSKARD7vv8NOKWRCQWWJ3fi768Sy+eLiAwutFhM/3vRDinlN2hjVrbD3FnSqkrTSNkSw8aRNpVEKSvEXGEQQqDNuT1qIQSkkkgpr0vXmM+znZJT+79spNbad4UY/7koZPfUZJLLNdNUP0xKnhyhTdb0jjVvaNcWxeA8Cp0spiSeSzFYeO9hWusHzYGPYghRpW6YP+OQN5yijGqV0hiLJynhTbJXqWTUSMViuuXZ2j4w9ml93ZYJch8pCFKKeX0Mz83e+zcPQMB04dy29LqUsq6MWZGSF5ArQ51v+2IIHxiusSjFY5DpGWOI1Aln8Ph7nOQe9yKHIzV9jo1Y/H0R4LqdOXYBioEAEQkqFahLdRIUEQ3oFO9HIrD4MMOGDk/EUTGjoo0aj8ROLSu6Bvvva92RNzxPTv7H6m4zQYYlulbjtKeXFiEshECYNmi7gtEBmBIICC2JQuGiQCmH1h4jpyhjqfcc4q5NQ7fnkXLvg7/tFX70qMd4ljHLClyLcj3aOaSPSC0zij5tKUlp13RTSxSGiAIf0fRIexQmH33n0Q+++b8csDdR+aO4fopoxsyEpg+SIBUqBiQhV3YUyVMRBSo6VHQIVWGDQLglmrgbozfQah0ZPcF27Bt7Th7+57hx05t+jOk/v28UHY23ID0oED3InoyNEExCxwyHI9CFHmRMykMAHCiv0b4Cr0AYghRnPwRnPWSEKsLuDvb0EZPUP1ppaZUlFMunFrBsGBP56o761zfNa26YHPzeLz+5wfJsxrqYMTXQB0VnBZ2scKZhaSrYFypoNC2ONTVjNuoZmwk6TPjAlQf5z3uqD78w3vnN75LcTa9h4pkYx2wZZhpmkuzPmouO6bgYsqidL77uuu6D6+vr7y6hpEWtPsUH1aDsjsfjh19yycHHe59IsrTW2ypLXea+lAz5503TXEeMKQxQlMyFxaRY/SHEeV0BmRd/yvlk4iYY3MppwRHM8/JjAvoNYbKcipVxCjmenUNle/fufRpQpRTHrcWNLlQW3ezOuUHpjDG6u48efZkPYUCF+xCG+gRCJGCc9x4hpdi3b9+P2L7vBmr2bda8P5uURbpYe/N2DmWM596MxfjmAuhz0UI/bfx6rhAOn11eXn6GUsqUv28BYZJo1xc5COq6GngzRFYWdGZjVEoOnzVG5+v4AbdRwhJiIRRVcA3OpQJwzjlWVlYeEmN42H0CPBzuLl13USlu2/YVXd+1QkpU5m7QWg/js4zfECP79u17odZ6Yvt+IKQ6l5RaDd77z7dte3OdCwiWORFDotwnJsNOCLDWin379/4YIJQSW7xCxph5ZcjsvTl1jVk0rMq4Ks9/0ctwJtkRj8Gp1xgGxDZMUolkOusSDDLyiWO33vZDq6urbjRq8LmGQVkwS+yk8EJvh3/K9v2AOaireuWS+139JrU0PmSnLaNRPbQyELB50TiD7+AMF7C//oWbvvCXVV1T1RUn106ilEbeC1fT6eTkyZNMNievw7nXk9u1ELIf5LRzaLDwJMoYpNbEmMFCWfM/p2RehDMdo1GDIFGNuAjGQNOA0GQwCQmoVFfQ91jHgUv37f5/rzl4zQ/oPAGFnNO61k1NMxolbIrzOSOjp+s7lFZUuc5423aEGOKnPv+pPzu8duQbu47D8/aKezzA83qmF09C3/cvczn1YhFNLKVKEzqjofLC+mwh74mOOZtssYQABMtK629YTJMrm3xpA5BiyloNC8m9PaqqWojxpxlbmC1T4wa36j6t9ZOccxf1OcXIDbbv/624chet7+RCz4j7tAY9Uyk1KvUkLkb1xQuVM7m8lVLXL/5egHblO+UZXOjz9yGxxfrFY0DHJ8s9FEUAZGXqc6bQ7qQIAc65/9W27Z8n71DaPG3mxlnsizwGHqiUenzBWmxHCjYoBGzf93/j3JxDY0v4cGhTUka0Us/UWj4h6VzzBd5ai7X2vL1qRcEv93WfZCWkaSNz5gFZDxCE7CdQ2URVuMTRJIs2nPP7c52EWjb0oafyHbEL2OkH/rw7ftfX7Fm67qeDvJq+PQBEgpmhZMgAKo+wOrE5yZSgX/uMKpWbBAFepGp6KjgqZejQuKWDjJaefC3d8hu4/YZv6d3UjtLZc2JqpBOAksgYEAFkdAgUhQQg6/fJ/xs9xJsDd975v3Owftjy/oc8tNMryGgIapQsqBARIiCJpCrAiblLMgXAhVR0y6keEUHGpAlWIfVff/e/fEie/MSP++6uqCwIKgSgY48QoFICKI5c+6FEDzwptcJD8BZpNDEKVABQuEbjhEDac7Hsnl352phpYJmoIwifGDBtmgjagGMKDXz5OuJJiCf8IFf+/kFbP8i1RyAGJiFpyV2tCMGxPOkQRIQGaSS+d4zqhhAaujZiR0vceWCJG5oT6+9dO/bznz+uXjsRMtX3FALok3dklsF2mZIiqBTxqbIi7bLH44sdbeg6+56+6z5YVdXjgCFNSypJ1/ZpEpMsFwEHFxeq7dpTQjDknhutnmSM2S+kJLiUJVMsX5+zC7a43i8w1i/F3PJLXPzz6pIxpkwZkUMS4/H4+vX19XddzDhzjPSztn2ZMeaNddMMYZxUxCgQcsQxu7oNsEcsKDqFHvhLVU7H0KeUutIY89XpORfNcSsobYhRX+DzrzJGYQDW5jFQLBwpZKKJV5LgI6PR6Pq27X7jYj1/mSmTp9Ppy5u6fo5ZXjYxKzBNXW/pu4LqB/aez6Zcon4xQtu2fzoajX54NBrl0ME81BpzXlIxhKWUejQev2o2nT3ROT8pbVhMbz1XP52akbLddu8Add+WZnC+dlla6ATO5hRBTfSrJ37xzjtuf5fMVa9idjkVl0hZGrcDUDKVwTqbviMSiv3QoYPPWL7iil/wNrtYSEyLFNdQvie/jU1DIFBCrR757Gefs76+fnL37j2pnUKgTldp5jxlNpl83E6nXeaVyYj+eQ3ve5BXCrY81dKE4BzRpTxkmSud4M5NrCaFPOsxqpp0nyFACFvaEwPQKOi49LID+1/7iAc+4j0K+aC1jTVCCPTdAjwjpjzouq6pmxopJba3jEYjpu2UWT9j3IzRWsc77rjzbZ/93NGvPnwsvNrG7B8vN7owHudWspgfC/30JbKk+1nb/obt7RZNPq2bW1HeBf1/IfF3Y6pnGa2zp6wMogXvQT63tZZZ254xU2e7R9939L0dFqXkomZLHLSg28fj8TNJub1ZLs4Tamfdn3Vd/9kCCkuKWKlnMW/JYG2V1n2JDKCzyenGSk5VrRY+BBSrdK60Fe/NhRzWWlxiZUxTMGdNFVSDGDgLFJFIM2oeI4S4/KIphvmnd+HjbdveGHyYY2iY048P8zCHyVIIYJtWRZzvVX3v3t/3/Wchra3ilLUpFi9anu/Ly8uPquv6ZZQAkhC50q/alsdq8fkX79d25MJ4DGKKbQt6vMpaYIgEFDIIBAaBQ1GYWVjgPk0/pz7FIIU3yE7SLHdMpqs9h9/zPWLk/3n/3q+730RHZgQ8IHQGGvplZJBEMcntyTEXTLbmTb7BiHUzRN0QCKxb2LX0EOrLzc9tru36yObJT/01zDAIKpFh3yEQpAIZECFjBACQeDR+ASyqRY8xm0ynn/64vU39yKjxb/TioGrjAVA1ISYeAxVdmQ2pvSK704o1JXqiABuX8/sOEy0NN9O6TVRogEhHRGXshgyCWZXd9RZ0AJd5+0cu4SSkUczwidDTBsa2TXkZiUgQ9NmVqxLrPOPf/YmykqKkABUREh7ZwiM89/+GjeY/fbnc/YN719ktTt6FGUtc7/GtY/fyMquzlspULKOwvWXDuZwatYReNtwxm6Gueigf3qe58e5b//EDd97+Syfg3VbqKFDEEJBBoqJPE5gU+10m4SpOkvLol3Ke9iSPeOGLBnXxENBnkq7tb2ib9uNVXT1SZexAyHHvMmSGBeQU9Px2Wl8+o5TQVV39b6UWwuB5iDFlF5BCCNbaOJ1OX2mdO3lybe2C7k0bQ11VLxyPx5fLwnmQNyCVrZ+yaBpj7qeU+qoQ4r+c1w1euHR93/2mdaPXliqG5fKL9LFiy+J9TxbBL2VZbGtVVdcrpQZreLGbyz6Ssw7+dHV19dM7ce26rp8xGo0ebYwpOxwyhxDnCplA65Sd0Pf96y5G34YwpPHGtu1+reu665qmFlpr4gLOonjSBoUhbn+TTXaYKAUFQ9/3r3HOvbKEIwRi7lGhKM2pP4zWLC8v/zCII9Pp9P/yC2HH87/XMHgkoRgep//szjEfLs6m82hzJCYgC4pIoOtI67X3h4/deut3Hhq17xFLTaO1TrEpEYZLLW60Z5JU12BrrmcIkdGo0Vc96EF/eNfHb3qs62eftdai9eLJths/gq4HVdf0x469+Vbxua/ae+2BnxzixRfolFFKDhpn9IGhTvopn5v3yTxaKABnPcqAVwqsR2uJcyENVg1+eoG+dK1TJ1iHF1EgeGA9kk+5+vIrnv3o5QNff+160PrECUylUAg2N0+yPB7T7NrFsRPHkKYeNGcpBDEjm621uFnHeGWl+/htn7nx/bfNXnkLfEBIYopNBXRVYQcipYzkzvnVIf8rK92pJLYpZ/uLrxbkvd63s9lLx6PRHxtjcDAoBs75fA/zxWN4vttxuS8MFm3MY6uquhzm6Y4xZxGEGAZvRN/3N02n05/1Pl5wNce+dwTv943G45dIIfAD6KGQJJVNNl27aZrrJ5Ppv8z9ghdHemv/qGvbX2ya5nKl9QIyvXhTmCv1sRh5Fze17t7Iohs5U+7uqev667Z8SJzS1zFinbPtbPYzfe9u3Yl2CCFuruv6D4t3KIVpsnWclZaieDVNc33f97/DxZieEaSShBiw1n1kNpv+bVVVT1VK47zbEmIpIZEFX9s5RWTPZMLyJEWk7/s3zGaznxuNRoeyU3zBYxC2rEshRpqmEUrpXwL2TCaTn/HebzsTbtGrcGqmQlkDTyf33mOQ41OKiCCm+LYAsBAcITSktwwQUEUdykNQZY9BL1O8PiiPcKCsoUIRVces+9g/nTzW/uSS/spX03y5CH6MizXESI1FETG5XGanBUSNCLuQAZSYAhGnICqJ9BYlJLXpCaFlzT8Is+dhe+XV7i3c+cEnMjk6kW5K8a85leoO+BzDT9t7wA/Y9ph/T7JHOTa7W3B3978gLj1wvT4weqB1DUIk0jITCxJaEVGE7OFQdCnO2l4CQDu+I13J76ETy+D3Q7wZjCdICLbCG4UPiZ8Am6gPl/PWd9Klfg75uViZBlrTekaWpW+j+fHd9NVym3y2s3ME2c+S8meBiej63UtwYA/mmmvM0pc/UNSX1iFojm8Qj63hZEQZhe8jvY9ELVmdTlmaOg7sPkTnp8x8x1qvOLG0xHTPHj4/1u79m3d/7IOrR99y2+bqnwB3at1E52waPiZtkrafolOGD94YoKbuJYHAhkxcF+P8gDY1ECVLuUbCpKQkuC/uwl7Wnb63b5nNZr+slLq2LOIxllgswEKMlkwgsw1fthRzFk+j9bOMMaIorTpbjcNlsgXftt27vY9dWcguVKztbwghvCRm33zJWIhxvgIKkVzK4/H4mZPJ9D8LhL8Yvvpyj96F2axtf9NU1cs181DHItK/bJ9xeBZf2koBsCUeDaC1/iZjzHjAfZDXNjEvBR5CwFn7sbbtbz/tSc9DlJYEHwghvjPG2JNBZjFGovcgUkZOUVS99zRN88SNjY29wIkLvf52pIQ5YiTM2valo1H31NFotEAiNteut6T6iXm58jNJUSh9mBu01vqN6XT6a6aqXqmiSCnmgwaRr5W/F0MkyogxRuzatevHlFKPa9v2/3DO/cuZslBOJznlVi1mCJ1NdsBjcIGTQ2vwie1OCZBRZi9CACXp7rzzdW78gMeOlv3zI3FYUIZF85ynN1jb54GXNlMpU9rhdDrliiuueNThzV2v6SbHvp+MR5MCfEGlbEPqumZzOkEhcFXVbmysn1y+TGO3VRvt7LJF48s/pZT4bLWw0A8C5rsAeSHLDgvvoanYf/8rrvnFy4WuRjYlj87OlbN3jgHUSEnVO6rg2d055GaP80lpk0ohRcISNMJQmQofPHVt0F6xevIEEU+sFN5z9MjqkQ99fvWWv/kUvONzcMtJ8KYG24HLOJGoVQIvhJAqZJZiTSFxLGeML0iJMApmC8r1l3BMOEZc27YvHY1Gv6u1HlLmtnyGhYXgVCvvDLIIMFNKXVfc9yEEhDaEmIqbiYxfSAxp/Y2Q0qIWSgHfa/GBD4QQTsQY9glASYWPpaJp+idESnGr6/oRwLVC8L8u+MLbEZHgKcGD7fvXxxD+T+DAqYpBwkgU71/gfBblL6aUrJOyESilrttScAdIuAIQcb75+RDeyQ5Ac30mWeu6/mhv7YeqqnrCgKPJP5VSieBHJa9wVVVj4JuEEH96scIJRax1f99b+491Xf+HpIDnDBpE8nAM7RGL4YGzyqA7iLki2nbd7yw7/71Cy6+USKIqwZQFSm4hkEqktU8omqahruvHTqfTf9jc3LzBWvs6a+0HICPZzyBCiKu01s83xvxo8kK6e6wtp8q2FINCfTGfDBGRS0TZHMPdSvMTCWe0RdO7pT91n77vVMqZtygMghE9tQ+YahaOf/KvXrwseHh98JFfvWYvxwHVUkrZqFyKyddsEAVEOSUgcCJlEES/CRKE0IQosXEFEUCJE6gKbo9XEq59wfODe9OH+7s/82qDpa4Ds75FN+BaSUASQtYc8w+dgAxELK5LlQK9ANw6IyPw04ZKgMiFjVzOylChzpMxZxMIk85nknIs3UruGYck4lULscJ3PUqm2g22KxUa09MhBDaG3k4WsS09nJUTCxztUd9++2GhRBrgiaVSIRbmXqd0PkuHDiCsZ6lZYk1ZYvSM+p4YI2v1pVRVxcr6HblfJF4oApJWjZgIyabSbGrJ+oph0lRMxjXrWsS7+tn68dUTt97a9R/9h1n74Rj7fwyET3v85B7DZXBmp/6im2tbW+ak88BsPgwT6eZ8xrg09ialn+6V0pbwG4Nrf4ekII2t9W9yLvx8Vemr1WJd+sGAEFtQ4gntvOhdSAxqMIQo8D5ijMJa/7Dl5eWHhPy5xCeQaMpjBGOqDPANm33v3ldVFV13YdxdkCwV7/1s/eTGuy+//PJnt22L94GsxaGkIfiI1gnYZ60Vy8tL121ubr404W/OtIAVjtUL27timPez93F9bW391fv26V8ej8d0XbdlUw2hgMIy54Ev+Ih5rPbsnoR709YSRiqvz/PbC2BSoF5eXv7mshnPi1UJnHUopei6lJ+/uTG5cSdCJQso+mB7d2MciycUBUtrk/rRBeD/Y+/N4yy7ynLhZ417n6Gqek53ZyAJCRmABEKQWUAJXolRQFAQUTCiF/HjXlA+EK+z30UBGVQUVAgyiChCYiAEJSpEJGAIJIGETJ2hu9Pd1V3DqTPsvdf4/bH2OrVq96nuCqmQNOTNr1LV5+xh7bXX8A7P+7wM1vp6PHrMzMw8f2Fh4e/T6wAAPIF3BCAsUdRQP4erLe7V5PD+jxtlkpnjB/3hH0mRXdZqtUjgCFhWDmndvuhJiPPM+9hGXyveh9891Su8Q3nw4KFX79y5/d8oZS14AudC2JCxwIBojQGlka3QQanAbyYEExs3zrwAwPNHo+GssearSqnrjTa7rcUcpfCUka2U0kdOT009lVL2eMZZO8xFBUI8CPWwzobncQ7eB6XE1vd9wKsrrk2W4+LL/wra7KAYYXrDVH//zd9+2eb2qVeTnGwVjMGY0brQptYeWbLzlJPfeqB/z/WZZVePygXINrCisGMajzkGLIX1Eg8HpRWMt6EqYsy2IIFjYYogxKjhoeGg4fXI0KIAyj7YwUW4PQdg7t6HctcBmNt7cLf2QPdouMUFwHshjhnr64GSuHhba0dFUbxbSvmOmGa2ZhIdErkODv/KWAsh+U9Et3Ha100+A6XUfwFYXK/3Ea/jnLvcGPPimJ2QsrCl7z8QKbGLALzdfReIApqbn/f+L7XW/9tauyGCNNNnIeN+JoetP/cnW+SBkkbfPpNSuil+Ps4UqQGgcQxorfcB+MZ6z0lr7aedc29JSbyipF6Eum9/mBAy5b3vA8vUv+vdx8ncGxMWWWuvqKrqG1mWPT4lj1rBcXGENSsdI0fpw2sWe73f6nY6b2u1WoQQBl1b85wxSJnVXD4JQmrl9cj0zPRx3vmLnHMXRb6EMV8BoSirMmQ0pfiC1MivnysyVzJrofFdKLt8NPGxoI4FwrJlYAGUtQboAFSLfSDffcvcjX//qlN+4Mf/oSLbZamOR0U9tAjweuEEmAeo42CewRAW2PkYA2BAYEGIBYFBQDgENAH3Q7RziaF7YmvqrMd+aPHmtz0dmNrLRgYZGDQbwFEHuNBVpMY0GFpPNveQ9lCvKtHBHOo31PwGHgELknwvqIQDICzgCMGIE3hGcJANcRlf+su/INXVHhjAY8l7t+A8lrxH3zosAdBCBMDZOMJBARA31gVZbe0eC2QxD6RElPhoNLpESvnGTqdz3FrOGwPhEBejw5Vl70Cmut2fiAFP71fSKccFjFKKou9VHvIAACAASURBVCiuBODXa1OI79Vae2VZlkZKyWNxlxQpnyoGnPMnUkqPd87tXpdGrEHi/a21s1VVvT/Lsl/Lsuyw4kRRmoWZ0k3roagg1JkBP54qO3ED0VpD1MRhjDEMh8OrABy9gt0aJJ3X1tqbtNa3CyFOm5Rul/YfY2yLlPLpVVV9Nn7/QBgQzevVHgRbFMXb8jz/KGPLRStSxSU+G2nMo/TvtXhcRsPiXZSQR3EufkkIDkbZmHXS+QYWIOIO4t/wMNoEh21tsMW0/KhMcB6zQJafYfn84AWLYaTUc/ygl587vNuWY4/Acnp6nSd/2Z033/xWWnfeemwmUkoURYEszyGlOHn6EY/4IKzNKALJzIpsi9jCCJr6PjByKQvusZC/TZZBYwAWdPHZSrmPKeUuV9p9QRvc4Czu8sAcpdCBhtejrkRdayL1TwTlNOg8vx8lJVFxzi2WZfm+1IJZk4yVg8bH4d87253OE+NxKegvHEPGuIOyLD+dkqisl1hrD5ZlOS4j27TA4iJbKwaZlPJH17UBq0hz4fbeo6qq91RVNYptSxfnpoejafU+VIUQIvI8vzB6OdJNbUzNWz9LWZafXfVC39m9AQDGGKe1viLFF6xGwMMYg5TyJ450vfWQOlMDwMp5WFXVJ4uiuC2OydjO+zIv1thOW5TlaweD/ieqSoXnFhLeA1UZXdZkrPg3sUXj8egC4ZZ1tq6oqKCUSqpgYhySjG2jkcTLunEVRqU1tDHVg64YuJqdjoLWWooGqILhBlo4aAtkUoKpElP8AND78u/P3X7FFRvFHCSGMJTAUAGLHM7ngA8vmcKGH0dBnQD1JOAi4ABi4cHhwUFMBvgc855irtMCtr38Odh20R9qaVDYEajJwHUGEANQEyoa1q707wnFwPsaHeMA4kGdB/EennhY6jFyBspacEuQaQJqgzfm3u1t7AfQgUQOiQwCHKGKonMUzlM4T8BbOVgmQTkHXPCwMAtIA+T6QR9+D7qki1L8uyzL9yilDq0tVEbga+6K4BlsarIElNKLpMhYiOsT1G4bRLsgLnpKqVsA7ALwgChrVVVdMQa9rWJpAaFPsiybuCmst0yy6Iwxd1ZV9aE6Lo9Jm8MkspiHcjiMMfa4LMtOntTv6eZsjDFKqc89UO1QSl2+mhcmlVox+FES07oeIIlhlAmluauiKN4GLL9/YHkjPlJYo6k8HkkIIbDGVYPB6GX9/uAvy7KCtQ6EUHAu4H3Er0RwYsTWhPkrhIDgAoxzsDp8QCkLNR8YW1YGlhMdxp7FMKYDVmP8GxTeYd+DvjLHvq11ouSL+n+MQimFLANGI0C22rrYd+8rDhw4sOs+WVSrSKUqtNttmKpClmUghODEU059nWi3f/oIrV7x63tZCBAQ6wkpRl1UZhlygWV0+WE1z6sSVik47xFqIwjw2uX1UKl++FCRxJqbLYriz9aygEaJC5FzIWiTWrSdTueiNI4cP28S9oxGoyvRwHSup2itP22Mcc0iOU2XK6UUUsqnAdj0QLUllUkLvFLqj4uiWEoVgOZxzT5cTWF4KAjn/KJA2rNSKYvjIm6ItVdnfj2t8rQ/tNZXK6V6k1Lmmt6DmvDqnOYxa3XT3xdJvSdRCVRKfaQsy5ti/ZJJfbKaN8l7P7wvzITOOTUcDl/T6/Ve3e/3C+fcuMbPkZQMa92KOhTN8RpZG6NSgLjL1s2uMT3jOkT1GvQvD7piEA2YqBgwhHTBoBB5wEt4SLgK6AgJ2+uh1Vk4OLr9gz8tBteMpnWBtvagnsEShoo7VELB8iFAh+DegjuAugzEZQBClcQQU/EgkmOpGmFmqotRbwmsuxkHxXaWnfry92H6nEcbWsGgAtM5mM4BGjwH3ElwL49Z3SAOFOk8pItxER8QqwgeA088vKAwgoE5Au4o2l6gWwCsClkfQ6FQCYWKG1huQbgHFwSiLnjECAcFBzEExgDaANoxaEgYyCO28ftB0gmfsgAWRfHOwWBwVNa5dEGrf+5sHNLudDpP0lqvUO4myXA4vOI7eYa1SB0uuFFrfdckxaDp1hZCzDDGznug2tNsW1O01neNRqO3aK1rrofJykGURDFwzrm7Hsj23lepF/5nr2A7TLwfseIlIQRFUXwGgF/vsEgce9baSin1uXSsp5Ja5PVG9UPrATI/UruMMat5scqlpaVfL8vSxGObikBy7Ir2O+fuXsv9G8qDL8vyvYPB4An9fv8Lo9GoqWyM7zdWSDGusBAs/pryPlj/y4B5ErNbSMAexNBDnIdKKRRFgeFw+F+j0eiPH3TF4DBpekKdQytvAQBKrZBnGYqlPtBqXbt/167X4n469AUPqPjRaITu1BTmFxaQ5zmmp6dnNp1wwj8A2HB/rn+sizEW1hoYa+B8WEQoYQHpCgQegRpD4C3gjIfRdlwBzNraikpeE6mrHz707Kqjyrpb03Fhjp6Y5PN+URQvB7BwH67lvfcfany8Jc/zzcaYw+K6jYWwb6394nqUEp4kycZweRrTblrdKQiRUnrOqhdcR0n7Id2ElFLvMMZc3lQMmj9p251z/wrUlT6/u7LqdKKU5pTSU5rvPSoGicfAK6UeEHxBKnV2wkT8Rvq7/v6cSaC+o8iaXW3RixLnIbBys1ZKXamUemsacohtnBRKqn92e+8/v9Y2RInXN8bc3O/3f3hubu5FzrnrfJDJJzWwQkAALaZlvCMgkUR8gl9+9wBgjClHo9Fne73eCxcXF59VFMX8g68YOACWwkQKWw8Qi8CLoAAQhaIcoqwtzKLSoBag/QPA4lc/sHTjP/7VFrsPXfRAaAWXtzB0HIYwgHJQH2odBNfEctoHqys/KjsC5wRt3wYrGNptCmUH6JHtMNuee3brtBf/NegOSriB4BbMMEgjYaHgoI7FzW2FUEdAHYEjgUciVHgMWQjchloLnhIYyWEAaO3APAUfWXQAECdAnAB1AswHnIEERwYO6RkkCCSin8aBQMO6Cg4VPLn/efIPtEQrgTGGXq/3GaXUOOYYv4uphaPR6BBj7CvpuWuRaLEAhy1K1x46dOhHB4PBdc45ny5K8fpxUa+qSvV6vT+qqurydOHMsmxpYWHhUOoujtYhEKxJrTWWlpb+UkpZPhDI73hPxhiUUh/VWhdVVY1dl3pcZIeMrdfhcOg553vTPqSUXjMajcqYQdEEMJZl6cuyvOJonpFJbYuS9r9zTi0uLr50OBy+RylVJJv/+Cd135Zl+Y2FhYVfQp0wvw5W94Ix5trUym9uToQQDIfDu6WUX4ufNYUQogHcXVUVhBArvDMxG6G+zlWc8xvid+thqU8a19baz1RVtS/2YfN50uONMXviNWrPx3WDwWAuUNiHjTz2SSjVbtDv968UQqxpcVFq+bCIKWm015dl+duLi4tvGAwG83GuxjEY331cA8qy3NPr9V5KKT0i6dAkif0Ru8kY808HDhx40uzs7AWDweCj1tq5Ztnk8WaPZVAxCbii0F9CgDIGgpobwbporC1476+8++67X71///7Ter3ehVVVfQqB8ubBT1c8qpAArCIrXAlBMyKA16Ph63bv3v24radufJILiGJ02m3oUQHB7v/jTU1Pv0gcf/zrl3bveztlHJIJKKvHxBjHaihhvWSMcm3wUDT/OlYlLgL1xv+zxpj3DQaD85xzW51zpJ6oAwC3GmOu0lofiOeuB7q/LMuvKKWeUhTFowkhZ1lrN6WKQd3GnnPuGufc7alpQSlFVVWL1tqnKKWeRynd4ZwTcSGjlFpjzKwx5r+NMV9K79vEH3yn0lRIrLX/rZQ6fzAYPJtSul0I0YoWebLgzWmtv6a1vir1YJRl+Tlr7bmj0eiZ3vtTnHOyvoellN5rrf1PrfXXmzTA90ecc8PhcPirVVW9hRBynvd+BwAZF+g6LGIAfNtae40xZpzmFzeq+yHlwYMHL6CU/gCl9PGU0h2o12zvvfPezxJCbjLG/KdzbglYqSzGflBKWWvtC0aj0fMppSelgL56vMx5779lrf28Mcsc4esVTmi2SSk1v7i4+MTBYHABgEcAmJpwWg/AzQA+HT+ox89dSqlHDwaDCxhjj2KMtRNLfdZa+zXn3NXWrqU27tpEa22ttW8viuL9hJAnADjJe98GkI5bD+Bua+3Vzrneet1bSmmstVctLS1dtbS0NAPgyVmWPSvLsvOFEGe0261NADqrna8qpayzPaP1fqX0TVqr67TW1ziH6xH6eKI8+IqBa9d/jFDzoYEAiEy9jno4rgOroQfgJJhjyOpqhaq8qVD77/oZs6H4r6mZM46zOA5cA9ZNw4CAEAXAjqsXLqsXDvAMzGYAAE8ViAeEmgYAaDmAAVBOnwvPHvX/YdD7hlrY+/kudeCw0FSE6x3je5+JgLf6QRgA5gBKoqYfCnloDhgJCApYCihGg7+OBC27JoJcIfFdxp+4xJPk2PtdpecBlsbGXimlPg9g7CZsxsdTWQ/Lu7620lp/3Xv/9fSaRwNgJVbX7caYP21+n8acm7JeXoNJipFz7ibn3E0Axt6C1aTZPq31rVrrW5vHTeqL1Z7tvkh0NRtj9gLYm353NMVvPfrQe19aa79orf3iWs9JlYLYRmvtrLX2r5rHRs9Ls63rCe5bZQzsVUp98Du83gHn3EdSC3+SrIdiHnkfak/RAhpzP+275tyscTX36/6pRwNhI/9cVVWfq6oKAMTcHDYihLs3YqWCUAJYrM/pARikFzpa+x58xeC+yAQFloAAxuw6cOddr9x41smXZjOZHA1HyPNWcA3db6XXg3Mht5988t/Ojg4+VVX9u9tZG5UeATxULPy+lmNcMVqrpArApNjopEV0PTamSUpHCoI6vIzqSqBSGkNtIv+994cxKzbPXy9ZDbi12n3i8ZP6sHmttVzvO5UUXxDvDSxvvrF/05hteu4DLenGNakN0aIFJo+PtG5CPCa2fT37Mm1Xis+4L33UxHXEdkZ5IECKk9oXQzpNfEnaX+s5h1bDs3jvNYDZ+meiNMfHWtv3oCsGvK61EB1uDpGHIErjxZBgsWrHgxXKFRgsyqUbP6v2sD/Yworfz+h2Yr2Eow6q5jKnUKAeNZdBXS2prhkAAriQGgFOCwCA0FOwBCjpHLxwEJuet5NuP/sjavYDP6KMG8Hl4KBwR65f8ZAXS0J/k5pO0yNgDWI6PPUe1AcvgvMengCKeSiGsYdnNZ049GntLxjn4qa/gUaRjYecNBei7zYZU/N+aXwxCIEb00oufxZxyM76urxt8jmJ53gcib9/PSyuJtBtrTLpueNnR7vOelq7kyzpVO5nqOCocrRnWU0hSvEb41h0Y3MBVsbVgclK1/0RIcQYi5G2+Tt5R0fazFKl4IHCyaTXXz+l78h9Hcb9co2i5c8ZGKOw9shek9Xauax4T55LDz74cC2yImHej8kaQtoFYA0ARjHcd+8f7du37zIpJbQxYOvAcwAsF9o48cQTnz61ffsfw1gCSmHc97m34EgS4wfHuDTBZt9tSRf0FKS13J5Jnexr/gmCwJ++rBiEMM7yInOk/Oz12CDWilU40r3ic69l05pkVd4fkVKOs0aAlcDP74ak1mnzp4klSCVUyVzeNOJmtham0fXcVGO6Z1Niuyc916QxP0maCnvKI3G0c++rRJxECv6cdAxjLOUDuN8S3tVKxT58bmGMXuENmPSz2pxpKmtNedA9Bqz2GHgAFnQctHekBhDZgKiE5fVxDqAahsUqeRwUQJtXqKq7jbq3vFh1/Vl8+lFnKLIdikoABNJlwfqNpzFbx9U1AA9W970dW8pDME+R262goOj5JZhpwLmX/QoWv3xdq/9vlyh3/0vSPthCfNwsItaAwBLUZUAB5gHmPDJ4MAMQEmrRZ7b2FsTxX/cf9fXw9QBiHYzlr5ftU9L44hiRplt2kqWyngpE0/3XFJG4sr1f9g7EXOUxQwiJenWtECCUk42FseL142KxXlbXai7k+O+07fG75r3jBtJclFP3d/x7vRW4uJlOeh4gWOZpm9dbeby/GIbVXMmxr+P36X0eSGu7KfflXpPGz6T3nSpT6/U+1nKd7+xeR1ZgJ72fdE47vzbjNJ0jK3FRk49/0BWDo0mTSW/STkJAoJVGnksMy2p+9q47X7rxsad/wWg9BX7/SHQopbDOQXCB/mAeW7sduuHUU989f/2/30BAvnZ4+74/JSqlxzoYsylNd3rcpJpu7TT2DKwf+GhSKCO1XJQ6sit7rBT4lXMpcqG5JBXugZZJyka6ccVjUgUhPTdNs1zLhrIeIYVUKUg3pEnfP1AyyQvSVJzSY1Plqdm+pjK22vhcr/GbYlgm4VyOJnE8pNdYyznr9V7SolNrUZajorhe7Tjs/SWKxFpG9qT+ShXx1RSTB10xWIlKdzjMxETN4w+94rCx6UkpLOewSoOUCtOcoux/8+tLNwxevfOcH/zQYn4CNVUXjHRBOAEbVgA8KAiUtaAsADlJja634EBgPqg3uT6sMbBcIMs2YuA08g0nT7FTf+ljxa1ffCroDYdyRsA1AyUcRasDxRg8lpDxLmAciGfgVoTn5eE+woaqVyGW/+BRA3tqAQ9wHzYY6kIdCF27Ajw4PAneFU8dPAEssVDMh1bXTY+va83T4BhRIFazEAGMwXtKqYmgryPFUtNrTDpmElAsbdP4fiy8J2YDB1psRVSHlaDwLAMrAcklCtcD44BXFIwwaGEBW49DwgDtAEpApIUzDsLVpZp5UC5YGC6oaFg6MsdqBE8BB4AhMK45aeE8QCxAXKiFQmgAull4gFFQKSGLESiAkUBNlDUdIh35EsAYoChgltcFziwIAZQGQp4LhZASVivAO3A4UFB4tEA8Q9nuAZQCA4aMcVgbMEQk60IrDebrguEcAAGoDs8rCOA84AWgLABK4T0DtRzEE9h8BBggdy04eEhRwlrAOQbakihMAVBAeoCo0FIBiWFm4H14HqsBLhmc8YDLkfMMIywABCCaIxM5SmLhGQUvhgAAwyi8Y2h5AQaGAforgJqpAjVp3K1VUbqvHqPm/VKMQ3pM07tzNEnDKE2Q5FrSQY+EEUqV/kkcIZPAkavN1dRztJoXY7X+Sb0bKSg0AkPTZ4xXoJSCcw6lVtI1N70CMaW2qTwuhxrIYX1CKT1GMAZrEFq7Ssc500X5d7t37/5zrTQY43UHW+R5DinlGFF8NAkviNZumzjpKGY2zJy+8cSTPgAKrrUFoXXJ26KAsxZSStiHMQjHvDStmsgoZow5zM0cJ3PTTUtpKHYS49XNFLGoYEgpIaVcYaUcLQY7FlIXWKFkpRHgHKANPDx0vcBYFy0PHzZNCoBzUMZqPvKA3YEH2llQMYwJlxpfmgAQEg4OFiaU5uYcnPKgoBgALugtjFN4eFgXaMwICFDPyQhe9QaHK4veA5SASgFSW57OhiZLGVUfD61DLQ4KCskykEDqHd4dpWN/qbEWlIY2OetqrEXsJ4y1WlL/j1KkKzFElkFQARoTbwng4MDAQEjoVwsbUswoAB5uzSnAIWCgYbSDNUHpAAGMCsRPFATahE2USgYKikpXgLWA98gEQyZCcRz4UKzeYiUb39HkgfYKNT0pkYQoeg1SZZlzvmK8NyXOmRgLb9IWe+/XBPw8Ekao6QmMG3NUrlIyo6aSHvEEcS7H6oTGmCN6YZr9E+/dzAKxNoyj1Z6x5oM47BlTpSveI1V+Qr0aPl6HJl3XWvvgewzutzgF4TWcz6HhYIkCYQD8PR77D7wxk+TxMzsf/4whPwEDq9Fvc3hPgWEFyTJUtSeCIubjB0AXc6TOvQ9T0DsOSxi0bWNEJcjMZki+9SJo93/s7PW/a91eyJwBqoJEhdxvQGkrWOoA4kDrWBABBzyDI7RedNz3Akbve1ZSgFSU1KW8QptvLB5NJPYk4FeSZz7+LP69lqwAaVeOngDNIXVCMwElAqV3cNzDeYPtNod3HvMZhTEOvKSgIOA6eLRGtQ9PaAbvGUa0DUszENKHJAzCMjhP4KyAJRRahrTdqbIFZTwqUDDZRu5HYWHKwu7aNgKAh40qiarg4FB2CazxmCoBBoGlLPTRtjL47fYLBceAthU1pRkHqQhU7RsRMLVnT4KAYMhM8JtYA+UMyNCDEArOKJwFjGvBw4M5BQ4DxoK3RHEAjsIRHhQg7cDhkbnA2FkoDm1rTBLxyHVQHJjIUOkKQnHkQChlawl6jAMQgCmgQWCpBzwDBADn4bWta5ECxBmUQoNwiqwESGlhYcHAoGx4lrJeqg13gCCo6uwpZlaGYuK4ScfdJOBqHL9rAYWudkz63WrHHGlja4bjoqEWN9c499JnSEN2a8V0xA08zr80bt+c103lKVVEmhiN9JxoAKTWf3P+T5Lm5hyve19CEE0FJW1LqnCkikPTM5L2MSHk2PcYMI6QzlGr9tGiIJwD3pe9PXte1uv19hFCwGhw+2qt6xdwdFeZtcsoV0ZDcQprTU3xynHCSSf9JqamLgTqAZ5ngTjG2WCBPSzHvKTx2Djho0WR0rE2JV2MV7MkmlbCWhaTFeeP/3P1zzKSgKAek94Ht7x3sLCoUMFYA+9cqJyJGDZK3Y0A5wxaK3jnwTiHNRbaK1jYQGBudLCydVR6yRhsYrQJHjNKaovdg1MBzhgMoucAsM4nEcS6xKy1sKg/k0GBNnVCs4evPRQeot5IGGGgYOHZjQFhNFjWWN4IKQnVQIMnpz4PDMaGNSO4LeosD+9rT0jwbtDYm7X1jvpQZ0MtkdCm0CeEUljUfa41GBgcHIwzAAE4F+M+ooSFqKitr2kdnK9vU/enzAIBm4uU8YQAQgaNwi+PmdQqbHqUolK6loyEw8bXEcZg9HQ1JbVMVzuvacWvBiRMN7JoATcLW61FmopI/LuJt0i9BtGNH++1DNhbWdEwbaNzbkUmxtH6J+2H9Lrpsc0sh6aXKG1L+ryRhny1VM5oeDT7+HvDY+AZnLUgqMDrcKR2FJI4eG+gq5t34+6ln2Wsf8X05rOzebIVWmswTgAKULOSV93T2tqjtSfTheJBzJYgkDCMw1mKkaMY0RamNj6B0xP5JU5VTzFVdQdohswqmKoCyQXsmPMvHcShIhYaXt+H5aErk1z7wJE1+6Z2nk7SlGM/TvT0HmtF1+txOkj9gQMAjyVEy0rXXm0DDWAODB4UnmhAkrC5C4qSdALWpN7TFAdAHbgJFrfyABgBLAUBQPkIDASSS6hSIdi0AsgsrFVgEGiJHNVwBEeAESkBVy43nEmAc2SVgrU1Gwh18GYEOI8ltCCFhBgGnpAMDhQGFoHzRMDCWwvPgcpbMKtCJ3AJTwgkRrAAnKAw2qE0ZfjeA4JRaGrgKOAqBuIJMhXozUsRFBDDCAwhsMZCMI4cPhQSI8ErQG0IB5RiCAiAQECVGmAlwICNtgVtNUwmAOthjA/pzcPo6aCgnqKkHGAcjA5hK8AiA+Nh8amsAaAB5uA4AyzQ0RTcAj2PkFKSKHNNazrKJCBhDHs1mPUOk3RcpuMz/p60Oaf3EUJMjLunm1uM5afKTbxvxEtMylb5TvESqVU/yetxJLxQ0/uSWtxNZSUNCa7WP/H5Jz1f3LibXoz0OCHEinBB0zvS9Bil92sqj+nPMe8xGBcYQTCKwChgHYxx8C7EInu9hX87sHfvb1VV5YUQYDSS9R5dKCEhH7zWwMJ9aFgcKEWlKmzdum3r9uN3/j0y2UUdF1rvtKmH5aElcSGYJNEamIQQjxZPc4FLMQtpUaWjyWp5ykloHKCAUrUnjVDkMq9BOR7WAsY6wOhgqkaj3/sQ284yWG/Dd5Qhkxk4Z/A+zKDYB4KKYNUbAwgxfl7nAzMjZ8ttFIyHyZqS7yDkZqMma/LwUFrBYXl+17AFMEJAQeB86GtnQ2Is5yw8pDGIvC3W1nF4QsEZB+ChlQqYIYMxdoFTAs5oba7bsI7UnWisgbYq2OzJvGZAQHlaBHwABdBZZqUlICirEt57ZDJL3g6BYDKEC6QEtIHVYZ+XmYQ2tfVHKWCSMWZDiEE5BXhASnHYOJgEGpzkco8x7KNJakGn12tu9k0rNn4X4+7ASgxOtMZjbL4Z74/zId4PODzjIn52pJ/otWh65uIa3fSiNDfmJkYite6jQpM+X3O+H61/0meYdEza39F7kLaxSVAV15h4fOrtSBWY2O9pG9N15Nj3GIDAEwIKB28B7trjxcR7AklDDQYz96V3mN36/JkTnvxTKj8eQ9eBc0AeGeDI+GoBh0RYYD6EBGce1Bl4Z5D5sNDEWoEj64D8OGzY9Jzzub7t3Wb2zleN/Bbksg+HDgAGeAnv60lMCoA4EL9MAHCMAPS/LyVW+6snI6llVaUgLnz1hHURhEgpzZ1zHWvtIgCbegrqhYVwzqcBEGNMz3vva2KtIyrvnDDv4b2tN61YHaesh9tODZxCBD/e65nMkOGHmS4LTvHIkceZoHQrHIwDrkHpDgBwTtYoAwVwhecVinpg5quu3ats6YACbSrJuQ6EwmMXLPYA7lDLA9phWgEdo1FBY8ZV4iwq24VRS//N4IcBXgNNDIQ2mHLAcwCeA6czYKcPiUAHNXDLp/KyrEpA8gzUepzhLclBNhJqSOH8wk182nnv4GzMa3JgpsRxhuMR6GRnYanrgPLDDkMqCLZri3OyqeyU0ahbQOFumvW/pirVIxQgFM92hk6Bo4IDB5BbCw2HNjgcDEY1x6kCcLd3/nZkXnCBZw0HhAIzDrDzwODbznvlgOdb1WWg2W3wxZ3WjPYRijzL4aoCnHBoCejK4QfLPiHABuOAfcDi/qrvWwB5DkA21RkhDAC3GiMAHA4KwEconKWHx8RTN7GU8gxjzIkNi3fkvb/XWnsP1pYOJSilTyaEPI4Qsh0A8d7Peu9vcM79F4CymW0AAJzzUzjn5yqlHIBrCCGzAOJmfTqAcwDAOXebtfaGdO7U86EthHgWpbSttV5yzv07CSA2YgAAIABJREFUAM0YO1dKubU+92ixeG+M+SqAft2mx1BKt8fNMHol0ni8tfYa1HUFmooPIWQ7IeSZhJDTAEjv/W7n3JcQCmj5+AxCiMd5709zzvWdc1cTQkYT+ud4zvn5NYjwWtR1OAghM0KIJwCgzrkRpfTrWuui+WCEkJk8z88vigIAvoZQF4EQQs4jhJwCYAnAFwGMK6Y2lJ6cUvp059xjKaWbCSGHAFxPCPmSc04d+4oBJYHhUKsabe3reKMDpwxlCbRyoF9Z27/33l+2ncWzOztPeMzyADyy08RaC8EDGjhuEM55OG/hEDwSZVmCc4Hjtm175d7i0LVBs6N4uPbisS/xnVNKkef5L3a73b/K83zs5mu6I+NiUxTF/HA4PK0oigUp5aNnZma+zhgTZVneMhgMzqmqSqWWSrvdfv3mzZvfDgBzc3NvHY1Gb3TOTe3cufNbAE5crX3zh+av8s4/Z4wriJkDJJj+HL71qEc96o5zRL7DWlt++M5vngStDk7J7GfPOf2s92+nTvZ6PX1nsfixpYXeKwpDvIeN1jI/dfsJ13W73cf2eOvG22677ZzCDrFt23Hvfsw0+9VMSrItaw8+d8ONv3mo0n+KTEBooPIaU6J1wlPOf9ytJwxV69Zbb/lbUw5e4WO41QDeY8PG7sybztq64xe6ElszXlu8IBgM1OArrP/J3XfP/q4x5k4KYHO25U1nnXXK/6VZiVvuuO3fvjnvLjDOOGc1hODgAKw2EEJMnXLCKXec28LWYlT06J7bT7XWzhtg544dO259Qraho7RG3tFLN15//bmg9C7RavETsq03nrBj85nWVsgYR5u1MOoP0Gm3YIyBYh66I7A4qjDcs/stty+Wb9ZGo5PTvzn77LN/AaKFf//Kda9Rg9FfZFOdkx8zc9q3pRRZOy+LA9/+5rlam9sYY2DgMN7A2hDKnMny95199tmv8rnA5679yiv2Vfjbk086/g/On9r2ZlmNSItzMOrBmYPSGq32NA7Oj5yc2/1YNRzdtJpVIaV8RKfTub7dbmepxRmV2rIs9yul3t/v9/8Y9cbZEArgldu3b/8tQsgjJuXne+8Pzs7Ovo0Q8k4AJnVndzqdv221Ws9wzqGqqr8YjUavidZtq9V6Tbfb/V+tVgvGmHJubu5xVVXdkt680+n83ubNm3+dUorBYNDv9/unee/n2+32p9vt9gkxle9osm/fvlc7594rpdw5PT399TzPeVQmYp2LOGfLssRoNHplWZYfjJ8bY8A539Fut9/WarV+WkrJ09g8IcT3+/3/6PV6F3vv7+Sc06mpqX/P83wDpRR79ux5CSHk48CyB6Dun7e3Wq2X1M936WAweAEA0ul0Lu12u8+KbRsMBt/s9/vPsNYuRmUGALIse1O3233Tpk2bsLi4+NvD4fAPpJRTW7Zs+Wqe57Tf72NxcfEiAJ9uhHBYnuev7XQ6b8qybFszy0MptVdr/fpjXzEgDtYqWN8FEJkUHQAD4wAHgX7pwWBA1B2L5p7+SzzZe3V32zM3aiLhaUiJccaCUIBTBu8dvFUgXMKyFioPGA8w4sGdAfF+XCmwUhYZGHpkBpDTZOOZ295uCVThszobrEYy17ZcJKhg0IAnda2ChxWIh6o0EL0bJwGXYmpVWZZp7LJjjOkAWCiKor1582ZBCIEQYkNVVRyASuO31tqpeD1jzHR9zxal9ETnHLIsQ1mWh6UyciG3aK1htQLxHgb1aKrRe9sB+oTCdp915z5wxvM3lkYQAE/n/Ek/dG9Pnj5UqFQlfnTnlp97r+l95uOQ/0BgAQdw5+gF+2enN2zQODQlutpWUPA4lftn/NSeEenYAtz1u2/Q2/74afTez/SG5o4eGDjN8XhdZM9aONQ6eUnhUeVw86U8A5zDdKVxDnDye3DCZ1tKnLmwt49iW467ZxSqssKZwxxTi7r7Uip/bmg2/uiLskPPKytcW1YHrn1C/yQ87bbboJR62hOJ3qEp9hICaO2guYRst/GM0dIzXib4FjLbx8LCwq2OkUV44ALgJ39hZDqnHphHUZY4d0ZOlx4/eQkb/YmuRuwMIadPG41grca0Uti+VEAbDdbK0acOh6REoTvoVxUODnrHfaXu5x8v+cwjD2kcKPrQEJtusgxsyd27pX/v7MbN+YmPGJjWiRo/9iYu31lWGhk8WlkLvaoACFq/Q/zzunfeg09Pz9jjKlzLAWwZlOf94qF9xDqLGzdsxBI0mGRwUkBUFpUZ0K42mxfdssmfWoSEEFRVNbV58+YsAgTLsoQQAsYYSCnR7Xa3l2X5m61W64LZ2dnnYNmqhjGGbdiw4b2dTufiOJxS8B0wtu637tix4639fv8xw+HwYgAmVux0zpGIL1haWiKpy7uqqj9rtVq/zBjLrbU55/y1VVW9JtlsN7ZarYu11pBSYjQafaCqqllKqWCMyRSboJRClmUwxiDLsrFrPSpBUsqsLEsopXLOOddao91ur0gVjEpP7TVgUXGo5/lZ09PTV05NTZ2Uzvu4STvnSLfbfTaA1y0uLr62qips3LhxeX5yfljIpnblj/uHEEJrJYRKKbfH5+Oco91uP8YY87rBYPA7jXWJtlqt8bXidQkhtCzLkC6feEbq55StVuuDU1NTL419luIRKKVotVrHt1qt9x77isFRxMODEgpGKax1UIPBtw4dOPA/s6z3dxu3nMD6wwqMMWR5BmcNlFLgnEMIiVIbEHaULoohiKh5EdImBO30u4fl2JXUG6C1/vJoNLosWVS2TU1NPaWenMVgMPhXSqmvlYcFrfWh9FpN3MlqIKRmrLJ2N2Jpaend1lq/AlgG9i3r6jgiwpCjJFKLx3j9xCcDEFLDOp0O5rTGCVu6/8cdcp+ilGo4wKjDLbJwj5DR432d5gSab9+x/TeK/Qu/aKwL3jW3HMulsZgWZcgo8pM3b/1HcVCcyRiD007fseeOS2/Yg2soQKfAnvFIsfFC2e2y0Wi09aST2h/efc/ofFfhC7MHD8456zZTSrNc4rmVwiVV3G+shRoV2MjyHxsOh6TjHHq29ynAOghOt87gRWVVoigIsjyHNgrbNsy8CGXvHVJC71vY93G/sO9UCoIZeGwSnae2252tpbeYm5+78S5g1+AgUHmg73AlowFrxDRHVVWQmRxnJ1BP1aJbvHybOOFXLDymBb/IGvdO1H2nqgoggBA4jzN+vHcOCwsLt2jgJl+/P+eDm/zgwYNfPGSH1xlYjGDBQNGHcxXBNzmjIZ3xCFJvnnZ+fv5XrLUHvPc7u93uK7rd7g/UG+kPtFqt/6W1/sMYK2+1Wr+a5/nFlFJCCEG/379tOBy+yzl3HQDBGHtqp9N5/fT09DYAkFK+3BjzxdFo9P703qvhZJxzdxhjPqyUehXnHFmWvawoij9wzu0nhCDP84uzLNtIKUVRFH1r7Tvr83S/33/DYDA4JSoqeZ4/VUr53NriH/R6vbcbY+J67JVS/xz7IVrhSinMz8//hlLq3ib4V2t9RTyeMdaenp7+WKfTOQkAyrJEVVVfMsZcYow5SAg5qd1uv5Qx9hRjTCvt87q9K+L7idI0/r6JC0mVL611DE28lnP+V8aYvWloY60pjfEcIcSb8zx/KaUUSimUZbl/aWnpPd77GymlXSnlj+R5/iIhxPQxrxiIum80i8yFFUiNrg7/rhdcXyN4fQEcvOEfeV6cn3We/oaRPAPGcAA5PPFwloAwBkEInDWwzMCDwRIKS0jNmejhiQfxgKxrOGhewRFA0w7gKYjrgniA0flwX1QACLyrgSyw+J7jD/4eF2PM1c65q8syoOudcxdMTU39S73YHKzdgS5aIU2JVklcIOKi0EQlN2ObcUGrqur1xhgXP/fewzM+JvBxAFReowcdQaY8DBwECmxUS2Ccj5WEjh2glBvxrY7HNqLtcb2C/axjj/0K9Au/5szHD4IBLANMBcCCYQQHDQVA8QqbRgwExg+l9Qc2ePqWcsvL32P3v+XTG+UdejgEA9BSHkRbSFAwHRbmnzPlz/0Ilecf3NCHMUb9AmUv22/kP1XEe3ggh/6TR5LBq97X9385s2ma/vpifual1ejFn0Hrgx9i6vIXuO4rOKV44XD4Y1dgcMk9BCFbwuWAd/QVtrpQzu7Gf+zYZj45IP9MFcCJOeHnl9hThDiIj3fa123enJ15wZ399i9Tcd6fOZzGDLvtXbCvdwAoC+/pEo1/3cGmnrNEgf/E3F+/i7I/84QAjMJoBbg2uKPgsFBVibzbAlChQoaKMXzClJ/6hZZ99QV7SnK6Fk9qo9hqwA8axmGswRbv8ASNC2cYhy8NPplln+xB+hYodpAujF+C8RZ/aHuX3QPyDpXlgDaYchqcsjq5geFo1UnrzcM5565yzt1BKYXW+iNlWd7AOT+ZMYZWq/V8Y8wf1t6umampqd/Osow45zAajb4xHA4vUEqNlVxjzNUALuOcfzHP861ZlhHv/RvKsrzE+1CmtTm2m6KUemtRFC+bnp5uZ1k2k2XZLxVF8fuUUtlqtf4fKSW01lhaWvqAMebuOOaNMR9qgAV/rdvtPrfOsOgXRfF7k/ohzqs496qqutQ59+26cyYeTyn9+VardW70uAyHww+WZflLzi0XybHWvlcI8TPOLafcpIpBNCKaGQ8p7iP9PP13WZaDTqfTzfN8g1LqzcaY18R7RC/AWsmtGGMntlqtX2u1gv7S7/fvHI1GP2SMuat+DhhjPqq1fjtj7GXHfFbC0SUMUONq5CihAOCHC4u/tWfP3qsoZWOXlLEGskZUm5q166hXjwjYcKs6tEtiiPdhOcalafWkqGRgOc84/S7+PelaTXR3/J0ipJv3TBHnh7XNujGSPwzt1Qdd/GY8NglBq9XG3NLc5zjnYJThxONO/C0AORgD3DL51op71x96+MVF1bsmb+XI8lzu4DO/i0IFxj8AeZ6HrB6EPHxrLbbRLT8vpYT3HrNLix/rD/ufsLCeUgohBQiIr1T1N0tm6WrGOITgmBJ4vobG/MLcpUBwY+/YvuMHKTCDer6BUoDzc6e60ycKwbEwP3/zQFW3CEEgpXy+lFIIIXDv0vwH7r7n7quFFMizTE538p9I+8hYD238mDdBShnAyK5mvNQhI4ARFphWYZfTBGPnwmMIfLm32DsAAJnI2i2Z/XAcFwQEkgq6Y8eO5zHGUCll53sLlxvYMZdEtGQDA4SvGSppzf1QZ02sYX2J61PqHi/Lsl8UxeettXH8nhitbO/9j0kpN9WZAX5xcfHXo1IQmQrrUMW3FxYW/tw5F1kMT6OUPnYSwn2SYqC1vr0oio/UMXzkef7LlNIupfSFUsqT6nYulWX5jtjOZgZOrHobvQFpzr8QYjwv0zTONGOhBmiuaFe60WZZdjEQNs2iKPZVVfW6qBREhd0YY8qy/JAx5h/SZ42/J2UZABgzoUZpegxqD8gnbM2i2+l0Xsk5P7P5XtcqUsqfyvO8G8HURVG8Xil1V3pM7TG5oSzLNx7zioFDCw4tgFT1D+AJEFAADAIagmg4kOCIE20wkQHFvZXf99mX0wNX7+mQRWRcAcaCiA4c7UArA0oIGDQIKQFaAbSCowaWWjjiYKmDpR6Weviak4D5gGeIVQZDRigF9QD1Hsx7UHhYwmFJUDwe1h+OTYmTvplmBByeWhUBW5MUhub56QLXJFGJMgYyeQ+OkDWXOYAZgGsPoQioD+Q8Hh6GaRim4cDhvETugIWWwDc3c3wS1d9d78nono2b8ALjHv1a0JdsshW2OI2S5ShpBsXMch0ML9ATHj3O2J/D/vV/bd2BzXvvwv9LWz+9ocTZp2UBuWamtqGUXQyQw9MKho6mXuzK80/evR+7Z2bwIYq/W4IKM8Q6QFkU3RZun2Lug0Rf/m26gK2LC7hI4wn3cuAeqv/1ViqX7sw6eBLnW54FPIU7gGmDHaaPC417XqvQZMZS/LVUl91MYB6pPf2fvvuTBZnCQiXc+zu47N1t9UkvOAprcLEXLzreWNIGkOUdOJ4DWQcKDlXLoZ8bzFKAYwottgGZzyBAwGgBYBCyGLIWjHFhxWEexBncTsnwE8R+1oOD0gwv0OaijTBwxMJLiqc5fepzrTjr9qlp3Mj4XQeo/9qs5BgQh5mqB0oUBLc4DRynAzizGOJ4U6EDEVQWogFy9HTDI0gnjjVrbS9iEYQQzwTGFuReY8yX4glKKSil0tDaFQlVMSOEnJPe4EgbV221v00pNaxDAjuzLHtRnuevEkJAKYWiKC4BcE8c700SnyRksIKcKD2+2Z50440hutgP8bz62B2dTucxSYjhUu/9Yrrhp4p9+nd6rxr93wWw4sday6uqWjGv07bV/X1JWZYLAJDneavVao1xBvF9rVWyLHtOJFRSSs1VVfXp9J5NOeZDCWsRSik4odDWQ2sDWvPJO+X2zd9110un2mf+az6zKTcaodocSQhBjtb3zWhAoCx7WL4PJC5G6QRtIJZXHF9bGZu63e5VhJCxy7X+fWLU5oHlhSt6ChhjaLfbH/be+4T8ZU6NqteTulq4B+BdKHVNPMEyyiCVmlirLrfNBQeAfQeL2Y9u2rz5VcQ57Gwd/0Zd3P5xLFchHyfVkvh/DzjnSQV8bnZ29htTrenHUUrEKdtbb96/v3g5ATA3N4cZSmuacQCUnjLVmea9pUUwzkzpcDMAZFkGVdXMftoAzmDkcYuUGQCDqWxqE8yoDWB0qDz0ue18+4vFdAubwX6cwF0JABKSbN+0/UK3sA/GWN/rFZ8iADhw4mmnnfZk3HkXZqv5r2qPvc7hs4UblQQk37J9y+PZPf1HOuB2pRTgAOcD86GzFlVlYVyogRAwmQHV6ayBR/hc8KBkEEQXenhvswcHlxqWvVJKiR07djxX3LsnQ103rgv+I1meSTMqsKgHl4Fxi5hWBo9QFZNgx/YdLzNleZ5lFB3v4USGcu7Au0ZQ164l2TBuWtGFXlvJ21ut1gURyKq1vi6OzzzPT0s2212o0xEbqW7RC7HXOTfy3rfrr3asGGkTvFypOOduL8vy/UKI19ZW8ZsopadRSlFVVb+qqj9JrzEpDp+AfVe46Se1ISLvGWPodrt/xxgr0kyBwWDwbqVUtPxP4Zxn8Tyt9dfSFMeo6Mf53niu8b23bNnyp977t6Vtrb0s00KIcUgxbWuSEbFQFMV7pZS/kWUZWq3WT1ZV9USl1H+noMI1CBVCnA4g8kpcD8A0PZGpgnPMKwaWho6RNSW3BYEDg6nry+UAYDwYN7DUwdVV4DIXtCfdv/4/3b2DN4I++10yP40UloEAkDKD9Rq+xgHQmneAeaAuRQcAUDxonMK0Au85XQIAaLIADwYPDg8K7mqiDToAAaBIu76eq2s5PizHsjRdqM2wQbQghBCi0+k8ORIgpZiCWC0ufgYsg4zqRftnhBDpef39avb3AcyhJgHI66FU1DwcwllQFwm9CIAcjlC0PUVbC+he8AT8LfB/z+qSn3/Tvr48w/szT2njJYMRPtqxDJ2KQs/4mtufoaVzEF+AOIePC2i2dOAPXsI3/VNZlPhd/8gXX66++RZBaUnaDlAKHhWEA3Ihpr1StMUFBmZjMY9slEFBW4eqdt1DETDRBgXmS7MZHaehjSHSWu4AfExUn/rxLf7FT52/By+E/ZE/EW0JQJ2jR9ueLqon3rZtMxYWFm6zlnwTFHiR9Rc+oqrkDZu24T8G1aXGDj0o2/1vdPS147Zte9pJjsmfhrjw7dDv1k6PDYEcFJwYMEbgOZAZh4p6WOFq4BKFBIXVHhU8XPT4uBLwQI+10PP2CzeTan7LzNSmH2Bu883Akz/B3RdgK/wYcOHO4QDXTHX9p+fEpYx6WK2C94csQXoOrz3+t9l23sj48ygZQluLWzobcJnhX7pSqGtrNukjSj2mCKX02d77R3vvTxZC/Eqe51sIISjL0lZVdQkAWGuJlHJzPM9aO5deJx3L9fhUhBATxzmldEOqGMd5MEniGB6NRn8ihHhlt9udEkKcEdMQy7L8C2PM7uZ5cTObZOmmG11azCyt12CtBeccnU7n8dGCjt6CoiiuopT+Q32Njan3wRhzIN4jKiLxOdL7N0OBnPPpSWGCeN3086ZiUOOK3lEUxcWMsW1Zlol2u/17SqkLj6RwTRBJKW1FLwohpJf2R1MI+R6olXA0oaAwMLANoEb9ikC5wHDf/j87ODv7kfiCxhzT7L50TySRCKRx4ZOH5XtNUjd/Gq88ksQJH1H6xhhnjHFaa+ecc95755zz6UIRFYe4sNUsZbuMMbu01ruqqtqllLoegcgEAFBX861vGlg7jyaMBUVYA3ft3r37fYwxKKdw3HFb38gpWkc6N8S+CWylL5vvz//31PQUjDVyR9Z989A5UMbGngZGKDgXGJQD5FmOsiqpg6cWHsooCC4gsjywMRoDCsa9r1H8tkKN+0OpcaWUYliWJTZu2HQynHtsjYX4HzKTnFKCObX0z4QQZawnm1jnRfPz87DWOgd3WZyci6b8FOMcWmtsEptePF4a6g2Q0ECHHPvTwa2slmodrDGh3oIxoCzE/8eHGAN43+ubwee998iynGTARVxIANiwsb3had4DzrndQ6e/Ok7Bw/J7M8Zg7tChucXB4q5+v7+rKEa7lFK7RhjtMpOqUU56R95DSsk3bdr01zt37rxs+/bt7960adMZUkpUVeWLoninUupf4jgjhPjEYh1bzDGcFa3uenMklNLxIKOU9pub3yRJsQLGmHvKsvxAGhYwxvSqqnpHek4aMkjm0TgMl5IU1Rb+uA/Da2VjemZjDKqq+nK/37+q1+td1e/3rxoOh1cVRXFdOgcbGUIybUfav6s9b92OA1VV7SqKYldZlruUUrustbucc4OmEpH2XbIXHaqq6m2xUmWe5/+Dc/7MpuGxFkmNjfQ+zTXMew9OWLBcp2zgJA9c5BSEeBhKkFcSri0xUAOAEnhvIYSEYgKQHIwFFtF2u41iNAIDAyMUzmsIRlATQgEgiLaxA+BrSz8Cp75jcWOetvhYCOSpYUCMxsdhhXpd1t8LU0Cwwld7/v01les99vhTn/K4JbsVC32C6ekZMDcEhwMbvwQJEMDSGpzkaoq5+nl8XdeO+ZVRCM/iihHW2jw+Nwntd0TCA6D1bNfUwRKDbDQEKAmxYaJr5ES9JnhAZ2E3cIrXC3UNMgIDCEEGE2hvwcO79cNAAUU3QBsLzkp4AlQkgDMI8aAe4DbcwLYcjLbogsFrBl0xKCowTRwkACoknDV11TgXpg8jwMCjxQSc9kBgkYCtna8gZrlzjl459SElk1IMUwxAWjwlDQtIKWMZ1QOzs7OnAhjFYxhjyLLsdzdu3Pg7aepU6q6UUmLv3r2nc85d/BwAWCZhtQWcCHF9WBB4SOcgQKDBoCSD6XBU1qJdERhXwYBCMYDRGVC08GVWAEX/rQdap108tAfar4M441sOL/QItUeYjHVHLTZ4D8MpLHFA5SGltK+16vffcOLWy8/75q14DGc/+TfAR48bGLQVRRccJTcoi0Fhuzv83qIgJ06r/HSo9kEG7LeAo/9/e2cebVlW1/fP3vsM9943VL2q7qru6mZopjhBYyPKMsTI0qBRMZIoQ0JMxCAxYsiKYUUCEaeoWSrBMRoJxOXSJYqCrbS4cAJkAUHotHbTaeiGbnqsN7/77nDO2VP+2Hufe+6tV12NRVtd5P5qvbrvnXumfc4efr/v7/v7/fqhU0sNec2purnquD1kr+xjVV7VejxSPfjghD0xHv/5z3LlN7qRl9f70Td45z/6z+AFJ/bP8pmrr+MdDxbvnNqGLOfaf+COPcft1DzUG23tc/hU7Xhq7iyrlPV1u4U/1jwohBTPfq3muvV88OlJo/EIGuUxmSJ3ihMGvFTkeGwtYmmlkIJZG0ftG/TEMqCkJ0smTkNWgfK8teYd37HRf9Ez7tjh+1j55j9uxv8hK+Tfv87adcZj3lwNb7pfyNrWDYXK0NawKwfUsofLPd/fHP7Ynb56Y84qe7rBbN6PLFfI6zGZgsoHJTIthGkhS4tm1/pM/XU6nbrpdPqXWuufqqrq7aGLerIs83VdbyeXVlEUpyEQ5WA+/W60jk/keT5IC0xd12fTotNNI5yU6bQQLrLp67p+Y9M031WWZd97z+7u7i875zaPciMsSjr/ottiMQFSt+YCwP7+/stTVEIiMabxGNu+l9rsvWdlZeXxo9GoLSW9gAq0SF8iPabxu7W19Wrn3NsW54y1tbXfXF9ff3EnlLB9Pun3hEBorX+prut/U5bldXmei16v9wbn3HvTc3fOtTUT0nyU0k9Ht4Vumma6urqK957pdHomtaH7jLqKifQ2FCOxBKUgrJ+R5JGqNjmLkMmKkRijqaoq5DqPJ21ju3EYHwuR2Itc9P+WxFnA2MPxzs6L73/g/h0hYH19ncl4PFe5ylqLNRazuO0ifnznX0AdjmCAex8UqHZwz746jyM5iPfnfFcUBf1+n6IoKCPDWAjR1n6QQsz9CCHx3sVOB71+nzwv0LpBE2Pa8wwyFRhnGqiin+oRRHVc7tJlOHflqAiCZIGk4xZ9ol0SYnfb+fyASims0bOohBYH61QbxaGbhsl4Eiw9HBKJxVDXNVVdh+MkFH15313jO3/lxMYG4/GYjSJ/NQjZTlgE/S8pJjbG0DdNQw7vuuWWWz6yuraKMaY8pfrfY23IRVpRgTWgsnucc7YoS6SUapXBl7SlAJxrwy4BCvjyRoekR5vjzY9nfZz3gYJw9uzZ35VSsTIYcObMmRc43MqxlcHzjh07xubW5mc0zUfyHLJMvUAp1VdKkmXZ6WtPnbjxy57+xTd+2Q3PvPGJp6/7OQTCe09VT4vV3uAfNbrG48llUKKM0eRFQQY4F4sgEWo9SAQm3nyv12MwGAR00sXMUpH0MYL3DIfDoVKS1WztqZXmCzY2Nr6pbhqKoqC4WqU/AAAgAElEQVSuqt+x3rWcgsRTSNFUADk5taln6EUkzAVQ4ug6CKmfRFje7O/vf8fm5ubzNzc3n727u3v68PDwOVVV/TbgU5+L9QnuTIx7IcSTgI2UUz/P83ZMR9fXc7wP+Swj6nVLuoekjKTF6SjIuuOe2JVSjlJkAfDJozg6R0k3I2O6bpKkNHRJwouEvaOUj7j/p7TWVchpkxPTM7fPt8v/WYw8SG3tjvH0d7pOh2vQIhydKJG5Y51zI631jyTlZTAYfHW/3/9SYO74dO/J3diJRLHGmE8mZSPP82cKITa6/aQ7rwghyOg/cwVg7Mbx9nsxS7ABSd/JjFwrJJ5cgnahypiwkml5de6KL1nBObQsQIX4fnwDPYfdP1tBZTMMEofAARIvJIi0aKRc55dGCvpYLNaOcJO/+kR1//YrNvr1205ceX1+1uV4s4YVoKUGYUFFklHkDDipH/4CFxCDCFEUcdQnYM75sOJb2QNRgDchDQMGRCihKxBhdhDQi3SR2kdrM1o1EIzzFH6lXRX8vsYgEWRxnLiYEMeLUPpWuhAoZW2N95axsEiZM8gd+aThxNDxpdCrdb0CMKihBAQSA9wpJZ+cTid1IT1ezhCbSHwrTLi3S/v2L166EwQc7WeE+cmkWw8+7d+NWOhmIkuKRxr43QnWuYRkhbLLQiq8cFgLKItWlrKB4yLjaptT5j3qckSeZ5QjWCszhkwQNOAVjcv5Xg5/+tXHzXd++6dYFWLj6UY572g4MR4AkkMhODsQDGQdOlYdOuwdK7m/ddz88Evk2o39QopvmE6+Lr9vh+HGgHsAXIF0cvtjdnrXNafX/85Ju8Pzmbz0z+BdhYQmH4OAfKL5wpqNf8rJl1ztN/jQGcnbP73/R6cmJ3hAH9Lkmr9S/g/37XBS2GLwSnvi6bdhX/p0fexEsad482D4BzuK5ssb+LvIb9PrDVJKPnzqFF7kZK7ATB13niy588SQr7sXbJbxXWXxbb9bTd701zmolYyVfThZ9tnTGgfoIgMryOyULCIxHo+RhkY04A0Z01CV0gEuEDRvR+z8yUi+93l9+QKlFN+/z7c8cZJ9/WdOrFNV0wfuluqDzoay0dJISuDUYY7OJBZ4oKzYy0LVWJRk9bCPQ9D0joX+0uzOIlQ6YbMwQ6q01j7m4LgLOiHWcfHpkthiFMIrlVJkWbZRFMU/aZrmzV2/OkCWZcVgMHhVgu+NMZ8BbukulN2FL0mXV9NdpLv7dBfWC0kXPUvjryuLBL20YHafURfZ69zDQ9Pp9LYsy54Vre+vy7LsS5umubkl6EWkAJBKqb61dnxUuGb3mS8q+IsugUUlKr2jqqp+oyiKV2dZdn2/30dr/YLFuSedt6tUpPY3TfOnxpivj2GSZZ7n/1Zr/UNdJKfzDFazJz/j+vsBSj8KD4Re6NPC4gRqVBSAQETCnZCCjIyyGFBcdfV3b1yTf4cQgjqYj3incbZmpbTcdfvoW/Wo+uMLvt1LKMF6CtCLyxVMp+988IH7/6vPn/j61dUnMjUZQoCTPprqbkExuDhUREd0JcEAbay5DMVdpJQziGBB2vJLPhwp0gl8uzHUc1AC68M1nHOx9LyjLHs0dXC2ODEjVEpPtN48RgjyPEM6gbMCY3TMH57z+JNXvHV66rTJlEINp/R7PRAS3XhEacb33Hn7M8FvzYdqfH6FbHQts/T3w+2X/LOLhKRFxSB91x2wXTQhTQC5kpjoC/d4RAzpd6GrhnftHQ6Pdx5vLFZKdFQUnbPhd1WAtRSSe2+/845fLvvXfF81rWRQWj1NU1PjaDw0WmPd7H7zsqCqahTc9MDu/e//4o2rvso7q6x1GBtSjZdZiTWWLTd82zWs/4CUkuO98kWDSv55Ubi3Nqa2ZBllj5MnVvv/Y2O0cU1gUKvRmOmve1eipMT3Shz1g4fV4YdPFiefp7Ksd+3KtT8ojGN/tM9eM3xHY6GQ6vGPu+bxX6FGU7b3tg/+ev/Bb7TQ5PQwGErAYr74q7LiLb1eKU6cOPHl2f7eE/Dco3WMOHAW7XwI04wkB2HB2pD0TCIRwlJVNc6FDASZiou4T/OF4KHhQ+9Ux695QdM0POXKa/9dURRX9oXm7p2t9zipxslIcuk9pYVHKXxa0wpA5Mj4b1JVsXQm5ywMSbrW+iKq0F2QFhbEG+u63hVCnCiKgvX19Z8YjUb3VlX1HmttKgq2MRgMfmZ9ff3ZMYKAqqp+lugYTNeUMcOe9z4DBt3F0TnnrLVtxEN3HJ1vcT1Kugp3kq6rojs2u0nFWk5Hh8eTXDJp/6qqfmV9ff1ZWZbR7/d7xpjfEkL8y7quPwg4Y4wqiuKGsizf0DTNg9baV6RzLiosRykKXXdH10BIbqCkVEV0uZ5MJm/I8/yd/X4fpZRI/InFtnfb2FH4fqNpmtcVRXEsplp+nVLq4PDw8FeAcSRGnymK4l/nef6KbLP3Rce6N6xl0OJyHxI5WQHeWaR1qHY6CT5Bv/bkcls/rczzHlVuIiTdoOQhUg7R5t4M5TH2gJxQIEriwDvsY4T3OFFNYKoqRy/TVL7y7H/kR/YL9ayrr8v+odSnaDIweBAOgSZzoMwaAE1+cREFA6uAoASExd2BcAExkAbrcvCtGRLcPN7jYnoVXDwUh0fQEtDdzJMgkeTO0kNSqR4FGTiFaDJ6MtRwsHOvw1PYuNQ4i1IFJgNnXOwHjjNTxeOK3spX3PkpVldXEXsVUpTUXtDQ58ozeXaP8eIQcGggD4FeyuNRLQx7uVM0E7O5a4UtKgepDHOyrrr7dK29ZEGl6IT0XZog1tbW3tuFM6WUeKNvpaq+25hZX5CKGHYHCsnUK/ZVj0xk5C4w7DWS2knk+goPAdIWOGPY6/f4zenhT78kFy8/ofobpXHkRc6kl7FKziqC07qHLgbUVcWVGHbx2Bz0au5+/oAffdFK791fW2kpcayKPsedonYN4HhDxs//49Xxy19zb37t41bO5L8qxr+8Mx1970Nwa0+b/uPIvvJ4NjjNhuP2s5v+9dXwv9wj+BTWgCzhsKIHvBX/Oy89sfa8p937AIOVwTWbheVmP948hPdpAV/vxDdd51X/1tWC2/abP/lVX3wAKSB3AWWTgOW2b6b/IydXTl775EObfQ288HbHm0RlMAw40Aq71ucAoPEgVaDSAODJkKzbPifNGmPlOGAT0w0AcYodSj5G+a6PeqZP8rL/7KE9Xdf7fPipZ/idcvPtRVOjlcOJgJ5V2jMcaE5OAlnzLWbjVYf16IWrCByGXTI2Zc//kNr6V5XjE3bBIu4uNF04+eH89Qso1MFoNPpB4GcGg4EYDAYnsyx7V13Xt2qtPyWEWCmK4oZer3dFqgMwmUzePx6PfyldJ91HguGzLPvn1tpv6d5b0zTNwcHBDcaYtupicsktWrEPJ13iYfc5LFrOaZtSiqIoWFtbu1FKWadt6RkMh8P/6Jy7CcAY86t7e3svW11dfW6e56ysrDyl3+//uTHmbmvtQ0qpq4uieIL3Ptvf3//tdI3uz/nCl48iLydloEvO7IrW+l3T6fR9WZZ9VeIyJAUj8Qq6Cke3/dba++u6/uEsy36qKArR7/fzfr//34qieC1wlxBiIKV8SpZlK1JKMrXAvHdRMZCxFJoNOYVnhSZEhxTlPdoYhNBxEfIIkSa8mJ3r4pD2R13SBGusw9YgwwLYVDu7L3+guP8Dx06detKjef22wmNSDIRDCIfzDlysSZ6sDyHaOOskYi4BWpdTEKCDQA4NlSDTopLnOc5KnLWozHf2P0Li5KK9wznwPlSabLTG+NYHRhY7eK5yZN5HSneO6hf4jYIZ0HF5KwVdSZNaGozn4xjAPDGqS87qfp8mFGNMS/4aDAbPTdEK6fjx8OBxs0lknlMSkhs5nLOUZQ9tNJIwNiUZUsWyz4CLitpkOqFUPHj38L7/vrFyzX9S0dcUrGiPROKdQ8Yog7wx2KaG1RwazSH6T+6+7+731nL1ed55xOoAATrkGpYYrbfuu2/vRQ9VvP3a/MyZPMvl8Y2NZ6zkG88oypwTk6Co7+7umj03fOPmFj8ZxiTkvRI7bSgVjI25qa7rKi/ynhSCuq44bMxNVgUe8gYb3+aco7Y12vN7RV7glMB0aMpFwWSvOvjDK7jiFXmec5K1b83y8Zvquru4Rjqw92DDZJsJgXMSj6PBkClFXmRBYYjIqcgkvm65IJv3HNzzgaetPeFr9XhMURRsb2/vHNb1+0VC070HpZDSYoyxlfEUznPV1Vddl+/sXLfWCzuWYpVsZQW1vfUFVvOJ7iDrck+Atu5LdAu0FulRFiXMlNzpdPqLQojTSqnXCCGKPM9VURTXW2uv7+43mUx8Xdd/NB6P/4W1ti0N3B0DWmuklL08z3tJ2e2UMl8DNhfZ+EkxPoqXsCjdsN9FFKSrDHXzOEgpWVlZeWoah+k5xDZdb4y5Kd5/pbV+cdM0b5NSPjfPc8qyzKy1T7HWPiWN96ZpnDHmL7vvYXFMH+UySGM7XXtRyenmOIjnME3TvL5pmj9TSqnOd36x3UfxOpqmeZMQ4phz7rW9Xi/P85x+v3/Ke38q3V9ELD6WHd+86e5wwgInkq85sOOFd0hlUT5OMs4FyFkIrM3xQF56bOPwosBah3UaoyssE3B3T/EHMZI/tiAE5ESs89KLECFWQkb2pTIZzjVoc8dDzQNnX9rvP/QbmUKl25VolIdch2iOYxfZDJWL4IIhW0MohRA4IbGRbLCn751If4iTIc2yx0aLRSLI8MrgPUxpwPkUlBDc+UJQp3EvFbZfurcfX9vv9/u5p8AE73J0HUX6Y+QaJN91VuZYAXWMhevJgsIrRBVYuKi10HlPGApZkIkMZxUfc4eTuwS+EYCX5B4yD40NSIeKK9hF5W679PLgcDi8BVg3xvyFtdYfRbg0xmwOh8ObvfcbxpiPeO/n1OUIZd4xHo8/AQhjzK1x0A8PDw9/tyiK69JE2yUmCSGYNvqvrBUEWzbB3KAQKCn5BNr8vp9+6K4r/FObxm3Wm2qCh3cP8ttuFtO7quF48kl4CBxlv089dWRqhR9i+ONfuN5cfV02eKYxhj/Wu+/YU4YVa9geb//vN66Vx7yXnz7Y2Z9KA3ntqBv4SF64W4rsO//vivsFKeVVO9UD7p7c/lreTBBFxmEOf9TwwfeVfNkVfvNVLxtc/S39vHz8sZX1rGms/1R+MLyN4Xs/tHb4i02h3lccet9zAyaAbjQUBQcq5yav777X6197/jUbXzMZT+RdJwfjv94dvjk7zJBIbry6tL3S3T3NyoduPeTdzUSDBpnX5GWOrRxCW36C/NduKMVz19H94bHcjCovKPC/mWcfvbLPdVNG9f/pcTtVGFgjKVC5xGuDtPBb5crNV/ft9Y3A3NErbqUKCdKkMCE7VOnYK7V/ywG/cMdJrukdK/p5ntkbx+5tdyIOfAzrklaR+Yw9qfjTsnzn63rFNVmeU2WO6XqP1WxKnmUYWyNl5g9NfocTdo6w2XVPGWP2x+PxR4UQJ4UQD2qth4v7PYx7wdZ1/frDw8M/EEK8siiK5ymlrnTOSSGE11qPm6b50HQ6/V/GmN/z3rexRalfaq3ffnh4OHDOiS560VEMpt77nXhMU1XV+5qmuUEIMbHWfvoo5O0oaZrmtvF4/HHnXN97PxduuOCuOzsajX5fSnltUmy6lUrTp7X25i7y1zTNA865r62q6sVFUXx7v9+/Aeg557yUcjiZTD5grX1r0zTvjtfyTdN8wDn3RVLKMdDmYujeU13XNyulblBKUdf1h+Nz8FVVfahpmp6Uctd7v9VVDKIS8v7xePwqa+3Lgcx7P9Fa/35sQzMajf5USvkka+2hc+7+Tvux1rqqqt5grb2paZrvybLsq2PeCumcq5um+XhVVb/dNM1bBEU0iH0RIbBkzkWoWsSAWefBRBRAZeCyYAJmBpoGipVo9VrQ05BxaHoAfkrmZmWKPQJLKEgUNlzaeLUsWiOKkP/c+BhUJ3rge1BcEbSilkugw6prQljiRbvMvY7nUIFUiAwMxGjd982d1E2FkyFKwNm0psRiPEoTb7jDTgfmyEXgog/5Jc7SBfEDwDsLbkitTO8rRaro+F0GrCDJIpPQRFWvJDLWCcv+nQjuwXBWEhWDEC/fBAIDhQvOkMc4oPSIpEvk6sKSQBtGdFSWsjRgu8dCx00QJ+p0jvOJRFKQh5j/SOcUQJEV9E3NaeAJcdtNeYHMM545ndBEgGEM3E2JzDKk83hnOC4ajnu4ltAHPhQ1+1UHJ4Enxe1/QeAR1yZyG5wgUxk3WE0J7AMTCfe6qARGLH6lADWFbwqnXVuhXNVYs4nZuxvMxwtAQq/JEPSonQpZBwsJtkY5z1Ve85UUDKnZKRWfqC0+X0drzdOYImLbtgHd32Da1Dg3QWYgrWJF5azriseRU6LJgPcUQFHyrFFNQUgS8RAwzNeCC8+NwhB14efphLEyBQ6A++I4Q1qUBLu6AU3DF07GnAJOEEKoP0TBCIvNBViDdAGJ084ghOf5PoyrHQicrpiybUJI9P5eDEVZ0tTVXF/y3rekuPRZliV1XZ/TBx9J5ryIhAnn3HHvfQ+wSqld771pOSYxP0BiuafzdvvzIkE3KQpp+2JhsS6B8UKSxke3dkJy26U2HKVkdMcYzMiE3e2L95FlWe693wgRN+wBNrV38T4Wn/Hi804hzIv35Jxr39nifJKkew3gHPdLFyFJcsSzFMBxpVQppdx3zlXtMzv/406JPmxEsBUC2UbPpSqBEOBJgQohN3GhSAHqMXgnxNWH2wtbO+jnpZTWk+LCQh+oRhpi1L1oyXwzmdH0Lj4MP5XRmC3MWbCnZbA8yxgtYplfuBNQn3KRThTgPX03Y/vPJbwTJQDKhoXDqtCCXKds+slzGt+XjMEpbr69Lj6vRK2oZQpriIok0WWQnmtgbpEtdDUrjvZ3LuWzlPicZcxjkLJopv6S3q0PHGIwg/CuRNWSUBREvCFDk0Mb0eJwaAQuBJakJBpAUYUjmiyM5QikY8QAPFyhJwgEW/14g96Dg2NNyJ84QgVeixgRs/qEGzSK0gXlUyDYV9VcB1yJ+tEwpg/JdZh7GhliYpSzCOExZZxM66DTh1DLtjYqhyoODh8+By4g4WEciRYidDE/SejvAt1mVA3jaJrFGxFBQS/NINCARYiyqOI4SY+/jgNeNmvBrcMhEshjA6dKxmcVFxMRkj45GeN32mcRfYj64jhOS1nKUXLBQPMOwT2GItIu/UFS9LQ497jLQFrWL74z/4jZALwEDfH4iNj87VztKElNX9Qcj9r2sAfM7SI+r3gFl4sImGXxFiJBShDj7YOO1n1xC/yI7hZ/vj2O2Alm/dgvbF+8wc4+/qh+coFDzytt4x2+e9Z2+6Moj7irp1lHzP392Z1jKUv53IkgWqYIA75N4IdrdQYTNfockEibJooIMCeTN+LRs+PTFTKC/hHP5w0BZYjJFx4THT9FBhAaIGJjPGAVKqIlBNspBiwmU218vpM+IslT5kSAOCF6RDsfZNELPzc5d6QfqkFwqIKFl9ng+jGdPB7CQxERnkYk0lu4rhDBSdC6EOIvNr3+CASUcXsdzNIOhBA+Wm7DYtGpeHw6RMZn2SSIy13umQwusXTfk58hOTq+h4ENWM04C77vVZ3hYz82gM5D/yqiR0oXwUIt9CwKBsJ7C5fxMT6mJCnTChgQIO1pzKiIciAlqg51RkSoJEKjElknctV84Cz19cy1ZOPwkkKRm/leX+ehAxY69J8mD9dVOiB+tojj0UHmBLkr4p/BhWZEGdAJYUE4lA7OMqsA4eiHaZCKIjxQGV2pbabOgIgIGcJ8hQu2vpApwZvCCRmyfwKi0cgOx0oX4WnmTQx3jCe2seSyFbH0cmx2ThZfbeCOxChpVARdzWNi/lzK55s8stR07aqUFsWOPJzSfQEL8jErn8Vgu9jmJVvhUlvSrQF1xG0c5U5ZfLdiZnqe5+REV1PccDn2i8e0XMg3l9A+P7/tvHK0KpoCZWfVFv0Cgtg5LDHFu9Bb659Lt30E0hgv7Y7GJT4L6ab5SkhcuK8WPWnb+bnpkKL7Ho5wQc7u7HxInQiRO+37Os8J+FsEFZfy/52IVhWOufzzGNCeqE69aBImioRKGq4I+xdt54wJJUhGouuUJwh+xXDFuIeIV7jELrJerF1gqZh52oHIp5ALqpBf+HHikelW55VYc0H4+UlxFsURJCDBM1M9TXcm6+yZTuBd+1zbGNnEus3mZxdlMkDEKpWOfrI48VgkXijwgl68om7faqrJsNLiJxJiPjhHnfaToUEqQkM+6gQywriac4k1S/ksJA6r3MawQmlnnQdQJljqYViL2biLVURX4vuKwA41eexZYb8Zbhh+G6QaJCJwEdqFvgjIT68FgIJXXVNHmknRWdg8ORrlQMXzjnNPIC532iWgNKFn1S0y4pHek0cffJ0DSDLdj2du8NLiskSOCT77Xh2WYhNOiwpARcjeLTvPUYcF14gsICcRCm3i95nN4+MN/bshJJXq+3kgTVPESq9RkZIhpXiKbspNC0jOezTS75H1KxJFQ0RsxgvwYsYRv9zjepbymJTsXE1ZPMxfnW1xgk/K91H7XB5G4Ywh8TdSwD9Hanv3LJfsuYkjnkN62ee8Z99+PWclHbFP+lqc49deyudcjnBTB/M7PvSFF3zUa+i637tj/Jx90+sU8wps93uRvl/Qrr04op8tDoKOIvHwo+I8352DanVwlfP55ph1+VbxuYDM2r7YiCOfyjnf+M7n3ClEtwmChRZcYoxxKZ/PIpLv0OXRcou+OpQBHH0r8FhqGUuQujL03TKYBipaCI48aLXtxBSOx0e3fdzsQ9YAurr1pZRz8y/25kEMUc1+95D4w4LkU7xYKePnDF+RnbyQhrzzfScneNoaOR79aDhMs3CfKlC+Q1ioZIZMGBHzUkS7UAi8FBAtrF5sbvDHCnwW+RdW0Iaw4ij8LIrBKbDRgOxNQ4aCOn0bEYsyhl9FMjsrOkykoyVicHGSBXN3PZJKhpkB4ViNbPWRzMDPzNKcqjP6cqrUv1TwmSurYgXP0D+m/bA6FVV411pG57YtkQhyGgSOqtONhYfSXIFCYNkCoIkdVrlwvzpxm7LANVhrwtwwjshUSfDLT1WMdPEBfEpRwzoe3o/tnpaB/FQ0CbkMlnoeWzuNiZpK2+A9NClPv4/9T4RRXdiAPDSqAWEQzkdkI+xfpyqpLg/tRCOAqVgP3IXsIEGmCAeijRYJEEBCHop4mjhMWbEFkDNU4Xkrl8Z7jCKK+TFKE1qXoqaWeMFSHg15eBw8as0z3/Bsc6vdRvFd9XxesX1MS4jGn0mygJOWfmk8HeEJPyYQl0cKpczMrEd0DvHYaN3nvwhZIMQZvAgKuowLVvhytt+cdd31zAezv4v2sHjs3PXm0aDWTriA8d3eTwtsiACjLxjgj3Q68Z1P0d63mOfLXBDte2Sd/7x7PAzH4IKXnZfA2A4/+1xyB+xSPt9lOTsvZSmXsWSExEJN1HBVuRpqf+gppyT9/+z49eeo1ReeURlGaw6LAiUVgyokQ0nx/snLMB+6KBBKhorf+HYd7ZoK1s0Qtflwu/DjXNQ4Wmh+fsopUrASzNLaxmt5QMjOsWK2b9t+G4qM+bhfOr3yHuk80qY1NCJk0mMlxKAGVppZJpHZedPvKcFNSoLTMX+SoqEDf0pnMM0VVS6Z5IpJoZjkGdNMMc4klYCpEGjwGuG891ZLWd+9N94eYberpt480PXW0NTbh9ZsTrCblfDbY222vWAXxD74fbzUrVXmgSXitpRHQS6SObeUpSzlUoogJsmMEbbWGLCWXi/PH3/V6ptP75cvXPUg6yYsbn5+Ab6QOJeiENLV4nXjwpilut2+s09cuDyQq8giFALROsBmhWOs6bjqCIpAmyZNQF4UeOewLtQPSbng2+IztlOVL90IAQxQ3rcKT1rUQ9tnYMEs5ayYD5AQoQWp/d19RHwAQkDZKzEGKtv4iakOd6f12V309h5m+xA2D2BzDNs1bE+Rmxq2NWIX2NbI4S4ZEzwGywTLBMeU4CLQs0fJnDr0SFG8pSzlbyhLxGApS7mMRZY5zksQeciW5yacLineMuF/Pmlw6mVCOQokojF4bckygZKKqQzmdakXWIFzn6BiJj7nQ4Kg8DmzqUsGzBbj9E1aoh1SiOjv9/i4sONnqVt1XnbxiXbhTS49Z01AMVxMQCZCavCkQEyzsMr7mFlR+qCAKB8KIFkvcFJQZ5JJoZgWgkkh0ZlgmktGhaKRAdlohKAGaiGphDSVVLsPHhzsjL3fPtRm66DR28Oq3jpsmq1am60Gs2Vgy8EmsO2g8TJkB22BERG5OYlCNM/HnWUIFef57KQ8FYT016qDzdRLxGApj4IsEYOlLOUyFmdjIZ227gLZqdMrv3jm/mMvE8KG+vLWk7tgvSslZxSgI0q7LkpTz1LxCgHIaK3HhdmZDlTv4ydRcRBg3Xwy73CsahEHn0iA7aE+ujPCgu+sQ0mJyjKUjCnZYzU66yxZr4iIQbiedCEZk0IihUIKSeMcWuvxsBrv7lDt71LvjmDzELYPYKuJi3sNW8GyZ7OC/QrsGFwVfqiABtFJAq+w2HN4FHPUhQvxGJJvYlEhuICcwxFZylI+h7LsWUtZymUsea/EWktuDacKstdV/Nz15corj68IkU0byrrAO4XICmSWYUQoa1w2BN98JkLACaQQ+SDeozxkQpLAfRCxEmen1oWdlUeb/98HwkLrsgg/IkLwSbGorMcKhRNQK0UjJZVSVEoxzTKasqTKMqpMMVWKynsm3tvG2GHl7XB7uH8w9mZrpOvtPVNv7Zn67NC67YlnW3u2tGMTz7aEiUBogTBCKJdcCI3v8Pq7a3iXPH3Ooh14DQgBZmEKbfedKUOxVghNJYgAAAQ0SURBVHoHCZlFFemuaZYOOS+1MB7djf5yS8RgKZ97WSIGS1nKZSy6qhGZQgjksWO9n7yuf/qVK2IqxpNNNlQ/lJYVCqFCAKI1NlazC3Xs9QUI7s65ufQHDo/FY+Kin6uUWIhWCUguBUgV9nzLawhleYnFuQRCZDjnqsaa0di50diZ/UPc5gi2xoitHZqtMXJrgtgaw3YFWxVixyFqDXWDayocUzwjglWv6RQQizKnsHiBf7g6CR0IQOUhJbHzjpac4AHvohbVzQHu5xWJ9NT87Ornvarv/FxQlgSDpTy6skQMlrKUy1gy4GSRy+9r9I//Pbn2mievrgijDVOT0+/3yYdTPI5JLzi4B5VBIRmvCpyzCDNDAjqVlmJmSolz4KVEK8k0F0xzwSQTaOE5LATD/iqNkDjvqYEG3FTIaSXEtFJydO/O7vbY++1DYzYPtN4cNc3OyJjtxpizGrYa5DZw6PETYAredBGGLJOtQtGSJWUgXAohoAnbWru5oxBIL9sqhUlcdz8gj8UH/NzK3KUbnl8E0Cg54w10SvimPZRUrUI1d2Qb2hC3u6BAhJwHItaWhMWqpzPKqH/kesRSlvJZyhIxWMpSLmPJMyXLsvzBJ66eec01g544uO9eHJbBylWMx2OOp1RWfkYYFIBzlqqq6Gflw50eZ6021tZTbeuDygz30Wf3abam+J0D2DoLmw1s2WDNb9awPYHJFEYVTCbgpwgqBFMEDQKLREpBJhTaOlKWhKOkW3O+m40srPe+u2ke/nchLfu5CcyYW+3dXMrzFIjpZ39FeMN7d/QpUjikODrSIXAskgLQvcEoqcxyB1VIi7+YIx+cqwIslYKlPFqyRAyWspTLUKSUCCHkj9nea58xKH74qp6T1lqGhWCa5UzZYNIv2BkEol+/8Vhr/W3raGMwx8euwqvtew6GOyNvtw50dXbXVNt7tto+8Jydwpbz7AB7wBDHEGhaMzVmCpQpmf/cMjX73Tk3P8sszjhHhd6dGxwR2hyX+e4pXKw+eM5Bwsf6I67N8tkeI2ZEwbmTLTZhLmRAxOop8w1xWdPZn7nfJbJVNdIyPwueDJ8mc51r+/nf5z5nLZZzfy1lKZ97WSIGS1nK5SkC+Pcn107+QKlq0zTD0XQ63dyDrT3L1pDh1hC1+WnqLQE7g2DVb96ec2At+xuOAwF+iGKKZ4JjTExQnoNSIcOvuUDGcn8O634JcC9lKZe7LBGDpSzlMhQpZSaEeFru2RdC7E4pKpwj9w5P0/rcr0TikexJH8L8kn2teoFcZyrAh/0lM7Z9sm+tQ/qUrqhT0WMO4e7asDMYXS78fVSI3aw64FHxel0ePwu/B3Gqmt1HNJ9Tpc8uGNHed/oi3bLtkgc5wkpP9UvOvTu4QN7BLgHyPKhJqRPHIVVD8ZHq4c89rr2/2X0tIYOlPBry/wDv/A0CGjjhxgAAAABJRU5ErkJggg=='

            # Create a new document with the provided base64 image and extracted images
            doc_io = create_document(images_base64, base64_img_first)

            # Return the new document for download
            return send_file(doc_io, as_attachment=True, download_name='extracted_images.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        except Exception as e:
            return f"An error occurred during processing: {str(e)}", 500

    return "File not allowed", 400

if __name__ == '__main__':
    app.run(debug=True)

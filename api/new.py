from docx import Document

def extract_text_between_sections(file_path, start_section, end_section):
    # Open the Word document
    doc = Document(file_path)
    
    # Variables to control extraction
    extracting = False
    extracted_text = []
    
    for paragraph in doc.paragraphs:
        # Start extracting after the start section
        if start_section in paragraph.text:
            extracting = True
            continue
        
        # Stop extracting when reaching the end section
        if extracting and end_section in paragraph.text:
            break
        
        # Append text if we're in the extraction range
        if extracting:
            extracted_text.append(paragraph.text)
    
    # Join extracted paragraphs into a single string
    return "\n".join(extracted_text)

# Usage
file_path = '/home/mac/Downloads/source.docx'  # Replace with the path to your Word document
start_section = "Course Aims"
end_section = "Course Learning Outcomes"
text_between_sections = extract_text_between_sections(file_path, start_section, end_section)
print(text_between_sections)

import os  # For file path operations (optional, if needed)

ALLOWED_EXTENSIONS = {'docx', 'xlsx'}

# Helper function to check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
import fitz

def extract_pdf_text(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text
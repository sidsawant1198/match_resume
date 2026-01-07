from pypdf import PdfReader

def extract_text(pdf_path):
    pdf = PdfReader(pdf_path)
    text_data = ""

    for page in pdf.pages:
        content = page.extract_text()
        text_data += content

    return text_data


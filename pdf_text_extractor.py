from pypdf import PdfReader

def extract_text(pdf_path):
    try:
        pdf = PdfReader(pdf_path)
    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}")

    if len(pdf.pages) == 0:
        raise ValueError("The uploaded PDF has no pages.")

    text_data = ""
    for page in pdf.pages:
        content = page.extract_text() or ""   # guard against None on scanned pages
        text_data += content

    text = text_data.strip()

    if not text:
        raise ValueError("No text could be extracted. The PDF may be scanned or image-based.")

    return text

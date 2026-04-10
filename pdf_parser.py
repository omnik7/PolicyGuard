import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"PDF parsing error: {e}")
        return ""

def extract_text_from_url(url):
    import requests
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.headers.get("content-type", "").startswith("application/pdf"):
            with open("temp.pdf", "wb") as f:
                f.write(response.content)
            text = extract_text_from_pdf("temp.pdf")
            os.remove("temp.pdf")
            return text
        else:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text()
    except Exception as e:
        print(f"URL extraction error: {e}")
        return ""
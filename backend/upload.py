from fastapi import APIRouter, UploadFile, File
import os
import pdfplumber
from vector_store import add_document

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # If PDF, extract text
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

        # Add to vector store
        add_document(text, doc_id=file.filename)

        return {
            "filename": file.filename,
            "status": "processed",
            "added_to_vector_store": True
        }
    
    return {
        "filename": file.filename,
        "status": "uploaded_only",
        "added_to_vector_store": False
    }

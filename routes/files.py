from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

# Importamos nuestros servicios
from services.pdf_service import PDFService
from services.vector_service import VectorService

router = APIRouter()
pdf_service = PDFService()
vector_service = VectorService()
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    
    temp_file_path=f"temp_{file.filename}"
    try:
        with open (temp_file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        print(f"Archivo '{file.filename}' subido correctamente.")
        chunks=pdf_service .process_pdf (temp_file_path)
        if not chunks:
            raise HTTPException(status_code=500, detail="Error al procesar el PDF.")
        vector_service.upload_chunks(chunks)
        return {"message":"Documento subido y procesado con éxito.", "total_chunks": len(chunks),"filename": file.filename}
    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        raise HTTPException (status_code=500, detail="Error al subir el archivo.")
    finally:
        file.file.close()
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
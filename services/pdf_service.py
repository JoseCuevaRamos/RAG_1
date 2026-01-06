import os
import tempfile
import shutil
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


class PDFService:
   """Service that processes PDFs from a file path into text chunks.

   This class uses LangChain's PyPDFLoader and a RecursiveCharacterTextSplitter
   to produce a list of document chunks (suitable for embeddings).
   """

   def __init__(self):
      self.text_splitter = RecursiveCharacterTextSplitter(
         chunk_size=1000,
         chunk_overlap=200,
         separators=["\n\n", "\n", " ", ""]
      )

   def process_pdf(self, file_path: str) -> List:
      """Load PDF from disk and split into chunks.

      Returns a list of LangChain Document-like objects. The caller is
      responsible for handling deletion of the file if desired.
      """
      try:
         loader = PyPDFLoader(file_path)
         documents = loader.load()
         chunks = self.text_splitter.split_documents(documents)
         print(f"PDF procesado. Total de chunks creados: {len(chunks)}")
         return chunks
      except Exception as e:
         print(f"Error al procesar el PDF: {e}")
         return []


def extract_text_and_chunks(upload_file) -> List:
   """Compatibility helper: accept a FastAPI UploadFile-like object,
   save it to a temporary file, process via PDFService and return chunks.

   This function preserves the previous expected API name so older imports
   (e.g. `from services.pdf_service import extract_text_and_chunks`) continue
   to work.
   """
   pdf_service = PDFService()
   # Create a temporary file on disk and write the uploaded content
   suffix = ".pdf"
   tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
   tmp_name = tmp.name
   try:
      # If upload_file is a Starlette/FastAPI UploadFile, it has .file
      if hasattr(upload_file, "file"):
         # copyfileobj expects binary
         upload_file.file.seek(0)
         shutil.copyfileobj(upload_file.file, tmp)
      else:
         # If caller passed a path-like string, just use it
         tmp.close()
         tmp_name = str(upload_file)
      tmp.close()

      chunks = pdf_service.process_pdf(tmp_name)
      return chunks
   finally:
      # Clean up temp file if it exists and was created here
      try:
         if os.path.exists(tmp_name):
            os.remove(tmp_name)
      except Exception:
         pass
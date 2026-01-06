from fastapi import FastAPI
from routes.files import router as files_router
from routes.chat import router as chat_router

app = FastAPI(title="Prueba de Ingesta RAG")

# Conectamos la ruta de subida y la ruta de chat
app.include_router(files_router, tags=["Archivos"])
app.include_router(chat_router, tags=["Chat"])

@app.get("/")
def read_root():
    return {"status": "Modo de prueba: Solo subida de archivos activo 📂"}
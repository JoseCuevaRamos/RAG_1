from qdrant_client import QdrantClient
from qdrant_client.http import models # Importamos modelos propios de Qdrant
from langchain_openai import OpenAIEmbeddings
from core.config import settings
import uuid

class VectorService:
    def __init__(self):
        # Inicializamos el cliente de Qdrant usando la configuración
        # Use getattr to avoid AttributeError if some settings are not present
        qdrant_url = getattr(settings, "QDRANT_URL", None)
        qdrant_api_key = getattr(settings, "QDRANT_API_KEY", None)
        if qdrant_url:
            # prefer URL if provided
            self.client = QdrantClient(url=str(qdrant_url), api_key=qdrant_api_key)
        else:
            qdrant_host = getattr(settings, "QDRANT_HOST", None)
            qdrant_port = getattr(settings, "QDRANT_PORT", None)
            if qdrant_host and qdrant_port:
                self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
            else:
                raise RuntimeError("Qdrant configuration not found in settings")
        self.collection_name = "documents"

        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=settings.OPENAI_API_KEY)

        self.create_collection_if_not_exists()
    def create_collection_if_not_exists(self):
        # Verificamos si la colección ya existe
        existing_collections = self.client.get_collections().collections
        if not any(col.name == self.collection_name for col in existing_collections):
            print(f"Creando colección '{self.collection_name}' en Qdrant...")
            # Definimos la configuración de la colección
            vector_size = 1536  # Tamaño del vector de OpenAI
            distance = models.Distance.COSINE  # Métrica de distancia
            # Creamos la colección en Qdrant
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=distance)
            )
    def upload_chunks(self,chunks):
        
        print("Generando embeddings y subiendo chunks a Qdrant...")
        texts=[chunk.page_content for chunk in chunks]
        metadata=[chunk.metadata for chunk in chunks]
        embeddings=self.embedding_model.embed_documents(texts)
        points = []
        for i , (text,vector , meta ) in enumerate (zip(texts,embeddings,metadata)):
            point_id = str(uuid.uuid4())
            point = models.PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": text,
                    "metadata": meta
                }
            )
            points.append(point)
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
            )
        print(f"Subidos {i + 1} de {len(chunks)} chunks.")
# RAG Backend

Este proyecto implementa un backend de Retrieval-Augmented Generation (RAG) usando FastAPI, Qdrant y OpenAI. Permite cargar documentos PDF y realizar preguntas, obteniendo respuestas generadas por IA basadas únicamente en la información de los documentos cargados.

## Características

- **Carga de documentos PDF**: Sube archivos PDF y almacena sus fragmentos en una base vectorial (Qdrant).
- **Búsqueda semántica**: Convierte preguntas en vectores y recupera los fragmentos más relevantes.
- **Generación de respuestas**: Usa OpenAI para responder preguntas usando solo el contexto recuperado.
- **Citación de fuentes**: Devuelve las fuentes (documentos) utilizadas para cada respuesta.

## Endpoints principales

- `POST /upload`: Sube un documento PDF.
		- Formato: multipart/form-data, campo `file`.
		- Respuesta: confirmación de carga.

- `POST /chat`: Realiza una pregunta sobre los documentos cargados.
		- Formato: JSON, campo `question`.
		- Respuesta: respuesta generada y lista de fuentes utilizadas.

## Estructura del proyecto

- `core/config.py`: Configuración y variables de entorno.
- `models/schemas.py`: Modelos Pydantic para requests y responses.
- `services/`: Lógica de negocio (PDF, vectores, RAG).
- `routes/`: Rutas de la API (carga y chat).
- `main.py`: Inicialización de FastAPI y registro de rutas.
- `Dockerfile` y `docker-compose.yml`: Despliegue con Docker.

## Ejemplo de uso

1. Sube un PDF con `/upload`.
2. Haz una pregunta con `/chat`:
		```json
		{
			"question": "¿Qué conclusiones se obtuvieron en la segunda reunión?"
		}
		```
3. Recibe una respuesta y las fuentes utilizadas:
		```json
		{
			"answer": "La segunda reunión se centró en...",
			"sources": ["documento1.pdf", "documento2.pdf"]
		}
		```

## Requisitos

- Python 3.10+
- Docker y Docker Compose
- Claves de API de OpenAI y configuración de Qdrant

## Despliegue

```bash
docker-compose build
docker-compose up
```
# RAG_1
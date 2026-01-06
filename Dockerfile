# Usamos Python 3.10 version ligera
FROM python:3.10-slim

# Configuraciones de Python para Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos e instalamos las librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos
COPY . .

# Exponemos el puerto
EXPOSE 8000

# Comando de arranque (aunque el docker-compose lo sobrescribirá con --reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
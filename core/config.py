# Importamos de la sub-librería específica
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CHAT_MODEL: str = "gpt-4o-mini"
    
    # --- AGREGA ESTO PARA QUE FUNCIONE LA BASE DE DATOS ---
    QDRANT_HOST: str = "qdrant" # El nombre del servicio en Docker
    QDRANT_PORT: int = 6333
    
    class Config:
        env_file = ".env"

# Instanciamos la clase para usarla
settings = Settings()
from functools import lru_cache


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Some modules import `get_settings` while others import the `settings`
    instance directly. Provide both to remain backwards compatible.
    """
    return settings
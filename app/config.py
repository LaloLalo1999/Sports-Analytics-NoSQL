from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "sports_analytics"
    
    # Cassandra
    CASSANDRA_HOSTS: str = "localhost"
    CASSANDRA_KEYSPACE: str = "sports_analytics"
    
    # Dgraph
    DGRAPH_HOSTS: str = "localhost:9080"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 
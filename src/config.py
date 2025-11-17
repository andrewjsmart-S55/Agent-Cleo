"""
Configuration settings for Agent-Cleo
Combines Studio55IQ RAG capabilities with Agent orchestration
"""
from pydantic_settings import BaseSettings
from typing import Optional, List, Union
import os
import json


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Agent-Cleo"
    app_version: str = "2.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 5000

    # Database
    database_url: str = "sqlite:///./agents.db"

    # Studio55IQ RAG Engine Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_search_results: int = 10
    similarity_threshold: float = 0.7

    # ChromaDB
    chroma_db_path: str = "./chroma_db"

    # Ollama (fallback for local testing)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    ollama_embedding_model: str = "nomic-embed-text"

    # Overlord Platform Integration
    overlord_api_url: str = os.getenv("OVERLORD_API_URL", "http://localhost:3000/api/v1")
    overlord_api_key: Optional[str] = os.getenv("OVERLORD_API_KEY")

    # Todoist Integration
    todoist_api_token: Optional[str] = os.getenv("TODOIST_API_TOKEN")

    # Agent System
    base_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uploads_dir: str = "./uploads"
    logs_dir: str = "./logs"

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    _cors_origins_str: str = os.getenv("CORS_ORIGINS", "")

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from environment or use defaults"""
        if self._cors_origins_str:
            try:
                # Try parsing as JSON array first
                return json.loads(self._cors_origins_str)
            except json.JSONDecodeError:
                # Fall back to comma-separated string
                return [origin.strip() for origin in self._cors_origins_str.split(",") if origin.strip()]
        return ["http://localhost:3000", "http://localhost:5000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

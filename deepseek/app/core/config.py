from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "DeepSeek API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for DeepSeek language model inference"
    MODEL_NAME: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    MAX_MODEL_LEN: int = 32768
    MAX_BATCH_SIZE: int = 4
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
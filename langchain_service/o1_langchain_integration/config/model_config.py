from pydantic import BaseSettings
from typing import Optional

class O1ModelConfig(BaseSettings):
    model_path: str
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    timeout: int = 300
    
    class Config:
        env_file = ".env"

model_config = O1ModelConfig()

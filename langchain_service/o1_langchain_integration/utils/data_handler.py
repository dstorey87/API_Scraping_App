from pathlib import Path
from typing import Union, List
import json

class DataHandler:
    @staticmethod
    def read_file(file_path: Union[str, Path]) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.read_text(encoding='utf-8')
    
    @staticmethod
    def write_file(file_path: Union[str, Path], content: str) -> None:
        path = Path(file_path)
        path.write_text(content, encoding='utf-8')
    
    @staticmethod
    def load_json(file_path: Union[str, Path]) -> dict:
        return json.loads(DataHandler.read_file(file_path))

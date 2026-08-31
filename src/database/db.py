import importlib
from importlib.metadata.diagnose import inspect

from fastapi import Path
from pymongo import AsyncMongoClient
from config import MONGO_URI
from beanie import Document, init_beanie
from redis import Redis

def get_beanie_models():
    models = []
    models_path = Path("src/models")

    for file in models_path.glob("*.py"):
        if file.name.startswith("_"):
            continue

        module = importlib.import_module(
            f"src.models.{file.stem}"
        )

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(cls, Document)
                and cls is not Document
                and cls.__module__ == module.__name__
            ):
                models.append(cls)
    return models

class DBManager:
    def __init__(self, db_name:str = "ProjetoAcademico"):
        self.client =  AsyncMongoClient(host = MONGO_URI)
        init_beanie(self.client[db_name], document_models = get_beanie_models())
        
    
    def close(self):
        self.client.close()
        print("conexão com banco fechada")
    

    
        
        
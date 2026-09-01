from pathlib import Path
import importlib
import inspect

from pymongo import AsyncMongoClient
from config import MONGO_URI, REDIS_URL
from beanie import Document, init_beanie
from redis import Redis
from redis_om import get_redis_connection

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
    @classmethod
    def start_mongo(cls, db_name:str = "ProjAcademico"):
        cls.db_name = db_name
        cls.mongo_client =  AsyncMongoClient(host = MONGO_URI)
        print(f"Conectado ao mongoDB -> DB: {cls.db_name}")

    @classmethod
    async def config_beanie(cls):
        db = cls.mongo_client[cls.db_name]
        await init_beanie(db, document_models = get_beanie_models())
        print("beanie configurado")
        
    @classmethod
    def start_redis(cls):
        cls.redis_client = get_redis_connection(url=REDIS_URL)
        print("Conectado ao redis")

        
    @classmethod
    async def close(cls):
        await cls.mongo_client.close()
        cls.redis_client.close()
        
    

    
        
        
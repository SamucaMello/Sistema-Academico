from pathlib import Path
import importlib
import inspect

from config import MONGO_URI, REDIS_URL, APPConfig

import redis_om
from redis_om import get_redis_connection


from pymongo import AsyncMongoClient

from beanie import Document, init_beanie
from redis import Redis


import redis 

from os import environ, getenv
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
    async def start_mongo(cls, db_name:str = "ProjAcademico"):
        cls.db_name = db_name
        cls.mongo_client =  AsyncMongoClient(host = MONGO_URI)
        try:
            await cls.mongo_client.admin.command('ping')
            print(f"Conectado ao mongoDB -> DB: {cls.db_name}")
        except Exception as ex:
            print(f"Algo deu errado -> {ex}")

    @classmethod
    async def config_beanie(cls):
        db = cls.mongo_client[cls.db_name]
        await init_beanie(db, document_models = get_beanie_models())
        print("beanie configurado")
        
    @classmethod
    def start_redis(cls):
        environ["REDIS_OM_URL"]  = REDIS_URL
         #cls.redis_client        = get_redis_connection(host = getenv("REDIS_HOST"), port = "REDIS_PORT",  decode_responses=True)     environ["REDIS_OM_URL"] = REDIS_URL
        cls.redis_client        = get_redis_connection(url=REDIS_URL, decode_responses=True)
        redis.Redis = cls.redis_client
        redis_om.redis          = cls.redis_client
        print(f"Conectado ao redis -> {REDIS_URL}")

        
    @classmethod
    async def close(cls):
        await cls.mongo_client.close()
        cls.redis_client.close()
        
    

    
        
        
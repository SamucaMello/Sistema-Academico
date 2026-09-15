from os import environ, getenv
import sys
from typing import Literal, Union

class APPConfig:
    @staticmethod
    def is_dev() -> bool:
        return "--dev" in sys.argv

    @classmethod
    def get_mongo_uri(cls) -> str:
        db_host         = getenv("DB_HOST", "mongodb")
        db_port         = getenv("DB_PORT", "27071")
        db_name         = getenv("DB_NAME", "")
        db_user         = getenv("DB_USER", "")
        db_password     = getenv("DB_PASSWORD", "")

        if cls.is_dev():
            db_host = "localhost"
        
        auth            = f"{db_user}:{db_password}@" if db_user and db_password else ""
        database        = f"/{db_name}" if db_name else ""

        return f"mongodb://{auth}{db_host}:{db_port}{database}"

    @classmethod
    def get_redis_uri(cls) -> str: # type: ignore
        redis_host      = getenv("REDIS_HOST", "redis")
        redis_port      = getenv("REDIS_PORT", "6379")
        redis_password  = getenv("REDIS_PASSWORD", "")

        if cls.is_dev():
            redis_host = "localhost"

        
        
        redis_auth      = f":{redis_password}@" if redis_password else ""


        URL =  f"redis://{redis_auth}{redis_host}:{redis_port}"

        environ["REDIS_OM_URL"] = URL

        return URL


        

    @staticmethod
    def get_port() -> int:
        return int(getenv("PORT", 8000))




MONGO_URI   = APPConfig.get_mongo_uri()
REDIS_URL   = APPConfig.get_redis_uri()
PORT        = APPConfig.get_port()

print(MONGO_URI, REDIS_URL, PORT)
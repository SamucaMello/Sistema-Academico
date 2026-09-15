from typing import Type

from redis import Redis
from redis_om import HashModel
from beanie import Document, PydanticObjectId

class DatabaseService:
    EXPIRES_IN = 60
    def __init__(self, redis_schema:Type[HashModel], mongo_schema:Type[Document]):
        self.redis_schema = redis_schema
        self.mongo_schema = mongo_schema

    def redis_save(self, document:Document):
        data = document.model_dump(mode="json")
        data["id"] = str(document.id)
        for key, value in data.items():
            if isinstance(value, dict) and "id" in value:
                data[key] = str(value["id"])
        
        self.redis_schema(**data).save().expire(self.EXPIRES_IN)
        

    def redis_get(self, id:PydanticObjectId):
        try: 
            return self.redis_schema.find(
                  self.redis_schema.id == str(id)
                    ).first()
        except Exception:
                return None

    def redis_delete(self, id:PydanticObjectId):
         if data := self.redis_get(id):
              data.delete()

    async def mongo_get(self, id:PydanticObjectId):
         return await self.mongo_schema.get(id, fetch_links=True)


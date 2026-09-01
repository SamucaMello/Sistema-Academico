
from pydantic import BaseModel, EmailStr


class CreateAlunoSchema(BaseModel):
    RA:str
    nome:str
    email:EmailStr
    curso:str 
    semestre:int 

class UpdateAlunoSchema(BaseModel):
    nome:str
    email:EmailStr
    curso:str 
    semestre:int 



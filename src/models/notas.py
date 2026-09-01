from beanie import Document


class Notas(Document):
    P1: float   
    P2: float 
    media: float       # (P1 + P2) / 2
    situacao:str       # consult. NotasEnum
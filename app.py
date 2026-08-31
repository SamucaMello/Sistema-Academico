import uvicorn 
from fastapi import FastAPI
from config import PORT

app = FastAPI(
    title = "API Projeto acadêmico",
)



if __name__ == "__main__":
    print(f"APP rodando na porta {PORT}")
    uvicorn.run(app, port = PORT)
    
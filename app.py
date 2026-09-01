from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
import uvicorn 
from fastapi import FastAPI, Request
from config import PORT
from src.exceptions.base_exception import BaseAppException
from src.routes.aluno_route import aluno_router
from src.database.db import DBManager


@asynccontextmanager
async def lifespan(app:FastAPI):
    DBManager.start_mongo()
    await DBManager.config_beanie()
    DBManager.start_redis()
    
    yield
    await DBManager.close()

app = FastAPI(
    title = "API Projeto acadêmico",
    lifespan=lifespan
)

@app.get("/") 
def main(): return {"message": "oi"}


app.include_router(aluno_router)


@app.exception_handler(BaseAppException)
async def exception_handler(request:Request, exc:BaseAppException):
    return JSONResponse(status_code = exc.status_code, content={"message":str(exc)})

@app.exception_handler(Exception)
async def exception_handler(request:Request, exc:Exception):
    return JSONResponse(status_code=500, content= {"message":"Algo deu errado, tente novamente mais tarde."})





if __name__ == "__main__":
    print(f"APP rodando na porta {PORT}")
    print("oi")
    uvicorn.run("app:app", host="0.0.0.0",  port=PORT, reload=True)
    
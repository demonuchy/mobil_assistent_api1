import jwt
import uvicorn
from fastapi import FastAPI, Request
from db_manager import engine
from acces_token import verefy_token
from middleware import VerefySessionMiddleware
from route import private_router, public_router
from logger import logger


app = FastAPI()


@app.on_event("startup")
async def startup():
    await engine.create_all_table()
    logger.info("__START__")


@app.on_event("shutdown")
async def shutdown():
    await engine.delete_all_table()
    logger.info("__CLOSE__")


if __name__ == "__main__":
    app.add_middleware(VerefySessionMiddleware)
    app.include_router(public_router)
    app.include_router(private_router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
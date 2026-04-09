from fastapi import FastAPI
from user.router_1 import router

app = FastAPI()
app.include_router(router)

from fastapi import FastAPI
from src.api.routes import upload_route

app = FastAPI()
app.include_router(upload_route.router)

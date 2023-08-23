from fastapi import FastAPI
from app.routes import Upload_Route

app = FastAPI()
app.include_router(Upload_Route.router)

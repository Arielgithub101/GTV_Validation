from fastapi import FastAPI
from app.routes import ExcelFix_Route

app = FastAPI()
app.include_router(ExcelFix_Route.router)

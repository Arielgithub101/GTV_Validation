import uvicorn
from src.config import Config

if __name__ == "__main__":
    uvicorn.run("src.api.service:app", host=Config.HOST, port=Config.PORT, reload=True)

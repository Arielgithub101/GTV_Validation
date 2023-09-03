import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.service:src", host="0.0.0.0", port=9900, reload=True)

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def first_func():
	return {"message": "Hello World!!!!!"}


if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
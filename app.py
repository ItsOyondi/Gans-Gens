from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Define a simple GET route
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Define a GET route with a parameter
@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}


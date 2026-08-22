from fastapi import FastAPI

app = FastAPI(title="ParkSpot API")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/location")
async def get_location(lat: float, lon: float):
    return {"latitude": lat, "longitude": lon}


app.mount("/", StaticFiles(directory="static", html=True), name="static")

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import requests
from pprint import pprint

from config import api_key

# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=61.78491&lon=34.34691&appid={api_key}")
# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=35.6839&lon=139.7744&appid={api_key}")


app = FastAPI(
    title="Weather Collector",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="0.1",
    description=""
)


@app.on_event("startup")
async def apply_migrations():
    print("hello 1")


@app.on_event("startup")
async def start_monitoring():
    print("hello 2")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")



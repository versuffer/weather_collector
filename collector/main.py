from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from services.database import DatabaseTools

app = FastAPI(
    title="Weather Collector",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="0.1",
    description="",
)


@app.on_event("startup")
async def init_db():
    await DatabaseTools.init_db()


@app.on_event("startup")
async def load_cities():
    await DatabaseTools.load_cities()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

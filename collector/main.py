from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from pprint import pprint

from config import api_key
from database import Base, engine

# import requests
# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=61.78491&lon=34.34691&appid={api_key}")
# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=35.6839&lon=139.7744&appid={api_key}")

from worker import print_hello

import csv

from database import Session, City, engine

from sqlalchemy.dialects.postgresql import insert

app = FastAPI(
    title="Weather Collector",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="0.1",
    description=""
)


@app.on_event("startup")
def apply_migrations():
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def load_cities():
    with open("cities.csv", "r") as cities_csv:
        reader = csv.reader(cities_csv, delimiter=";")
        with Session() as session:
            cities_table = Base.metadata.tables[City.__tablename__]
            row_number = 0
            for row in reader:
                if row_number > 0:
                    insert_city = insert(
                        cities_table
                    ).values(
                        name=row[0],
                        lat=float(row[1]),
                        lon=float(row[2]),
                        country=row[3]
                    ).on_conflict_do_update(
                        constraint=City.__table_args__[0],
                        set_={
                            "name": row[0],
                            "lat": float(row[1]),
                            "lon": float(row[2]),
                            "country": row[3],
                        }
                    )
                    session.execute(insert_city)
                row_number += 1

            session.commit()
            print("Cities table successfully loaded to database.")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/hello", status_code=201)
async def hello():
    task = print_hello.delay()
    return {"message": "hello", "task": task.id}

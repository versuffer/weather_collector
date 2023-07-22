from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from services.database import Base

import csv

from services.database import Session, City, engine

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
    with open("data/cities.csv", "r") as cities_csv:
        reader = csv.reader(cities_csv, delimiter=";")
        cities_table = Base.metadata.tables[City.__tablename__]
        with Session() as session:
            row_number = 0
            for row in reader:
                if row_number > 0:
                    values = {
                        "name": row[0],
                        "lat": float(row[1]),
                        "lon": float(row[2]),
                        "country": row[3],
                    }

                    insert_city = insert(
                        cities_table
                    ).values(
                        name=values.get("name"),
                        lat=values.get("lat"),
                        lon=values.get("lon"),
                        country=values.get("country")
                    ).on_conflict_do_update(
                        constraint=City.__table_args__[0],
                        set_=values
                    )
                    session.execute(insert_city)
                row_number += 1

            session.commit()
            print("Cities table successfully loaded to database.")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


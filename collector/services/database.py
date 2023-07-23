import csv
import os

from models.database import Base, City, Forecast, Measurement
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(os.environ.get("DATABASE_URL"))
async_session = async_sessionmaker(bind=engine)


class DatabaseTools:
    @staticmethod
    async def init_db() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def load_cities() -> None:
        with open("data/cities.csv", "r") as cities_csv:
            reader = csv.reader(cities_csv, delimiter=";")
            cities_table = Base.metadata.tables[City.__tablename__]
            async with async_session() as session:
                row_number = 0
                for row in reader:
                    if row_number > 0:
                        values = {
                            "name": row[0],
                            "lat": float(row[1]),
                            "lon": float(row[2]),
                            "country": row[3],
                        }

                        insert_city = (
                            insert(cities_table)
                            .values(
                                name=values.get("name"),
                                lat=values.get("lat"),
                                lon=values.get("lon"),
                                country=values.get("country"),
                            )
                            .on_conflict_do_update(
                                constraint=City.__table_args__[0], set_=values
                            )
                        )
                        await session.execute(insert_city)
                    row_number += 1

                await session.commit()
                print("Cities table successfully loaded to database.")

    @staticmethod
    async def get_city_credentials() -> list:
        async with async_session() as session:
            cities_table = Base.metadata.tables[City.__tablename__]
            select_lat_lon = select(
                cities_table.c.id, cities_table.c.lat, cities_table.c.lon
            )
            result = await session.execute(select_lat_lon)
            return result.fetchall()

    @staticmethod
    async def save_weather_data(
        forecasts: list[Forecast], measurements: list[Measurement]
    ) -> None:
        async with async_session() as session:
            session.add_all(forecasts)
            session.add_all(measurements)
            await session.commit()

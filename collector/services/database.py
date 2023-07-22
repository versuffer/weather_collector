import csv
import os
from datetime import datetime

from sqlalchemy import UniqueConstraint, create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.sql import func

engine = create_engine(os.environ.get("DATABASE_URL"))

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("lat", "lon", name="unique_location"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=True)

    forecasts: Mapped[list["Forecast"]] = relationship(back_populates="city")


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    time_fetched: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    city: Mapped["City"] = relationship(back_populates="forecasts")
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="forecast")


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    time_measured: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=True)
    humidity: Mapped[float] = mapped_column(nullable=True)
    wind_speed: Mapped[float] = mapped_column(nullable=True)

    forecast: Mapped["Forecast"] = relationship(back_populates="measurements")


class DatabaseTools:
    @staticmethod
    def load_schema():
        Base.metadata.create_all(bind=engine)

    @staticmethod
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
                        session.execute(insert_city)
                    row_number += 1

                session.commit()
                print("Cities table successfully loaded to database.")

    @staticmethod
    def get_coordinates() -> list[tuple[float, float]]:
        with Session() as session:
            cities_table = Base.metadata.tables[City.__tablename__]
            select_lat_lon = select(cities_table.c.lat, cities_table.c.lon)
            return session.execute(select_lat_lon)

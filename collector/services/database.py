import csv
import os
from datetime import datetime

from services.parsing import ParsingTools
from sqlalchemy import UniqueConstraint, create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.sql import func

engine = create_engine(os.environ.get("DATABASE_URL"))

Session = sessionmaker(bind=engine)


from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("lat", "lon", name="unique_location"),)

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)

    forecasts = relationship("Forecast", back_populates="city")


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True)
    time_fetched = Column(DateTime, nullable=False, server_default=func.now())

    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="forecasts")

    measurements = relationship("Measurement", back_populates="forecast")


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)
    time_measured = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)

    forecast_id = Column(Integer, ForeignKey("forecasts.id"))
    forecast = relationship("Forecast", back_populates="measurements")


class DatabaseTools:
    @staticmethod
    def load_schema() -> None:
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def load_cities() -> None:
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
    def get_city_credentials() -> list:
        with Session() as session:
            cities_table = Base.metadata.tables[City.__tablename__]
            select_lat_lon = select(
                cities_table.c.id, cities_table.c.lat, cities_table.c.lon
            )
            return session.execute(select_lat_lon).fetchall()

    @staticmethod
    def load_weather_data(result_dict: dict) -> None:
        with Session() as session:
            for city_credentials, result in result_dict.items():
                if result and (measurements_list := result.get("list")):
                    msr_objects = []

                    forecast_object = Forecast(city_id=city_credentials[0])

                    for measurement in measurements_list:
                        msr_object = Measurement(
                            time_measured=datetime.fromtimestamp(measurement.get("dt")),
                            temperature=ParsingTools.get_single_match_value(
                                measurement, "$.main.temp"
                            ),
                            humidity=ParsingTools.get_single_match_value(
                                measurement, "$.main.humidity"
                            ),
                            wind_speed=ParsingTools.get_single_match_value(
                                measurement, "$.wind.speed"
                            ),
                            forecast=forecast_object,
                        )
                        msr_objects.append(msr_object)

                    session.add(forecast_object)
                    session.add_all(msr_objects)

            session.commit()

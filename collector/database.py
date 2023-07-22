from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float

from sqlalchemy import ForeignKey

from config import DATABASE_URL

from datetime import datetime

from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

import os

engine = create_engine(os.environ.get("DATABASE_URL"))

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (
        UniqueConstraint("lat", "lon", name="unique_location"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=True)

    forecasts: Mapped[list["Forecast"]] = relationship(back_populates="city")


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    time_fetched: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

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




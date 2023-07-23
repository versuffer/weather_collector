from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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

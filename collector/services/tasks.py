import asyncio
import os

import aiohttp
from celery import Celery
from celery.signals import worker_ready
from config import Config
from services.database import DatabaseTools
from services.parsing import ParsingTools

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.beat_schedule = Config.BEAT_SCHEDULE


async def fetch_forecast(
    session: aiohttp.ClientSession, lat: float, lon: float, api_key: str
) -> dict | None:
    async with session.get(
        url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    ) as response:
        if response.ok:
            try:
                return await response.json()
            except:
                pass


async def weather_collector():
    # Asynchronously fetching weather data from api.openweathermap.org
    async with aiohttp.ClientSession() as session:
        coroutine_list = []
        city_credentials = await DatabaseTools.get_city_credentials()
        for _, lat, lon in city_credentials:
            coroutine_list.append(fetch_forecast(session, lat, lon, Config.API_KEY))

        result_list = await asyncio.gather(*coroutine_list)

    result_dict = {
        city_credentials[index]: result_list[index]
        for index in range(len(city_credentials))
    }

    # Parsing weather data
    forecasts, measurements = ParsingTools.parse_weather_data(result_dict)

    # Saving weather data to database
    await DatabaseTools.save_weather_data(forecasts, measurements)


@celery_app.task(name="fetch_forecasts", ignore_result=True)
def fetch_forecasts():
    asyncio.get_event_loop().run_until_complete(weather_collector())


@worker_ready.connect
def fetch_forecasts_on_startup(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("fetch_forecasts")

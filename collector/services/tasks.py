from celery import Celery
import os
from config import BEAT_SCHEDULE, API_KEY
import aiohttp
import asyncio

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.beat_schedule = BEAT_SCHEDULE


async def get_forecast(session: aiohttp.ClientSession, lat: float, lon: float, api_key: str) -> dict | None:
    async with session.get(
        url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    ) as response:
        if response.ok:
            try:
                return await response.json()
            except:
                pass


async def weather_collector():
    coordinates_list = [(35.6897, 139.6922), (-6.175, 106.8275), (28.61, 77.23)]
    coroutine_list = []

    async with aiohttp.ClientSession() as session:
        for lat, lon in coordinates_list:
            coroutine_list.append(get_forecast(session, lat, lon, API_KEY))

        result = await asyncio.gather(*coroutine_list)
        from pprint import pprint
        pprint(result)


@celery_app.task(name="fetch_forecasts", ignore_result=True)
def fetch_forecasts():
    asyncio.run(weather_collector())

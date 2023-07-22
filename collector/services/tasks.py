import asyncio
import os

import aiohttp
from celery import Celery
from celery.signals import worker_ready
from config import API_KEY, BEAT_SCHEDULE
from services.database import DatabaseTools

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.beat_schedule = BEAT_SCHEDULE


async def get_forecast(
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
    async with aiohttp.ClientSession() as session:
        coroutine_list = []
        for lat, lon in DatabaseTools.get_coordinates():
            coroutine_list.append(get_forecast(session, lat, lon, API_KEY))

        result_list = await asyncio.gather(*coroutine_list)
        for result in result_list:
            print(result.get("list"))


@celery_app.task(name="fetch_forecasts", ignore_result=True)
def fetch_forecasts():
    asyncio.run(weather_collector())


@worker_ready.connect
def startup_execution(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("fetch_forecasts")

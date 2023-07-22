import aiohttp
import asyncio

# import requests
# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=61.78491&lon=34.34691&appid={api_key}")
# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=35.6839&lon=139.7744&appid={api_key}")


async def get_forecast(session: aiohttp.ClientSession, lat: float, lon: float, api_key: str) -> dict | None:
    async with session.get(
        url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    ) as response:
        if response.ok:
            try:
                return await response.json()
            except:
                pass


# Tokyo;35.6897;139.6922;Japan
# Jakarta;-6.175;106.8275;Indonesia
# Delhi;28.61;77.23;India

api_key = "8953fa20886f5d3fb215133460b97586"
coordinates_list = [(35.6897, 139.6922), (-6.175, 106.8275), (28.61, 77.23)]
coroutine_list = []


async def main():
    async with aiohttp.ClientSession() as session:
        for lat, lon in coordinates_list:
            coroutine_list.append(get_forecast(session, lat, lon, api_key))

        result = await asyncio.gather(*coroutine_list)
        from pprint import pprint
        pprint(result)

if __name__ == "__main__":
    asyncio.run(main())

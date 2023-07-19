from fastapi import FastAPI
import requests
from pprint import pprint

from config import api_key

# response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=61.78491&lon=34.34691&appid={api_key}")
response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?lat=35.6839&lon=139.7744&appid={api_key}")

data = response.json()

pprint(data)
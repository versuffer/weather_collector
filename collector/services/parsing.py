from datetime import datetime

from models.database import Forecast, Measurement


class ParsingTools:
    @staticmethod
    def parse_weather_data(
        result_dict: dict,
    ) -> tuple[list[Forecast], list[Measurement]]:
        forecasts_list = []
        measurements_list = []

        for city_credentials, result in result_dict.items():
            if result and (measurements := result.get("list")):
                forecast_object = Forecast(city_id=city_credentials[0])

                for measurement in measurements:
                    time_measured = None
                    temperature = None
                    humidity = None
                    wind_speed = None

                    if dt := measurement.get("dt"):
                        time_measured = datetime.fromtimestamp(dt)

                    if main := measurement.get("main"):
                        temperature = main.get("temp")
                        humidity = main.get("humidity")

                    if wind := measurement.get("wind"):
                        wind_speed = wind.get("speed")

                    msr_object = Measurement(
                        time_measured=time_measured,
                        temperature=temperature,
                        humidity=humidity,
                        wind_speed=wind_speed,
                        forecast=forecast_object,
                    )
                    measurements_list.append(msr_object)
                forecasts_list.append(forecast_object)

        return forecasts_list, measurements_list

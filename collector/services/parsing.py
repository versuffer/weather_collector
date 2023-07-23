from datetime import datetime

from jsonpath_ng import parse
from models.database import Forecast, Measurement


class ParsingTools:
    @staticmethod
    def _get_match_list(data: dict, expression: str) -> list | None:
        parser = parse(expression)
        if (match_list := parser.find(data)) != []:
            return match_list

    @classmethod
    def get_single_match_value(
        cls, data: dict, expression: str
    ) -> int | float | str | list | dict | None:
        if match_list := cls._get_match_list(data, expression):
            return match_list[0].value

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
                    measurements_list.append(msr_object)
                forecasts_list.append(forecast_object)

        return forecasts_list, measurements_list

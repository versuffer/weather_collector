from jsonpath_ng import parse


class ParsingTools:
    @staticmethod
    def _get_match_list(data: dict, expression: str) -> list | None:
        parser = parse(expression)
        if (match_list := parser.find(data)) != []:
            return match_list

    @classmethod
    def get_single_match_value(
        cls, data: dict, expression: str
    ) -> int | str | list | dict | None:
        if match_list := cls._get_match_list(data, expression):
            return match_list[0].value

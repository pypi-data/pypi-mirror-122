from typing import Any, List


class Test:
    def __init__(self, data: dict) -> None:
        self.__query = data["query"]
        self.__fields = data["bindings"]
        self.__rows = data["rows"]
        self.__results = data["results"]
        self.__skip = data["skip"]
        self.__description = data["description"]
        pass
    def get_query(self) -> str:
        return self.__query

    def get_expected_number_of_rows(self) -> int:
        return self.__results
    
    def get_expected_rows(self) -> List[dict[str, Any]]:
        return self.__rows

    def get_expected_bindings(self) -> dict[str, Any]:
        return self.__fields
    
    def get_description(self) -> str:
        return self.__description
    
    def to_run(self) -> bool:
        return self.__skip is not True

from typing import List
from kgdd.test import Test


class TestFile:
    def __init__(self, data : dict) -> None:
        test_items = []
        for test in data["tests"]:
            test_items.append(Test(test))
        
        self.__test_items = test_items
        pass

    def get_tests(self) -> List[Test] :
        try:
            return self.__test_items
        except:
            raise Exception("No more test to run")
    
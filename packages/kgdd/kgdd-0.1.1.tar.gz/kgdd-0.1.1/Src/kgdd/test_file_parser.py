import json

from kgdd.test_file import TestFile

class TestFileParser:
    def __init__(self) -> None:
        pass
    
    def parse(self, path: str):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                f.close()
                return TestFile(data)
        except IOError:
            raise IOError(f"error opening {path}")




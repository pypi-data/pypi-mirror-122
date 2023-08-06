from rdflib import Graph
from rdflib.query import Result


class SparqlQueryResult:
    def __init__(self, qres: Result) -> None:
        self.__qres = qres
        pass
  
    def get_results_count(self) -> int:
        return len(self.__qres)

    def get_rows(self):
        return self.__qres

class KGReader:

    def __init__(self) -> None:
        pass

    def read_kg(self, path: str) -> None :
        g = Graph()
        g.parse(path)
        self.__graph = g 
        pass

    def run_query(self, query: str):
        if not self.__graph:
            raise Exception("No graph open to be queried") 
        qres = self.__graph.query(query)
        return SparqlQueryResult(qres)
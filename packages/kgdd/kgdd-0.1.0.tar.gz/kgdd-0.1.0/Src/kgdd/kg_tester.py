from typing import Any, List
from kgdd.kg_reader import KGReader, SparqlQueryResult
from kgdd.logger import Logger
from kgdd.test import Test
from kgdd.test_file import TestFile
from kgdd.test_file_parser import TestFileParser

class KGTester:

    def __init__(self, kg_reader : KGReader, logger: Logger, test_file_parser: TestFileParser):
        self.__kg_reader = kg_reader
        self.__logger = logger
        self.__test_file_parser = test_file_parser
        self._test_counter = 0
        self.__test_passed = 0
        self.__test_failed = 0

    def run_tests(self, graph_path, test_path):

        self.__logger.log_space()
        self.__logger.log_text(f"* * * * * * *  * * * ")
        self.__logger.log_text(f" * * * KGT run * * * ")
        self.__logger.log_text(f"* * * * * * *  * * * ")
        self.__logger.log_space()

        self.__logger.log_message(f"reading testbed {test_path}")
        try:
            test_file : TestFile = self.__test_file_parser.parse(test_path)

        except Exception:
            self.__logger.log_program_error(f"failed reading testbed {test_path}")


        self.__logger.log_message(f"parsing KG {graph_path}")
        try:
            self.__kg_reader.read_kg(graph_path)
        
        except Exception:
            self.__logger.log_program_error(f"failed reading grapg {graph_path}")

        for test in test_file.get_tests():
            self.__logger.log_space()
            self._test_counter += 1
            if test.to_run():
                self.__logger.log_message(f"Running Test {self._test_counter}: {test.get_description()}")
                self.run_test(test)
            else:
                self.__logger.log_skip(f"SKIPPED: {test.get_description()}")

        self.__logger.log_space()
        self.__logger.log_message(f"Testbed complete. Passed {self.__test_passed} Failed {self.__test_failed}")

        if  self.__test_failed == 0:
            self.__logger.log_correct(f"All test passed! :-)")
        else:
            self.__logger.log_error(f"Some test failed... :-(")

    def run_test(self, test : Test):


        results = self.__kg_reader.run_query(test.get_query())

        if self.has_value(test.get_expected_number_of_rows()):
            self.check_expected_number_of_rows(results, test.get_expected_number_of_rows())

        if self.has_value(test.get_expected_bindings()):
            self.check_expected_bindings(results, test.get_expected_bindings())
        
        if self.has_value(test.get_expected_rows()):
            self.check_expected_rows(results, test.get_expected_rows())



    def check_expected_number_of_rows(self, results: SparqlQueryResult, number_of_rows: int):

        if number_of_rows == -1:
            try:            
                assert results.get_results_count() > 0
                self.__logger.log_correct(f"\tTest passed: rows count {results.get_results_count()} greater than 0")
                self.add_test_passed()
                return
            except:
                self.__logger.log_error(f"\tTest failed: rows found 0")
                return            

        try:
            assert results.get_results_count() == number_of_rows
            self.__logger.log_correct(f"\tTest passed: expected rows count correct {number_of_rows}")
            self.add_test_passed()
        except:
            self.__logger.log_error(f"\tTest failed: expected number of rows {number_of_rows} found {results.get_results_count()}")
            self.add_test_failed()

        pass


    def check_expected_bindings(self, results: SparqlQueryResult, expected_bindings: dict[str, Any]):

        rows = results.get_rows()

        binding_check_results = {}


        for row in rows:
            for variable_name in expected_bindings.keys():

                try:

                    self.__logger.verbose_debug(f"Test matching {row[variable_name]} type {type(row[variable_name])} {expected_bindings[variable_name]} type {type(expected_bindings[variable_name])} with variable {variable_name}")


                    if str(row[variable_name]) == expected_bindings[variable_name]:

                        self.__logger.debug(f"Found binding match for variable {variable_name} expected {expected_bindings[variable_name]} found {row[variable_name]}")
                        binding_check_results[variable_name] = expected_bindings[variable_name]


                except Exception:
                    self.__logger.verbose_debug(f"binding not found for variable {variable_name} in row ${row}")

        try:
            assert binding_check_results.keys() == expected_bindings.keys()
            self.__logger.log_correct(f"\tTest passed: expected bindings are correct {expected_bindings}")
            self.add_test_passed()
        except:
            self.__logger.log_error(f"\tTest failed: expected bindings {expected_bindings} found bindings {binding_check_results}")
            self.add_test_failed()


    def check_expected_rows(self, results: SparqlQueryResult, expected_rows: List[dict[str, Any]]):

        rows = results.get_rows()

        expected_row_results = []

        for row in rows:
            for expected_row in expected_rows:
                variables = expected_row.keys()
                try:
                    # we want all the bindings of expected row the same as found row 
                    for variable in variables:
                        assert str(row[variable]) == expected_row[variable]
                    if expected_row not in expected_row_results:
                        expected_row_results.append(expected_row)
                except:
                    pass
        
        try:
            assert expected_row_results == expected_rows
            self.__logger.log_correct(f"\tTest passed: expected rows {expected_rows} found rows {expected_row_results}")
            self.add_test_passed()
        except:
            self.__logger.log_error(f"\tTest failed: expected rows {expected_rows} found rows {expected_row_results}")
            self.add_test_failed()

        self.__logger.verbose_debug(f"Found rows: {rows}, expected rows {expected_rows}, expected row results {expected_row_results}, {expected_rows == expected_row_results }")

        pass

    
    def add_test_passed(self):
        self.__test_passed +=1
    
    def add_test_failed(self):
        self.__test_failed +=1

    def has_value(self, test_option):
        return test_option is not None

from typing import List

import argparse

from kgdd.kg_reader import KGReader
from kgdd.logger import Logger
from kgdd.test_file_parser import TestFileParser
from kgdd.kg_tester import KGTester
from kgdd.test_file import TestFile
from kgdd.test import Test

# Cli for the package

CLI_DESCRIPTION="A cli program to automate TDD KG development. Define some basic query and expected outputs in a test. Kgdd will take care of run queries and see if they match expedted results."

def main():
    
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
    parser.add_argument("-t", "--test", help="Path to testbed file. File should be in Json format", type=str, required=True)
    parser.add_argument("-f", "--file", help="Path to KG file", type=str, required=True)
    parser.add_argument("-v", "--verbose", help="Verbose output. Verbosity level = 0,1,2 . Default 0 no verbose. 2 is really verbose", choices=[0,1,2], default=0)

    args = parser.parse_args()
    
    verbosity_switch = {
        0: Logger(debug=False, verbose_debug=False),
        1: Logger(debug=True, verbose_debug=False),
        2: Logger(debug=True, verbose_debug=True)
    }


    kgreader = KGReader()
    logger = verbosity_switch.get(args.verbose)
    test_file_parser = TestFileParser()

    kgtester = KGTester(kgreader,logger,test_file_parser)

    kgtester.run_tests(args.file, args.test)



if __name__ == '__main__':
    main()
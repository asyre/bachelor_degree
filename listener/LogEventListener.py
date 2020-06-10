import logging
from typing import NoReturn, Optional

from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.EventListener import EventListener


class LogEventListener(EventListener):
    def __init__(self):
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
        ch.setFormatter(formatter)

        logger = logging.getLogger('LogEventListener')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        self.__logger = logger

    def on_framework_start(self) -> NoReturn:
        self.__logger.info("Started working")

    def on_framework_end(self) -> NoReturn:
        self.__logger.info("Finished working")

    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        self.__logger.debug("Started executing test suit with name: {}".format(test_suite.name))

    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        self.__logger.debug("Started executing test-case with name: {}".format(test_case.name))

    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        if error is not None:
            self.__logger.debug(
                "Finished executing test-case with name: {}, STATUS: {}, Error: {}".format(test_case.name, is_ok,
                                                                                           error))
        else:
            self.__logger.debug("Finished executing test-case with name: {}, STATUS: {}".format(test_case.name, is_ok))

    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        self.__logger.debug("Finished executing test suit with name: {}".format(test_suite.name))

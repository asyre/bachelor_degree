from abc import abstractmethod, ABCMeta
from typing import List, NoReturn, Optional

from executor.test_case import TestCase
from executor.test_suite import TestSuite


class EventListener(metaclass=ABCMeta):

    @abstractmethod
    def on_framework_start(self) -> NoReturn:
        pass

    @abstractmethod
    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        pass

    @abstractmethod
    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        pass

    @abstractmethod
    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        pass

    @abstractmethod
    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        pass

    @abstractmethod
    def on_framework_end(self) -> NoReturn:
        pass

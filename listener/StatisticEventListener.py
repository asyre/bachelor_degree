import time
from dataclasses import dataclass
from typing import NoReturn, Dict, List, Optional

from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.EventListener import EventListener


@dataclass
class TestCaseStatistic:
    test_name: str
    test_status: bool
    test_time: float = 0.0


@dataclass
class TestSuiteStatistic:
    test_case_count: int = 0
    test_case_ok: int = 0
    suite_time: float = 0.0
    test_cases: List[TestCaseStatistic] = None


class StatisticEventListener(EventListener):

    def __init__(self):
        self.suite_time_start: float = 0
        self.suite_time_end: float = 0

        self.case_time_start: float = 0
        self.case_time_end: float = 0

        self.test_suites_statistics: Dict[str, TestSuiteStatistic] = {}

    def collect_stats(self) -> Dict[str, TestSuiteStatistic]:
        return self.test_suites_statistics

    def on_framework_start(self) -> NoReturn:
        pass

    def on_framework_end(self) -> NoReturn:
        pass

    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        self.suite_time_start = time.time()

    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        self.case_time_start = time.time()

    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        self.case_time_end = time.time()
        result = self.case_time_end - self.case_time_start
        if self.test_suites_statistics.get(test_suite.name) is None:
            self.test_suites_statistics[test_suite.name] = TestSuiteStatistic(test_cases=[])
        self.test_suites_statistics[test_suite.name].test_case_count += 1
        self.test_suites_statistics[test_suite.name].test_case_ok += 1 if is_ok else 0
        self.test_suites_statistics[test_suite.name].test_cases.append(TestCaseStatistic(test_case.name, is_ok, result))

    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        self.suite_time_end = time.time()
        result = self.suite_time_end - self.suite_time_start
        self.test_suites_statistics[test_suite.name].suite_time = result

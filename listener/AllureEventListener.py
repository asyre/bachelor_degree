from typing import NoReturn, Dict, Optional
from uuid import uuid4

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_commons.model2 import TestResult, TestStepResult, Status, Parameter
from allure_commons.reporter import AllureReporter
from allure_commons.utils import now

from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.EventListener import EventListener
from listener.StatisticEventListener import StatisticEventListener


class AllureEventListener(EventListener):
    def on_framework_start(self) -> NoReturn:
        pass

    def on_framework_end(self) -> NoReturn:
        pass

    def __init__(self, allure_report_path: str):
        self.reporter = AllureReporter()
        self.file_reporter = AllureFileLogger(allure_report_path)
        allure_commons.plugin_manager.register(self.file_reporter)

        self.test_suite_uuid: Dict[TestSuite, str] = {}
        self.test_suite_test_result: Dict[TestSuite, TestResult] = {}
        self.test_case_uuid: Dict[TestCase, str] = {}

    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        suite_uuid = str(uuid4())
        self.test_suite_uuid[test_suite] = suite_uuid
        suite = TestResult(uuid=suite_uuid,
                           fullName=test_suite.name,
                           start=now(),
                           description=test_suite.description,
                           historyId=suite_uuid)
        self.reporter.schedule_test(suite_uuid, suite)
        self.test_suite_test_result[test_suite] = suite

    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        case_uuid = str(uuid4())
        self.test_case_uuid[test_case] = case_uuid
        case = TestStepResult(name=test_case.name, start=now(), description=test_case.description,
                              parameters=[Parameter(name="node", value=test_case.node)])
        self.reporter.start_step(self.test_suite_uuid[test_suite], case_uuid, case)

    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        if is_ok:
            status = Status.PASSED
        else:
            status = Status.FAILED

        self.reporter.stop_step(self.test_case_uuid[test_case], stop=now(), status=status)

    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        if is_ok:
            status = Status.PASSED
        else:
            status = Status.FAILED

        test_result = self.test_suite_test_result[test_suite]
        test_result.status = status
        test_result.stop = now()

        self.reporter.close_test(self.test_suite_uuid[test_suite])

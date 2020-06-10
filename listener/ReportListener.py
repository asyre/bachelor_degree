import json
from typing import NoReturn, Optional
from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.EventListener import EventListener
from listener.StatisticEventListener import StatisticEventListener


class ReportListener(EventListener):
    def __init__(self, statistic: StatisticEventListener, report_dir: str):
        self.statistic_event_listener = statistic
        self.report_dir = report_dir

    def on_framework_start(self) -> NoReturn:
        pass

    def on_framework_end(self) -> NoReturn:
        stats = self.statistic_event_listener.collect_stats()
        total_cases = 0
        total_cases_success = 0
        total_cases_time = 0
        for i in stats:
            total_cases += stats[i].test_case_count
            total_cases_success += stats[i].test_case_ok
            total_cases_time += stats[i].suite_time
        data_set = {"total": total_cases, "success": total_cases_success, "time": total_cases_time,
                    "suite_cases": stats}
        json_dump = json.dumps(data_set, default=lambda o: o.__dict__)
        with open('{}/stats.json' % self.report_dir, 'w') as f:
            f.write(json_dump + '\n')

    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        pass

    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        pass

    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        pass

    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        pass

from typing import List, NoReturn, Optional

from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.EventListener import EventListener


class CompositeEventListener(EventListener):
    def on_framework_start(self) -> NoReturn:
        for listener in self.listeners:
            listener.on_framework_start()

    def on_framework_end(self) -> NoReturn:
        for listener in self.listeners:
            listener.on_framework_end()

    def __init__(self, listeners: List[EventListener]):
        self.listeners = listeners

    def add_listener(self, listener: EventListener) -> NoReturn:
        self.listeners.append(listener)

    def on_test_suite_start(self, test_suite: TestSuite) -> NoReturn:
        for listener in self.listeners:
            listener.on_test_suite_start(test_suite)

    def on_test_case_start(self, test_suite: TestSuite, test_case: TestCase) -> NoReturn:
        for listener in self.listeners:
            listener.on_test_case_start(test_suite, test_case)

    def on_test_case_end(self, test_suite: TestSuite, test_case: TestCase, is_ok: bool,
                         error: Optional[Exception]) -> NoReturn:
        for listener in self.listeners:
            listener.on_test_case_end(test_suite, test_case, is_ok, error)

    def on_test_suite_end(self, test_suite: TestSuite, is_ok: bool) -> NoReturn:
        for listener in self.listeners:
            listener.on_test_suite_end(test_suite, is_ok)

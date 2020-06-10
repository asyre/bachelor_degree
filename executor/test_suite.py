from typing import Dict, Optional, List, Any

from executor.scheduler import Scheduler
from executor.test_case import TestCase
from runner.ConnectionData import ConnectionData


class TestSuite:
    def __init__(self, name: str,
                 description: Optional[str],
                 connection_data: Dict[str, ConnectionData],
                 env: Optional[Dict[str, List[str]]],
                 tests: List[TestCase],
                 cls: Any,
                 scheduler: Optional[Scheduler],
                 order: Optional[int],
                 skip: Optional[bool]):
        self.skip = skip
        self.order = order
        self.scheduler = scheduler
        self.cls = cls
        self.tests = tests
        self.env = env
        self.connection_data = connection_data
        self.description = description
        self.name = name

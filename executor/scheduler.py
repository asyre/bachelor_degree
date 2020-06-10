import itertools
from abc import ABCMeta, abstractmethod
from typing import List, Dict
from enum import IntEnum, auto

from executor.test_case import TestCase


class SchedulerType(IntEnum):
    Parallel = auto()
    Priority = auto()


class Scheduler(metaclass=ABCMeta):

    @abstractmethod
    def schedule(self, test: List[TestCase]) -> List[TestCase]:
        pass


class PriorityScheduler(Scheduler):
    def schedule(self, test: List[TestCase]) -> List[TestCase]:
        return sorted(test,
                      key=lambda x: (float('inf') if x.order is None else x.order, x.node))


class ParallelScheduler(Scheduler):
    def schedule(self, test: List[TestCase]) -> List[TestCase]:
        result_list: List[TestCase] = []
        dictionary: Dict[str, List[TestCase]] = {}
        for t in test:
            dictionary.setdefault(t.node, []).append(t)
        # dictionary = (map(lambda x: sorted(x, key=lambda y: y.order), dictionary))
        acc: List[List[TestCase]] = []
        for key, value in dictionary.items():
            acc.append(sorted(value, key=lambda te: te.order if te.order is not None else float("inf")))
        for i in itertools.zip_longest(*acc):
            result_list.extend(filter(lambda item: item is not None, i))
        return result_list


class UnknownSchedulerType(Exception):
    pass


def create_scheduler_from_type(scheduler_type: SchedulerType) -> Scheduler:
    if scheduler_type is SchedulerType.Parallel:
        return ParallelScheduler()

    if scheduler_type is SchedulerType.Priority:
        return PriorityScheduler()

    raise UnknownSchedulerType


def create_scheduler_from_string(scheduler_str: str) -> Scheduler:
    if scheduler_str == "parallel":
        return ParallelScheduler()

    if scheduler_str == "priority":
        return PriorityScheduler()

    raise UnknownSchedulerType

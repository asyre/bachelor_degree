import itertools
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import groupby
from typing import Dict, List, Iterator, Optional

from executor.connection import Connection
from executor.loader import discover
from executor.scheduler import Scheduler, PriorityScheduler, ParallelScheduler
from executor.test_case import TestCase
from executor.test_suite import TestSuite
from listener.AllureEventListener import AllureEventListener
from listener.CompositeEventListener import CompositeEventListener
from listener.LogEventListener import LogEventListener
from listener.ReportListener import ReportListener
from listener.StatisticEventListener import StatisticEventListener
from runner.NetworkHardwareConnection import NetworkHardwareMachineConnection, create_machine_connection

__pyroutertest = True


class TestProgram(object):

    def __init__(self,
                 scheduler: Scheduler = PriorityScheduler(),
                 discover_dir: Optional[str] = ".",
                 allure_dir: Optional[str] = "./reports",
                 report_dir: Optional[str] = "./",
                 log_enabled: Optional[bool] = True,
                 path_exclude_reg: Optional[str] = "",
                 name_exclude_reg: Optional[str] = "",
                 path_include_reg: Optional[str] = "",
                 name_include_reg: Optional[str] = "",
                 listeners=None
                 ):
        if listeners is None:
            listeners = []

        listener = CompositeEventListener(listeners)

        stat_listener = StatisticEventListener()
        listener.add_listener(stat_listener)

        if log_enabled:
            log_listener = LogEventListener()
            listener.add_listener(log_listener)

        if report_dir is not None:
            report_listener = ReportListener(stat_listener, report_dir)
            listener.add_listener(report_listener)

        if allure_dir is not None:
            allure_listener = AllureEventListener(allure_dir)
            listener.add_listener(allure_listener)

        test_suites: List[TestSuite] = discover(discover_dir, path_include_reg, name_include_reg, path_exclude_reg,
                                                name_exclude_reg)
        test_suites.sort(key=lambda x: x.order if x.order is not None else float("inf"))
        listener.on_framework_start()
        for test_suite in test_suites:
            if test_suite.skip:
                continue

            machines_connections: Dict[str, NetworkHardwareMachineConnection] = {}

            for machine in test_suite.connection_data:
                machines_connections[machine] = create_machine_connection(test_suite.connection_data[machine].hostname,
                                                                          test_suite.connection_data[machine].port,
                                                                          test_suite.connection_data[machine].username,
                                                                          test_suite.connection_data[machine].password)
            for machine in machines_connections:
                machines_connections[machine].execute("load default")
            if test_suite.env is not None:
                for setting in test_suite.env:
                    for command in test_suite.env[setting]:
                        if setting in machines_connections:
                            machines_connections[setting].execute(command)

            connections: Dict[str, Connection] = {}

            # TODO тут можно нормально через map написать
            for node, hardware_connection in machines_connections.items():
                connections[node] = Connection(hardware_connection)

            """Выбираем порядок запуска тестов"""
            test_case_scheduler = test_suite.scheduler
            if test_case_scheduler is None:
                test_case_scheduler = scheduler
            tests = test_case_scheduler.schedule(test_suite.tests)

            is_ok = True
            """Стартуем TestSuite"""
            test_suite_instance = test_suite.cls()
            test_suite_instance.initializer()
            listener.on_test_suite_start(test_suite)
            if isinstance(scheduler, ParallelScheduler):
                grouped_test: Dict[str, Iterator[TestCase]] = dict(groupby(tests, lambda test: test.node))
                index_map = grouped_test.keys()

                executor = ThreadPoolExecutor(max_workers=len(index_map))

                def __execute(test: TestCase):
                    if test is None:
                        return

                    if test.skip:
                        return

                    try:
                        listener.on_test_case_start(test_suite, test)
                        test.func(test_suite_instance, connections[test.node])
                        listener.on_test_case_end(test_suite, test, True, None)
                    except Exception as e:
                        listener.on_test_case_end(test_suite, test, False, e)

                listener.on_test_suite_end(test_suite, is_ok)
                try:
                    for execution_list in itertools.zip_longest(*grouped_test.values()):
                        executor.map(__execute, execution_list)
                except Exception:
                    is_ok = False

                listener.on_test_suite_end(test_suite, is_ok)
            else:
                for test in tests:
                    if test.skip:
                        continue

                    if test.node is not None:
                        """Стартуем Test"""
                        try:
                            listener.on_test_case_start(test_suite, test)
                            test.func(test_suite_instance, connections[test.node])
                            listener.on_test_case_end(test_suite, test, True, None)
                        except Exception as e:
                            listener.on_test_case_end(test_suite, test, False, e)
                            is_ok = False
                listener.on_test_suite_end(test_suite, is_ok)
            test_suite_instance.finalizer()
        listener.on_framework_end()


main = TestProgram

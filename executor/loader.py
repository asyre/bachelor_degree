import inspect
import os
import importlib.util
from typing import List

from executor.meta.connection import has_connection, get_connection
from executor.meta.description import get_description
from executor.meta.env import has_env, get_env
from executor.meta.name import get_name, has_name
from executor.meta.node import get_node
from executor.meta.order import get_order
from executor.meta.scheduler import get_scheduler
from executor.meta.skip import has_skip, get_skip
from executor.parser import connection_parser, env_parser
from executor.test_case import TestCase
from executor.test_suite import TestSuite

exclude_dirs = ['__pycache__']

exclude_files = ['__main__.py', '__init__.py']

supported_extensions = ['.py']


def discover(start_dir: str, path_include_reg: str = "",
             name_include_reg: str = "", path_exclude_reg: str = "", name_exclude_reg: str = "") -> List[TestSuite]:
    acc: List[TestSuite] = []
    top_level_dir = os.path.abspath(start_dir)

    for root, _, filenames in os.walk(top_level_dir):
        if root in exclude_dirs:
            continue

        for filename in filenames:
            name, extension = os.path.splitext(filename)
            if extension not in supported_extensions:
                continue

            acc.extend(__extract_tests(os.path.join(root, filename), filename))

    return acc


class ConnectionInformationMissing(Exception):
    pass


def __extract_tests(file_path: str, module_name: str) -> List[TestSuite]:
    acc: List[TestSuite] = []
    module_spec = importlib.util.spec_from_file_location(
        module_name, file_path
    )

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    clsmembers = inspect.getmembers(module, inspect.isclass)
    for cls_name, cls in clsmembers:
        if not cls_name.endswith("TestSuite"):
            continue

        if not has_connection(cls):
            raise ConnectionInformationMissing()

        connection_data = connection_parser(get_connection(cls))

        env = None
        if has_env(cls):
            env = env_parser(get_env(cls))

        name = cls_name
        if has_name(cls):
            name = get_name(cls)
        skip = None
        if has_skip(cls):
            skip = get_skip(cls)
        test_acc = []
        acc.append(TestSuite(name, get_description(cls), connection_data, env, test_acc, cls, get_scheduler(cls),
                             get_order(cls), skip))
        funcs = inspect.getmembers(cls, inspect.isfunction)
        for func_name, func in funcs:
            if not func_name.endswith("TestCase"):
                continue

            node = get_node(func)
            order = get_order(func)

            skip = None
            if has_skip(cls):
                skip = get_skip(cls)

            name = func_name
            if has_name(cls):
                name = get_name(cls)

            test_acc.append(TestCase(name, get_description(cls), node, func, order, skip))

    return acc

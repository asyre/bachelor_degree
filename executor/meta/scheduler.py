from enum import IntEnum, auto
from typing import Any, Optional, Union

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import has_meta_information, get_meta_information, set_meta_information
from executor.scheduler import SchedulerType, Scheduler, create_scheduler_from_type, create_scheduler_from_string

__scheduler_key = "scheduler"


def has_scheduler(obj: Any) -> bool:
    return has_meta_information(obj, __scheduler_key)


def get_scheduler(obj: Any) -> Optional[Scheduler]:
    return get_meta_information(obj, __scheduler_key)


def scheduler(value: Union[str, SchedulerType, Scheduler]):
    def __decorator(func):
        if isinstance(value, Scheduler):
            scheduler = value
        elif isinstance(value, SchedulerType):
            scheduler = create_scheduler_from_type(value)
        else:
            scheduler = create_scheduler_from_string(must_extract_env_var_if_present(value))
        set_meta_information(func, __scheduler_key, scheduler)
        return func

    return __decorator

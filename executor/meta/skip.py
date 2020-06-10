from typing import Any, Optional, Union

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__skip_key = "skip"


def has_skip(obj: Any) -> bool:
    return has_meta_information(obj, __skip_key)


def get_skip(obj: Any) -> Optional[bool]:
    return get_meta_information(obj, __skip_key)


def skip(value: Union[bool, str]):
    def __decorator(func):
        if isinstance(value, bool):
            set_meta_information(func, __skip_key, value)
        else:
            set_meta_information(func, __skip_key, bool(must_extract_env_var_if_present(value)))

        return func

    return __decorator

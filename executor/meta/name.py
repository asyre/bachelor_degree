from typing import Any, Optional

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__name_key = "name"


def has_name(obj: Any) -> bool:
    return has_meta_information(obj, __name_key)


def get_name(obj: Any) -> Optional[str]:
    return get_meta_information(obj, __name_key)


def name(value: str):
    def __decorator(func):
        set_meta_information(func, __name_key, must_extract_env_var_if_present(value))
        return func

    return __decorator

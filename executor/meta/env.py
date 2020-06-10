from typing import Any, Optional

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__env_key = "env"


def has_env(obj: Any) -> bool:
    return has_meta_information(obj, __env_key)


def get_env(obj: Any) -> Optional[str]:
    return get_meta_information(obj, __env_key)


def env(path: str):
    def __decorator(func):
        set_meta_information(func, __env_key, must_extract_env_var_if_present(path))
        return func

    return __decorator

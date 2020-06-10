from typing import Any, Optional

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__path_key = "connection"


def has_connection(obj: Any) -> bool:
    return has_meta_information(obj, __path_key)


def get_connection(obj: Any) -> Optional[str]:
    return get_meta_information(obj, __path_key)


def connection(path: str):
    def __decorator(func):
        set_meta_information(func, __path_key, must_extract_env_var_if_present(path))
        return func

    return __decorator

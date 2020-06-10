from typing import Any, Optional

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__description_key = "description"


def has_description(obj: Any) -> bool:
    return has_meta_information(obj, __description_key)


def get_description(obj: Any) -> Optional[str]:
    return get_meta_information(obj, __description_key)


def description(value: str):
    def __decorator(func):
        set_meta_information(func, __description_key, must_extract_env_var_if_present(value))
        return func

    return __decorator

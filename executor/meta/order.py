from typing import Any, Optional, Union

from executor.meta.env_var import must_extract_env_var
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__order_key = "order"


def has_order(obj: Any) -> bool:
    return has_meta_information(obj, __order_key)


def get_order(obj: Any) -> Optional[int]:
    return get_meta_information(obj, __order_key)


def order(value: Union[int, str]):
    def __decorator(func):
        if isinstance(value, int):
            set_meta_information(func, __order_key, value)
        else:
            set_meta_information(func, __order_key, int(must_extract_env_var(value)))

        return func

    return __decorator

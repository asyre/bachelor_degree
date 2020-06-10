from typing import Any, Optional

from executor.meta.env_var import must_extract_env_var_if_present
from executor.meta.meta import set_meta_information, has_meta_information, get_meta_information

__node_key = "node"


def has_node(obj: Any) -> bool:
    return has_meta_information(obj, __node_key)


def get_node(obj: Any) -> Optional[str]:
    return get_meta_information(obj, __node_key)


def node(name: str):
    def __decorator(func):
        set_meta_information(func, __node_key, must_extract_env_var_if_present(name))
        return func

    return __decorator

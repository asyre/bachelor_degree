from typing import Any, Dict, Optional
# key is an object and values are [name, "
__META_TABLE: Dict[Any, Dict[str, Any]] = {}


def has_meta_information(obj: Any, key: str) -> bool:
    obj_meta = __META_TABLE[obj]
    if obj_meta is None:
        return False

    return key in obj_meta


def get_meta_information(obj: Any, key: str) -> Optional[Any]:
    return __META_TABLE.setdefault(obj, {}).get(key)


def set_meta_information(obj: Any, key: str, value: Any):
    __META_TABLE.setdefault(obj, {})[key] = value

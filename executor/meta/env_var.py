import os
from typing import Optional


def is_env_var(value: str) -> bool:
    return value.startswith("$")


def extract_env_var(value: str) -> Optional[str]:
    return os.environ[value[1:]]


def must_extract_env_var(value: str) -> str:
    env = extract_env_var(value)
    if env is None:
        raise MissingEnvVar
    return env


def must_extract_env_var_if_present(value: str) -> str:
    if is_env_var(value):
        return must_extract_env_var(value)
    return value


class MissingEnvVar(Exception):
    pass

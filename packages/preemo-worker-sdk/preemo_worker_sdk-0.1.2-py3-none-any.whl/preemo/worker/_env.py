import os
from typing import Optional


def get_optional_env(name: str) -> Optional[str]:
    value = os.getenv(key=name)
    if value is None or len(value) == 0:
        return None

    return value


def get_required_env(name: str) -> str:
    value = get_optional_env(name)
    if value is None:
        raise Exception(f"missing required env variable: {name}")

    return value

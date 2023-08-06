from typing import Callable, Optional

def register(
    outer_function: Optional[Callable] = ...,
    *,
    name: Optional[str] = ...,
    namespace: Optional[str] = ...,
) -> Callable: ...

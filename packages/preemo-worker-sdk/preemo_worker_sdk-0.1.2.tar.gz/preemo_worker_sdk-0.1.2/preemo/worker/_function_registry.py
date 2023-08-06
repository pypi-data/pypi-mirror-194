from typing import Callable, Dict, Optional


class FunctionRegistry:
    def __init__(self) -> None:
        self._global_functions_by_name: Dict[str, Callable] = {}
        self._functions_by_namespace_and_name: Dict[str, Dict[str, Callable]] = {}

    def register_function(
        self, function: Callable, *, name: str, namespace: Optional[str] = None
    ) -> None:
        if namespace is None:
            if name in self._global_functions_by_name:
                raise Exception(
                    f"must not register multiple functions with the same name: {name}"
                )
            self._global_functions_by_name[name] = function

            return

        if namespace not in self._functions_by_namespace_and_name:
            self._functions_by_namespace_and_name[namespace] = {}
        functions_by_name = self._functions_by_namespace_and_name[namespace]

        if name in functions_by_name:
            raise Exception(
                f"must not register multiple functions with the same namespace: {namespace} and name: {name}"
            )
        functions_by_name[name] = function

    def get_function(self, *, name: str, namespace: Optional[str] = None) -> Callable:
        if namespace is None:
            function = self._global_functions_by_name.get(name)
            if function is None:
                raise Exception(f"cannot find registered function with name: {name}")

            return function

        function = self._functions_by_namespace_and_name.get(namespace, {}).get(name)
        if function is None:
            raise Exception(
                f"cannot find registered function with namespace: {namespace} and name: {name}"
            )

        return function

from contextlib import contextmanager
from typing import List, Optional, Type

from graphql import GraphQLError
from graphql.execution import MiddlewareManager

from .types import ContextValue, Extension


class ExtensionManager:
    __slots__ = ("extensions", "extensions_reversed")

    def __init__(self, extensions: Optional[List[Type[Extension]]] = None):
        if extensions:
            self.extensions = tuple(ext() for ext in extensions)
            self.extensions_reversed = tuple(reversed(self.extensions))
        else:
            self.extensions_reversed = self.extensions = tuple()

    def as_middleware_manager(
        self, manager: Optional[MiddlewareManager]
    ) -> MiddlewareManager:
        if manager and manager.middlewares:
            return MiddlewareManager(*manager.middlewares, *self.extensions)
        return MiddlewareManager(*self.extensions)

    @contextmanager
    def request(self, context: ContextValue):
        for ext in self.extensions:
            ext.request_started(context)
        try:
            yield
        finally:
            for ext in self.extensions_reversed:
                ext.request_finished(context)

    def has_errors(self, errors: List[GraphQLError]):
        for ext in self.extensions:
            ext.has_errors(errors)

    def format(self) -> dict:
        data = {}
        for ext in self.extensions:
            ext_data = ext.format()
            if ext_data:
                data.update(ext_data)
        return data

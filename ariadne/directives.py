from typing import Callable, Union, Optional, List, Dict

from graphql.type import GraphQLObjectType, GraphQLSchema, GraphQLField
from graphql.language import DirectiveNode, StringValueNode

from .types import Resolver, SchemaBindable
from .interfaces import _type_implements_interface


class DirectiveType(SchemaBindable):
    _field: Union[None, Resolver]

    def __init__(self, name: str) -> None:
        self.name = name
        self._field = None

    def field(self, f: Resolver) -> Callable[[Resolver], Resolver]:
        self._field = f
        return f

    def _call_directives(
        self,
        directives: List[DirectiveNode],
        field: Union[GraphQLObjectType, GraphQLField],
    ) -> None:
        for directive in directives:
            if directive.name.value != self.name:
                continue

            arguments: dict = {}

            for arg in directive.arguments:
                if isinstance(arg.name, StringValueNode) and isinstance(
                    arg.value, StringValueNode
                ):
                    arguments[arg.name.value] = arg.value.value

            if self._field:
                self._field(field, **arguments)

    def bind_to_schema(self, schema: GraphQLSchema) -> None:
        directive = schema.get_directive(self.name)

        if not self._field:
            raise ValueError(
                "Directive %s doesnot have any resolver function" % self.name
            )

        if not directive:
            raise ValueError("Directive %s is not defined in the schema" % self.name)

        for graphql_type in schema.type_map.values():
            if not isinstance(graphql_type, GraphQLObjectType):
                continue

            ast_node = graphql_type.ast_node
            if graphql_type and ast_node and ast_node.directives:
                self._call_directives(ast_node.directives, graphql_type)

            for field in graphql_type.fields.values():
                if field.ast_node:
                    self._call_directives(field.ast_node.directives, field)

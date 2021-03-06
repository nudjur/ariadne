from unittest.mock import Mock

import pytest

from ariadne import ExtensionManager, graphql
from ariadne.types import Extension


context = {}
exception = ValueError()


def test_request_started_event_is_called_by_extension_manager():
    extension = Mock(spec=Extension)
    manager = ExtensionManager([Mock(return_value=extension)])
    with manager.request(context):
        pass

    extension.request_started.assert_called_once_with(context)


def test_request_finished_event_is_called_by_extension_manager():
    extension = Mock(spec=Extension)
    manager = ExtensionManager([Mock(return_value=extension)])
    with manager.request(context):
        pass

    extension.request_finished.assert_called_once_with(context)


def test_has_errors_event_is_called_with_errors_list():
    extension = Mock(spec=Extension)
    manager = ExtensionManager([Mock(return_value=extension)])
    manager.has_errors([exception])
    extension.has_errors.assert_called_once_with([exception])


def test_extensions_are_formatted():
    extensions = [
        Mock(spec=Extension, format=Mock(return_value={"a": 1})),
        Mock(spec=Extension, format=Mock(return_value={"b": 2})),
    ]
    manager = ExtensionManager([Mock(return_value=ext) for ext in extensions])
    assert manager.format() == {"a": 1, "b": 2}


class BaseExtension(Extension):
    pass


@pytest.mark.asyncio
async def test_default_extension_hooks_dont_interrupt_query_execution(schema):
    _, response = await graphql(
        schema, {"query": "{ status }"}, extensions=[BaseExtension]
    )
    assert response["data"] == {"status": True}

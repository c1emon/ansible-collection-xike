from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
from typing import Protocol, cast

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.connection import Connection, ConnectionError

from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.errors import (
    XikeOSCommandError,
    XikeOSConfigError,
    XikeOSConnectionError,
)


JsonValue = None | bool | int | float | str | list[object] | dict[str, object]
ConfigFlags = list[str] | tuple[str, ...] | None
ConfigResponse = dict[str, object] | list[object]


class XikeOSModule(Protocol):
    """Minimal protocol for the AnsibleModule objects used by XikeOS helpers.

    Runtime callers pass an AnsibleModule instance. This protocol documents only
    the dynamic attributes these helpers read or cache on that AnsibleModule.
    """

    _socket_path: str
    _xikeos_connection: Connection
    _xikeos_capabilities: dict[str, JsonValue]


def get_connection(module: XikeOSModule) -> Connection:
    if hasattr(module, "_xikeos_connection"):
        return module._xikeos_connection
    module._xikeos_connection = Connection(module._socket_path)
    return module._xikeos_connection


def get_capabilities(module: XikeOSModule) -> dict[str, JsonValue]:
    if hasattr(module, "_xikeos_capabilities"):
        return module._xikeos_capabilities
    try:
        capabilities = Connection(module._socket_path).get_capabilities()
    except ConnectionError as exc:
        raise XikeOSConnectionError("failed to get Xike OS capabilities", detail=to_text(exc)) from exc
    module._xikeos_capabilities = json.loads(capabilities)
    return module._xikeos_capabilities


def run_commands(module: XikeOSModule, commands: list[str], check_rc: bool = True) -> list[object]:
    connection = get_connection(module)
    try:
        return cast(list[object], connection.run_commands(commands=commands, check_rc=check_rc))
    except ConnectionError as exc:
        raise XikeOSCommandError("command execution failed", commands=commands, detail=to_text(exc)) from exc


def get_config(module: XikeOSModule, source: str = "running", flags: ConfigFlags = None, format: str | None = None) -> str:
    connection = get_connection(module)
    try:
        return to_text(connection.get_config(source=source, flags=flags, format=format), errors="surrogate_or_strict")
    except ConnectionError as exc:
        raise XikeOSConnectionError("failed to get Xike OS config", detail=to_text(exc)) from exc


def load_config(module: XikeOSModule, commands: list[str]) -> ConfigResponse:
    connection = get_connection(module)
    try:
        response = connection.edit_config(candidate=commands)
    except ConnectionError as exc:
        raise XikeOSConfigError("failed to apply Xike OS configuration", commands=commands, detail=to_text(exc)) from exc
    if isinstance(response, str):
        return cast(ConfigResponse, json.loads(response))
    return cast(ConfigResponse, response)

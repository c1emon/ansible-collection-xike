from __future__ import absolute_import, division, print_function

__metaclass__ = type

from typing import Any, Sequence


class XikeOSError(Exception):
    """Base typed error for Xike OS helpers."""

    def __init__(self, message: str, *, commands: Sequence[str] | None = None, detail: Any = None, context: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.commands = list(commands) if commands is not None else None
        self.detail = detail
        self.context = context

    def __str__(self) -> str:
        return self.message


class XikeOSConnectionError(XikeOSError):
    pass


class XikeOSCommandError(XikeOSError):
    pass


class XikeOSConfigError(XikeOSError):
    pass


class XikeOSFactsError(XikeOSError):
    pass


class XikeOSParseError(XikeOSError):
    pass

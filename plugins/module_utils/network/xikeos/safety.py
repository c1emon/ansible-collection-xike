from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from typing import Any


REDACTION_MARKER = "<redacted>"

MUTATING_COMMAND_PREFIXES: tuple[str, ...] = (
    "config",
    "configure",
    "copy",
    "delete",
    "erase",
    "format",
    "reload",
    "reset",
    "write",
)

SENSITIVE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?im)^(\s*(?:username\s+\S+\s+password|password|secret|enable\s+secret)\s+)(\S+)(.*)$"),
    re.compile(r"(?im)^(\s*(?:snmp-server\s+community)\s+)(\S+)(.*)$"),
    re.compile(r"(?im)^(\s*(?:radius-server|tacacs-server)\s+key\s+)(\S+)(.*)$"),
    re.compile(r"(?im)^(\s*(?:key-string|pre-shared-key)\s+)(\S+)(.*)$"),
)


def normalize_command(command: Any) -> str:
    """Return a single command string from Ansible command input."""
    if isinstance(command, dict):
        return str(command.get("command") or "")
    return str(command or "")


def is_mutating_command(command: Any) -> bool:
    """Classify known mutating/destructive command prefixes conservatively."""
    command_text = normalize_command(command).strip().lower()
    if not command_text:
        return False
    first_token = command_text.split(None, 1)[0]
    return first_token in MUTATING_COMMAND_PREFIXES


def find_mutating_commands(commands: list[Any]) -> list[str]:
    """Return commands that are unsafe for default xikeos_command execution."""
    return [normalize_command(command) for command in commands if is_mutating_command(command)]


def redact_text(value: str) -> str:
    """Redact common secret values while preserving surrounding context."""
    redacted = value
    for pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub(lambda match: "%s%s%s" % (match.group(1), REDACTION_MARKER, match.group(3)), redacted)
    return redacted


def redact_value(value: Any) -> Any:
    """Recursively redact sensitive strings in returned data structures."""
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    return value

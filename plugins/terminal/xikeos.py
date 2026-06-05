from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
import json

from ansible.errors import AnsibleConnectionFailure
from ansible_collections.ansible.netcommon.plugins.plugin_utils.terminal_base import TerminalBase


class TerminalModule(TerminalBase):
    terminal_stdout_re = [
        re.compile(rb"[\r\n]?[A-Za-z0-9_.:/-]+(?:\([^)]+\)){0,3}[>#]\s?$"),
    ]

    terminal_stderr_re = [
        re.compile(rb"% ?Error", re.I),
        re.compile(rb"invalid (?:input|command)", re.I),
        re.compile(rb"incomplete command", re.I),
        re.compile(rb"ambiguous command", re.I),
        re.compile(rb"permission denied", re.I),
        re.compile(rb"authorization failed", re.I),
        re.compile(rb"access denied", re.I),
        re.compile(rb"command authorization failed", re.I),
    ]

    terminal_config_prompt = re.compile(r"^.+\(config[^)]*\)#$")

    def on_open_shell(self):
        for command in (b"terminal length 0", b"terminal width 512"):
            try:
                self._exec_cli_command(command)
            except AnsibleConnectionFailure:
                if command == b"terminal length 0":
                    raise

    def on_become(self, passwd=None):
        prompt = self._get_prompt()
        if prompt and prompt.strip().endswith(b"#"):
            return
        cmd = b"enable"
        if passwd:
            cmd = json.dumps({"command": "enable", "prompt": "[Pp]assword: ?$", "answer": passwd})
        self._exec_cli_command(cmd)

    def on_unbecome(self):
        prompt = self._get_prompt()
        if prompt and prompt.strip().endswith(b"#"):
            self._exec_cli_command(b"disable")

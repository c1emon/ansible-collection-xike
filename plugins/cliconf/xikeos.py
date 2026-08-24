# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: "clemon (@c1emon)"
name: xikeos
short_description: Use Xike OS cliconf to run commands on Xike switches
description:
  - This cliconf plugin provides the Xike OS command, configuration, and facts transport used with C(ansible.netcommon.network_cli).
  - Use with C(ansible_network_os=c1emon.xikeos.xikeos).
version_added: "0.1.0"
options:
  config_commands:
    description:
      - Commands used by the cliconf plugin to enter and leave configuration mode.
    default:
      - configure terminal
      - end
    type: list
    elements: str
"""

import json
import re
from typing import Any, Optional

from ansible.module_utils.common.collections import is_sequence
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.ansible.netcommon.plugins.plugin_utils.cliconf_base import CliconfBase


def _to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if is_sequence(value):
        return list(value)
    return [value]


class Cliconf(CliconfBase):
    def get(
        self,
        command: Optional[str] = None,
        prompt: Any = None,
        answer: Any = None,
        sendonly: bool = False,
        newline: bool = True,
        output: Any = None,
        check_all: bool = False,
    ) -> str:
        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def get_config(
        self, source: str = "running", flags: Any = None, format: Optional[str] = None
    ) -> str:  # type: ignore
        if source not in ("running", "startup"):
            raise ValueError("fetching configuration from %s is not supported" % source)
        if format not in (None, "text"):
            raise ValueError("configuration format %s is not supported" % format)
        command = (
            "show running-config" if source == "running" else "show startup-config"
        )
        flag_text = " ".join(_to_list(flags))
        if flag_text:
            command = "%s %s" % (command, flag_text)
        return self.send_command(command)

    def edit_config(
        self,
        candidate: Any = None,
        commit: bool = True,
        replace: Any = None,
        diff: bool = False,
        comment: Optional[str] = None,
    ) -> str:  # type: ignore
        if replace:
            raise ValueError("replace config is not supported on Xike OS")

        requests = []
        responses = []
        commands = _to_list(candidate)
        if commit and commands:
            self.send_command("configure terminal")
            try:
                for line in commands:
                    command = line.get("command") if isinstance(line, dict) else line
                    if not command or str(command).startswith("!"):
                        continue
                    if command == "end":
                        continue
                    requests.append(command)
                    responses.append(self.send_command(command))
            finally:
                self.send_command("end")
        return json.dumps({"diff": "", "request": requests, "response": responses})

    def get_device_info(self) -> dict[str, Any]:  # type: ignore
        info = {"network_os": "xikeos"}
        try:
            output = to_text(self.get("show version"), errors="surrogate_or_strict")
        except Exception:
            return info

        version = re.search(
            r"(?:Version|Software version)\s*[: ]\s*([^\s,]+)", output, re.I
        )
        model = re.search(r"(?:Model|Device model)\s*[: ]\s*(.+)$", output, re.I | re.M)
        hostname = re.search(r"^\s*(\S+)\s+uptime", output, re.I | re.M)
        if not hostname:
            hostname = re.search(
                r"(?:Hostname|System name)\s*[: ]\s*(\S+)", output, re.I
            )
        if version:
            info["network_os_version"] = version.group(1)
        if model:
            info["network_os_model"] = model.group(1).strip()
        if hostname:
            info["network_os_hostname"] = hostname.group(1)
        return info

    def get_capabilities(self) -> str:  # type: ignore
        result = super(Cliconf, self).get_capabilities()
        if isinstance(result, str):
            result = json.loads(result)
        result["rpc"] += ["get_config", "edit_config", "run_commands"]
        result["device_operations"] = {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": False,
            "supports_generate_diff": False,
            "supports_replace": False,
        }
        result["format"] = ["text"]
        result["network_api"] = "cliconf"
        return json.dumps(result)

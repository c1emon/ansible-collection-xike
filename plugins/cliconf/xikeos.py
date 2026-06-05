from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import re

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.common.collections import is_sequence
from ansible_collections.ansible.netcommon.plugins.plugin_utils.cliconf_base import CliconfBase


def _to_list(value):
    if value is None:
        return []
    if is_sequence(value):
        return list(value)
    return [value]


class Cliconf(CliconfBase):
    def get(self, command=None, prompt=None, answer=None, sendonly=False, newline=True, output=None, check_all=False):
        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def get_config(self, source="running", flags=None, format=None):
        if source not in ("running", "startup"):
            raise ValueError("fetching configuration from %s is not supported" % source)
        if format not in (None, "text"):
            raise ValueError("configuration format %s is not supported" % format)
        command = "show running-config" if source == "running" else "show startup-config"
        flag_text = " ".join(_to_list(flags))
        if flag_text:
            command = "%s %s" % (command, flag_text)
        return self.send_command(command)

    def edit_config(self, candidate=None, commit=True, replace=None, diff=False, comment=None):
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
        return {"request": requests, "response": responses}

    def get_device_info(self):
        info = {"network_os": "xikeos"}
        try:
            output = to_text(self.get("show version"), errors="surrogate_or_strict")
        except Exception:
            return info

        version = re.search(r"(?:Version|Software version)\s*[: ]\s*([^\s,]+)", output, re.I)
        model = re.search(r"(?:Model|Device model)\s*[: ]\s*(.+)$", output, re.I | re.M)
        hostname = re.search(r"^\s*(\S+)\s+uptime", output, re.I | re.M)
        if version:
            info["network_os_version"] = version.group(1)
        if model:
            info["network_os_model"] = model.group(1).strip()
        if hostname:
            info["network_os_hostname"] = hostname.group(1)
        return info

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
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

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Action plugin for xikeos_vlans controller-side parser templates."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from ansible.errors import AnsibleActionFail
from ansible.plugins.action.normal import ActionModule as NormalActionModule


SHOW_VLAN_TEMPLATE = "show_vlan.textfsm"


class ActionModule(NormalActionModule):
    """Inject bundled parser templates before normal module execution."""

    def run(self, tmp=None, task_vars=None):
        task_vars = task_vars or {}
        self._task.args = dict(self._task.args or {})
        templates = dict(self._task.args.get("_textfsm_templates") or {})
        templates[SHOW_VLAN_TEMPLATE] = self._load_textfsm_template(SHOW_VLAN_TEMPLATE)
        self._task.args["_textfsm_templates"] = templates
        return super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

    def _load_textfsm_template(self, template_name):
        template_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "module_utils",
                "facts",
                "textfsm_templates",
                template_name,
            )
        )
        if not os.path.isfile(template_path):
            raise AnsibleActionFail(
                "Required parser template '{0}' was not found on the controller at '{1}'. "
                "Reinstall or rebuild the xike.xikeos collection and verify the file exists under "
                "plugins/module_utils/facts/textfsm_templates/.".format(template_name, template_path)
            )

        with open(template_path, "r", encoding="utf-8") as template_file:
            return template_file.read()

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Internal TextFSM parser helpers for facts modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os


TEXTFSM_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "textfsm_templates")


def parse_textfsm_template(output, template_name):
    """Parse command output with a bundled TextFSM template."""
    if not output:
        return []

    try:
        import textfsm
    except ImportError as exc:
        raise ImportError(
            "The Python package 'textfsm' is required for Xike OS complex table parsing. "
            "Install it with `pip install textfsm` or install this collection's Python dependencies."
        ) from exc

    template_path = os.path.join(TEXTFSM_TEMPLATE_DIR, template_name)
    if not os.path.isfile(template_path):
        raise FileNotFoundError(
            "Bundled TextFSM template '{0}' was not found at '{1}'. Reinstall the "
            "xike.xikeos collection or verify collection packaging includes "
            "plugins/module_utils/facts/textfsm_templates/*.textfsm.".format(
                template_name,
                template_path,
            )
        )

    with open(template_path, "r", encoding="utf-8") as template_file:
        parser = textfsm.TextFSM(template_file)
        records = parser.ParseText(output)

    headers = [header.lower() for header in parser.header]
    return [dict(zip(headers, record)) for record in records]

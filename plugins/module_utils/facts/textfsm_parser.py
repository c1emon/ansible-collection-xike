#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Internal TextFSM parser helpers for facts modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any

import io
import os


TEXTFSM_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "textfsm_templates")


def parse_textfsm_template(
    output: str | None,
    template_name: str,
    templates: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
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

    template_content = (templates or {}).get(template_name)
    template_path = os.path.join(TEXTFSM_TEMPLATE_DIR, template_name)

    if template_content is not None:
        template_file = io.StringIO(template_content)
    elif os.path.isfile(template_path):
        template_file = open(template_path, "r", encoding="utf-8")
    else:
        raise FileNotFoundError(
            "Bundled TextFSM template '{0}' was not injected and was not found at '{1}'. "
            "Run through the module action plugin or reinstall the xike.xikeos collection and "
            "verify collection packaging includes plugins/module_utils/facts/textfsm_templates/*.textfsm.".format(
                template_name,
                template_path,
            )
        )

    with template_file:
        parser = textfsm.TextFSM(template_file)
        records = parser.ParseText(output)

    headers = [header.lower() for header in parser.header]
    return [dict(zip(headers, record)) for record in records]

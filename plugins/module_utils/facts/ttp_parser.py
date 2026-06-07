#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Internal TTP parser helpers for facts modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os


TTP_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "ttp_templates")


def parse_ttp_template(output, template_name, result_key=None, templates=None):
    """Parse command output with a bundled TTP template.

    Args:
        output: Command output to parse.
        template_name: File name under the bundled ``ttp_templates`` directory.
        result_key: Optional top-level key to extract from the flattened result.
        templates: Optional mapping of template names to injected template content.

    Returns:
        A predictable flattened Python result suitable for facts parsers. Empty
        input or no matches returns an empty list.
    """
    if not output:
        return []

    template = _load_ttp_template(template_name, templates=templates)

    try:
        from ttp import ttp
    except ImportError as exc:
        raise ImportError(
            "The Python package 'ttp' is required for Xike OS facts parsing. "
            "Install it with `pip install ttp` or install this collection's "
            "Python dependencies."
        ) from exc

    parser = ttp(data=output, template=template)
    parser.parse(one=True)
    return _flatten_ttp_result(parser.result(), result_key=result_key)


def _load_ttp_template(template_name, templates=None):
    template_content = (templates or {}).get(template_name)
    if template_content is not None:
        return template_content

    template_path = os.path.join(TTP_TEMPLATE_DIR, template_name)
    if not os.path.isfile(template_path):
        raise FileNotFoundError(
            "Bundled TTP template '{0}' was not injected and was not found at '{1}'. "
            "Run through the module action plugin or reinstall the xike.xikeos collection and "
            "verify collection packaging includes plugins/module_utils/facts/ttp_templates/*.ttp.".format(
                template_name,
                template_path,
            )
        )

    with open(template_path, "r", encoding="utf-8") as template_file:
        return template_file.read()


def _flatten_ttp_result(result, result_key=None):
    flattened = result
    while isinstance(flattened, list) and len(flattened) == 1:
        flattened = flattened[0]

    if not flattened:
        return []

    if result_key is not None:
        if isinstance(flattened, dict):
            return _ensure_list(flattened.get(result_key, []))
        return []

    if isinstance(flattened, dict) and len(flattened) == 1:
        return _ensure_list(next(iter(flattened.values())))

    return flattened


def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

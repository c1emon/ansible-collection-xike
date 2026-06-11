"""Tests for the shared resource-module lifecycle helper."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import Mock

import pytest

from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.lifecycle import run_resource_module_lifecycle

from .lifecycle_helpers import ExitJson, fake_module


def _gather(module):
    return list(module.params.get("before", []))


def _build_commands(config, state, before):
    if state == "rendered":
        return ["render {0}".format(item["name"]) for item in config]
    before_names = {item["name"] for item in before}
    return ["set {0}".format(item["name"]) for item in config if item["name"] not in before_names]


def _build_after(before, config, state):
    after = {item["name"]: dict(item) for item in before}
    if state in ("merged", "replaced"):
        if state == "replaced":
            after = {}
        for item in config:
            after[item["name"]] = dict(item)
    elif state == "deleted":
        for item in config:
            after.pop(item["name"], None)
    return [after[name] for name in sorted(after)]


def test_resource_lifecycle_noop_returns_common_fields_without_apply():
    module = fake_module({"before": [{"name": "one"}]})
    apply_config = Mock()

    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(
            module,
            [{"name": "one"}],
            "merged",
            _gather,
            _build_commands,
            _build_after,
            apply_config=apply_config,
        )

    assert module.exit_json.call_args.kwargs == {
        "changed": False,
        "commands": [],
        "before": [{"name": "one"}],
        "after": [{"name": "one"}],
    }
    apply_config.assert_not_called()


def test_resource_lifecycle_changed_and_check_mode_flow():
    module = fake_module({"before": []}, check_mode=True)
    apply_config = Mock()

    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(
            module,
            [{"name": "one"}],
            "merged",
            _gather,
            _build_commands,
            _build_after,
            apply_config=apply_config,
        )

    assert module.exit_json.call_args.kwargs["changed"] is True
    assert module.exit_json.call_args.kwargs["commands"] == ["set one"]
    apply_config.assert_not_called()


def test_resource_lifecycle_changed_flow_applies_and_can_regather_after():
    module = fake_module({"before": [], "after": [{"name": "one"}]})
    apply_config = Mock()

    def gather(module):
        if apply_config.called:
            return module.params["after"]
        return module.params["before"]

    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(
            module,
            [{"name": "one"}],
            "merged",
            gather,
            _build_commands,
            _build_after,
            apply_config=apply_config,
            gather_after_apply=True,
        )

    apply_config.assert_called_once_with(module, ["set one"])
    assert module.exit_json.call_args.kwargs["after"] == [{"name": "one"}]


def test_resource_lifecycle_gathered_rendered_and_unsupported_states():
    gathered = fake_module({"before": [{"name": "one"}]})
    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(gathered, [], "gathered", _gather, _build_commands, _build_after)
    assert gathered.exit_json.call_args.kwargs == {"changed": False, "gathered": [{"name": "one"}]}

    rendered = fake_module({"before": []})
    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(rendered, [{"name": "one"}], "rendered", _gather, _build_commands, _build_after)
    assert rendered.exit_json.call_args.kwargs["changed"] is False
    assert rendered.exit_json.call_args.kwargs["commands"] == ["render one"]

    unsupported = fake_module({"before": []})
    unsupported.fail_json.side_effect = ExitJson
    with pytest.raises(ExitJson):
        run_resource_module_lifecycle(unsupported, [], "parsed", _gather, _build_commands, _build_after)
    assert "unsupported" in unsupported.fail_json.call_args.kwargs["msg"]

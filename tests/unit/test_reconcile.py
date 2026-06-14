"""Unit tests for the internal reconciliation planner."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.reconcile import (
    FieldPolicy,
    Operation,
    ReconciliationInputError,
    ResourcePolicy,
    UnsupportedRemovalError,
    apply_operations_to_state,
    plan_operations,
)


def test_planner_is_deterministic_and_emits_operations():
    policy = ResourcePolicy(
        identity=("name",),
        fields={
            "mode": FieldPolicy(kind="scalar", removal_supported=False),
            "members": FieldPolicy(kind="set", identity=()),
        },
    )
    current = {"eth-trunk 1": {"mode": "static", "members": ["0/0/1"]}}
    desired = {"eth-trunk 1": {"mode": "dynamic", "members": ["0/0/1", "0/0/2"]}}

    ops1 = plan_operations(current, desired, "replaced", policy)
    ops2 = plan_operations(current, desired, "replaced", policy)

    assert ops1 == ops2
    assert all(isinstance(operation, Operation) for operation in ops1)
    assert [operation.action for operation in ops1] == ["set_field", "add_item"]


def test_scalar_field_set_and_unsupported_unset_failure():
    policy = ResourcePolicy(
        identity=("name",),
        fields={"mode": FieldPolicy(kind="scalar", removal_supported=False)},
    )
    current = {"eth-trunk 1": {"mode": "static"}}
    desired = {"eth-trunk 1": {"mode": "dynamic"}}

    ops = plan_operations(current, desired, "replaced", policy)
    assert ops == [Operation("set_field", (("name", "eth-trunk 1"),), "mode", "dynamic")]

    with pytest.raises(UnsupportedRemovalError):
        plan_operations(current, {"eth-trunk 1": {"mode": None}}, "replaced", policy)


def test_set_field_add_and_remove_planning():
    policy = ResourcePolicy(
        identity=("name",),
        fields={"members": FieldPolicy(kind="set", identity=())},
    )
    current = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}
    desired = {"eth-trunk 1": {"members": ["0/0/2", "0/0/3"]}}

    ops = plan_operations(current, desired, "replaced", policy)

    assert [operation.action for operation in ops] == ["remove_item", "add_item"]
    assert [operation.value for operation in ops] == ["0/0/1", "0/0/3"]


def test_replaced_explicit_empty_set_removes_all_current_items():
    policy = ResourcePolicy(
        identity=("name",),
        fields={"members": FieldPolicy(kind="set", identity=())},
    )
    current = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}
    desired = {"eth-trunk 1": {"members": []}}

    ops = plan_operations(current, desired, "replaced", policy)
    after = apply_operations_to_state(current, ops, policy)

    assert [operation.action for operation in ops] == ["remove_item", "remove_item"]
    assert after == {"eth-trunk 1": {"members": []}}


def test_merged_set_fields_do_not_remove_current_only_items():
    policy = ResourcePolicy(
        identity=("name",),
        fields={"members": FieldPolicy(kind="set", identity=())},
    )
    current = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}
    desired = {"eth-trunk 1": {"members": ["0/0/2", "0/0/3"]}}

    ops = plan_operations(current, desired, "merged", policy)

    assert [operation.action for operation in ops] == ["add_item"]
    assert ops[0].value == "0/0/3"


def test_replaced_only_updates_listed_resources_and_explicit_fields():
    policy = ResourcePolicy(
        identity=("name",),
        fields={
            "mode": FieldPolicy(kind="scalar", removal_supported=False),
            "members": FieldPolicy(kind="set", identity=()),
        },
    )
    current = {
        "eth-trunk 1": {"mode": "static", "members": ["0/0/1", "0/0/2"]},
        "eth-trunk 2": {"mode": "dynamic", "members": ["0/0/8"]},
    }
    desired = {"eth-trunk 1": {"members": ["0/0/2", "0/0/3"]}}

    ops = plan_operations(current, desired, "replaced", policy)
    after = apply_operations_to_state(current, ops, policy)

    assert "eth-trunk 2" in after
    assert after["eth-trunk 2"] == {"mode": "dynamic", "members": ["0/0/8"]}
    assert after["eth-trunk 1"]["mode"] == "static"
    assert after["eth-trunk 1"]["members"] == ["0/0/2", "0/0/3"]


def test_apply_operations_to_state_is_deterministic():
    policy = ResourcePolicy(
        identity=("name",),
        fields={"members": FieldPolicy(kind="set", identity=())},
    )
    current = {"eth-trunk 1": {"members": ["0/0/2"]}}
    operations = [
        Operation("add_item", (("name", "eth-trunk 1"),), "members", "0/0/3"),
        Operation("remove_item", (("name", "eth-trunk 1"),), "members", "0/0/2"),
    ]

    after = apply_operations_to_state(current, operations, policy)

    assert after == {"eth-trunk 1": {"members": ["0/0/3"]}}


def test_malformed_input_fails_fast():
    policy = ResourcePolicy(identity=("name",), fields={"members": FieldPolicy(kind="set", identity=())})

    with pytest.raises(ReconciliationInputError):
        plan_operations(["not-a-mapping"], {}, "merged", policy)

    with pytest.raises(ReconciliationInputError):
        plan_operations({}, {"eth-trunk 1": {"members": "not-a-list"}}, "merged", policy)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class ReconciliationError(Exception):
    """Base error for reconciliation planning failures."""


class ReconciliationInputError(ReconciliationError):
    """Raised when policy or normalized input is malformed."""


class UnsupportedRemovalError(ReconciliationError):
    """Raised when a requested removal is not supported by policy."""


@dataclass
class FieldPolicy:
    kind: str
    identity: tuple[str, ...] = ()
    removal_supported: bool = True

    def __post_init__(self) -> None:
        if self.kind not in {"scalar", "set"}:
            raise ReconciliationInputError("unsupported field kind: {0}".format(self.kind))
        if not isinstance(self.identity, tuple):
            self.identity = tuple(self.identity)


@dataclass
class ResourcePolicy:
    identity: tuple[str, ...]
    fields: dict[str, FieldPolicy]

    def __post_init__(self) -> None:
        if not self.identity:
            raise ReconciliationInputError("resource identity must not be empty")
        if not isinstance(self.identity, tuple):
            self.identity = tuple(self.identity)
        if not isinstance(self.fields, dict):
            self.fields = dict(self.fields)


@dataclass(frozen=True)
class Operation:
    action: str
    resource: tuple[tuple[str, Any], ...]
    field: str
    value: Any = None


def resource_identity(resource: Mapping[str, Any], policy: ResourcePolicy) -> tuple[tuple[str, Any], ...]:
    """Build a canonical resource identity tuple from normalized resource data."""
    missing = [field for field in policy.identity if field not in resource]
    if missing:
        raise ReconciliationInputError(
            "resource is missing identity fields: {0}".format(", ".join(missing))
        )
    return tuple((field, resource[field]) for field in policy.identity)


def item_identity(item: Any, policy: FieldPolicy) -> tuple[tuple[str, Any], ...]:
    """Build a canonical set-item identity tuple from normalized item data."""
    if isinstance(item, Mapping):
        if policy.identity:
            missing = [field for field in policy.identity if field not in item]
            if missing:
                raise ReconciliationInputError(
                    "set item is missing identity fields: {0}".format(", ".join(missing))
                )
            return tuple((field, item[field]) for field in policy.identity)
        return tuple((key, item[key]) for key in sorted(item))

    if policy.identity:
        if len(policy.identity) != 1:
            raise ReconciliationInputError(
                "scalar set items require exactly one identity field when identity is configured"
            )
        return ((policy.identity[0], item),)

    return (("value", item),)


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _sort_token(identity: tuple[tuple[str, Any], ...]) -> str:
    return repr(identity)


def _resource_key_from_input(key: Any, resource: Mapping[str, Any], policy: ResourcePolicy) -> tuple[tuple[str, Any], ...]:
    if isinstance(key, tuple) and key and all(isinstance(entry, tuple) and len(entry) == 2 for entry in key):
        canonical_key = tuple((str(field), value) for field, value in key)
    elif len(policy.identity) == 1:
        canonical_key = ((policy.identity[0], key),)
    elif isinstance(key, tuple) and len(key) == len(policy.identity):
        canonical_key = tuple((field, value) for field, value in zip(policy.identity, key))
    else:
        canonical_key = resource_identity(resource, policy)

    resource_key = resource_identity(resource, policy) if all(field in resource for field in policy.identity) else canonical_key
    if resource_key != canonical_key and all(field in resource for field in policy.identity):
        raise ReconciliationInputError(
            "resource identity mismatch between key and data: {0} != {1}".format(canonical_key, resource_key)
        )
    return canonical_key


def _normalize_resource_map(resources: Any, policy: ResourcePolicy, label: str) -> dict[tuple[tuple[str, Any], ...], dict[str, Any]]:
    if resources is None:
        return {}
    if not isinstance(resources, Mapping):
        raise ReconciliationInputError("{0} state must be a mapping of resource identities to data".format(label))

    normalized: dict[tuple[tuple[str, Any], ...], dict[str, Any]] = {}
    for key, resource in resources.items():
        if not isinstance(resource, Mapping):
            raise ReconciliationInputError("{0} resource must be a mapping".format(label))
        canonical_key = _resource_key_from_input(key, resource, policy)
        if canonical_key in normalized:
            raise ReconciliationInputError("duplicate resource identity: {0}".format(canonical_key))
        normalized[canonical_key] = dict(resource)
    return normalized


def _normalize_set_items(
    values: Any,
    policy: FieldPolicy,
    label: str,
    resource_key: tuple[tuple[str, Any], ...],
    field_name: str,
) -> list[tuple[tuple[tuple[str, Any], ...], Any]]:
    if values is None:
        return []
    if not _is_sequence(values):
        raise ReconciliationInputError(
            "{0} set field {1} on resource {2} must be a list".format(label, field_name, resource_key)
        )

    normalized: list[tuple[tuple[tuple[str, Any], ...], Any]] = []
    for item in values:
        identity = item_identity(item, policy)
        normalized.append((identity, dict(item) if isinstance(item, Mapping) else item))
    return normalized


def _display_resource_key(identity: tuple[tuple[str, Any], ...]) -> Any:
    if len(identity) == 1:
        return identity[0][1]
    return tuple(value for _, value in identity)


def plan_operations(
    current: Any,
    desired: Any,
    state: str,
    policy: ResourcePolicy,
) -> list[Operation]:
    """Plan semantic operations for normalized resource state."""
    if state == "rendered":
        # Rendered mode plans desired commands from a synthetic current state;
        # merged semantics produce additive operations without gathering a device.
        state = "merged"
    if state not in {"merged", "replaced"}:
        raise ReconciliationInputError("unsupported reconciliation state: {0}".format(state))

    current_map = _normalize_resource_map(current, policy, "current")
    desired_map = _normalize_resource_map(desired, policy, "desired")
    operations: list[Operation] = []

    for resource_key in sorted(desired_map, key=_sort_token):
        current_resource = current_map.get(resource_key, {})
        desired_resource = desired_map[resource_key]

        for field_name, field_policy in policy.fields.items():
            desired_has = field_name in desired_resource
            current_has = field_name in current_resource

            if field_policy.kind == "scalar":
                if not desired_has:
                    continue
                desired_value = desired_resource[field_name]
                if desired_value is None:
                    if current_has and not field_policy.removal_supported:
                        raise UnsupportedRemovalError(
                            "removal is not supported for resource {0}, field {1}, state {2}".format(
                                resource_key, field_name, state
                            )
                        )
                    if current_has:
                        operations.append(Operation("unset_field", resource_key, field_name, None))
                    continue

                if (not current_has) or current_resource.get(field_name) != desired_value:
                    operations.append(Operation("set_field", resource_key, field_name, deepcopy(desired_value)))
                continue

            if not desired_has:
                continue

            desired_items = _normalize_set_items(desired_resource[field_name], field_policy, "desired", resource_key, field_name)
            current_items = _normalize_set_items(current_resource.get(field_name, []), field_policy, "current", resource_key, field_name)
            desired_by_id = {identity: value for identity, value in desired_items}
            current_by_id = {identity: value for identity, value in current_items}

            if state == "merged":
                for item_identity_value in sorted(desired_by_id, key=_sort_token):
                    if item_identity_value not in current_by_id:
                        operations.append(Operation("add_item", resource_key, field_name, deepcopy(desired_by_id[item_identity_value])))
                continue

            for item_identity_value in sorted(current_by_id, key=_sort_token):
                if item_identity_value not in desired_by_id:
                    if not field_policy.removal_supported:
                        raise UnsupportedRemovalError(
                            "removal is not supported for resource {0}, field {1}, state {2}".format(
                                resource_key, field_name, state
                            )
                        )
                    operations.append(Operation("remove_item", resource_key, field_name, deepcopy(current_by_id[item_identity_value])))

            for item_identity_value in sorted(desired_by_id, key=_sort_token):
                if item_identity_value not in current_by_id:
                    operations.append(Operation("add_item", resource_key, field_name, deepcopy(desired_by_id[item_identity_value])))

    return operations


def apply_operations_to_state(
    current: Any,
    operations: Sequence[Operation],
    policy: ResourcePolicy,
) -> dict[Any, dict[str, Any]]:
    """Apply planned operations to normalized state and return simulated after-state."""
    state_map = _normalize_resource_map(current, policy, "current")

    for operation in operations:
        if operation.field not in policy.fields:
            raise ReconciliationInputError("unknown field in operation: {0}".format(operation.field))
        field_policy = policy.fields[operation.field]
        resource_state = state_map.setdefault(operation.resource, {})

        if operation.action == "set_field":
            resource_state[operation.field] = deepcopy(operation.value)
            continue

        if operation.action == "unset_field":
            resource_state.pop(operation.field, None)
            continue

        if operation.action not in {"add_item", "remove_item"}:
            raise ReconciliationInputError("unsupported operation action: {0}".format(operation.action))

        existing_items = _normalize_set_items(resource_state.get(operation.field, []), field_policy, "state", operation.resource, operation.field)
        by_identity = {identity: value for identity, value in existing_items}
        payload_identity = item_identity(operation.value, field_policy)

        if operation.action == "add_item":
            by_identity[payload_identity] = deepcopy(operation.value)
        else:
            by_identity.pop(payload_identity, None)

        resource_state[operation.field] = [deepcopy(by_identity[item_identity_key]) for item_identity_key in sorted(by_identity, key=_sort_token)]

    return {
        _display_resource_key(resource_key): state_map[resource_key]
        for resource_key in sorted(state_map, key=_sort_token)
    }

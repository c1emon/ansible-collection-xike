from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence


"""Pure reconciliation helpers for normalized XikeOS resource state.

This module plans semantic operations from normalized resource dictionaries. It
does not import AnsibleModule, connect to a device, or render CLI commands. Each
resource module owns normalization and CLI rendering, while this module owns the
common state semantics for scalar fields and identity-based set fields.

Resource data is represented as a mapping keyed by resource identity, for
example::

    current = {"eth-trunk 1": {"mode": "static", "members": ["0/0/1"]}}
    desired = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}

Policies describe how to identify resources and set items. The planner then
returns operations such as ``set_field``, ``add_item``, and ``remove_item`` for
module-specific renderers to convert into XikeOS CLI.
"""


class ReconciliationError(Exception):
    """Base error for reconciliation planning failures."""


class ReconciliationInputError(ReconciliationError):
    """Raised when policy or normalized input is malformed."""


class UnsupportedRemovalError(ReconciliationError):
    """Raised when a requested removal is not supported by policy."""


class UnrenderedOperationError(ReconciliationError):
    """Raised when a semantic operation cannot be rendered completely."""


@dataclass
class FieldPolicy:
    """Describe reconciliation semantics for one resource field.

    Args:
        kind: ``"scalar"`` for single-value fields, or ``"set"`` for list fields
            whose items are compared by identity rather than list position.
        identity: Field names used to identify set items. Empty identity means
            the item itself is its identity, which is useful for scalar list
            items such as LAG member port strings.
        removal_supported: Whether the field can be removed/unset. If false,
            planning a removal raises :class:`UnsupportedRemovalError`.

    Examples:
        LAG mode is a scalar field::

            FieldPolicy(kind="scalar", removal_supported=False)

        L3 IPv4 addresses are set items identified by address and mask::

            FieldPolicy(kind="set", identity=("address", "subnet_mask"))

        LAG members are string set items::

            FieldPolicy(kind="set", identity=())
    """

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
    """Describe how a resource type is identified and reconciled.

    Args:
        identity: Resource-level identity fields. Current L3/LAG modules use
            ``("name",)`` so ``vlan-interface 10`` and ``eth-trunk 1`` are the
            resource keys.
        fields: Mapping of field name to :class:`FieldPolicy`.

    Example:
        Policy for a LAG resource::

            ResourcePolicy(
                identity=("name",),
                fields={
                    "mode": FieldPolicy(kind="scalar", removal_supported=False),
                    "lacp_mode": FieldPolicy(kind="scalar", removal_supported=True),
                    "members": FieldPolicy(kind="set", identity=()),
                },
            )
    """

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
    """A semantic resource operation produced by the planner.

    Operations are intentionally not CLI commands. Resource modules render them
    into the correct command context, such as ``interface vlan-interface 10``.

    Attributes:
        action: One of ``set_field``, ``unset_field``, ``add_item``, or
            ``remove_item``.
        resource: Canonical resource identity tuple, e.g.
            ``(("name", "eth-trunk 1"),)``.
        field: Resource field being changed.
        value: New scalar value or set item payload, depending on action.

    Example:
        Adding one LAG member yields::

            Operation(
                "add_item",
                (("name", "eth-trunk 1"),),
                "members",
                "0/0/2",
            )
    """

    action: str
    resource: tuple[tuple[str, Any], ...]
    field: str
    value: Any = None


@dataclass(frozen=True)
class ResourcePlan:
    """One immutable, fully rendered resource transition.

    The pure reconciler produces ``operations`` without CLI knowledge. A module
    renderer must acknowledge every operation before this object is created, so
    lifecycle code cannot report a changed/after result for a transition that
    has no command representation.
    """

    operations: tuple[Operation, ...]
    commands: tuple[str, ...]
    after: Any
    changed: bool


def resource_identity(resource: Mapping[str, Any], policy: ResourcePolicy) -> tuple[tuple[str, Any], ...]:
    """Build a canonical resource identity tuple from normalized resource data.

    Example:
        With ``ResourcePolicy(identity=("name",), fields={...})``::

            resource_identity({"name": "eth-trunk 1"}, policy)
            # (("name", "eth-trunk 1"),)
    """
    missing = [field for field in policy.identity if field not in resource]
    if missing:
        raise ReconciliationInputError(
            "resource is missing identity fields: {0}".format(", ".join(missing))
        )
    return tuple((field, resource[field]) for field in policy.identity)


def item_identity(item: Any, policy: FieldPolicy) -> tuple[tuple[str, Any], ...]:
    """Build a canonical set-item identity tuple from normalized item data.

    Dict items use the configured identity fields. Scalar list items use the
    item value when no identity fields are configured.

    Examples:
        IPv4 dict item identity::

            item_identity(
                {"address": "10.0.0.1", "subnet_mask": "255.255.255.0"},
                FieldPolicy(kind="set", identity=("address", "subnet_mask")),
            )
            # (("address", "10.0.0.1"), ("subnet_mask", "255.255.255.0"))

        LAG member string identity::

            item_identity("0/0/1", FieldPolicy(kind="set", identity=()))
            # (("value", "0/0/1"),)
    """
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
    """Normalize a caller-supplied map key into canonical resource identity.

    Resource maps may be keyed by a plain value (``"eth-trunk 1"``), a tuple of
    identity values, or a canonical identity tuple. If the resource payload also
    contains identity fields, the key and payload must agree.
    """
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
    """Validate and canonicalize a normalized resource-state mapping."""
    if resources is None:
        return {}
    if not isinstance(resources, Mapping):
        raise ReconciliationInputError("{0} state must be a mapping of resource identities to data".format(label))

    normalized: dict[tuple[tuple[str, Any], ...], dict[str, Any]] = {}
    for key, resource in resources.items():
        if not isinstance(resource, Mapping):
            raise ReconciliationInputError("{0} resource must be a mapping".format(label))
        if label == "desired":
            known_fields = set(policy.identity) | set(policy.fields)
            unknown_fields = sorted(set(resource) - known_fields)
            if unknown_fields:
                raise ReconciliationInputError(
                    "unknown desired fields for resource {0}: {1}".format(key, ", ".join(unknown_fields))
                )
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
    """Validate and canonicalize set-field items for identity comparison.

    Returns ``[(identity, value), ...]`` so callers can build dictionaries keyed
    by item identity while preserving the original item payload for operations.
    """
    if values is None:
        return []
    if not _is_sequence(values):
        raise ReconciliationInputError(
            "{0} set field {1} on resource {2} must be a list".format(label, field_name, resource_key)
        )

    normalized: list[tuple[tuple[tuple[str, Any], ...], Any]] = []
    seen: set[tuple[tuple[str, Any], ...]] = set()
    for item in values:
        identity = item_identity(item, policy)
        if identity in seen:
            raise ReconciliationInputError(
                "duplicate set item identity for resource {0}, field {1}: {2}".format(
                    resource_key, field_name, identity
                )
            )
        seen.add(identity)
        normalized.append((identity, dict(item) if isinstance(item, Mapping) else item))
    return normalized


def _display_resource_key(identity: tuple[tuple[str, Any], ...]) -> Any:
    """Convert canonical identity back to the public state-map key shape."""
    if len(identity) == 1:
        return identity[0][1]
    return tuple(pair_value for _field_name, pair_value in identity)


def plan_operations(
    current: Any,
    desired: Any,
    state: str,
    policy: ResourcePolicy,
) -> list[Operation]:
    """Plan semantic operations for normalized resource state.

    ``merged`` is additive for set fields: desired-only set items are added, but
    current-only set items are left untouched. ``replaced`` synchronizes only
    resources listed in ``desired`` and only fields explicitly present in each
    desired resource. Omitted fields are no-ops; explicit empty set fields remove
    current set items when removal is supported.

    Args:
        current: Current normalized resource state, keyed by resource identity.
        desired: Desired normalized resource state, keyed by resource identity.
        state: ``merged``, ``replaced``, or ``rendered``. Rendered maps to merged
            semantics because modules pass a synthetic current state.
        policy: Resource policy defining identities and field semantics.

    Returns:
        A deterministic list of semantic :class:`Operation` objects.

    Raises:
        ReconciliationInputError: If inputs, policies, or state are malformed.
        UnsupportedRemovalError: If the requested state requires a removal for a
            field whose policy disallows removal.

    Example:
        Add a LAG member without removing existing members in ``merged``::

            policy = ResourcePolicy(
                identity=("name",),
                fields={"members": FieldPolicy(kind="set", identity=())},
            )
            current = {"eth-trunk 1": {"members": ["0/0/1"]}}
            desired = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}

            plan_operations(current, desired, "merged", policy)
            # [Operation("add_item", (("name", "eth-trunk 1"),), "members", "0/0/2")]

        Synchronize members in ``replaced``::

            current = {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}
            desired = {"eth-trunk 1": {"members": ["0/0/2", "0/0/3"]}}

            plan_operations(current, desired, "replaced", policy)
            # remove_item("0/0/1"), add_item("0/0/3")
    """
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
                    raise ReconciliationInputError(
                        "canonical desired state must omit None for resource {0}, field {1}; "
                        "use an explicit typed reset when supported".format(resource_key, field_name)
                    )

                if (not current_has) or current_resource.get(field_name) != desired_value:
                    operations.append(Operation("set_field", resource_key, field_name, deepcopy(desired_value)))
                continue

            if not desired_has:
                continue

            desired_items = _normalize_set_items(desired_resource[field_name], field_policy, "desired", resource_key, field_name)
            current_items = _normalize_set_items(current_resource.get(field_name, []), field_policy, "current", resource_key, field_name)
            desired_by_id = dict(desired_items)
            current_by_id = dict(current_items)

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


def seal_resource_plan(
    current: Any,
    operations: Sequence[Operation],
    policy: ResourcePolicy,
    render_operation: Callable[[Operation], Sequence[str]],
    state: str,
) -> ResourcePlan:
    """Render every operation and return one immutable lifecycle plan.

    ``render_operation`` receives exactly one semantic operation and must return
    the complete command sequence needed for it, including any resource context.
    An empty result is an explicit error rather than a silent operation drop.
    """
    rendered: list[str] = []
    frozen_operations = tuple(operations)
    for operation in frozen_operations:
        commands = tuple(render_operation(operation))
        if not commands or any(not isinstance(command, str) or not command.strip() for command in commands):
            raise UnrenderedOperationError(
                "renderer did not produce complete commands for operation: {0}".format(operation)
            )
        rendered.extend(commands)

    after = apply_operations_to_state(current, frozen_operations, policy)
    commands_tuple = tuple(rendered)
    return ResourcePlan(
        operations=frozen_operations,
        commands=commands_tuple,
        after=after,
        changed=bool(commands_tuple) if state != "rendered" else False,
    )


def apply_operations_to_state(
    current: Any,
    operations: Sequence[Operation],
    policy: ResourcePolicy,
) -> dict[Any, dict[str, Any]]:
    """Apply planned operations and return deterministic simulated after-state.

    This helper is used by modules to produce check-mode or planned ``after``
    data without connecting to the device after rendering commands. It applies
    operations to a copy of the normalized current state and returns a state map
    keyed by display resource keys such as ``"eth-trunk 1"``.

    Example:
        Simulate adding one member::

            policy = ResourcePolicy(
                identity=("name",),
                fields={"members": FieldPolicy(kind="set", identity=())},
            )
            current = {"eth-trunk 1": {"members": ["0/0/1"]}}
            operations = [
                Operation("add_item", (("name", "eth-trunk 1"),), "members", "0/0/2")
            ]

            apply_operations_to_state(current, operations, policy)
            # {"eth-trunk 1": {"members": ["0/0/1", "0/0/2"]}}
    """
    state_map = _normalize_resource_map(current, policy, "current")

    for operation in operations:
        if operation.field not in policy.fields:
            raise ReconciliationInputError("unknown field in operation: {0}".format(operation.field))
        field_policy = policy.fields[operation.field]
        resource_state = state_map.setdefault(operation.resource, dict(operation.resource))

        if operation.action == "set_field":
            resource_state[operation.field] = deepcopy(operation.value)
            continue

        if operation.action == "unset_field":
            resource_state.pop(operation.field, None)
            continue

        if operation.action not in {"add_item", "remove_item"}:
            raise ReconciliationInputError("unsupported operation action: {0}".format(operation.action))

        existing_items = _normalize_set_items(resource_state.get(operation.field, []), field_policy, "state", operation.resource, operation.field)
        by_identity = dict(existing_items)
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

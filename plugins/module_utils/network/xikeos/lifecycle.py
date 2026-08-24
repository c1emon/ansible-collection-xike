from __future__ import absolute_import, division, print_function

__metaclass__ = type
# pylint: disable=unsupported-binary-operation

from typing import TYPE_CHECKING, Any, Callable, TypeVar

if TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule

from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.xikeos import (
    load_config,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.errors import (
    XikeOSError,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.reconcile import (
    ReconciliationError,
    ResourcePlan,
)
from ansible_collections.c1emon.xikeos.plugins.module_utils.network.xikeos.safety import (
    redact_value,
)


DEFAULT_MUTATING_STATES: tuple[str, ...] = (
    "merged",
    "replaced",
    "overridden",
    "deleted",
)
T = TypeVar("T")


def _exit(module: "AnsibleModule", **payload: Any) -> None:
    module.exit_json(**redact_value(payload))


def _fail(module: "AnsibleModule", **payload: Any) -> None:
    module.fail_json(**redact_value(payload))


def gather_with_error_boundary(
    module: "AnsibleModule",
    gather: Callable[[], T],
    msg: str,
    context: str,
    fallback: T,
    fail_kwargs: dict[str, Any] | None = None,
    include_exception_in_msg: bool = False,
) -> T:
    """Run a resource gather callback and convert failures into module errors."""
    payload = dict(fail_kwargs or {})
    try:
        return gather()
    except XikeOSError as exc:
        payload.update(
            msg=msg,
            error=str(exc),
            detail=getattr(exc, "detail", None),
            context=getattr(exc, "context", None) or context,
        )
        _fail(
            module,
            **payload,
        )
        return fallback
    except Exception as exc:
        fail_msg = "{0}: {1}".format(msg, exc) if include_exception_in_msg else msg
        payload.update(msg=fail_msg, error=str(exc), context=context)
        _fail(module, **payload)
        return fallback


def run_resource_module_lifecycle(
    module: "AnsibleModule",
    config: Any,
    state: str,
    gather: Callable[["AnsibleModule"], Any],
    build_commands: Callable[[Any, str, Any], list[str]],
    build_after: Callable[[Any, Any, str], Any],
    build_plan: Callable[[Any, str, Any], ResourcePlan] | None = None,
    mutating_states: tuple[str, ...] = DEFAULT_MUTATING_STATES,
    gathered_states: tuple[str, ...] = ("gathered",),
    rendered_states: tuple[str, ...] = ("rendered",),
    rendered_key: str = "rendered",
    rendered_current: Any = None,
    apply_config: Callable[["AnsibleModule", list[str]], Any] = load_config,
    gather_after_apply: bool = False,
) -> None:
    """Run the standard lifecycle for a Xike OS declarative resource module.

    The helper owns common result fields and control flow while callers keep
    resource-specific parsing, diffing, validation, and after-state simulation.

    Args:
        module: Active ``AnsibleModule`` instance, or an instance of a subclass
            or compatible test double. The helper calls its ``exit_json()``,
            ``fail_json()``, and reads ``check_mode``.
        config: Desired resource configuration from module params. The concrete
            shape is module-specific, commonly ``list[dict[str, Any]]`` for
            migrated resource modules. Falsy values are normalized to an empty
            list for no-op handling.
        state: Requested module state, such as ``merged``, ``replaced``,
            ``deleted``, ``gathered``, or ``rendered``.
        gather: Callback that gathers current resource state from the device.
            It receives ``module`` and returns the normalized ``before`` state.
        build_commands: Callback that computes command diffs. It receives
            ``config``, ``state``, and ``before``, then returns CLI commands.
        build_after: Callback that computes the expected ``after`` state for
            mutating executions. It receives ``before``, ``config``, and
            ``state``.
        build_plan: Optional sealed-plan callback. When supplied, it is the
            sole source of operations, commands, changed status, and simulated
            after-state; legacy ``build_commands``/``build_after`` callbacks
            are retained only for modules not yet migrated.
        mutating_states: States that are allowed to apply configuration.
        gathered_states: Non-mutating states that return gathered facts.
        rendered_states: Non-mutating states that return rendered commands.
        rendered_key: Result key used to expose rendered commands.
        apply_config: Callback used to apply commands to the device, normally
            ``load_config``.
        gather_after_apply: When true, gather current state again after a
            successful apply and use it as ``after``.

    Returns:
        None. This helper terminates module execution through ``exit_json()`` or
        ``fail_json()``.
    """
    config = config or []
    result: dict[str, Any] = {
        "changed": False,
        "commands": [],
        "before": [],
        "after": [],
    }

    if state in rendered_states:
        try:
            current = [] if rendered_current is None else rendered_current
            if build_plan is not None:
                commands = list(build_plan(config, state, current).commands)
            else:
                commands = build_commands(config, state, current)
        except ReconciliationError as exc:
            _fail(
                module,
                msg="failed to plan resource commands",
                changed=False,
                commands=[],
                error=str(exc),
                context="resource planning",
            )
            return
        _exit(module, changed=False, commands=commands, **{rendered_key: commands})

    try:
        before = gather(module)
    except XikeOSError as exc:
        _fail(
            module,
            msg="failed to gather resource state",
            changed=False,
            commands=[],
            before=[],
            after=[],
            gather_context=getattr(gather, "__name__", "resource gather"),
            error=str(exc),
            detail=getattr(exc, "detail", None),
            resource_commands=getattr(exc, "commands", None),
        )
        return
    result["before"] = before

    if state in gathered_states:
        _exit(module, changed=False, gathered=before)

    if state not in mutating_states:
        _fail(module, msg="unsupported resource module state: {0}".format(state))
        return

    if not config:
        result["after"] = before
        _exit(module, **result)

    try:
        plan = build_plan(config, state, before) if build_plan is not None else None
        commands = (
            list(plan.commands)
            if plan is not None
            else build_commands(config, state, before)
        )
    except ReconciliationError as exc:
        _fail(
            module,
            msg="failed to plan resource commands",
            changed=False,
            commands=[],
            before=before,
            after=before,
            error=str(exc),
            context="resource planning",
        )
        return
    result["commands"] = commands
    result["changed"] = plan.changed if plan is not None else bool(commands)
    if plan is not None:
        result["after"] = plan.after
    elif commands:
        try:
            result["after"] = build_after(before, config, state)
        except ReconciliationError as exc:
            _fail(
                module,
                msg="failed to plan resource commands",
                changed=False,
                commands=commands,
                before=before,
                after=before,
                error=str(exc),
                context="resource planning",
            )
            return
    else:
        result["after"] = before

    if module.check_mode:
        _exit(module, **result)

    if commands:
        try:
            apply_config(module, commands)
        except XikeOSError as exc:
            _fail(
                module,
                msg="failed to apply resource commands",
                changed=True,
                commands=commands,
                before=before,
                after=result["after"],
                partial_change=True,
                error=str(exc),
                detail=getattr(exc, "detail", None),
                resource_commands=getattr(exc, "commands", commands),
            )
            return
        if gather_after_apply:
            try:
                result["after"] = gather(module)
            except XikeOSError as exc:
                _fail(
                    module,
                    msg="failed to verify final state after applying resource commands",
                    changed=True,
                    commands=commands,
                    before=before,
                    after=result["after"],
                    verification_context="final-state",
                    error=str(exc),
                    detail=getattr(exc, "detail", None),
                    resource_commands=getattr(exc, "commands", None),
                )
                return

    _exit(module, **result)


def exit_rendered_or_fail(
    module: "AnsibleModule",
    module_name: str,
    config: Any,
    state: str,
    build_commands: Callable[[Any, str], list[str]],
    render_state: str,
) -> None:
    """Expose explicit rendered output and fail fast for unsafe mutating states.

    Args:
        module: Active ``AnsibleModule`` instance, or an instance of a subclass
            or compatible test double. The helper calls its ``exit_json()`` or
            ``fail_json()``.
        module_name: Human-readable module name used in the failure message.
        config: Desired resource configuration from module params. The concrete
            shape is module-specific, commonly ``dict[str, Any]`` for specialty
            modules. Falsy values return a no-op result.
        state: Requested module state. Only ``rendered`` is accepted as a
            non-mutating command-rendering state.
        build_commands: Callback that renders commands. It receives ``config``
            and ``render_state``.
        render_state: Existing command-builder state to use when rendering
            commands, for example ``merged`` or ``present``.

    Returns:
        None. This helper terminates module execution through ``exit_json()`` or
        ``fail_json()``.
    """
    result: dict[str, Any] = {"changed": False, "commands": []}
    if not config:
        _exit(module, **result)

    if state == "rendered":
        commands = build_commands(config, render_state)
        _exit(module, changed=False, commands=commands, rendered=commands)

    _fail(
        module,
        msg=(
            "{0} supports state=rendered only until lifecycle-safe gather, diff, "
            "and load_config apply support is implemented; state={1} is unsupported"
        ).format(module_name, state),
    )

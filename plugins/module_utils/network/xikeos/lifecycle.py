from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.xike.xikeos.plugins.module_utils.network.xikeos.xikeos import load_config


DEFAULT_MUTATING_STATES = ("merged", "replaced", "overridden", "deleted")


def run_resource_module_lifecycle(
    module,
    config,
    state,
    gather,
    build_commands,
    build_after,
    mutating_states=DEFAULT_MUTATING_STATES,
    gathered_states=("gathered",),
    rendered_states=("rendered",),
    rendered_key="rendered",
    apply_config=load_config,
    gather_after_apply=False,
):
    """Run the standard lifecycle for a Xike OS declarative resource module.

    The helper owns common result fields and control flow while callers keep
    resource-specific parsing, diffing, validation, and after-state simulation.
    """
    config = config or []
    result = {
        "changed": False,
        "commands": [],
        "before": [],
        "after": [],
    }

    before = gather(module)
    result["before"] = before

    if state in gathered_states:
        module.exit_json(changed=False, gathered=before)

    if state in rendered_states:
        commands = build_commands(config, state, before)
        module.exit_json(changed=False, commands=commands, **{rendered_key: commands})

    if state not in mutating_states:
        module.fail_json(msg="unsupported resource module state: {0}".format(state))
        return

    if not config:
        result["after"] = before
        module.exit_json(**result)

    commands = build_commands(config, state, before)
    result["commands"] = commands
    result["changed"] = bool(commands)
    result["after"] = build_after(before, config, state) if commands else before

    if module.check_mode:
        module.exit_json(**result)

    if commands:
        apply_config(module, commands)
        if gather_after_apply:
            result["after"] = gather(module)

    module.exit_json(**result)


def exit_rendered_or_fail(module, module_name, config, state, build_commands, render_state):
    """Expose explicit rendered output and fail fast for unsafe mutating states."""
    result = {"changed": False, "commands": []}
    if not config:
        module.exit_json(**result)

    if state == "rendered":
        commands = build_commands(config, render_state)
        module.exit_json(changed=False, commands=commands, rendered=commands)

    module.fail_json(
        msg=(
            "{0} supports state=rendered only until lifecycle-safe gather, diff, "
            "and load_config apply support is implemented; state={1} is unsupported"
        ).format(module_name, state)
    )

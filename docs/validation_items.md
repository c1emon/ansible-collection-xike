# Xike OS real-device validation items

The unit tests and manual review cover the reference architecture, but these items still require real switch validation before broad release:

- Prompt variants for user mode (`>`), privileged mode (`#`), global config (`(config)#`), interface config (`(config-if)#`), VLAN mode, AAA mode, and other sub-modes.
- Exact command error strings for invalid input, incomplete command, ambiguous command, permission denied, and authorization failure responses.
- Save behavior. The implementation uses `write memory` only when `xikeos_config save: true` is set; validate whether supported devices prefer `write memory`, `copy running-config startup-config`, or another command.
- Paging controls: validate `terminal length 0` and `terminal width 512` on each supported model and software version.

# XikeOS 命令证据登记

本登记为 `unify-xikeos-resource-architecture-and-safety` 的变更命令准入依据。软件
单元测试只能证明集合行为；只有此处记录的人工复核原始资料才可准入新的或语义改变的
设备写命令。

## 已复核来源

- 文件：`docs/三层配置手册.pdf`
- 页数：393
- SHA-256：`71f3428ea5948d8101ebd0fcef5eebafc3c540ebe0e2a14b747c76cbc26b2625`
- 适用范围：该资料中描述的三层交换机 CLI；并不单独证明所有 SKS8300 固件版本的
  物理兼容性。

`docs/manual_zh.md` 是该 PDF 的自动转换产物，不能独立作为命令依据。以下页码均已按
原始 PDF 的版式、命令格式与示例复核。

## 核心资源准入矩阵

| 资源 | 已准入命令与观察 | PDF 页 | 限制 / fail-closed 决定 |
| --- | --- | --- | --- |
| VLAN | `vlan`、`no vlan`、`description`、`show vlan` | 51、55 | VLAN 1 删除仍由模块策略拒绝。 |
| 基础接口 | `interface ethernet`、`description`/`no description`、`speed`/`no speed`、`duplex`/`no duplex`、`shutdown`/`no shutdown`、`show interface ethernet` | 41-47 | `mtu` 未在已复核页中准入；写入或重置 MTU 必须显式拒绝。 |
| 二层接口 | `switchport pvid`、`switchport link-type`、trunk/hybrid tagged/untagged VLAN 及对应 `no` 形式 | 43-45、52-54 | 显式空集合只可调用已准入的 `no switchport ... vlan` 形式；不推断全局清除。 |
| VLAN 三层接口 | `interface vlan-interface`、IPv4/IPv6 `ip address`/`ipv6 address` 与对应 `no`、`show ip/ipv6 interface vlan-interface` | 314-318 | 只拥有已解析并能回读的地址字段；未知接口字段不下发。 |
| LAG | `interface eth-trunk`、`no interface eth-trunk`、`link-aggregation mode`、成员增删、`lacp mode`/`no lacp mode`、LACP show | 162-166 | 仅向资料明确的子模式下渲染；未记录的 LACP 标量 reset 拒绝。 |
| IPv4 静态路由 | `ip route dst-net mask next-hop [distance]`、`no ip route dst-net mask [next-hop]`、`show ip route` | 330-331 | 同 destination/mask/next-hop 出现多个距离或无法确定删除范围时拒绝；不得用 `no ip route static all` 实现 `replaced`。 |
| IPv6 静态路由 | 无 | 无 | 所有会写入或删除 IPv6 静态路由的状态必须在渲染前拒绝，直到另有原始资料或设备证据。 |
| ACL | IP/MAC/混合 ACL 的 `access-list` 与 `no access-list ... [subitem/rule_id]`；`show access-list config/runtime` | 83-87 | 选择 positional 模型：资料显示子项编号可自动生成，但未给出可稳定回读的 sequence 数据。非空 `sequence`、ACL/rule `remark` 必须拒绝；变化仅使用已准入的整 ACL 或明确 rule-id 过渡。 |

## 使用规则

1. 每次变更现有正向、删除、CLI 模式、排序或验证行为时，必须更新本表并添加回归测试。
2. 已有 renderer 仅在命令序列逐字节保持不变时可作为软件兼容基线；不得据此宣称新增的物理兼容性。
3. 真实设备验证应单独记录型号、固件、输入、返回输出和观察结果；它补强而不替代本登记。

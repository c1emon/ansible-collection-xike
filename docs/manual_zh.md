# 兮克交换机三层配置手册

> 本文档由兮克三层交换机配置手册 PDF 自动转换生成。

> 验证说明：自动转换内容存在标题、表格和代码块错位。当前实现只将下列人工复核过的命令作为 command/config/VLAN 参考：`show version`、`show running-config`、`show startup-config`、`show vlan`、`configure terminal`、`end`、`vlan <vlan-id>`、`description <name>`、`no vlan <vlan-id>`、`terminal length 0`、`terminal width 512`、`write memory`（保存命令仍需真机确认）。其他损坏章节不得直接作为实现依据。

## 已验证实现参考：命令、配置与 VLAN

### 运行命令

```text
show version
show running-config
show startup-config
show vlan
```

### 终端与配置模式

```text
terminal length 0
terminal width 512
configure terminal
end
```

### VLAN 配置

```text
vlan <vlan-id>
description <name>
no vlan <vlan-id>
```

### 保存配置

```text
write memory
```

`write memory` is implemented only behind explicit `xikeos_config save: true` and remains an open real-device validation item.


# 1. 端口配置


## 1.1. interface ethernet


**命令功能**

进入端口配置模式

**命令格式**

```
interface ethernet port-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如 0/0/1 |


## 1.2. duplex


**命令功能**

在端口模式下配置端口双工模式，默认为auto

**命令格式**

```
duplex [auto | full | half]
No duplex
```


**参数说明**

*无*


## 1.3. speed


**命令功能**

在端口模式下用来配置端口速率，默认为auto

**命令格式**

```
speed [10|100|1000|10000|auto]
no speed
```


**参数说明**

*无*


## 1.4. priority


**命令功能**

在端口模式下配置端口优先级

**命令格式**

```
priority value
no priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 默认0 | 0-7 |


## 1.5. shutdown


**命令功能**

在端口模式下(取消)使能端口

**命令格式**

```
shutdown
no shutdown
```


**参数说明**

*无*


## 1.6. description


**命令功能**

在端口模式下（删除）配置端口描述信息

**命令格式**

```
(no)description string
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | 描述信息 | 除？号以外任意字符，空格需要加上双引号 |


## 1.7. switchport ethernet


**命令功能**

在vlan 模式下将端口加入或删除

**命令格式**

```
(no) switchport [ethernet port-id | all]
```


**参数说明**


## 1.8. ingress filtering


**命令功能**

在端口模式下添加或删除端口报文过滤

**命令格式**

```
(no) ingress filtering
```


**参数说明**

*无*


## 1.9. switchport pvid


**命令功能**

在端口模式下修改端口PVID

**命令格式**

```
(no) switchport pvid vlan-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | 取vlan id | 1-4094 |

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | 1.10. |

```
ingress acceptable-frame
```


**命令功能**

在端口模式下添加或删除端口下接收帧类型

**命令格式**

```
(no)ingress acceptable-frame [tagged | all | untagged]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| tagged | 只接收带tag 报文 | 无 |
| all | 所有报文都接收 | 无 |
| untagged | 只接收带untagged | 报文 |

无
```
switchport trunk allowed vlan
```


**命令功能**

在端口模式下添加或删除trunk 端口下所属vlan

**命令格式**

```
(no) switchport trunk allowed vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不支持空格，长度范围是 |
| 1-128。Vlan 范围1-4094 | all | 所有已配置vlan |

无
```
switchport hybrid untagged vlan
```


**命令功能**

在端口模式下添加或删除hybrid untagged 端口下所属vlan

**命令格式**

```
(no)switchport hybrid untagged vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不支持空格，长度范围是 |
| 1-128。vlan 范围1-4094 | all | 所有已配置vlan |

无
```
switchport hybrid tagged vlan
```


**命令功能**

在端口模式下添加或删除hybrid tagged 端口下所属vlan

**命令格式**

```
(no)switchport hybrid tagged vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，长度范围是1-128。vlan |
| 范围1-4094 | all | 所有已配置vlan |

无
```
switchport link-type
```


**命令功能**

在端口模式下配置端口的链路类型

**命令格式**

```
(no) switchport link-type [access | hybrid | trunk ]
```


**参数说明**

*无*

```
show interface ethernet
```


**命令功能**

查看端口信息

**命令格式**

```
show interface [enter |ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， |

```
show interface brief
```


**命令功能**

查看端口简要信息

**命令格式**

```
show interface brief [enter | ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， |

```
show description interface
```


**命令功能**

查看端口描述信息

**命令格式**

```
show description interface [enter | ethernet port-id]
```


**参数说明**

```
show ingress interface
```


**命令功能**

查看端口接收帧类型与过滤开关状态

**命令格式**

```
show ingress interface [enter | ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |
| 机：0/0/1-0/1/4 | 参数 | 参数说明 |
| 取值 | port-id | 端口号 |

根据交换机物理端口来定，

**配置举例**

```
DUT(config)#int ethernet 0/0/1         //进入端口
DUT(config-if-ethernet-0/0/1)#duplex full          //双工模式
DUT(config-if-ethernet-0/0/1)#speed 1000            //配置端口速率
DUT(config-if-ethernet-0/0/1)#priority 5         //配置端口优先级
DUT(config-if-ethernet-0/0/1)#shutdown       //down 掉端口
DUT(config-if-ethernet-0/0/1)#no shutdown          //使能端口
DUT(config-if-ethernet-0/0/1)#description test       //端口描述
DUT(config-if-ethernet-0/0/1)#switchport pvid 1        //配置端口pvid
DUT(config-if-ethernet-0/0/1)#ingress acceptable-frame tagged      //配置端口接收帧类型
DUT(config-if-ethernet-0/0/1)#switchport link-type trunk      //配置端口类型
DUT(config-if-ethernet-0/0/1)#switchport trunk allowed vlan all       //trunk 端口允许所有VLAN 通过
DUT(config-if-ethernet-0/0/1)#show int brief ethernet 0/0/1     //查看单个端口信息
Port    Desc   Link shutdn Speed         Pri PVID Mode TagVlan    UtVlan
e0/0/1  test   down false  f1000         5   1    trk  all        1
Total entries: 1 .
```


# 2. 端口统计


## 2.1.  show statistics interface


**命令功能**

查看端口统计详细信息

**命令格式**

```
show statistics interface brief [enter | ethernet port-id]
show statistics interface [enter | ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， |


## 2.2.  clear interface


**命令功能**

清除端口统计信息

**命令格式**

```
clear interface [enter | ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 2.3.  show cpu-statistics


**命令功能**

命令查看CPU 端口统计信息

**命令格式**

```
show cpu-statistics [enter | ethernet port-id]
```


**参数说明**


## 2.4.  clear cpu-statistics


**命令功能**

清除CPU 端口统计信息

**命令格式**

```
clear cpu-statistics
```


**参数说明**

*无*


## 2.5.  show statistics dynamic


**命令功能**

查看所有端口实时统计信息

**命令格式**

```
show statistics dynamic [interface|eth-trunk]
```

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， |


**参数说明**

*无*


## 2.6.  show statistics eth-trunk


**命令功能**

查看聚合端口统计信息

**命令格式**

```
show statistics eth-trunk id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 聚合组id | 1-16 |


## 2.7.  show utilization


**命令功能**

查看所有端口实时利用率

**命令格式**

```
show utilization interface
show utilization eth-trunk
```


**参数说明**

*无*


## 2.8.  配置举例

```
#查看单端口统计信息
DUT2(config)#show statistics interface ethernet 0/0/1
Port number  :  e0/0/1
last 5 minutes input rate 0 bits/sec, 0 packets/sec
last 5 minutes output rate 856 bits/sec, 1 packets/sec
64 byte packets:0
65-127 byte packets:0
128-255 byte packets:0
256-511 byte packets:0
512-1023 byte packets:0
1024-1518 byte packets:0
0 packets input, 0 bytes , 0 discarded packets
0 unicasts, 0 multicasts, 0 broadcasts
0 input errors, 0 FCS error, 0 symbol error, 0 false carrier
0 runts, 0 giants
1012 packets output, 100886 bytes, 0 discarded packets
0 unicasts, 512 multicasts, 500 broadcasts
0 output errors, 0 deferred, 0 collisions
0 late collisions
Total entries: 1.
```


# 3. MTU 配置


## 3.1. mtu


**命令功能**

端口下配置最大传输单元

**命令格式**

```
mtu <pkt-size>
no mtu
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pkt-size | 报文大小 | 64-16127 |


## 3.2. show mtu interface


**命令功能**

查看mtu 配置

**命令格式**

```
show mtu interface [enter | ethernet port-id]
```


**参数说明**

*无*


# 4. Lookback


## 4.1. loopback internal


**命令功能**

端口内环检测

**命令格式**

```
loopback internal
```


**参数说明**

*无*


## 4.2. loopback external


**命令功能**

端口外环检测

**命令格式**

```
loopback external
```


**参数说明**

*无*


# 5. 802.1Q 配置


## 5.1. vlan


**命令功能**

在全局创建vlan 或进入vlan 模式

**命令格式**

```
vlan vlan-list
no vlan [all|vlan-list]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是1-128。字符串范围1-4094 | all | 所有已配置vlan |

无

## 5.2. switchport


**命令功能**

在vlan 模式下将端口加入vlan

**命令格式**

```
(no) switchport [ethernet <port-id | all]
```


**参数说明**


## 5.3. switchport pvid


**命令功能**

在端口模式下修改PVID

**命令格式**

```
(no) switchport pvid vlan-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | 取vlan id | 1-4094 |


## 5.4. switchport link-type


**命令功能**

端口模式下修改端口的链路类型
| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | all |
| 所有端口 | 无 | 命令格式 |

```
(no) switchport link-type [ access | hybrid | trunk ]
```


**参数说明**

*无*


## 5.5. switchport trunk allowed vlan


**命令功能**

端口模式下配置trunk 端口下所属vlan

**命令格式**

```
(no) switchport trunk allowed vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是1-128。字符串范围1-4094 | all | 所有已配置vlan |

无

## 5.6. switchport hybrid untagged vlan


**命令功能**

端口下修改hybrid 端口 untagged vlan

**命令格式**

```
(no)switchport hybrid untagged vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是1-128。字符串范围1-4094 | all | 所有已配置vlan |

无

## 5.7. switchport hybrid tagged vlan


**命令功能**

端口下修改hybrid 端口tagged vlan

**命令格式**

```
(no)switchport hybrid tagged vlan [vlan-list|all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-list | 取VLAN id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是1-128。字符串范围1-4094 | all | 所有已配置vlan |

无

## 5.8. priority


**命令功能**

端口模式下修改优先级

**命令格式**

```
(no)priority value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 取优先级 | 0-7 默认0 |


## 5.9. ingress acceptable-frame


**命令功能**

端口模式下修改端口接收帧类型

**命令格式**

```
(no)ingress acceptable-frame [tagged|all|untagged]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| tagged | 只接收带tag 报文 | 无 |
| all | 所有报文都接收 | 无 |
| untagged | 只接收带untagged | 报文 |

无
```
ingress filtering
```


**命令功能**

端口模式下开启端口报文过滤

**命令格式**

```
(no) ingress filtering
```


**参数说明**

*无*

description

**命令功能**

Vlan 模式下配置vlan 名称

**命令格式**

```
(no)description string
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | 端口描述 | <1-128>除？号以外任意字符，空格需要加 |

上双引号
```
show vlan
```


**命令功能**

查看vlan 信息

**命令格式**

```
Show vlan [enter |vlan-id ]
Show vlan brief [enter | vlan-id | interface ethernet port-id]
```


**参数说明**

*无*


**配置举例**

```
DUT(config)#
DUT(config)#vlan 1-4094                   //创建vlan
DUT(config-if-vlan-1-4094)#switchport ethernet 0/0/1       //给vlan 添加端口
DUT(config-if-vlan-1-4094)#int ethernet 0/0/1                //进入端口模式
DUT(config-if-ethernet-0/0/1)#switchport pvid 2       //修改端口pvid
DUT(config-if-ethernet-0/0/1)#switchport link-type trunk          //配置端口类型
DUT(config-if-ethernet-0/0/1)#switchport trunk allowed vlan 20      //配置允许通过的vlan
DUT(config-if-ethernet-0/0/1)#show int brief         //查看端口信息
Port    Desc   Link shutdn Speed         Pri PVID Mode TagVlan    UtVlan
e0/0/1  test   down false  f1000         5   2    trk  all        2
e0/0/2         down false  auto          0   1    hyb             1
e0/0/3         down false  auto          0   1    hyb             1
e0/0/4         down false  auto          0   1    hyb             1
e0/0/5         down false  auto          0   1    hyb             1
e0/0/6         down false  auto          0   1    hyb             1
e0/0/7         down false  auto          0   1    hyb             1
e0/0/8         down false  auto          0   1    hyb             1
e0/0/9         up   false  auto-f1000    0   1    hyb             1
e0/0/10        up   false  auto-f1000    0   1    hyb             1
e0/0/11        up   false  auto-f1000    0   1    hyb             1
e0/0/12        up   false  auto-f1000    0   1    hyb             1
e0/0/13        down false  auto          0   1    hyb             1
e0/0/14        up   false  auto-f1000    0   1    hyb             1
e0/0/15        down false  auto          0   1    hyb             1
e0/0/16        down false  auto          0   1    hyb             1
e0/0/17        down false  auto          0   1    hyb             1
e0/0/18        down false  auto          0   1    hyb             1
e0/0/19        down false  auto          0   1    hyb             1
e0/0/20        down false  auto          0   1    hyb             1
e0/0/21        down false  auto          0   1    hyb             1
e0/0/22        down false  auto          0   1    hyb             1
e0/1/1         down false  auto          0   1    hyb             1
e0/1/2         down false  auto          0   1    hyb             1
Total entries: 24 .
```


# 6. Mac-vlan 配置


## 6.1. mac-vlan mac-address


**命令功能**

配置mac vlan 转发表

**命令格式**

```
(no)mac-vlan mac-address mac-add vlan-id pri
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Mac-add | mac 地址 | 可用有效mac 地址 |
| vlan-id | Vlan id | 1-4094 |
| pri | 优先级 | 0-7 |


## 6.2. no mac-vlan mac-address


**命令功能**

删除macc vlan 转发表

**命令格式**

```
no mac-vlan
```


**参数说明**

*无*


## 6.3. show mac-vlan mac-address


**命令功能**

查看 mac vlan 配置

**命令格式**

```
show mac-vlan [enter | mac-address mac-address]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-address | mac 地址 | 可用有效mac 地址 |


## 6.4. 配置举例

```
DUT(config)#mac-vlan mac-address 00:00:00:1:2:3 vlan 2 priority 5    //配置mac-vlan
DUT(config)#show mac-vlan mac-address 00:00:00:1:2:3      //查看mac-vlan
MAC Address        VLAN ID  Priority  Status
00:00:00:01:02:03     2     5         active
Total active entries: 1.
Total inactive entries: 0.
```


# 7. Ip-subnet-vlan 配置


## 7.1. Ip-subnet-vlan IPv4 a.b.c.d


**命令功能**

配置基于ip 子网的vlan 转发表

**命令格式**

```
(no)ip-subnet-vlan ipv4 ipadd mask mask vlan vlan-id priority pri
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipadd | Ip 地址 | 可用有效ip 地址 |
| mask | 掩码 | 0.0.0.0-255.255.255.255 |
| vlan-id | Vlan id | 1-4094 |
| pri | 优先级 | 0-7 |


## 7.2. no ip-subnet-vlan


**命令功能**

删除所有基于ip 子网vlan 的转发表

**命令格式**

```
no ip-subnet-vlan
```


**参数说明**

*无*


## 7.3. ip-subnet-vlan precede


**命令功能**

(取消)使能ip-subnet-vlan 优先mac-vlan 转发

**命令格式**

```
(no)ip-subnet-vlan precede
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipadd | Ip 地址 | 可用有效ip 地址 |
| mask | 掩码 | 0.0.0.0-255.255.255.255 |


## 7.4. show ip-subnet-vlan


**命令功能**

查看基于子网vlan 的所有配置

**命令格式**

```
show ip-subnet-vlan ipv4 [ipadd mask]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipadd | Ip 地址 | 可用有效ip 地址 |
| mask | 掩码 | 0.0.0.0-255.255.255.255 |


## 7.5. 配置举例

```
DUT(config)#ip-subnet-vlan ipv4 192.168.1.1 mask 255.0.0.0 vlan 1 priority 4   //配置ip-subnet-vlan
DUT(config)#ip-subnet-vlan precede        //配置子网优先匹配
DUT(config)#show ip-subnet-vlan              //查看ip-subnet-vlan
The precedence of ip-subnet-based VLAN is higher than mac-based VLAN.
IP Address   IP Mask    VLAN ID  Priority  Status
192.168.1.1  255.0.0.0     1     4         active
Total active entries: 1.
Total inactive entries: 0.
```


# 8. protocol-vlan 配置


## 8.1. protocol-vlan profile id frame-type ethernet2 ether-type


**命令功能**

配置protocol-vlan 转发表中的frame-type

**命令格式**

```
(no)protocol-vlan profile profile-id frame-type ethernet2 ether-type value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Profile-id | 表项ID | 1-8 |
| value | Etherenet type | 1-FFFF |


## 8.2. protocol-vlan profile id vlan vid


**命令功能**

配置protocol-vlan 转发表中的vlan

**命令格式**

```
protocol-vlan profile profile-id vlan vid [priority priority]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Profile-id | 表项ID | 1-8 |
| vid | Vlan 取值 | 1-4094 |
| priority | 优先级 | 0-7，可选参数 |


## 8.3. protocol-vlan


**命令功能**

端口模式下（取消）使能protocol-vlan

**命令格式**

```
(no) protocol-vlan profile
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Profile-id | 表项ID | 1-3 |


## 8.4. no protocol-vlan profile id


**命令功能**

删除protocol-vlan 转发表

**命令格式**

```
no protocol-vlan profile [ enter | profile-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Profile-id | 表项ID | 1-3 |


## 8.5. show protocol-vlan profile


**命令功能**

查看protocol-vlan 转发表配置

**命令格式**

```
show protocol-vlan profile [id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Profile-id | 表项ID | 1-8 |


## 8.6. show protocol-vlan interface


**命令功能**

查看端口使能配置

**命令格式**

```
show protocol-vlan interface [enter|ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据设备而定，格式般是0/0/1 |


## 8.7. 配置举例

```
DUT(config)#protocol-vlan profile 1 frame-type ethernet2 ether-type 8035
DUT(config)#protocol-vlan profile 1 vlan 2
DUT(config-if-ethernet-0/0/1)#protocol-vlan
DUT(config)#interface ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#show protocol-vlan interface ethernet 0/0/1
Port    Profile Index VLAN ID ActionStatus
e0/0/1  1             2       active
Total port entries: 1.
Total active action entries: 1.
Total inactive action entries: 0.
```


# 9. vlan-trunking 配置


## 9.1. vlan-trunking mode


**命令功能**

配置vlan-trunking 模式

**命令格式**

```
vlan mode [auto | manual]
no vlan-trunking mode
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| auto | 自动模式，开启后则所有VLAN 都能透传,不需 | 要手动创建静态VLAN. |
| 无 | manual | 手动模式，开启后, 已经存在的手动创建的静 |
| 态VLAN 都能透传。 | 无 | 9.2. vlan-trunking |


**命令功能**

端口下(取消)使能vlan-trunking

**命令格式**

```
[no]vlan-trunking
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-trunking | 1. 需要先在全局配置mode，并且端口必须是trunk。 | 2. 当mode=manual 时，端口下开启vlan-trunking，会 |
| 自动配置透传vlan：switchport trunk allowed | vlan ……；如果再配置no switchport trunk allowed | vlan ……会导致vlan 报文无法转发； |
| 3. 当mode=manual 时，端口需要关闭功能时：必须配 | 置两条命令：no vlan-trunking，no switchport trunk | allowed vlan ……； |

无

## 9.3. show vlan-trunking


**命令功能**

查看配置

**命令格式**

```
show vlan-trunking
```


**参数说明**

*无*


# 10. vlan-swap 配置

```
vlan swap
```


**命令功能**

端口模式下配置vlan 转换

**命令格式**

```
vlan swap <startid> <endid> <swapid><priority value>
no vlan swap <startid> <endid>
no vlan swap all
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| startid | Start vlan id | 1-4094 |
| endid | End vlan id | 1-4094 |
| swapid | Swap vlan id | 1-4094 |
| priority value | 优先级 | 0-7 |


# 11. QinQ 配置

qinq

**命令功能**

全局模式开启(关闭)qinq 功能

**命令格式**

qinq
```
no qinq
```


**参数说明**

*无*

```
qinq inner-tpid
```


**命令功能**

配置 inner-tpid

**命令格式**

（no）qinq inner-tpid <protocol-number>

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| protocol-number | 协议号 | 1-ffff,默认8100 |

```
qinq outer-tpid
```


**命令功能**

配置outer-tpid

**命令格式**

（no）qinq outer-tpid <protocol-number>

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| protocol-number | 协议号 | 1-ffff，默认8100 |

```
qinq mode
```


**命令功能**

端口下配置qinq 模式，默认uplink

**命令格式**

```
qinq mode [customer | uplink]
no qinq mode
```


**参数说明**

*无*

```
vlan insert
```


**命令功能**

在端口下配置qinq 插入vlan

**命令格式**

```
vlan insert <start-vlan><end-vlan><service-vlan><priority>
no vlan insert <start-vlan><end-vlan>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-vlan | 超始vlan | 1-4094 |
| end-vlan | 结束vlan | 1-4094 |
| service-vlan | service VLAN | 1-4094 |
| priority | 优先级 | 0-7 |

```
vlan pass-through
```


**命令功能**

端口下配置透传vlan

**命令格式**

```
vlan pass-through <start-vlan>< end-vlan>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-vlan | 超始vlan | 1-4094 |
| end-vlan | 结束vlan | 1-4094 |

```
no vlan pass-through
```


**命令功能**

在端口下删除透传vlan

**命令格式**

```
no vlan pass-through <start-vlan ><end-vlan>
no vlan pass-through all
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-vlan | 超始vlan | 1-4094 |
| end-vlan | 结束vlan | 1-4094 |

```
show qinq
```


**命令功能**

查看qinq 配置信息

**命令格式**

```
show qinq
```


**参数说明**

*无*

```
show flexible-vlan interface
```


**命令功能**

查看灵活qinq 配置信息

**命令格式**

```
show flexible-vlan interface [enter | ethernet portid]
```


**参数说明**

*无*


## 11.10. 配置举例

如图
```
TCA ----1 DUT 2 -------TCB
1. 创建vlan1-200，并包含端口1，2
dut1(config)#vlan 1-200
dut1(config-vlan-range)#switchport ethernet 0/0/1 ethernet 0/0/2
dut1(config-vlan-range)#interface eth 0/0/2
dut1(config-if-ethernet-0/0/2)#switchport hybrid tagged vlan all
2. 全局开启qinq，端口1 配置为customer 模式
dut1(config)#qinq
dut1(config)#interface eth 0/0/1
dut1(config-if-ethernet-0/0/1)#qinq mode customer
3. 端口下配置vlan insert 10-20，服务vlan 为100
dut1(config-if-ethernet-0/0/1)#vlan insert 10 20 100 5
4. TCA 发送vlan10 的报文，TCB 抓包查看
TCB 抓到的双tag 报文：inner-tag=10,outer-tag=100;
```


# 12. MAC 地址管理

```
mac-address-table learning
```


**命令功能**

在全局或端口下（取消）使能mac 地址学习

**命令格式**

```
mac-address-table learning
no mac-address-table learning
```


**参数说明**

*无*

```
mac-address-table age-time time
```


**命令功能**

配置MAC 地址老化时间

**命令格式**

```
mac-address-table age-time second
no mac-address-table age-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| second | MAC 地址老化时 | 间，单位秒。默 |
| 认为300s | 10-1000000 | 12.3. |

```
mac-address-table age-time disable
```


**命令功能**

关闭MAC 地址老化功能

**命令格式**

```
mac-address-table age-time disable
```


**参数说明**

*无*

```
mac-address-table permanent
```


**命令功能**

配置永久MAC 地址表

**命令格式**

```
mac-address-table permanent <mac-add> interface ethernet <port-id> vlan <vlan-id>
no mac-address-table permanent <mac-add> [interface ethernet port-id] vlan <vlan-id>
no mac-address-table permanent vlan <vlan-id>
no mac-address-table permanent interface ethernet <port-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-add | MAC 地址 | 48 位二进制数，格式为X:X:X:X:X:X |
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |
| 机：0/0/1-0/1/4 | vlan-id | 取vlan id |

1-4094
```
mac-address-table static
```


**命令功能**

配置静态MAC 地址

**命令格式**

```
mac-address-table static <mac-add> interface ethernet <port-id> vlan <vlan-id>
no mac-address-table static <mac-add> [interface ethernet port-id] vlan <vlan-id>
no mac-address-table static vlan <vlan-id>
no mac-address-table static interface ethernet <port-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-add | MAC 地址 | 48 位二进制数，格式为X:X:X:X:X:X |
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |
| 机：0/0/1-0/1/4 | vlan-id | 取vlan id |

1-4094
```
mac-address-table dynamic
```


**命令功能**

配置动态MAC 地址表

**命令格式**

```
mac-address-table dynamic <mac-add> interface ethernet <port-id> vlan <vlan-id>
no mac-address-table dynamic <mac-add> [interface ethernet port-id] vlan <vlan-id>
no mac-address-table dynamic vlan <vlan-id>
no mac-address-table dynamic interface ethernet <port-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-add | MAC 地址 | 48 位二进制数，格式为X:X:X:X:X:X |
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |
| 机：0/0/1-0/1/4 | vlan-id | 取vlan id |

1-4094
```
mac-address-table blackhole
```


**命令功能**

配置黑洞MAC 地址表

**命令格式**

```
mac-address-table blackhole <mac-add> vlan <vlan-id>
no mac-address-table blackhole <mac-add> vlan <vlan-id>
no mac-address-table blackhole vlan <vlan-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-add | MAC 地址 | 48 位二进制数，格式为X:X:X:X:X:X |
| vlan-id | 取vlan id | 1-4094 |

```
mac-address-table max-mac-count
```


**命令功能**

端口模式或vlan 模式下配置mac 地址学习数量

**命令格式**

```
(no)mac-address-table max-mac-count count
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| count | Mac 地址个数 | 1-40976,默认最大值，不能设置取值不同 |

```
mac-address-table control-learning
```


**命令功能**

(取消)使能mac 地址学控制

**命令格式**

```
(no) mac-address-table control-learning
```


**参数说明**

*无*


## 12.10. show mac-address-table max-mac-count


**命令功能**

查看MAC 学习数量限制配置信息

**命令格式**

```
Show mac-address max-mac-count interface ethernet port-id
Show mac-address max-mac-count vlan vlan-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 不同设备取值不同 |
| Vlan-id | Vlan id | 1-4094 |


## 12.11. show mac-address-table age-time


**命令功能**

查看MAC 地址老化时间配置信息

**命令格式**

```
show mac-address-table age-time
```


**参数说明**

*无*


## 12.12. show mac-address-table


**命令功能**

查看MAC 地址表

**命令格式**

```
show mac-address-table
show mac-address-table ethernet port-id
show mac-address-table ethernet port-id vlan vlan-id
show mac-address-table vlan vlan-id
show mac-address-table static [ethernet |eth-trunk] <port-id> vlan <vlan-id>
show mac-address-table permanent [ethernet |eth-trunk] <port-id> vlan <vlan-id>
show mac-address-table dynamic [ethernet |eth-trunk] <port-id> vlan <vlan-id>
show mac-address-table blackhole [vlan <vlan-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， |
| vlan-id | 取vlan id | 1-4094 |


## 12.13. show mac-address-table learning


**命令功能**

查看mac 地址学习状态，默认使能

**命令格式**

```
show mac-address-table learning interface [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 不同设备取值不同，格式0/0/1 |


## 12.14. 配置举例

```
DUT(config)#mac-address-table permanent 00:00:00:01:02:03 interface ethernet 0/0/1 vlan 1//配置静态mac 地址
DUT(config)#int ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#mac-address-table max-mac-count 250    //配置端口mac 地址最大学习数
DUT(config-if-ethernet-0/0/1)#show mac-address-table      //查看mac 地址表
MAC Address           VLAN ID  port     status
00:00:00:01:02:03     1        0/0/1    static
00:0a:6a:00:00:06     1        0/0/10   dynamic
80:1f:02:4c:19:60     1        0/0/14   dynamic
Total entries: 3 .
DUT(config-if-ethernet-0/0/1)#show mac-address-table max-mac-count interface ethernet 0/0/1   //查看单个端
口mac 地址最大学习数
Port        Mac address max count
e0/0/1      250
Total entries: 1
DUT(config)#mac-address-table age-time 250        //配置mac 地址老化时间
DUT(config)#show mac-address-table age-time
mac address table agingtime is 250 seconds.
```


# 13. 流量控制配置

flow-control

**命令功能**

(取消)使能流控功能

**命令格式**

（no）flow-control

**参数说明**

*无*

```
show flow-control interface
```


**命令功能**

查看流控配置

**命令格式**

```
show flow-control interface [ethernet port-id]
```


**参数说明**

*无*


**配置举例**

```
DUT(config)#int ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#flow-control
DUT(config-if-ethernet-0/0/1)#show flow-control interface ethernet 0/0/1
port    flow-control-state
e0/0/1  enable
Total entries: 1.
```


# 14. 带宽控制配置

```
bandwidth ingress kbps
```


**命令功能**

在端口模式下配置入方向的带宽限速

**命令格式**

```
(no)bandwidth ingress [kbps | percent] <rate>
no bandwidth ingress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 限制的具体带宽 | 64-10000000 |

```
bandwidth ingress kbps
```


**命令功能**

在端口模式下配置出方向的带宽限速

**命令格式**

```
bandwidth egress [kbps | percent] <rate>
no bandwidth egress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 限制的具体带宽 | 64-10000000 |

```
show bandwidth interface
```


**命令功能**

查看端口的带宽限速配置

**命令格式**

```
show bandwidth interface [enter | ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，格式0/0/1 |


**配置举例**

```
DUT(config)#
DUT(config)#int ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#bandwidth egress kbps 64
DUT(config-if-ethernet-0/0/1)#show bandwidth interface ethernet 0/0/1
Port-bandwith informations:
port      egress bandwidth
e0/0/1    64kbps
DUT(config-if-ethernet-0/0/1)#
```


# 15. Dlf-Control 配置

```
unknown-discard unicast vlan
```


**命令功能**

(取消)使能丢弃指定vlan 的未知单播报文功能

**命令格式**

```
(no)unknown-discard unicast vlan <vid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | vlan id | 1-4094 |

```
unknown-discard multicast vlan
```


**命令功能**

(取消)使能丢弃指定vlan 的未知组播报文功能

**命令格式**

```
(no)unknown-discard multicast vlan <vid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | vlan id | 1-4094 |

```
show unknown-discard vlan
```


**命令功能**

查看未知报文丢弃功能配置

**命令格式**

```
show unknown-discard vlan [enter | vid]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | vlan id | 1-4094 |


# 16. Local-Switch 配置

local-switch

**命令功能**

端口模式下配置本地转发功能

**命令格式**

```
(no)local switch
```


**参数说明**

*无*

```
show local-switch
```


**命令功能**

查看本地转发配置信息

**命令格式**

```
show local-switch
```


**参数说明**

*无*


# 17. 端口镜像配置

```
mirror group id source-interface
```


**命令功能**

配置镜像源

**命令格式**

```
mirror group <group-id> source-interface ethernet <port-id> [ingress | egress | both]
mirror group <group-id> source-interface cpu [ingress | egress | both]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-id | 组号 | 1-3 |
| port-id | 端口号 | 根据交换机物理端口来定 |

```
mirror group id destination-interface
```


**命令功能**

配置镜像目的端口

**命令格式**

```
mirror group group-id destination-interface ethernet <port-id>
```


**参数说明**

*无*

```
no mirror group
```


**命令功能**

删除镜像组

**命令格式**

```
no mirror group all
no mirror group group-id
no mirror group group-id source-interface [ cpu | ethernet <port-id >]
no mirror group group-id destination-interface ethernet <port-id >
```


**参数说明**

*无*

```
show mirror group
```


**命令功能**

查看镜像配置信息

**命令格式**

```
show mirror group [all|group-id]
```


**参数说明**

*无*


**配置举例**

//配置镜像组2:镜像 1-5 端口的入方向报文
```
DUT(config)#mirror group 2 source-interface ethernet 0/0/1 to ethernet 0/0/5 ingress
//配置镜像组2:镜像目的端口 7
DUT(config)#mirror group 2 destination-interface ethernet 0/0/7
DUT(config)#show mirror group 2
Information about mirror groups:
Group number                : 2
The monitor port            : e0/0/7
The mirrored egress ports   :
The mirrored ingress ports  : e0/0/1-e0/0/5.
Total entries: 1 .
```


# 18. Sflow 配置

```
sflow agent
```


**命令功能**

配置采样本地代理地址

**命令格式**

```
sflow agent [ip <ip> | ipv6 <ipv6>]
no sflow agent
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 代理所使用的 | IPv4 地址 |
| X.X.X.X，X∈ [0-255] | ipv6 | 代理所使用的 |
| IPv6 地址 | XXXX:XXXX:XXXX:XXXX:XXXX:XXXX: | XXXX:XXX，X∈ [0-F]十六进制 |

```
sflow collector
```


**命令功能**

配置采样远端收集者

**命令格式**

```
sflow collect <Id> [ip <ip> | ipv6 <ipv6>] owner <owner> [datagram-size <size>] [time-
out <time-value>] [port <port>]
no sflow collect <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 收集者ID | [1-10] |
| ip | 代理所使用的 | X.X.X.X，X∈ [0-255] |
| IPv4 地址 | ipv6 | 代理所使用的 |
| IPv6 地址 | XXXX:XXXX:XXXX:XXXX:XXXX:XXXX: | XXXX:XXX，X∈ [0-F]十六进制 |
| owner | 拥有者 | 1-127 个字符 |
| size | 数据包大小 | [256-1400] |
| time-value | 超时时间 | [30-2147483647] |
| port | Sflow 协议端口号 | [1-2147483647] |

```
sflow counter collector id
```


**命令功能**

端口下配置counter 采样并关联collector

**命令格式**

```
(no)sflow counter collector <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 收集者ID | [1-10] |

```
sflow counter interval
```


**命令功能**

端口下配置Counter 采样周期

**命令格式**

```
(no)sflow counter interval <interval>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Interval | 采样周期 | [3-2147483647] |

```
sflow flow collector id
```


**命令功能**

端口下配置flow 采样并关联collector

**命令格式**

```
(no)sflow flow collector <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 收集者ID | [1-10] |

```
sflow flow sampling-rate
```


**命令功能**

端口下配置flow 采样速率

**命令格式**

```
(no)sflow flow sampling-rate <rate>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 采样速率 | 1-32767 |

```
sflow flow max-header
```


**命令功能**

端口下配置Flow 采样原始报文从头部开始截取长度

**命令格式**

```
(no)sflow flow max-header <size>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| size | 采样报文内容截 | 取长度 |

64-128
```
show sflow collector
```


**命令功能**

查看收集者配置信息

**命令格式**

```
show sflow collector <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 收集者ID | 1-10 |

```
show sflow flow
```


**命令功能**

查看端口Flow 采样配置信息

**命令格式**

```
show sflow flow [enter | ethernet <portId>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 不同设备取值不同，例如0/0/1 |


## 18.10. show sflow counter


**命令功能**

查看端口Counter 采样配置信息

**命令格式**

```
show sflow counter [enter | ethernet <portId>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 不同设备取值不同，例如0/0/1 |


## 18.11. 配置举例

组网
PC1-----------1 DUT 2------------PC2
|
collector（192.168.1.25）
配置
DUT3(config)#interface vlan-interface 1
DUT3(config-if-vlanInterface-1)#ip address 192.168.1.62 255.255.255.0
DUT3(config-if-vlanInterface-1)#exit
DUT3(config)# sflow agent ip 192.168.1.62
DUT3(config)# sflow collector 1 ip 192.168.1.25 owner mycollector
```
#Port1 开启flow 采样
DUT3(config)# interface eth 0/0/1
DUT3(config-if-ethernet-0/0/1)# sflow flow sampling-rate 1000
DUT3(config-if-ethernet-0/0/1)# sflow flow max-header 64
DUT3(config-if-ethernet-0/0/1)# sflow flow collector 1
#Port2 开启counter 采样
DUT3(config-if-ethernet-0/0/1)#interface eth 0/0/2
DUT3(config-if-ethernet-0/0/2)# sflow counter interval 10
DUT3(config-if-ethernet-0/0/2)# sflow counter collector 1
```


# 19. ACL 配置

```
access-list <id> match-order
```


**命令功能**

全局配置ACL 匹配顺序

**命令格式**

```
access-list <id> match-order [auto| config]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 访问控制列表号 | 1-2999 |
| auto | 长度大优先 | 默认 |
| config | 配置序号小优先 | 19.2. |

```
access-list step
```


**命令功能**

ACL 子项目编号的步长

**命令格式**

```
access-list step step_value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Step_value | 访问控制列表步 | 长 |

INTEGER<1-10>
```
access-list <1-999>
```


**命令功能**

全局配置 IP 访问控制列表

**命令格式**

```
access-list id [permit|deny] [IPv4_protocol] [ src_ipv4 mask | host | any ] [ dst_ipv4 mask |
host | any ] [fragments|dscp|precedence|tos value] [time-range name]
access-list id [permit|deny] [IPv6_protocol] [src_ipv6/mask_l|ipv6any]
[dst_ipv6/mask_l|ipv6any] [traffic-class value] [time-rang name ]
no access-list all|<id> [<subitem_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 访问控制列表号 | [1-999]，表示ip acl 类型 |
| IPv4_protocol | Type protocol number | 0-255,部分协议可使用关键字 |
| 如udp tcp | src_ip | 源IPv4/6地址 |
| 合法的ip地址 | dst_ip | 目的IPv4/6地址 |
| 合法的ip地址 | mask_l | 掩码长度 |
| 1-128 | value | 具体取值 |
| Dscp 0-63 | Precedence 0-7 | tos 0-15 |
| traffic-class 0-255 | name | 指定访问控制列表生效时间 |

String<1-32>
```
access-list <1000-1999>
```


**命令功能**

全局配置二层访问控制列表

**命令格式**

```
access-list <id> [permit|deny] [L2_protocol] [<source_mac>[<mask|host]|any]
[<dst_mac>[<mask|host]|any] [vlan vid] [cos value] [time-range name]
no access-list all|<id> [<rule_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 访问控制列表号 | [1000-1999]，表示二层访问控制列表类型 |
| L2_protocol | 帧的协议类型 | 0-FFFF，部分可取关键字，如arp，ip |
| source_mac | 指定源mac地址 | 范围 |
| 合法地址 | protocal | 以太网承载的协 |
| 议类型 | 十六进制表示，HEX<0-FFFF> | mask |
| 掩码 | 合法值 | cos |
| 802.1p的优先级 | 0-7 | vid |
| Vlan id | 1-4094 | 19.5. |

```
access-list <2000-2999>
```


**命令功能**

全局配置混合访问控制列表

**命令格式**

```
access-list <id> [permit | deny] {<0-255> |<cos>|[<dst-mac>|<src-mac> [<mask>|<host>]
<cos>|<src-ip>|<src-ipv6><dst-mac><vlan> ] <vlan>}
no access-list all|<id> [<rule_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 访问控制列表号 | 2000-2999 |
| 0-255 | ipv4协议号或者ipv6下 | 一跳头部 |
| cos_value | 指定cos值 | [0-7] |
| source_mac | 指定源mac地址范围 | [any,带有掩码的mac地址] |
| 例如：00:00:00:00:00:10 00:00:00:00:00:ff | 注意：掩码使用反码 | vlan_value |
| 指定报文所属vlan | [1-4094] | destination_mac |
| 指定目的mac地址范围 | [any,带有掩码的mac地址] | 例如：00:00:00:00:00:20 00:00:00:00:00:ff |

注意：掩码使用反码
access-group

**命令功能**

全局或端口模式下激活访问控制列表

**命令格式**

```
access-group [ ip-acl id ] [ mac-acl id] [ hybrid-acl id ] [ subitem sub-num] [in | out ]
no access-group <type> {<id> | <name>} [subitem <rule_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 访问控制列表号 | [1-2999] |
| 取值范围和选择的type相关 | sub_num | 规则id号，添加规则时 |
| 自动生成 | 0-127 | 19.7. |

time-range

**命令功能**

全局配置时间，并且进入时间段视图

**命令格式**

```
time-range <name>
no time-range <name>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 间段名字(最长为 | 32 个字节，必须 |
| 以[a-z,A-Z]开头, | 不区分大小写) | String<1-32> |

absolute

**命令功能**

时间段视图配置绝对时间段

**命令格式**

```
absolute start <start_time> <start_date> end <end_time> <end_date>
no absolute start <start_time> <start_date> end <end_time> <end_date>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start_time | 起始时间 | 00:00:00-23:59:59 |
| start_date | 起始年月日 | 2000/01/01-2099/12/31 |
| end_time | 结束时间 | 00:00:00-23:59:59 |
| end_date | 结束年月日 | 2000/01/01-2099/12/31 |

periodic

**命令功能**

时间段视图配置相对时间段

**命令格式**

```
periodic <date_list> <start_time> to <end_time>
no periodic <date_list> <start_time> to <end_time>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| date_list | 日期列表 | [0- |
| 6,Daily,fri,mon,sat,sun,thu,tue,wed,weekdays,w | eekend] | start-time |
| 起始时间 | 00:00:00-23:59:59 | end-time |
| 结束时间 | 00:00:00-23:59:59 | 19.10. show time-range |


**命令功能**

查看时间段配置信息

**命令格式**

```
show time-range {all | statistics | name <name>}
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 时间段名字(最长 | 为32个字节，必须 |
| 以[a-z,A-Z] 开头, | 不区分大小写) | 1-32 |


## 19.11. show access-list config


**命令功能**

查看访问控制列表配置信息

**命令格式**

```
show access-list config [all|brief|acl_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl_id | 访问控制列表号 | [1-2999] |


## 19.12. show access-list runtime


**命令功能**

查看已经激活的访问控制列表信息

**命令格式**

```
show access-list runtime [all|brief|acl_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl_id | 访问控制列表号 | [1-2999] |


## 19.13. 配置举例

```
DUT2(config)#time-range ceshi
DUT2(config-timerange-ceshi)#absolute start 09:00:00 2020/9/30 end 18:00:00 2025/9/30   //配置绝对时间段
DUT2(config)#access-list 1 deny any any               //配置ACL
DUT2(config)#access-group ip-acl 1 subitem 0 in        //激活ACL
DUT2(config)#show access-list runtime all       //查看已经激活的访问控制列表信息
access-list 1 subitem 0 running inbound
total runtime rules: 1 rules
```


# 20. QACL 配置

```
traffic insert-vlan
```


**命令功能**

配置指定流插入外层vlan

**命令格式**

```
traffic insert-vlan [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] vlan vid
no traffic insert-vlan [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl_id | Acl 编号 | [1-2999] |
| vid | Vlan编号 | [1-4094] |

```
traffic statistic
```


**命令功能**

全局视图配置流统计

**命令格式**

（no）traffic statistic [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] [ in | out ]

**参数说明**

*无*

```
traffic mirror
```


**命令功能**

全局视图配置指定流镜像

**命令格式**

```
traffic mirror [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] [cpu | interface
ethernet port-id]
no traffic mirror [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num]
```


**参数说明**

*无*

```
traffic priority
```


**命令功能**

配置指定流标记优先级

**命令格式**

```
traffic priority [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] [cos | dscp |local-
precedence|precedence] value
no traffic priority [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 根据具体关键字 | 取值 |
| dscp 0-63 | cos 0-7 | precedence 0-7 |

```
Local-precedence 0-7
traffic rate-limit
```


**命令功能**

配置对特定流限速

**命令格式**

```
traffic rate-limit [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] rate [in|out]
no traffic rate-limit[ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] [in | out ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 目标速率 | GE端口 <64-1000000> |

10GE端口 <64-10000000>
```
traffic redirect
```


**命令功能**

命令配置报文重定向

**命令格式**

```
Traffic redirect [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] [ interface
ethernet port-id | cpu ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Acl-id | 访问控制列表 | [2000-2999] |
| [1-999] | [1000-1999] | port-id |
| 端口号 | 根据交换机物理端口来定，例如28 口交换 | 机：0/0/1-0/1/4 |
| subitem | 三层、二层、混 | 合acl 列表的子项 |
| 号 | 0-127 | 20.7. |

```
traffic rewrite-vlan
```


**命令功能**

配置修改指定流的vlan

**命令格式**

```
traffic rewrite-vlan [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num] vlan-id
no traffic rewrite-vlan [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | 重写vlan id | 1-4094 |

```
clear traffic statistic
```


**命令功能**

清除流量统计信息

**命令格式**

```
clear traffic statistic [all | [ mac-acl | ip-acl | hybrid-acl ] acl_id [subitem sub_num]]
[ in|out]
```


**参数说明**

*无*

```
show traffic all | brief
```


**命令功能**

显示所有的QoS 配置

**命令格式**

```
show traffic all
show traffic brief
```


**参数说明**

*无*


## 20.10. show traffic insert-vlan


**命令功能**

显示vlan 插入配置

**命令格式**

```
show traffic insert-vlan
```


**参数说明**

*无*


## 20.11. show traffic mirror


**命令功能**

显示所有的流镜像配置

**命令格式**

```
show traffic mirror
```


**参数说明**

*无*


## 20.12. show traffic priority


**命令功能**

显示优先级标记的配置

**命令格式**

```
show traffic priority
```


**参数说明**

*无*


## 20.13. show traffic rate-limit


**命令功能**

显示流限速的配置
命令格式     show traffic rate-limit

**参数说明**

*无*


## 20.14. show traffic redirect


**命令功能**

显示重定向的配置

**命令格式**

```
show traffic redirect
```


**参数说明**

*无*


## 20.15. show traffic rewrite-vlan


**命令功能**

显示vlan 重写的参数设置

**命令格式**

```
show traffic rewrite-vlan
```


**参数说明**

*无*


## 20.16. show traffic statistic


**命令功能**

显示所有流统计配置

**命令格式**

```
show traffic statistic
```


**参数说明**

*无*


## 20.17. 配置举例

```
#配置并激活ACL
DUT(config)#access-list 150 permit any 192.168.1.150 255.255.255.252
#标记ACL 优先级
DUT(config)#traffic priority ip-acl 150 cos 7
```


# 21. Cos 配置

```
queue-scheduler group_id strict-priority
```


**命令功能**

配置队列调度策略 strict-priority

**命令格式**

```
queue-scheduler group_id strict-priority
no queue-scheduler [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group_id | 队列组 | 1-1 |

```
queue-scheduler group_id wfq
```


**命令功能**

配置队列调度策略wfq

**命令格式**

queue-schedulergroup_id wfq q_wt1 q_wt2 q_wt3 q_wt4 q_wt5 q_wt6 q_wt7 q_wt8
```
no queue-scheduler [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| q_wt | 队列权重 | 一共有8条队列，每条队列的权重值取值范围 |

是[0-100]
```
queue-scheduler id sp-wfq
```


**命令功能**

配置队列调度策略sp-wfq

**命令格式**

```
queue-scheduler group_id sp-wfq q_wt1 q_wt2 q_wt3 q_wt4 q_wt5 q_wt6 q_wt7 q_wt8
no queue-scheduler [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| q_wt | 队列权重 | 一共有8条队列，每条队列的权重值取值范围 |

是[0-100]
```
queue-scheduler group_id cos-map
```


**命令功能**

配置802.1P 与硬件队列映射关系

**命令格式**

```
queue-scheduler cos-map group_id priority queue_id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| priority | 802.1p优先级 | [0-7] |
| queue_id | 硬件队列号 | [0-7] |

```
queue-scheduler dscp-map
```


**命令功能**

(取消)使能dscp map，默认未使能；.

**命令格式**

```
queue-scheduler dscp-map
no queue-scheduler dscp-map
```


**参数说明**

*无*

```
queue-scheduler dscp-map group_id priority dscp
```


**命令功能**

配置dscp 值与硬件队列映射关系

**命令格式**

```
queue-scheduler dscp-map group_id <dscp_value> <queue_id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dscp value | dscp值 | [0-63] |
| queue | 硬件队列号 | [0-7] |

queue-scheduler

**命令功能**

配置端口 queue-scheduler:所属的组、cos-map、dscp-map

**命令格式**

```
queue-scheduler group_id
queue-scheduler cos-map group_id
queue-scheduler dscp-map group_id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group_id | 队列组 | [1-1] |

```
show queue-scheduler
```


**命令功能**

查看队列调度的状态及方式

**命令格式**

```
show queue-scheduler [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group_id | 调度组号 | [1-1] |

```
show queue-scheduler cos-map
```


**命令功能**

查看802.1P 与硬件队列映射表

**命令格式**

```
show queue-scheduler cos-map [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group_id | 调度组号 | [1] |


## 21.10. show queue-scheduler dscp-map


**命令功能**

查看dscp 值与硬件队列映射表

**命令格式**

```
show queue-scheduler dscp-map [group_id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group_id | 调度组号 | [1] |


## 21.11. show queue-scheduler port-map


**命令功能**

查看端口配置

**命令格式**

```
show queue-scheduler port-map
```


**参数说明**

*无*


## 21.12. 配置举例

```
#配置队列调度策略
DUT2(config)#queue-scheduler 1 sp-wrr 1 2 0 4 3 0 2 1
DUT2(config)#show queue-scheduler 1
Queue-scheduler group : 1
Queue scheduler mode  : SP+WRR
Queue weights         : 1 2 0 4 3 0 2 1
#配置cos 值映射到队列
DUT2(config)#queue-scheduler cos-map 1 3 5
DUT2(config)#show queue-scheduler cos-map
Information about map of cos:
802.1P Priority  Queue of class
group 1-------------------------------
0                0
1                1
2                2
3                5
4                4
5                5
6                6
7                7
```


# 22. 双速三色配置

```
two-rate-policer set-pre-color
```


**命令功能**

配置DSCP 到颜色的映射

**命令格式**

```
two-rate-policer set-pre-color <dscp-value> <color>
no two-rate-policer set-pre-color <dscp-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dscp-value | DSCP值 | [0-63] |
| color | 颜色 | [green,yellow,red] |

```
two-rate-policer mode
```


**命令功能**

配置双速三色模式

**命令格式**

```
two-rate-policer mode [color-aware |color-blind ]
```


**参数说明**

*无*

```
two-rate-policer Id
```


**命令功能**

配置双速三色

**命令格式**

```
two-rate-policer <Id> cir <c-rate> cbs <c-volume> pir <p-rate> pbs <p-volume> [green-
action <action> yellow-action <action> red-action <action>]
no two-rate-policer <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 双速三色ID | [0-255] |
| c-rate | C盒令牌速率 | [64-10000000] |
| c-volume | C盒令牌容积 | [3600-1073741824] |
| p-rate | P盒令牌速率 | [64-10000000] |
| p-volume | P盒令牌容积 | [3600-1073741824] |
| action | 行为 | [copy-to-cpu, transmit, drop, set_dscp_value] |

```
show two-rate-policer
```


**命令功能**

查看双速三色配置信息

**命令格式**

```
show two-rate-policer
show two-rate-policer policer_id
show two-rate-policer set-pre-color
```


**参数说明**

*无*


## 22.5. 配置举例

```
DUT(config)#access-list 1 permit any any
DUT(config)#two-rate-policer 0 cir 64 cbs 6400 pir 128 pbs 12800
DUT(config)#traffic rate-limit ip-acl 1 two-rate-policer 0 in
DUT(config)#show two-rate-policer 0
two rate policer 0 :
CIR : 64Kbps    CBS : 6400bytes    PIR : 128Kbps    PBS : 12800bytes
color aware : color-blind
```


# 23. 端口隔离配置

```
interface port-isolate group group-id
```


**命令功能**

配置并进入隔离组模式

**命令格式**

```
interface port-isolate group group-id
no no interface port-isolate group [group-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-id | 隔离组编号 | 1-31 |

```
switchport [all | ethernet port-id]
```


**命令功能**

在隔离组模式下配置成员

**命令格式**

```
[no]switchport [all| ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定， 格式如0/0/1 |

```
port-isolate group group-id
```


**命令功能**

在端口模式下将本端口加入隔离组，效果等同上一步；

**命令格式**

```
[no]port-isolate group group-id
```


**参数说明**

*无*

```
show port-isolation group
```


**命令功能**

查看端口隔离配置

**命令格式**

```
show port-isolate group [group-id]
```


**参数说明**

*无*


**配置举例**

```
#端口1 与端口2 隔离
Switch(config)#interface port-isolate group 1
Switch(config-port-isolate-1)#switchport ethernet 0/0/1 ethernet 0/0/2
Switch(config-port-isolate-1)#exit
Switch(config)#show port-isolate group 1
Port-isolation informations:
group : port list
1     : e0/0/1-e0/0/2.
```


# 24. storm-control 配置

```
storm-control type unit vlaue
```


**命令功能**

在端口模式下配置风暴抑制报文类型和阈值

**命令格式**

```
storm-control [broadcast|multicast | unicast ] kbps kbps-value
storm-control [broadcast|multicast | unicast ] pps pps-value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pps-value | 会自动调整成3200 的 | 最大倍数 |
| 3200-14881000 | kbps-value | 会自动调整成6400 的 |
| 最大倍数，1K=1000; | 6400-10000000 | 24.2. |

```
storm-control action
```


**命令功能**

在端口模式下配置风暴抑制处理动作

**命令格式**

```
storm-control action [logging| shutdown] trap]
no storm-control action
```


**参数说明**

*无*

```
storm-control broadcast [kbps|pps] value
```


**命令功能**

在端口模式下配置广播风暴抑制

**命令格式**

```
[no]storm-control broadcast [ kbps | pps ] value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 取值 | Kbps <8-10000000> |

```
Pps <100-14881000>
storm-control multicast [ kbps | pps ] value
```


**命令功能**

在端口模式下配置组播风暴抑制

**命令格式**

```
[no]storm-control multicast [ kbps | pps ] value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 取值 | Kbps <8-10000000> |

```
Pps <100-14881000>
storm-control unicast [ kbps | pps ] value
```


**命令功能**

在端口模式下配置单播风暴抑制

**命令格式**

```
[no]storm-control unicast [ kbps | pps ] value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 取值 | Kbps <8-10000000> |

```
Pps <100-14881000>
show storm-control interface
```


**命令功能**

显示风暴抑制配置信息

**命令格式**

```
show storm-control interface [enter | ethernet <port-ID>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 设备支持的所有端口，如：0/0/1 |


**配置举例**

```
DUT(config)#int ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#storm-control broadcast pps 3200   //配置广播风暴控制
DUT(config-if-ethernet-0/0/1)#storm-control unicast pps 6400      //配置未知单播风暴控制
DUT(config-if-ethernet-0/0/1)#storm-control multicast pps 3200    //配置组播风暴控制
DUT(config-if-ethernet-0/0/1)#show storm-control interface ethernet 0/0/1   //查看单端口风暴控制
Port number: e0/0/1
Storm-control action: N/A
Broadcast storm control has been 3200pps
Multicast storm control target rate is 3200pps
Unicast storm control target rate is 6400pps
Total entries: 1 .
```


# 25. Port-Security 配置

```
port-security enable
```


**命令功能**

端口下开启port-security

**命令格式**

```
port-security enable
```


**参数说明**

*无*

```
port-security disable
```


**命令功能**

端口下关闭port-security

**命令格式**

```
port-security disable
```


**参数说明**

*无*

```
port-security permit|deny ip-address
```


**命令功能**

端口下配置（删除）IP 规则

**命令格式**

```
[no] port-security [permit | deny] ip-address <start-ip> to <end-ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-ip | 可配置有效的ip | 地址 |
| 32 位二进制数，格式为X.X.X.X | end-ip | 可配置有效的ip |
| 地址 | 32 位二进制数，格式为X.X.X.X | 25.4. |

```
port-security permit|deny mac-address
```


**命令功能**

端口下配置（删除）MAC 规则

**命令格式**

```
[no] port-security [ permit | deny ] mac-address mac-address [ vlan-id vlan-id | ip-address
ip-address ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-address | 单播MAC 地址 | 128 位二进制数，格式为X:X:X:X:X:X |
| vlan-id | VLAN 编号 | 1-4094 |
| ip-address | 可配置有效的ip | 地址 |

32 位二进制数，格式为X.X.X.X
```
port-security maximum
```


**命令功能**

配置（删除）最大地址数目值规则

**命令格式**

```
port-security maximum <value>
no port-security maximum
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 最大地址数目 | 0-4000 |

```
port-security permit mac-address sticky
```


**命令功能**

配置(删除) mac sticky 规则

**命令格式**

```
[no] port-security permit mac-address sticky <mac-address> [vlan-id <vlan-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-address | 单播MAC 地址 | 128 位二进制数，格式为X:X:X:X:X:X |
| vlan-id | VLAN 编号 | 1-4094 |

```
no port-security all
```


**命令功能**

删除所有端口安全相关配置

**命令格式**

```
no port-security all
```


**参数说明**

*无*

```
port-security violation
```


**命令功能**

配置（删除）收到非法报文的处理策略

**命令格式**

```
[no] port-security violation [ protect |restrict | shutdown ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| protect | 丢弃报文 | 无 |
| restrict | 丢弃报文并告警 | 无 |
| shutdown | 丢弃报文和告 | 警，并关闭端口 |

无
```
port-security violation log-interval
```


**命令功能**

配置（删除）收到非法报文的日志间隔时间

**命令格式**

```
[no] port-security violation log-interval <value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 间隔时间 | 0-86400 |


## 25.10. show port-security ip-address


**命令功能**

查看ip 规则配置

**命令格式**

```
show port-security ip-address [ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 25.11. show port-security mac-address


**命令功能**

查看mac 规则配置

**命令格式**

```
show port-security mac-address [ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 25.12. show port-security


**命令功能**

显示安全配置

**命令格式**

```
show port-security [ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 25.13. show port-security active-address


**命令功能**

查看下发的激活表象

**命令格式**

```
show port-security active-address [configured | learned | ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 25.14. show port-security violation


**命令功能**

查看收到非法报文的日志间隔时间

**命令格式**

```
show port-security violation log-interval
```


**参数说明**

*无*


## 25.15. 配置举例

组网
```
DUT 1----------- PC
配置
DUT(config)#int eth 0/0/1
DUT(config-if-ethernet-0/0/1)#port-security enable
DUT(config-if-ethernet-0/0/1)#port-security permit mac-address 00:00:00:11:22:33
```


# 26. IP-Source-Guard 配置

```
ip source
```


**命令功能**

端口模式下配置（删除）过滤方式

**命令格式**

```
[no] ip source [ip | ip-mac | ip-mac-vlan]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 端口只根据ip 报 | 文的源ip 地址来 |
| 过滤报文 | 无 | ip-mac |
| 端口根据ip 报文 | 的源ip 和mac 来 | 过滤报文 |
| 无 | ip-mac-vlan | 端口根据ip 报文 |
| 的源ip、mac 和 | vlan 来过滤报文 | 无 |

```
ip source bind
```


**命令功能**

配置（删除）绑定表项

**命令格式**

```
[no] ip source bind ip-address [mac-address [interface ethernet port-id vlan vlan-id]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | 可配置有效的ip | 地址 |
| 32 位二进制数，格式为X.X.X.X | mac-address | 可配置对应端口 |
| mac 地址 | 48 位二进制数，格式为X:X:X:X:X:X | port-id |
| 端口号 | 根据交换机物理端口来定，例如28 口交换 | 机：0/0/1-0/1/4 |
| vlan-id | VLAN 编号 | 1-4094 |

```
ip source permit-igmp
```


**命令功能**

(取消)使能转发igmp 协议报文

**命令格式**

```
ip source permit-igmp
no ip source permit-igmp
```


**参数说明**

*无*

```
ip source vlan
```


**命令功能**

(取消)使能vlan 的过滤功能

**命令格式**

```
[no] ip source vlan vlan-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | VLAN 编号 | 1-4094 |

```
show ip source
```


**命令功能**

查看配置信息

**命令格式**

```
show ip source
```


**参数说明**

*无*

```
show ip source bind
```


**命令功能**

查看绑定表项

**命令格式**

```
show ip source bind [ip-address]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | 配置有效的ip 地 | 址 |

32 位二进制数，格式为X.X.X.X
```
show ip source permit-igmp
```


**命令功能**

命令查看配置信息

**命令格式**

```
show ip source permit-igmp
```


**参数说明**

*无*

```
show ip source vlan
```


**命令功能**

命令查看配置信息

**命令格式**

```
show ip source vlan
```


**参数说明**

*无*


**配置举例**

组网
```
TCA----- 1 DUT 2 -----TCB
配置
DUT(config)#ip source bind 192.168.1.10
DUT(config)#interface eth 0/0/1
DUT(config-if-ethernet-0/0/1)#ip source ip
```


# 27. ARP anti-flood 配置

```
arp anti-flood
```


**命令功能**

(取消)使能arp anti-flood 功能

**命令格式**

```
(no)arp anti-flood
```


**参数说明**

*无*

```
arp anti-flood action
```


**命令功能**

配置对于ARP 攻击报文的处理策略

**命令格式**

```
arp anti-flood action [deny-all |deny-arp]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| deny-all | 丢弃所有 | 无 |
| deny-arp | 丢弃arp | 无，默认 |

```
arp anti-flood bind blackhole
```


**命令功能**

绑定洪泛攻击生成的攻击表项变成静态黑洞MAC，deny-all 进时有效

**命令格式**

```
arp anti-flood bind blackhole [all|mac]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| all | 所有动态黑洞 | 无 |
| mac | mac 地址 | 攻击表项中的mac |

```
arp anti-flood rate-limit
```


**命令功能**

全局或物理接口下配置arp 速率阀值

**命令格式**

```
arp anti-flood rate-limit <num>
no arp anti-flood rate-limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-100 pps | 27.5. |

```
arp anti-flood recover
```


**命令功能**

手动恢复禁止用户

**命令格式**

```
arp anti-flood recover [all|mac]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| all | 所有禁止用户 | 无 |
| mac | Mac 地址 | 攻击表项中的mac |

```
arp anti-flood recover-time
```


**命令功能**

配置攻击表项恢复时间

**命令格式**

```
arp anti-flood recover-time time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 0-1440 min,0 表示不恢复 | 27.7. |

```
show arp anti-flood
```


**命令功能**

查看防泛洪配置

**命令格式**

```
show arp anti-flood
```


**参数说明**

*无*

```
show arp anti-flood rate-limit
```


**命令功能**

查看端口arp 阀值

**命令格式**

```
show arp anti-flood rate-limit
```


**参数说明**

*无*


**配置举例**

组网
```
PC----- 1 DUT
配置
DUT(config)#arp anti-flood
DUT(config)#arp anti-flood action deny-arp
DUT(config-if-ethernet-0/0/1)#show arp anti-flood
Informations of arp anti-flood
Arp anti-flood: enabled
Arp anti-flood rate-limit: 16pps
Arp anti-flood user recovery time: 10 minutes
Arp anti-flood deny type: DenyARP
DeniedSrcMAC       SourceIP         Port     Vlan  DenyType  RemainAgingTime(m:s)
Total entries: 0.
```


# 28. ARP anti-spoofing 配置

```
arp anti-spoofing
```


**命令功能**

(取消)使能arp anti-spoofing 功能

**命令格式**

```
(no)arp anti-spoofing
```


**参数说明**

*无*

```
arp anti-spoofing action
```


**命令功能**

配置对于未知arp 的处理策略

**命令格式**

```
arp anti-spoofing action [discard|flood]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| discard | 丢弃 | 无 |
| flood | 泛洪 | 无 |

```
arp anti-spoofing bind
```


**命令功能**

配置允许通过的主机

**命令格式**

```
arp anti-spoofing bind ip <ip> ethernet <port-list>
no arp anti-spoofing bind [ip <ip> [ethernet <port-list>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | ip 地址 | 合法单播地址 |
| port-list | 端口列表 | 格式如0/0/1 |

```
arp anti-spoofing gateway-disguiser
```


**命令功能**

(取消)使能网关防欺骗功能

**命令格式**

```
arp anti-spoofing gateway-disguiser
no arp anti-spoofing gateway-disguiser
```


**参数说明**

*无*

```
arp anti-spoofing source-mac-check
```


**命令功能**

(取消)使能arp 报文源地址一致性检查

**命令格式**

```
arp anti-spoofing source-mac-check
no arp anti-spoofing source-mac-check
```


**参数说明**

*无*

```
arp anti-attack trust
```


**命令功能**

端口模式配置为信任端口

**命令格式**

```
arp anti-attack trust
no arp anti-attack trust
```


**参数说明**

*无*

```
show arp anti-spoofing
```


**命令功能**

查看防欺骗配置

**命令格式**

```
show arp anti-spoofing
```


**参数说明**

*无*

```
show arp anti-spoofing bind
```


**命令功能**

查看bind 表项

**命令格式**

```
show arp anti-spoofing bind
```


**参数说明**

*无*

```
show arp anti-attack
```


**命令功能**

查看端口配置信息

**命令格式**

```
show arp anti-attack [ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4

## 28.10. 配置举例

组网
```
PC----- 1 DUT
配置
DUT(config)#arp anti-spoofing
DUT(config)#arp anti-spoofing action discard
DUT(config-if-ethernet-0/0/1)#sinterface ethernet 0/0/1
DUT(config-if-ethernet-0/0/1)#arp anti-attack trust
```


# 29. DHCP anti-attack 配置

```
dhcp anti-attack
```


**命令功能**

防攻击功能开关

**命令格式**

```
dhcp anti-attack
no dhcp anti-attack
```


**参数说明**

*无*

```
dhcp anti-attack action
```


**命令功能**

配置处理方式

**命令格式**

```
dhcp anti-attack action [deny-all |deny-dhcp ]
dhcp anti-attack action [deny-all |deny-dhcp ] [threshold rate]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| deny-all | 拒绝所有报文 | 无 |
| deny-dhcp | 拒绝dhcp 报文 | 无 |
| rate | 阀值 | 1-100pps,default:16pps |

```
dhcp anti-attack threshold
```


**命令功能**

全局或端口配置速率阈值

**命令格式**

```
(no)dhcp anti-attack threshold <rate >
(no)dhcp anti-attack action [deny-all |deny-dhcp ] [threshold rate]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 阀值 | 1-100pps,default:16pps |

```
dhcp anti-attack bind blackhole
```


**命令功能**

绑定黑洞mac

**命令格式**

```
dhcp anti-attack bind blackhole [all | mac ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac | 具体mac | 合法mac |

```
dhcp anti-attack recover-time
```


**命令功能**

配置自动恢复时间

**命令格式**

```
dhcp anti-attack recover-time <time >
no dhcp anti-attack recover-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 取值 | 0-1440 min,0 表示不恢复 |

```
dhcp anti-attack recover
```


**命令功能**

手动恢复攻击表项

**命令格式**

```
dhcp anti-attack recover [all | mac ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac | 具体mac | 合法mac |

```
dhcp anti-attack trust
```


**命令功能**

端口下配置端口为trust 口

**命令格式**

```
(no)dhcp anti-attack trust
```


**参数说明**

*无*

```
show dhcp anti-attack
```


**命令功能**

查看运行信息

**命令格式**

```
show dhcp anti-attack
```


**参数说明**

*无*

```
show dhcp anti-attack interface
```


**命令功能**

查看端口配置信息

**命令格式**

```
show dhcp anti-attack interface [ethernet <port-num>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-num | 端口号 | 格式如0/0/1 |


## 29.10. 配置举例

组网
```
PC----- 1 DUT
配置
DUT(config)#dhcp anti-attack
DUT(config)#dhcp anti-attack action deny-dhcp
DUT(config)#dhcp anti-attack threshold 10
DUT(config)#dhcp anti-attack recover-time 3
```


# 30. errdisable 配置

```
errdisable detect cause
```


**命令功能**

(取消)使能 errdisable 检测协议

**命令格式**

```
(no)errdisable detect cause [all | bpdu-guard | dhcp-snooping | loopback |
port-security | storm-control ]
```


**参数说明**

*无*

```
errdisable recovery cause
```


**命令功能**

(取消)使能 errdisable 自动恢复协议

**命令格式**

```
(no)errdisable recovery cause [all | bpdu-guard | dhcp-snooping | loopback |
port-security | storm-control ]
```


**参数说明**

*无*

```
errdisable recovery interval
```


**命令功能**

配置恢复周期

**命令格式**

```
(no)errdisable recovery interval <value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 具体取值 | INTEGER<10-10000>,default:300s |

```
show errdisable
```


**命令功能**

查看配置及运行信息

**命令格式**

```
show errdisable
```


**参数说明**

*无*


# 31. 防DOS 攻击配置

```
anti-dos packets class
```


**命令功能**

(取消)使能防报文攻击

**命令格式**

```
(no)anti-dos packets class type<num>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 报文分类 | 0-14，意思分别如下： |
| type0：Source MAC and dst MAC equal | type1:Source IP and dst IP equal | type2:UDP with sport and dport equal |
| type3:TCP with sport and dport equal | type4:ICMPv4 maxinum length | type5:ICMPv6 maxinum length |
| type6:TCP control flags and sequence equal 0 | type7:TCP SYN flags unviable | type8:Check IP first fragments |
| type9:Minimum size of IPv6 fragments | type10:Fragmented ICMP packets | type11:TCP fragments with offset value of |
| 1(*8) | type12:TCP with SYN & FIN bits | type13:TCP with FIN,URG and PSH bits,and |
| sequence equal 0 | type14:TCP frist fragments with minimum TCP | header length |

```
show anti-dos
```


**命令功能**

查看防dos 配置

**命令格式**

```
show anti-dos
```


**参数说明**

*无*


# 32. BPDU-Discard 配置

bpdu-discard

**命令功能**

(取消)使能丢弃bpdu 报文

**命令格式**

bpdu-discard
```
no bpdu-discard
```


**参数说明**

*无*

```
show bpdu-discard
```


**命令功能**

查看配置信息

**命令格式**

```
show bpdu-discard
```


**参数说明**

*无*


# 33. CPU-Car 配置

```
cpu-car
```


**命令功能**

配置cpu 的处理速率

**命令格式**

```
cpu-car <rate>
no cpu-car <rate>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rate | 取值 | 1-10000 pps |

```
show cpu-car
```


**命令功能**

查看配置信息

**命令格式**

```
show cpu-car
```


**参数说明**

*无*


# 34. CPU-ratelimit 配置

```
cpu-ratelimit queue id limit rate
```


**命令功能**

配置每个队列cpu 的处理速率

**命令格式**

```
(no)cpu-ratelimit queue id limit rate
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 队列取值 | 0-7 |
| rate | 速率取值 | 1-20000 |

```
show cpu-ratelimit
```


**命令功能**

查看配置信息

**命令格式**

```
show cpu-ratelimit
```


**参数说明**

*无*


# 35. PPPOE+配置

pppoeplus

**命令功能**

全局或端口(取消)使能pppoeplus

**命令格式**

pppoeplus
```
no pppoeplus
```


**参数说明**

*无*

```
pppoeplus delimiter
```


**命令功能**

配置分隔符，当报文类型配置为self-defined 时，此配置有效。

**命令格式**

```
pppoeplus delimiter [colon | dot | slash | space]
no pppoeplus delimiter
```


**参数说明**

*无*

```
pppoeplus format
```


**命令功能**

配置报文编码方式，当报文类型配置为self-defined 时，此配置有效。

**命令格式**

```
pppoeplus format [ascii | binary]
no pppoeplus format
```


**参数说明**

*无*

```
pppoeplus type
```


**命令功能**

全局配置报文格式

**命令格式**

```
pppoeplus type [standard | huawei | self-defined [circuit-id | remote-id] [client-mac |
hostname | port | switch-mac | vlan] <user-difined-string>]
no pppoeplus type
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user-difined-string | 自定义字符串 | 1-63 个字符 |

```
pppoeplus circuit-id
```


**命令功能**

端口下配置报文circuit-id 内容

**命令格式**

```
(no)pppoeplus circuit-id <user-difined-string>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user-difined-string | 用户自定义字符 | 串 |

1-63 个字符
```
pppoeplus drop
```


**命令功能**

端口下(取消)使能丢弃padi/pado 报文

**命令格式**

```
(no)pppoeplus drop [padi | pado]
```


**参数说明**

*无*

```
pppoeplus strategy
```


**命令功能**

端口下配置策略

**命令格式**

```
pppoeplus strategy [drop | keep | replace | transmit]
no pppoeplus strategy
```


**参数说明**

*无*

```
pppoeplus trust
```


**命令功能**

端口下配置为信任端口

**命令格式**

```
pppoeplus trust
no pppoeplus trust
```


**参数说明**

*无*

```
show pppoeplus interface [ethernet <pid>]
```


**命令功能**

查看pppoeplus 端口配置

**命令格式**

```
show pppoeplus interface [ethernet <pid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pid | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


## 35.10. 配置举例

组网
```
Clinet----- 1 DUT 2 -----Server
配置
DUT(config)#pppoeplus
DUT(config)#interface eth 0/0/1
DUT(config-if-ethernet-0/0/1)#pppoeplus
DUT(config-if-ethernet-0/0/1)#interface eth 0/0/2
DUT(config-if-ethernet-0/0/2)#pppoeplus
DUT(config-if-ethernet-0/0/2)#pppoeplus trust
```


# 36. 802.1x 配置

```
dot1x [enable|disable]
```


**命令功能**

（取消）使能dot.1X 功能。

**命令格式**

```
dot1x enable
dot1x disable
```


**参数说明**

*无*

```
dot1x eap-relay enable
```


**命令功能**

使能EAP 终结模式:eap-finish

**命令格式**

```
dot1x eap-relay enable
```


**参数说明**

*无*

```
dot1x eap-relay disable
```


**命令功能**

使能EAP 中继模式:eap-transfer

**命令格式**

```
dot1x eap-relay disable
```


**参数说明**

*无*

```
dot1x max-reauth
```


**命令功能**

配置客户端无回应eap-response/md5 challenge 报文时，重新发送请求eap-
request/md5 challenge 报文的次数。

**命令格式**

```
dot1x max-reauth times
no dot1x max-reauth
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 最大发送报文次 | 数，默认为2 |

1-10
```
dot1x max-req
```


**命令功能**

配置（恢复)客户端无回应eap-response/identity 报文时，重新发送请求eap-
request/identity 报文的次数。

**命令格式**

```
dot1x max-req times
no dot1x max-req
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 最大发送报文次 | 数，默认为2 |

1-10
```
dot1x quiet-period-value
```


**命令功能**

配置静默时间

**命令格式**

```
dot1x quiet-period-value times
no dot1x quiet-period-value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 静默时间，默认 | 为60 |

0-600
```
dot1x radius-acl-format
```


**命令功能**

配置下发的ACL 序号格式。

**命令格式**

```
dot1x radius-acl-format [integer | string]
no radius-acl-format
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| integer | 以整数格式下发 | acl |
| 无 | string | 以字符串格式下 |
| 发acl | 无 | 36.8. |

```
dot1x syslog [enable|disable]
```


**命令功能**

（取消）使能日志

**命令格式**

```
dot1x syslog enable
dot1x syslog disable
```


**参数说明**

*无*

```
dot1x timeout
```


**命令功能**

配置服务器与客户端的超时时间。

**命令格式**

```
(no)dot1x timeout server-timeout times
(no)dot1x timeout supp-timeout times
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| tiems | 超时时间，默认 | 为30s |

15-3600

## 36.10. dot1x critical-vlan


**命令功能**

在端口模式下配置critical-vlan (因服务器不可达导致认证失败时加入此vlan)

**命令格式**

```
dot1x critical-vlan Vlan-id
no dot1x critical-vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Vlan-id | Vlan id | 1-4094 |


## 36.11. dot1x defaut-active-vlan


**命令功能**

在端口模式下配置Default-active-vlan(用于802.1X 用户在通过认证时，但没有下发
```
Radius VLAN 的情况，此时用户仅能访问Default-active-vlan 中的资源。)
```


**命令格式**

```
dot1x default-active-vlan Vlan-id
no dot1x default-active-vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Vlan-id | Vlan id | 1-4094 |


## 36.12. dot1x eapol-relay


**命令功能**

在端口下（取消）使能EAPOL 报文透传功能

**命令格式**

```
(no)dot1x dot1x eapol-relay
```


**参数说明**

*无*


## 36.13. dot1x eapol-relay-uplink


**命令功能**

在端口模式下（取消）使能EAPOL 上行端口功能

**命令格式**

（no）dot1x eapol-relay uplink

**参数说明**

*无*


## 36.14. dot1x guest-vlan


**命令功能**

在端口模式下配置访客VLAN（用户认证失败时加入此vlan）

**命令格式**

```
dot1x guest-vlan Vlan-id
no dot1x guest-vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Vlan-id | Vlan id | 1-4094 |


## 36.15. dot1x max-authfail


**命令功能**

在端口模式下配置最大认证失败次数

**命令格式**

```
dot1x max-authfail times
no dot1x max-authfail
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 认证失败次数， | 默认为1 |

1-10

## 36.16. dot1x max-user-num


**命令功能**

（no）dot1x max-user-num <users>
命令在端口模式下配置（删除）允许通过认证的最大用户数

**命令格式**

```
dot1x max-user-num 5
no dot1x max-user-num
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| users | 用户数，默认100 | 1-100 |


## 36.17. dot1x multicast-trigger


**命令功能**

在端口模式下（取消）使能守望者功能

**命令格式**

```
dot1x multicast-trigger
no dot1x multicast-trigger
```


**参数说明**

*无*


## 36.18. dot1x multicast-period


**命令功能**

在端口模式下配置守望者功能报文发送间隔时间

**命令格式**

```
dot1x multicast-period times
no dot1x multicast-period
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 默认为60 | 10-600 |


## 36.19. dot1x native-vlan-free


**命令功能**

在端口模式下（取消）使能允许未认证用户在PVID 内通信功能

**命令格式**

```
dot1x native-vlan-free
no dot1x native-vlan-free
```


**参数说明**

*无*


## 36.20. dot1x port-control [auto | forceauthorized |

forceunauthorized]

**命令功能**

在端口模式下配置端口控制模式

**命令格式**

（no）dot1x port-control [auto | forceauthorized | forceunauthorized]

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| auto | 自动，认证通过 | 后即可通信，默 |
| 认为此模式 | 无 | forceauthorized |
| 强制认证，配置 | 该模式后不认证 | 端口也可通信 |
| 无 | forceunauthorized | 强制不认证，配 |
| 置该模式后端口 | 对认证信息不做 | 处理，不能通信 |

无

## 36.21. dot1x port-method [macbased | portbased ]


**命令功能**

在端口模式下开启dot.1X 认证并配置认证模式

**命令格式**

```
dot1x port-method macbased
dot1x port-method portbased
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| macbased | 基于mac 认证 | 无 |
| portbased | 基于端口认证 | 无 |


## 36.22. dot1x portbased [multi-hosts | single-host]


**命令功能**

在端口模式下配置主机模式

**命令格式**

(no ) dot1x portbased host-mode [multi-hosts | single-host]

**参数说明**

参数

**参数说明**

参数
multi-hosts
多主机模式，默
认模式，当该端
口上有一个用户
认证通过后，该
端口上的其它用
户无需认证即可
以访问网络,默认
该模式
无
single-host
单主机模式，该
端口上只允许一
个认证通过的用
户访问网络，其
它用户无法访问
网络，也无法再
认证通过
无

## 36.23. dot1x re-authenticate


**命令功能**

在端口模式下立即执行重认证

**命令格式**

```
dot1x re-authenticate
```


**参数说明**

*无*


## 36.24. dot1x re-authentication


**命令功能**

在端口模式下(取消)使能周期性重认证

**命令格式**

```
(no)dot1x re-authentication
```


**参数说明**

*无*


## 36.25. dot1x timeout re-authperiod


**命令功能**

在端口模式下配置周期性重认证间隔

**命令格式**

（no）dot1x timeout re-authperiod time

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 间隔时间，默认 | 3600s |

1-3600

## 36.26. dot1x station-move [disbale | enable ]


**命令功能**

端口模式下(取消)使能认证端口迁移功能

**命令格式**

```
dot1x station-move [disbale | enable ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| enable | 使能迁移功能 | 后，用户在一个 |
| 端口上认证通过 | 后，可迁移到另 | 外一个端口进行 |
| 无 | 认证，在新的端 | 口上认证之前会 |
| 删除原端口上的 | 认证结果。 | disable |
| 禁用迁移功能 | 后，用户在一个 | 端口上认证通过 |
| 后，不能迁移到 | 另外一个端口进 | 行认证，除非该 |
| 用户在原端口已 | 经下线。 | 无 |


## 36.27. dot1x keepalive


**命令功能**

在端口模式下（取消）使能心跳检测功能

**命令格式**

```
dot1x keepalive
no dot1x keepalive
```


**参数说明**

*无*


## 36.28. dot1x keepalive period


**命令功能**

全局模式配置心跳检测周期

**命令格式**

```
dot1x keepalive period value
no dot1x keepalive period
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 发送心跳检测报 | 文的周期(s),默认 |
| 为25s | 1-3600 | 36.29. dot1x user cut |


**命令功能**

强制用户下线

**命令格式**

```
dot1x user cut username value
dot1x user cut mac-address macaddress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 需要下线的用户 | 名 |
| 合法在线用户名 | macaddress | 需要下线的mac |

合法在线用户的mac

## 36.30. show dot1x [ethernet port-id]


**命令功能**

查看dot.1X 配置信息

**命令格式**

```
show dot1x [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |


## 36.31. show dot1x config-vlan [ethernet port-id]


**命令功能**

查看配置的dot.1X vlan 信息

**命令格式**

```
show dot1x config-vlan [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |


## 36.32. show dot1x eapol-relay


**命令功能**

查看EAPOL 透传配置信息

**命令格式**

```
show dot1x eapol-relay [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |


## 36.33. show dot1x keepalive [ethernet port-id]


**命令功能**

查看心跳检测配置信息

**命令格式**

```
show dot1x keepalive [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |


## 36.34. show dot1x multicast-trigger [ethernet port-id]


**命令功能**

查看守望者功能配置信息

**命令格式**

```
show dot1x multicast-trigger [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |


## 36.35. show dot1x radius-acl


**命令功能**

查看radius 下发的acl

**命令格式**

```
show dot1x radius-acl
```


**参数说明**

*无*


## 36.36. show dot1x user


**命令功能**

查看认证的用户信息

**命令格式**

```
show dot1x user [ethernet<port-id> | mac-address<mac-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，如ethernet 0/0/1 |
| mac-id | mac 地址 | 48 位二进制数，格式为X:X:X:X:X:X |


## 36.37. show dot1x port-auth


**命令功能**

查看端口认证结果，在portbased 才有用

**命令格式**

```
show dot1x port-auth
```


**参数说明**

*无*


## 36.38. 配置举例

组网
```
PC -----  44 dut 12 ----radius server
命令
1. 配置radius 服务器
Switch(config)#aaa
Switch(config-aaa)#radius host demo
Switch(config-aaa-radius-demo)#primary-auth-ip 10.2.5.240 1812
Switch(config-aaa-radius-demo)#primary-acct-ip 10.2.5.240 1813
Switch(config-aaa-radius-demo)#auth-secret-key maipu
Switch(config-aaa-radius-demo)#acct-secret-key maipu
Raisecom(config-aaa-radius-demo)#username-format without-domain
Switch(config-aaa-radius-demo)#exit
Switch(config-aaa)#domain test
Switch(config-aaa-domain-test)#radius host binding demo
Switch(config-aaa-domain-test)#state active
Switch(config-aaa-domain-test)#exit
Switch(config-aaa)#default domain-name enable test
2. 全局开启dot.1X，端口配置基于mac 认证
Switch(config)#dot1x enable
Switch(config)#dot1x eap-relay enable
Switch(config)#interface eth 0/0/44
Switch(config-if-ethernet-0/0/44)#dot1x port-method macbased
3.PC 发起认证，dut 查看认证用户
Switch(config)#show dot1x user
No 1  mac       : 00:e0:53:12:2a:51  ip    : N/A
username  : maipu@test         status: online
port      : e0/0/44            vlan  : 10
acl       : N/A
login time: 07:02:18 2021/09/01
Total online [1]. (guest online [0], critical online [0])
```


# 37. RADIUS 配置

aaa

**命令功能**

```
aaa 进入aaa 配置模式
```


**命令格式**

aaa

**参数说明**

*无*

```
radius host name
```


**命令功能**

```
aaa 模式下配置radius 名称 ，并进入radius 配置模式
```


**命令格式**

```
radius host name
no radius host
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | radius 主机名 | STRING<1-32> |

primary-auth-ip

**命令功能**

```
radius 模式下配置主认证服务器
```


**命令格式**

```
(no) primary-auth-ip ip-address port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | port |
| tcp 端口号，必须 | 配置 | 1-65535 |

second-auth-ip

**命令功能**

```
radius 模式下配置备份认证服务器
```


**命令格式**

```
(no) second-auth-ip ip-address port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | port |
| tcp 端口号，必须 | 配置 | 1-65535 |

primary-acct-ip

**命令功能**

```
radius 模式下配置主计费服务器
```


**命令格式**

```
(no) primary-acct-ip ip-address port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | port |
| tcp 端口号,必需 | 配置 | 1-65535 |

second-acct-ip

**命令功能**

```
radius 模式下配置从计费服务器
```


**命令格式**

```
(no) second-acct-ip ip-address port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | port |
| tcp 端口号,必须 | 配置 | 1-65535 |

acct-secret-key

**命令功能**

```
radius 模式下配置主认证密码
```


**命令格式**

```
(no)acct-secret-key key
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key | 认证密码 | STRING<1-16> |

auth-secret-key

**命令功能**

```
radius 模式下配置备份认证密码
```


**命令格式**

```
(no) auth-secret-key key
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key | 认证密码 | STRING<1-16> |

realtime-acount

**命令功能**

```
(no) realtime-account <interval <time> >
radius-name 模式下配置（恢复）计费报文发送周期
```


**命令格式**

```
realtime-account interval 10
realtime-account
no realtime-account
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 报文周期 | 1-255s |


## 37.10. username-format [without-domain | with-domain]


**命令功能**

```
radius 模式下(取消)使能带域名认证
```


**命令格式**

```
username-format without-domain
username-format with-domain
```


**参数说明**

*无*


## 37.11. nas-ipaddress


**命令功能**

```
radius 模式下(取消)使能携带NAS_IP Address
```


**命令格式**

```
(no) nas-ipaddress ip-address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | 合法ip |


## 37.12. preemption-time


**命令功能**

```
radius 模式下配置主从服务器的抢占时间
```


**命令格式**

```
preemption-time time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 抢占时间，默认 | 为0 |

0-1440

## 37.13. domain


**命令功能**

AAA 模式下配置并进入域模式

**命令格式**

```
domain name
no domain
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 域名 | Staring<1-24> |


## 37.14. radius host binding [enter | name]


**命令功能**

domain 模式下配置（删除）绑定radius name

**命令格式**

（no）radius host binding [enter | name]

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | radius-name | String<1-32> |


## 37.15. State [active |block]


**命令功能**

domain 模式下(取消)使能域

**命令格式**

```
state active
state block
```


**参数说明**

*无*


## 37.16. access-limit


**命令功能**

domain 模式下配置接入域的用户数量限制

**命令格式**

```
access-limit [enable num | disable ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 允许接入数量 | 1-640 |


## 37.17. scheme [radius | local]


**命令功能**

domain 模式下配置域认证方式

**命令格式**

```
scheme radius
scheme radius local
scheme local
```


**参数说明**

*无*


## 37.18. local-user


**命令功能**

```
aaa 模式下配置本地用户
```


**命令格式**

```
local-user <username name password password vlan vlan-id>
no local-user username name
no local-user all
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 用户名 | 1-64 |
| password | 密码 | 1-64 |
| Vlan-id | Vlan id | 1-4094 |


## 37.19. defaut domain-name


**命令功能**

```
aaa 模式下（取消）使能默认域并配置默认引用的域名
```


**命令格式**

```
default domain-name enable name
default domain-name disable
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 域名 | STRING<1-24> |


## 37.20. radius vlan


**命令功能**

```
(no)radius vlan enable
aaa 模式下开启（关闭）radius 下发vlan 控制
```


**命令格式**

```
radius vlan enable
no radius vlan
```


**参数说明**

*无*


## 37.21. radius vlan-format


**命令功能**

```
radius vlan-format [integer | string2decimal | string2hex | vlanname] aaa 模式下配置
radius 下发vlan 控制格式
```


**命令格式**

```
radius vlan-format string2hex
```


**参数说明**

*无*


## 37.22. radius 8021p enable


**命令功能**

```
aaa 模式下（取消）使能radius 下发802.1p
```


**命令格式**

```
(no) radius 8021p enable
```


**参数说明**

*无*


## 37.23. radius bandwidth-limit


**命令功能**

```
aaa 模式下(取消)使能radius 下发端口带宽控制
```


**命令格式**

```
radius bandwidth-limit enable
no radius bandwidth-limit
```


**参数说明**

*无*


## 37.24. radius mac-address-number


**命令功能**

```
(no) radius mac-address-number enable
aaa 模式下开启（关闭）radius 下发mac 数量控制
```


**命令格式**

```
radius mac-address-number enable
no radius mac-address-number
```


**参数说明**

*无*


## 37.25. radius config-attribute


**命令功能**

```
aaa 模式下修改radius 属性号
```


**命令格式**

```
radius config-attribute access-bandwidth [ downlink | uplink] vendor
radius config-attribute access-bandwidth unit [ kbps | bps]]
radius config-attribute dscp vendor
radius config-attribute mac-address-number vendor
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vendor | 属性号 | 1-500 |


## 37.26. radius accounting


**命令功能**

```
aaa 模式下(取消)使能radius 计费功能
```


**命令格式**

```
(no) radius accounting
```


**参数说明**

*无*


## 37.27. accounting-on


**命令功能**

```
aaa 模式下配置计费报文发送个数
```


**命令格式**

```
accounting-on enable <num>
accounting-on disable
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 报文个数 | 1-255 |


## 37.28. radius server-disconnect


**命令功能**

```
(no)radius server-disconnect drop 1x
aaa 模式下开启（关闭）计费报文无响应切断用户
```


**命令格式**

```
radius server-disconnect drop 1x
no radius server-disconnect drop 1x
```


**参数说明**

*无*


## 37.29. h3c-cams [enable | disable ]


**命令功能**

```
aaa 模式下（取消）使能兼容H3C Cams 特性
```


**命令格式**

h3c-cams [enable | disable ]

**参数说明**

*无*


## 37.30. uprate-value


**命令功能**

（no）uprate-value <value>
AAA 模式下配置（删除）在开启h3c-cams enable 功能下，上行速率的属性值

**命令格式**

```
uprate-value 1
no uprate-value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 1-32 | 37.31. dnrate-value |


**命令功能**

```
aaa 模式下配置上行速率的属性值(开启h3c-cams enable 功能时才会生效)
```


**命令格式**

( no )dnrate-value <value>

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 属性值 | 1-32 |


## 37.32. radius client-version attribute


**命令功能**

```
aaa 模式下(取消)使能上 报客户端版本号给server
```


**命令格式**

```
(no) radius client-version attribute
```


**参数说明**

*无*


## 37.33. show domain


**命令功能**

```
show domaine [enter | name]
查看域 配置信息
```


**命令格式**

```
show domain
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 域名 | Staring<1-24> |


## 37.34. show radius host


**命令功能**

```
show radius host [enter | name]
查看radius 主机配置
```


**命令格式**

```
show radius host
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | radius-server name Staring<1-32> | 37.35. show radius client-version |


**命令功能**

```
show radius client-version
查看radius 客户端版本属性
```


**命令格式**

```
show radius client-version
```


**参数说明**

*无*


## 37.36. show rate-attribute-value


**命令功能**

```
aaa 模式下查看rate 属性运行信息
```


**命令格式**

```
show rate-attribute-value
```


**参数说明**

*无*


## 37.37. show radius config-attribute


**命令功能**

```
show radius config-attribute
查看radius 配置属性
```


**命令格式**

```
show radius config-attribute
```


**参数说明**

*无*


## 37.38. 配置举例

组网
```
PC -----  44 dut 12 ----radius server
配置过程
1.配置radius 服务器，认证密钥，认证时不带域名
Switch(config)#aaa
Switch(config-aaa)#radius host demo
Switch(config-aaa-radius-demo)#primary-auth-ip 10.2.5.240 1812
Switch(config-aaa-radius-demo)#primary-acct-ip 10.2.5.240 1813
Switch(config-aaa-radius-demo)#auth-secret-key maipu
Switch(config-aaa-radius-demo)#acct-secret-key maipu
Raisecom(config-aaa-radius-demo)#username-format without-domain
Switch(config-aaa-radius-demo)#exit
2.配置域，并绑定radius 服务器，激活该域，配置默认引用的域名
Switch(config-aaa)#domain test
Switch(config-aaa-domain-test)#radius host binding demo
Switch(config-aaa-domain-test)#state active
Switch(config-aaa-domain-test)#exit
Switch(config-aaa)#default domain-name enable test
3. 查看配置的radius 服务器
Raisecom(config-aaa)#show radius host
------------------------------------------------------------------------
ServerName  = demo
PrimAuthServerIP = 10.2.5.240       PrimAcctServerIP = 10.2.5.240
SecAuthServerIP  = 0.0.0.0          SecAcctServerIP  = 0.0.0.0
PrimAuthPort     = 0                PrimAcctPort     = 0
SecAuthPort      = 1812             SecAcctPort      = 1813
Auth-secretKey  = maipu         Acct-secretKey  = maipu
UserNameFormat = without-domain
RealTimeAcctSwitch = open       RealTimeAcctTime = 12
RadiusClientIP  =
------------------------------------------------------------------------
Total [1 item(s), printed [1] item(s).
4. 查看配置的域
Raisecom(config-aaa)#show domain
Default domain name : test
DomainName       : test
RADIUSServerName : demo
Access-limit     : disabled
AccessedNum      : 0
Scheme           : radius local
State            : Active
----------------------------------------------------------------------
Total [1] item(s).
```


# 38. Muser 配置

```
muser local [enter | none]
```


**命令功能**

配置认证方式为本地认证

**命令格式**

```
muser local [enter | none]
```


**参数说明**

*无*

```
muser none
```


**命令功能**

配置认证方式为不认证

**命令格式**

```
muser none
```


**参数说明**

*无*

```
muser radius [enter|local|none|local none ]
```


**命令功能**

配置认证方式为radius

**命令格式**

```
muser radius name [enter|local|none|local none ]
```


**参数说明**

*无*

```
muser radius [ pap | chap]
```


**命令功能**

配置radius 认证加密方式

**命令格式**

```
muser radius name [ pap | chap ]
```


**参数说明**

*无*

```
muser radius name account
```


**命令功能**

使能radius 认证时记录上线下线时间

**命令格式**

```
muser radius name account
```


**参数说明**

*无*

```
muser tacacs+[enter|local|none|local none ]
```


**命令功能**

配置认证方式为tacacs+

**命令格式**

```
muser tacacs+ [enter|local|none|local none ]
```


**参数说明**

```
muser tacacs+ [command-account|author | account|
command-author]
```


**命令功能**

配置认证方式为tacacs+

**命令格式**

```
muser tacacs+ [author [account| command-account |command-author]]
muser tacacs+ [account [author | command-account |command-author]]
muser tacacs+ [command-account [author | account| command-author]]
muser tacacs+ [command-author [author | account| command-account ]]
```


**参数说明**

*无*

```
tacacs+ primary server
```


**命令功能**

配置主认证服务器参数

**命令格式**

```
tacacs+ primary server ip [[encrypt-key enkey | key key] port port tiemout time]]
no tacacs+ primary server
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | ip 地址 | enkey |
| 加密后的密码 | STRING<1-66> | key |
| 明文密码 | STRING<1-32> | Port |
| tcp 端口号 | 1-65535 | time |
| 超时时间，默认 | 5s | INTEGER<1-70> |
| tacacs+ secondary server | 命令功 | 配置备份认证服务器参数 |


**命令格式**

```
(no) tacacs+ secondary server ip [[encrypt-key enkey | key key] port port tiemout time]]
no tacacs+ secondary server
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | ip 地址 | enkey |
| 加密密码 | STRING<1-66> | key |
| 明文密码 | STRING<1-32> | Port |
| tcp 端口号 | 1-65535 | time |
| 超时时间，默认 | 5s | 1-70s default：5s |


## 38.10. tacacs+ encrypt-key


**命令功能**

（取消）使能密码加密

**命令格式**

```
tacacs+ encrypt-key
no tacacs+ encrypt-key
```


**参数说明**

*无*


## 38.11. tacacs+ authentication-type [ascii |chap |pap ]


**命令功能**

配置tacacs+认证加密类型

**命令格式**

```
tacacs+ authentication-type [ascii |chap |pap ]
```


**参数说明**

*无*


## 38.12. tacacs+ preemption-time


**命令功能**

配置主从服务器抢占时间

**命令格式**

```
tacacs+ preemption-time time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 抢占时间 | 0-1440 |


## 38.13. show muser login


**命令功能**

查看登录认证配置

**命令格式**

```
show muser login
```


**参数说明**

*无*


## 38.14. show tacacs+


**命令功能**

查看 tacacs+服务器配置

**命令格式**

```
show tacacs+
```


**参数说明**

*无*


## 38.15. 配置举例

组网
```
PC--- dut -----tacacs+ server
命令
1. 配置tacacs+服务器（服务器地址和dut 可通信）
Switch(config)#tacacs+ primary server 10.2.2.50 key 1234
Switch(config)#tacacs+ secondary server 10.2.2.51 key 1234
2. 配置认证方式为tacacs+
Switch(config)#muser tacacs+
3. 在pc 上使用cmd Telnet 上交换机,使用tacacs 服务器用户进行认证
```


# 39. 二级密码认证配置

```
muser enable local
```


**命令功能**

配置二级密码提权使用本地认证

**命令格式**

```
muser enable local [none]
```


**参数说明**

*无*

```
muser enable none
```


**命令功能**

配置二级密码提权不认证

**命令格式**

```
muser enable none
```


**参数说明**

*无*

```
muser enable radius name [enter | local | none ]
```


**命令功能**

配置二级密码提权使用radius 认证

**命令格式**

```
muser enable radius name [enter | local | none ]
```


**参数说明**

*无*

```
muser enable radius
```


**命令功能**

配置二级密码提权radius 认证密码类型

**命令格式**

```
muser enable radius <name> [ pap | chap]
```


**参数说明**

*无*

```
muser enable tacacs+ [enter | local | none ]
```


**命令功能**

二级密码提权为tacacs+s 认证

**命令格式**

```
muser enable tacacs+ [enter | local | none ]
```


**参数说明**

*无*

```
enable password 0 password
```


**命令功能**

配置二级密码明文密码

**命令格式**

```
enable password 0 password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Password | 明文密码 | STRING<1-128> |

```
enable password 7 password
```


**命令功能**

配置二级密码密文密码

**命令格式**

```
enable password 7 password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Password | 密文密码 | STRING<1-128> |

```
enable password level
```


**命令功能**

配置二级密码提权等级

**命令格式**

```
enable password level level [ 0 | 7 ] password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level | 特权级别 | 1-15 |

```
show muser enable
```


**命令功能**

查看置二级密码提权配置

**命令格式**

```
show muser enable
```


**参数说明**

*无*


## 39.10. 配置举例

组网
无
命令
1. 创建用户，等级为1
```
switch(config)#username test privilege 1 password 0 test
2. 配置二级密码提权认证为本地
switch(config)#muser enable local
3. 配置提权12，密码
switch(config)#enable password level 12 0 123
Please input your login password:*****
Super password has been updated, please save configuration
(copy running-config startup-config).
4. 使用等级为1 的用户登录，进行二级提权
Username(1-64 chars):test
Password(1-128 chars):****
switch>enable 12
Please input password : ***
Current user privilege level is ADMIN.
Privilege note: 0~1:NORMAL, 2~15:ADMIN.
```


# 40. LACP 配置

```
interface eth-trunk id
```


**命令功能**

配置或进入汇聚组

**命令格式**

```
interface eth-trunk id
no interface eth-trunk <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 聚合组号 | 1-16 |

32.4 link-aggregation mode [dynamic|static]

**命令功能**

汇聚组模式下配置聚合类型

**命令格式**

```
link-aggregation mode [dynamic|static]
no link-aggregation mode
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dynamic | 动态 | 无 |
| static | 静态 | 无 |

```
link-aggregation members ethernet
```


**命令功能**

汇聚组模式下添加汇聚组成员端口

**命令格式**

```
[no] link-aggregation members ethernet port-id
```


**参数说明**

*无*

```
link-aggregation eth-trunk
```


**命令功能**

端口模式下配置端口加入汇聚组

**命令格式**

```
[no]link-aggregation eth-trunk id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 聚合组号 | 1-16 |

```
lacp mode [active|passive]
```


**命令功能**

端口模式下配置协商模式

**命令格式**

```
lacp mode [active|passive]
no lacp mode
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| passive | 被动 | 无 |
| active | 主动 | 无 |

```
lacp period
```


**命令功能**

端口模式下配置超时方式

**命令格式**

```
lacp period [long|short ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| short | 短超时 | 无 |
| long | 长超时 | 无 |

```
lacp port-priority
```


**命令功能**

端口配置下配置端口优先级

**命令格式**

```
lacp port-priority num
no lacp port-priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 优先级 | 1-65535 |

```
lacp system-priority
```


**命令功能**

配置系统优先级

**命令格式**

```
lacp system-priority num
no lacp system-priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 优先级 | 1-65535 |

```
link-aggregation load-balance
```


**命令功能**

配置汇聚组负载均衡策略

**命令格式**

```
link-aggregation load-balance <dst-ip |dst-mac|src-dst-ip|src-dst-mac|src-ip|src-mac>
no link-aggregation load-balance
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dst-ip | 目的ip | 无 |
| dst-mac | 目的mac | 无 |
| src-dst-ip | 源目的ip | 无 |
| src-dst-mac | 源目的mac | 无 |
| src-ip | 源ip | 无 |
| src-mac | 源mac,默认 | 无 |

```
show lacp local [enter | eth-trunk id]
```


**命令功能**

显示本端聚合组状态

**命令格式**

```
show lacp local [enter | eth-trunk id]
```


**参数说明**


## 40.10. show lacp neighbor


**命令功能**

显示对端聚合组状态

**命令格式**

```
show lacp neighbor [enter | eth-trunk id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 聚合组号 | 1-16 |


## 40.11. show lacp sys-id


**命令功能**

显示系统id 信息

**命令格式**

```
show lacp sys-id
```


**参数说明**

*无*


## 40.12. 配置举例

```
#配置静态链路汇聚组
DUT2(config)#interface eth-trunk 1  //创建汇聚组
DUT2(config-if-eth-trunk-1)#link-aggregation mode static     //配置汇聚组模式为静态
DUT2(config-if-eth-trunk-1)#link-aggregation members ethernet 0/0/10
DUT2(config-if-eth-trunk-1)#link-aggregation members ethernet 0/0/11
DUT2(config-if-eth-trunk-1)#exit
DUT2(config)#link-aggregation load-balance dst-mac
DUT2(config)#show lacp local
Load balance: dst-mac
eth-trunk ID: 1, static channel
Port     State   A-Key  O-Key  Priority   Logic-port   Actor-state
e0/0/10  bndl    -      -      -          10           -
e0/0/11  bndl    -      -      -          10           -
```


# 41. Flex-link 配置

```
flex-link flush MMU send
```


**命令功能**

(取消)使能发送通知MAC 地址漂移

**命令格式**

```
flex-link flush send
no flex-link flush send
id
聚合组号
1-16
```


**参数说明**

*无*

```
flex-link flush MMU receive
```


**命令功能**

(取消)使能接收处理MAC 地址漂移通知

**命令格式**

```
flex-link flush receive
no flex-link flush receive
```


**参数说明**

*无*

```
flex-link group id
```


**命令功能**

创建或删除flex-link 组

**命令格式**

```
flex-link group Id
no flex-link group <Id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | Group ID | [0-30] |

```
master-port [eth portid | eth-trunk lagId]
```


**命令功能**

flex-link 组模式下配置master port

**命令格式**

```
master-port [eth portid | eth-trunk lagId]
no master-port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合组ID | [1-16] |

```
slave-port [eth portid | eth-trunk lagId]
```


**命令功能**

flex-link 组模式下配置slave port

**命令格式**

```
slave-port [eth portid | eth-trunk lagId]
no slave-port
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合组ID | [1-16] |

```
preemption mode [role|bandwidth]
```


**命令功能**

flex-link 组模式下配置抢占模式

**命令格式**

```
preemption mode [role|bandwidth]
no preemption mode
```


**参数说明**

*无*

```
preemption delay time-value
```


**命令功能**

flex-link 组模式下配置抢占延时

**命令格式**

```
preemption delay time-value
no preemption delay
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 抢占延迟 | [1-60] |

```
preemption mode off
```


**命令功能**

flex-link 组模式下关闭抢占功能

**命令格式**

```
preemption mode off
no preemption mode
```


**参数说明**

*无*

```
show flex-link flush
```


**命令功能**

查看flex-link MMU 处理统计信息

**命令格式**

```
show flex-link flush
```


**参数说明**

*无*


## 41.10. show flex-link group


**命令功能**

查看flex-link 组配置信息

**命令格式**

```
show flex-link group Id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | Group ID | [0-30] |


# 42. Monitor-link 配置

```
monitor-link group Id
```


**命令功能**

创建或删除monitor-link 组

**命令格式**

```
monitor-link group Id
no monitor-link group Id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | Group ID | [1-5] |

```
uplink-port [eth portId | eth-trunk lagId]
```


**命令功能**

```
monitor-link group 下添加上行口
```


**命令格式**

```
(no)uplink-port [eth portId | eth-trunk lagId]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合组ID | [1-16] |

```
downlink-port [eth portId | eth-trunk lagId]
```


**命令功能**

```
monitor-link group 下添加下行口
```


**命令格式**

```
(no)downlink-port [eth portId | eth-trunk lagId]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合组ID | [1-16] |

```
show monitor-link
```


**命令功能**

查看monitor-link 组配置信息

**命令格式**

```
show monitor-link group <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | Group ID | [1-5] |


# 43. STP/RSTP 配置

stp

**命令功能**

全局或物理接口使能stp

**命令格式**

stp
```
no stp
```


**参数说明**

*无*

```
stp mode [stp|rstp]
```


**命令功能**

全局配置stp 模式

**命令格式**

```
stp mode [stp|rstp]
no stp mode
```


**参数说明**

*无*

```
stp hello-time
```


**命令功能**

全局配置STP 协议报文发送间隔

**命令格式**

```
stp hello-time  < seconds >
no stp hello-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | Hello 报文发送间 | 隔时间 |

1-10 s，默认2s
```
stp forward-time
```


**命令功能**

全局配置端口forward-delay 时间

**命令格式**

```
stp forward-time  < seconds >
no stp forward-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 变更为Forward 状 | 态延迟时间 |

4-30 s，默认15s
```
stp max-age
```


**命令功能**

全局配置STP 协议报文老化时间

**命令格式**

```
stp max-age < num >
no stp max-age
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 根桥老化时间 | 6-40 s，默认20s |

```
stp pathcost-standard [dot1d-1998|dot1t]
```


**命令功能**

全局配置stp cost 计算方式

**命令格式**

```
stp pathcost-standard [dot1d-1998|dot1t]
no stp pathcost-standard
```


**参数说明**

*无*

```
stp priority
```


**命令功能**

全局配置网桥的stp 优先级

**命令格式**

```
stp priority <num>
no stp priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 优先级大小 | 0-61440 且4096 倍数,默认32768 |

```
stp root-guard action [block-port|drop-bpdu]
```


**命令功能**

全局配置根桥保护行为

**命令格式**

```
stp root-guard action [block-port|drop-bpdu]
```


**参数说明**

*无*

```
stp tc-protection
```


**命令功能**

全局使能TC 保护

**命令格式**

```
stp tc-protection
no stp tc-protection
```


**参数说明**

*无*


## 43.10. stp tc-protection interval


**命令功能**

全局配置TC 保护周期

**命令格式**

```
stp tc-protection interval  <seconds>
no stp tc-protection interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 1-255，默认10s | 43.11. stp tc-protection threshold |


**命令功能**

全局配置保护周期内处理的TC 报文的最大个数

**命令格式**

```
stp tc-protection threshold   <num>
no stp tc-protection threshold
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-255，默认6 | 43.12. stp time-factor |


**命令功能**

全局配置根桥超时因子

**命令格式**

```
stp time-factor  <num>
no stp time-factor
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-10，默认3 | 43.13. stp bpdu-guard |


**命令功能**

物理接口使能bpdu-guard 功能

**命令格式**

```
stp bpdu-guard
no stp bpdu-guard
```


**参数说明**

*无*


## 43.14. stp bpdu-filter


**命令功能**

全局或物理接口过滤bpdu 报文

**命令格式**

```
stp bpdu-filter
no stp bpdu-filter
```


**参数说明**

*无*


## 43.15. stp cost


**命令功能**

物理接口配置根路径的cost

**命令格式**

```
stp cost  <num>
no stp cost
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-200000000 | 43.16. stp portfast [autoedge|disable|edgeport] |


**命令功能**

物理接口配置边缘端口

**命令格式**

```
(no)stp portfast [autoedge|disable|edgeport]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| autoedge | 端口up 后3s 内没 | 有收到bpdu 报文 |
| 自动变成边缘端 | 口 | disable |
| 端口不会变成边 | 缘端口 | edgeport |
| 端口up 后直接变 | 成边缘端口 | 43.17. stp link-type [auto |point-to-point|shared] |


**命令功能**

物理接口配置链路类型

**命令格式**

```
stp link-type [auto |point-to-point|shared]
no stp link-type
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| auto | 自动检测 | point-to-point |
| 点到点 | shared | 非点到点 |


## 43.18. stp loop-guard


**命令功能**

物理接口配置loop-guard 功能

**命令格式**

```
stp loop-guard
no stp loop-guard
```


**参数说明**

*无*


## 43.19. stp mcheck


**命令功能**

执行mcheck 功能

**命令格式**

```
stp mcheck
```


**参数说明**

*无*


## 43.20. stp port-priority


**命令功能**

物理接口配置端口的stp 优先级

**命令格式**

```
stp port-priority <num>
no stp port-priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 优先级大小 | 0-240 且16 倍数，默认128 |


## 43.21. stp root-guard


**命令功能**

物理接口配置root-guard 功能

**命令格式**

```
stp root-guard
no stp root-guard
```


**参数说明**

*无*


## 43.22. stp tcn-restricted


**命令功能**

物理接口配置tcn 传播限制功能

**命令格式**

```
stp tcn-restricted
no stp tcn-restricted
```


**参数说明**

*无*


## 43.23. stp transmit-limit


**命令功能**

配置物理接口最大处理bpdu 报文个数

**命令格式**

```
stp transmit-limit <num >
no stp transmit-limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-255，默认3 | 43.24. show stp interface |


**命令功能**

显示接口stp 信息

**命令格式**

```
show stp interface [brief| ethernet <interface-list>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| brief | 简要信息 | interface-list |

端口列表

## 43.25. 配置举例

组网
DUT1(1,2) ==========(1,2) DUT2 14 ----------PC
11  12
|  |
DUT1 与DUT2 对应1,2 端口互连（环路），DUT2 的11,12 端口自连（自环）。其中DUT1 是根桥。配
置详情如下：
```
#配置根桥
DUT1(config)#stp
DUT1(config)#stp priority 4096
#配置非根桥
DUT2(config)#stp
DUT2(config)#show stp interface brief
Spanning-tree protocol: Enabled, spanning-tree mode: RSTP
Port Protect: R-RootGuard, L-LoopGuard, B-BpduGuard, F-BpduFilter
-----------------------------------------------------------------
Port        Cost      Priority  Protect       Role       State
e0/0/1      20000     128       N/A       Root       Forwarding
e0/0/2      20000     128       N/A       Alternate   Discarding
e0/0/11     20000     128       N/A       Designated  Forwarding
e0/0/12     20000     128       N/A       Backup     Discarding
e0/0/14     200000    128       N/A       Designated  Forwarding
DUT2(config)#show stp interface
Spanning-tree protocol: Enabled, spanning-tree mode: RSTP
STP info timeout factor: 3
TC protection: Enabled, interval: 10, threshold: 6
Bridge time: HelloTime 2s, MaxAge 20s, ForwardDelay 15s
Bridge ID: 32768-000a.6a01.0222
Root Bridge: 4096-000a.6a00.0006                    //根桥信息
Path cost to root bridge: 20000
Topo change times: 13
e0/0/1 STP state: Forwarding
Spanning-tree protocol: Enabled
remote loop detect is Disabled  Port role: RootPort
Port path cost: 20000
Port priority: 128
Root guard: Disabled(block-port)
Loop guard: Disabled, port is not in loop-inconsistent state
Designated bridge: 4096-000a.6a00.0006
Port is a non-edge port                             //非边缘端口
Connected link type: point-to-point
Max transmit limit: 3 BPDUs per HelloTime
Port time: HelloTime 4s, MaxAge 25s, ForwardDelay 20s, MessageAge 0
Rx info expired count: 0, last time:
Rx TC BPDU count: 6, last time: 2019/12/15 17:15:04
TC Protection status: Normal
Tx BPDU: 10
TCN: 0, RST: 10, Config: 0
Rx BPDU: 287
TCN: 0, RST: 287, Config: 0
e0/0/14 STP state: Forwarding
Spanning-tree protocol: Enabled
remote loop detect is Disabled  Port role: DesignatedPort
Port path cost: 200000
Port priority: 128
Root guard: Disabled(block-port)
Loop guard: Disabled, port is not in loop-inconsistent state
Designated bridge: 32768-000a.6a01.0222
Port is an edge port                                //边缘端口
Connected link type: point-to-point
Max transmit limit: 3 BPDUs per HelloTime
Port time: HelloTime 4s, MaxAge 25s, ForwardDelay 20s, MessageAge 1
Rx info expired count: 0, last time:
Rx TC BPDU count: 0, last time:
TC Protection status: Normal
Tx BPDU: 520
TCN: 0, RST: 520, Config: 0
Rx BPDU: 0
TCN: 0, RST: 0, Config: 0
```


# 44. MSTP 配置

stp

**命令功能**

全局或物理接口使能stp

**命令格式**

stp
```
no stp
```


**参数说明**

*无*

```
stp mode mstp
```


**命令功能**

全局配置mstp 模式

**命令格式**

```
stp mode mstp
no stp mode
```


**参数说明**

*无*

```
mstp hello-time
```


**命令功能**

全局配置STP 协议报文发送间隔

**命令格式**

```
mstp hello-time  < seconds >
no mstp hello-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 1-10 s，默认2s | 44.4. |

```
mstp forward-time
```


**命令功能**

全局配置端口forward-delay 时间

**命令格式**

```
mstp forward-time < seconds >
no mstp forward-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 4-30 s，默认15s | 44.5. |

```
mstp max-age
```


**命令功能**

全局配置STP 协议报文老化时间

**命令格式**

```
mstp max-age < num >
no mstp max-age
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 6-40 s，默认20s | 44.6. |

```
mstp max-hops
```


**命令功能**

全局配置域内STP 最大跳数

**命令格式**

```
mstp max-hops < num >
no mstp max-hops
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-255 s，默认20 | 44.7. |

```
mstp instance <id> priority
```


**命令功能**

全局配置生成树实例的优先级

**命令格式**

```
mstp instance <id> priority <num2>
no mstp instance <id> priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | 0-15 |
| num2 | 优先级 | 0-61440 且4096 倍数，默认32768 |

```
mstp root-guard action [block-port|drop-bpdu]
```


**命令功能**

全局配置根桥保护行为

**命令格式**

```
mstp root-guard action [block-port|drop-bpdu]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| drop-bpdu | 丢弃报文 | block-port |
| 阻塞端口 | 默认值 | 44.9. |

```
mstp tc-protection
```


**命令功能**

全局使能TC 保护

**命令格式**

```
mstp tc-protection
no mstp tc-protection
```


**参数说明**

*无*


## 44.10. mstp tc-protection interval


**命令功能**

全局配置TC 保护周期

**命令格式**

```
mstp tc-protection interval <seconds>
no mstp tc-protection interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 1-255，默认10s | 44.11. mstp tc-protection threshold |


**命令功能**

全局配置保护周期内处理的TC 报文的最大个数

**命令格式**

```
mstp tc-protection threshold <num>
no mstp tc-protection threshold
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-255，默认6 | 44.12. mstp time-factor |


**命令功能**

全局配置根桥超时因子

**命令格式**

```
mstp time-factor <num>
no mstp time-factor
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 1-10，默认3 | 44.13. mstp bpdu-guard |


**命令功能**

物理接口使能bpdu-guard

**命令格式**

```
mstp bpdu-guard
no mstp bpdu-guard
```


**参数说明**

*无*


## 44.14. mstp bpdu-filter


**命令功能**

全局或物理接口使能过滤bpdu 报文

**命令格式**

```
mstp bpdu-filter
no mstp bpdu-filter
```


**参数说明**

*无*


## 44.15. mstp instance <id> vlan <vlan-list>


**命令功能**

全局配置生成树实例映射到VLAN

**命令格式**

```
(no)mstp instance <id> vlan <vlan-list>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | 0-15 |
| vlan-list | vlan 列表 | 44.16. mstp region-name |


**命令功能**

全局配置域名

**命令格式**

```
mstp region-name <name>
no mstp region-name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 域名 | STRING<1-32> |


## 44.17. mstp enable instance


**命令功能**

全局使能生成树实例

**命令格式**

```
mstp enable instance <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | 0-15 |


## 44.18. mstp disable instance


**命令功能**

全局去使能生成树实例

**命令格式**

```
mstp disable instance <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | 0-15 |


## 44.19. mstp revision-level


**命令功能**

全局配置revision 级别

**命令格式**

```
mstp revision-level <level>
no mstp revision-level
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level | 级别 | 0-65535 |


## 44.20. mstp flap-guard


**命令功能**

全局使能flap-guard，配置最大震荡次数，配置震荡保护恢复时间

**命令格式**

```
mstp flap-guard [max-flaps <num> time <S1>|recovery-time<S2>]
no mstp flap-guard[max-flaps|recovery-time]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 震荡次数 | 1-100s，默认5s |
| S1 | 震荡间隔时间 | 1-60s，默认10s |
| S2 | 恢复时间 | 30-1000s，默认30s |


## 44.21. mstp external cost


**命令功能**

物理接口配置mstp 域间cost

**命令格式**

```
mstp external cost <num>
no mstp external cost
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 花费开销 | 1-200000000 |


## 44.22. mstp instance <id> cost


**命令功能**

物理接口配置域内的cost

**命令格式**

```
mstp instance <id> cost <num>
no mstp instance <id> cost
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 花费开销 | 1-200000000 |
| id | 实例号 | 0-15 |


## 44.23. mstp portfast


**命令功能**

物理接口配置为边缘端口

**命令格式**

```
mstp portfast[autoedge |disable|edgeport]
no mstp portfast[autoedge |disable|edgeport]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| autoedge | 端口up 后3s 内没 | 有收到bpdu 报文 |
| 自动变成边缘端 | 口 | disable |
| 端口不会变成边 | 缘端口 | edgeport |
| 端口up 后直接变 | 成边缘端口 | 44.24. mstp link-type |


**命令功能**

物理接口配置链路类型

**命令格式**

```
mstp link-type  <auto |point-to-point|shared >
no mstp link-type
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| auto | 自动检测 | point-to-point |
| 点到点 | shared | 非点到点 |


## 44.25. mstp loop-guard


**命令功能**

物理接口配置loop-guard 功能

**命令格式**

```
mstp loop-guard
no mstp loop-guard
```


**参数说明**

*无*


## 44.26. mstp root-guard


**命令功能**

物理接口配置root-guard 功能

**命令格式**

```
mstp root-guard
no mstp root-guard
```


**参数说明**

*无*


## 44.27. mstp mcheck


**命令功能**

物理接口执行mcheck 功能

**命令格式**

```
mstp mcheck
```


**参数说明**

*无*


## 44.28. mstp instance <id> port-priority


**命令功能**

物理接口配置mstp 的实例优先级

**命令格式**

```
mstp instance <id> port-priority   <num>
no mstp instance <id> port-priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 优先级大小 | 0-240 且16 倍数，默认128 |
| id | 实例号 | 0-15 |


## 44.29. mstp instance <id> cost


**命令功能**

物理接口配置mstp 的实例cost 值

**命令格式**

```
mstp instance <id> cost <cost>
no mstp instance <id> cost
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| cost | cost 大小 | 1-200000000 |
| id | 实例号 | 0-15 |


## 44.30. mstp config-digest-snooping


**命令功能**

物理接口配置兼容思科

**命令格式**

```
mstp config-digest-snooping
no mstp config-digest-snooping
```


**参数说明**

*无*


## 44.31. show mstp instance brief


**命令功能**

查看mstp 信息

**命令格式**

```
show mstp instance brief
```


**参数说明**


## 44.32. show mstp instance <id> interface


**命令功能**

查看mstp 信息

**命令格式**

```
show mstp instance <id> interface <port-list>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-list | 端口号 | id |
| 实例号 | 0-15 | 44.33. show mstp disabled-instance |


**命令功能**

查看去使能实例

**命令格式**

```
show mstp disabled-instance
```


**参数说明**

*无*


## 44.34. show mstp config-id


**命令功能**

查看mstp 的域配置

**命令格式**

```
show mstp config-id
```


**参数说明**

*无*


## 44.35. 31.35 配置举例

```
#组网
------------21 DUT3 22 --
|                      |
21                      22
DUT1(1,2) ==========(1,2) DUT2 14 ----------PC
11  12
|  |
DUT1 与DUT2 对应1,2 端口互连（环路），DUT2 的11,12 端口自连（自环）。其中DUT1、DUT2 属于
同一个域region2，且DUT1 属于region1 域根；DUT3 属于另外一个域region1，且在整个生成树中，
DUT3 属于总根。配置详情如下：
#配置总根桥
DUT3(config)#stp
DUT3(config)#stp mode mstp
DUT3(config)#mstp region-name region1
DUT3(config)#mstp instance 0 priority 0
DUT3(config)#mstp hello-time 6
DUT3(config)#mstp forward-time 24
DUT3(config)#mstp max-age 30
#配置域根桥
DUT1(config)#stp
DUT1(config)#stp mode mstp
DUT1(config)#mstp region-name region2
DUT1(config)#mstp instance 0 priority 4096
#配置非根桥
DUT2(config)#stp
DUT2(config)#stp mode mstp
DUT2(config)#mstp region-name region2
DUT2(config)#show mstp instance brief
Current spanning tree protocol is MSTP
Spanning tree protocol is enable
Received information time factor is 3
TC protection is enable, interval is 10, threshold is 6
Flap guard is disable, max count 5, detect perid 10 s, recovery period 30 s
MSTP Instance 0     vlans mapped:1-4094
Bridge ID           32768-000a.6a01.0222
CIST root           0-000a.6a00.03cc                    //总根桥
Region root         4096-000a.6a00.0006                 //域根桥
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15,MaxHops 20
Cist Root time       HelloTime 6,MaxAge 30,ForwardDelay 24,RemainingHops 19
External rpc: 20000, Internal rpc: 20000
PortID      Role    Sts    ExternalCost   InternalCost     Prio.Nbr  Type
e0/0/1      Root   FWD   20000        20000          128.1     P2P
e0/0/2      Alte    DIS    20000        20000          128.2     P2P   //域根备份端口
e0/0/11     Design  FWD   20000        20000          128.11    P2P
e0/0/12     Backup  DIS    20000        20000          128.12    P2P
e0/0/14     Design  FWD   200000       200000         128.14    P2P
e0/0/22     Alte    DIS    20000         20000         128.22    P2P  //总根备份端口
DUT2(config)#show mstp instance 0 interface
Current spanning tree protocol is MSTP
Spanning tree protocol is enable
Received information time factor is 3
TC protection is enable, interval is 10, threshold is 6
Flap guard is disable, max count 5, detect perid 10 s, recovery period 30 s
Bridge id is 32768-000a.6a01.0222
Cist root is 0-000a.6a00.03cc,root port is e0/0/1
Region root is 4096-000a.6a00.0006,root port is e0/0/1
Bridge time:HelloTime 2,MaxAge 20,ForwardDelay 15,MaxHops 20
Cist Root time:HelloTime 6,MaxAge 30,ForwardDelay 24,RemainingHops 19
External root path cost is 20000,internal root path cost is 20000
Port e0/0/1 of instance 0 is forwarding
Port role is RootPort, priority is 128
Port external path cost is 20000,internal path cost is 20000
Root guard disable and port is not in root-inconsistent state
Loop guard disable and port is not in loop-inconsistent state
Designated bridge is 4096-000a.6a00.0006,designated port is e0/0/2
Port is a(n) non-edge port,link type is point-to-point              //非边缘端口
Port time:HelloTime 6,MaxAge 30,FwdDelay 24,MsgAge 1,RemainingHops 19
Received TC flag BPDU count:6; last time:2019/12/15 18:17:20
TC Protection status: Normal
Received information expired count:0; last time:
Received BPDUs:TCN 0,RST 89,Config BPDU 0
Transmitted BPDUs:TCN 0,RST 13,Config BPDU 0
Port e0/0/14 of instance 0 is forwarding
Port role is DesignatedPort, priority is 128
Port external path cost is 200000,internal path cost is 200000
Root guard disable and port is not in root-inconsistent state
Loop guard disable and port is not in loop-inconsistent state
Designated bridge is 32768-000a.6a01.0222,designated port is e0/0/14
Port is a(n) edge port,link type is point-to-point                    //边缘端口
Port time:HelloTime 6,MaxAge 30,FwdDelay 24,MsgAge 1,RemainingHops 19
Received TC flag BPDU count:0; last time:
TC Protection status: Normal
Received information expired count:0; last time:
Received BPDUs:TCN 0,RST 0,Config BPDU 0
Transmitted BPDUs:TCN 0,RST 95,Config BPDU 0
#配置端口域内根路径消费，端口优先级
DUT2(config)#interface ethernet 0/0/2
DUT2(config-if-ethernet-0/0/2)#mstp instance 0 cost 18000       //消费最小的端口将作为根端口
DUT2(config-if-ethernet-0/0/2)#interface ethernet 0/0/12
DUT2(config-if-ethernet-0/0/12)#mstp instan 0 port-priority 64  //优先级更大的端口不容易阻塞
DUT2(config-if-ethernet-0/0/12)#show mstp instance brief
Current spanning tree protocol is MSTP
Spanning tree protocol is enable
Received information time factor is 3
TC protection is enable, interval is 10, threshold is 6
Flap guard is disable, max count 5, detect perid 10 s, recovery period 30 s
MSTP Instance 0     vlans mapped:1-4094
Bridge ID           32768-000a.6a01.0222
CIST root           0-000a.6a00.03cc
Region root         4096-000a.6a00.0006
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15,MaxHops 20
Cist Root time      HelloTime 6,MaxAge 30,ForwardDelay 24,RemainingHops 19
External rpc: 20000, Internal rpc: 18000
PortID      Role    Sts    ExternalCost   InternalCost    Prio.Nbr   Type
e0/0/1      Alte    DIS    20000        20000         128.1     P2P
e0/0/2      Root   FWD   20000        18000         128.2     P2P
e0/0/11     Backup  DIS    20000        20000         128.11    P2P
e0/0/12     Design  FWD   20000        20000         64.12     P2P
e0/0/14     Design  FWD   200000       200000        128.14    P2P
e0/0/22     Alte    DIS    20000         20000        128.22     P2P
DUT2(config-if-ethernet-0/0/12)#interface ethernet 0/0/22
DUT2(config-if-ethernet-0/0/22)#mstp external cost 18000
DUT2(config-if-ethernet-0/0/22)#show mstp instance brief
Current spanning tree protocol is MSTP
Spanning tree protocol is enable
Received information time factor is 3
TC protection is enable, interval is 10, threshold is 6
Flap guard is disable, max count 5, detect perid 10 s, recovery period 30 s
MSTP Instance 0     vlans mapped:1-4094
Bridge ID           32768-000a.6a01.0222
CIST root           0-000a.6a00.03cc
Region root         32768-000a.6a01.0222       //由于DUT2 到总根消费更小，DUT2 成为域根
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15,MaxHops 20
Cist Root time      HelloTime 6,MaxAge 30,ForwardDelay 24,RemainingHops 20
External rpc: 18000, Internal rpc: 0
PortID      Role   Sts   ExternalCost    InternalCost    Prio.Nbr  Type
e0/0/1      Design FWD   20000        20000         128.1     P2P
e0/0/2      Design FWD   20000        18000         128.2     P2P
e0/0/11     Backup DIS    20000        20000         128.11    P2P
e0/0/12     Design FWD   20000        20000         64.12     P2P
e0/0/14     Design FWD   200000       200000        128.14    P2P
e0/0/22     Root   FWD   18000        20000         128.22    P2P
说明：当DUT2 取代DUT1 成为域根之后，原来的域内根端口，域内根备份端口全部转变为指定端口，所
以端口1,2 都是转发状态，相反DUT1 将会存在一个域内根端口和域内根备份端口。
```


# 45. PVST 配置

```
stp mode [pvst|rapid-pvst]
```


**命令功能**

全局配置pvst 模式

**命令格式**

```
stp mode [pvst|rapid-pvst]
no stp mode
```


**参数说明**

*无*

```
pvst forward-time
```


**命令功能**

全局配置切换forwarding 状态延迟时间

**命令格式**

```
pvst forward-time <time-value>
no pvst forward-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 延迟时间值 | [4-30] |

```
pvst hello-time
```


**命令功能**

全局配置hello 间隔时间

**命令格式**

```
pvst hello-time <time-value>
no pvst hello-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | hello 间隔时间值 | [1-10] |

```
pvst instance id priority
```


**命令功能**

全局配置实例优先级

**命令格式**

```
pvst instance <id> priority <pri-value>
no pvst instance <id> priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | [0-15] |
| pri-value | 实例优先级 | [0-61440] |

```
pvst instance id vlan
```


**命令功能**

全局配置实例映射VLAN

**命令格式**

```
pvst instance <id> vlan <vid>
no pvst instance <id> vlan <vid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | [0-15] |
| vid | VLAN ID | [2-4094] |

```
pvst max-age
```


**命令功能**

全局配置根桥超时时间

**命令格式**

```
pvst max-age <time-value>
no pvst max-age
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 时间值 | [6-40] |

```
pvst instance id cost
```


**命令功能**

端口下配置实例消费

**命令格式**

```
pvst instance <id > cost <cost-value>
no pvst instance <id> cost
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例号 | [0-15] |
| cost-value | 路径消费 | [1-200000000] |

```
pvst instance id port-priority
```


**命令功能**

端口下配置实例消费

**命令格式**

```
pvst instance <id> port-priority <pri-value>
no pvst instance <id> port-priority
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| iid | 实例号 | [0-15] |
| pri-value | 优先级 | [0-240] |

```
show pvst instance brief
```


**命令功能**

全局配置实例优先级

**命令格式**

```
show pvst instance brief [<iid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| iid | 实例号 | [0-15] |


## 45.10. 配置举例

组网
1 DUT1 11----------- 12 DUT 2 2
|_________________________|
配置
```
DUT1(config)#stp
DUT1(config)#stp mode pvst
DUT1(config)#vlan 2
DUT1(config-vlan-2)#interface range eth 0/0/1 ethernet 0/0/11
DUT1(config-if-range)#switchport hybrid tagged vlan 2
DUT1(config-if-range)#ex
DUT1(config)#pvst instance 1 vlan 2
DUT1(config)#pvst instance 0 priority 4094
DUT1(config)#pvst instance 1 priority 4094
DUT2(config)#stp
DUT2(config)#stp mode pvst
DUT2(config)#vlan 2
DUT2(config-vlan-2)#interface range eth 0/0/2 ethernet 0/0/12
DUT2(config-if-range)#switchport hybrid tagged vlan 2
DUT2(config-if-range)#ex
DUT2(config)#pvst instance 1 vlan 2
DUT1(config)#show pvst instance brief
Current spanning tree protocol is pvst
PVST Instance 0     1,3-4094
Bridge ID           0-000a.6a00.03ee
Root   ID           0-000a.6a00.03ee
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root   time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root path cost:     0
PortID      Config Role   Sts   PathCost  Prio.Nbr  Type
-----------------------------------------------------------
GE0/0/1     YES    Design FWD   20000     128.1     P2P
GE0/0/11    YES    Design FWD   20000     128.11    P2P
PVST Instance 1     vlans mapped: 2
Bridge ID           0-000a.6a00.03ee
Root   ID           0-000a.6a00.03ee
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root   time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root path cost:     0
PortID      Config Role   Sts   PathCost  Prio.Nbr  Type
-----------------------------------------------------------
GE0/0/1     YES    Design FWD   20000     128.1     P2P
GE0/0/11    YES    Design FWD   20000     128.11    P2P
DUT2(config)#show pvst instance brief
Current spanning tree protocol is pvst
PVST Instance 0     1,3-4094
Bridge ID           0-000a.6a00.03ee
Root   ID           0-000a.6a00.03ee
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root   time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root path cost:     0
PortID      Config Role   Sts   PathCost  Prio.Nbr  Type
-----------------------------------------------------------
GE0/0/1     YES    Design FWD   20000     128.1     P2P
GE0/0/11    YES    Design FWD   20000     128.11    P2P
PVST Instance 1     vlans mapped: 2
Bridge ID           0-000a.6a00.03ee
Root   ID           0-000a.6a00.03ee
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root   time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root path cost:     0
PortID      Config Role   Sts   PathCost  Prio.Nbr  Type
-----------------------------------------------------------
GE0/0/1     YES    Design FWD   20000     128.1     P2P
GE0/0/11    YES    Design FWD   20000     128.11    P2P
DUT2(config)#show pvst instance brief 1
Current spanning tree protocol is pvst
PVST Instance 1     vlans mapped: 2
Bridge ID           32768-0011.2233.4455
Root   ID           0-000a.6a00.03ee
Bridge time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root   time         HelloTime 2,MaxAge 20,ForwardDelay 15
Root path cost:     20000
PortID  Config Role   Sts   PathCost  Prio.Nbr  Type
-----------------------------------------------------------
e0/0/2  YES    Root   FWD   20000     128.2     P2P
e0/0/12 YES    Alte   DIS   20000     128.12    P2P
```


# 46. LBD 配置

```
loopback-detection action [discarding | shutdown]
```


**命令功能**

配置环路处理模式。

**命令格式**

```
loopback-detection action [discarding | shutdown]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| discarding | 设置环回端口为 | discarding 状态 |
| (默认模式) | 无 | shutdown |
| 关闭环回端口 | 无 | 46.2. |

```
loopback-detection interface [enter | ethernet <portid >]
```


**命令功能**

开启/关闭端口的loopback-detection 功能

**命令格式**

```
(no)loopback-detection interface [enter | ethernet <portid >]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portid | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | 46.3. |

loopback-detection

**命令功能**

开启/关闭全局的loopback-detection 功能。
在端口模式下执行此命令，开启该端口的loopback-detection 功能

**命令格式**

loopback-detection
```
no loopback-detection
```


**参数说明**

*无*

```
loopback-detection interval-time
```


**命令功能**

配置环路处理间隔时间。

**命令格式**

(no ) loopback-detection interval-time <times>

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 间隔时间(单位: | 秒, 默认值: 5 秒 5-300 |

```
show loopback-detection
```


**命令功能**

查看loopback-derection 配置。

**命令格式**

```
show loopback-detection [ethernet <portid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portid | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | 46.6. |


**配置举例**

组网
DUT1 -/11---------9/11 DUT2
配置
1. 开启全局和端口的loopback-detection 功能
```
dut1(config)#loopback-detection
dut1(config)#loopback-detection interface
dut2(config)#loopback-detection
dut2(config)#loopback-detection interface
2. 查看loopback-detection 状态，解除环路，端口11 为discard 状态
dut1(config)#s loopback-detection ethernet  0/0/9 ethernet 0/0/11
LB-Detect:Enable
Loopback-detection action is Discarding
The interval time is 5 seconds
The recovery time of the discarding action is 15 seconds
Port Information:
port     loopback  status
e0/0/9   Enable    Normal
e0/0/11  Enable    Discarding
dut2(config)#s loopback-detection ethernet 0/0/9 ethernet 0/0/11
LB-Detect:Enable
Loopback-detection action is Discarding
The interval time is 5 seconds
The recovery time of the discarding action is 15 seconds
Port Information:
port     loopback  status
e0/0/9   Enable    Normal
e0/0/11  Enable    Normal
```


# 47. EAPS 配置

eaps

**命令功能**

全局(取消)使能eaps

**命令格式**

eaps
```
no eaps
```


**参数说明**

*无*

```
eaps domain
```


**命令功能**

全局下创建或删除域

**命令格式**

```
eaps domain <domain-id>
no eaps domain <domain-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| domain-id | 域ID | [0-15] |

```
eaps fail-timer
```


**命令功能**

全局下配置信息超时定时器

**命令格式**

```
eaps fail-timer <time-value>
no eaps fail-timer
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 超时时间 | [3-30] |

```
eaps hello-timer
```


**命令功能**

全局下配置健康报文定时器

**命令格式**

```
eaps hello-timer <time-value>
no eaps hello-timer
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | Hello 报文间隔时 | 间 |

[1-10]
```
eaps preup-timer
```


**命令功能**

全局下配置延迟恢复定时器

**命令格式**

```
eaps preup-timer <time-value>
no eaps preup-timer
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 超时时间 | [0-30] |

control-vlan

**命令功能**

域下配置主环控制vlan

**命令格式**

```
control-vlan <vid>
no control-vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN ID 号 | [1-4093] |

```
ring rid role
```


**命令功能**

域下配置环角色

**命令格式**

```
ring <rid> role [master | transmit | edge | assistant-edge] primary-port [eth <pid> | eth-
trunk <lagid>] secondary-port [eth <pid> | eth-trunk <lagid>] level <level-id>
no ring ring-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rid | 环号 | [0-15] |
| pid | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagid | 聚合口ID | [1-16] |
| level-id | 环级别 | [0,1] |

```
ring rid [enable | disable]
```


**命令功能**

域下（取消）使能环

**命令格式**

```
ring <rid> [enable | disable]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| rid | 环号 | [0-15] |

```
topo-collect
```


**命令功能**

域下（取消）使能拓扑收集

**命令格式**

```
topo-collect
no topo-collect
```


**参数说明**

*无*


## 47.10. work-mode


**命令功能**

域下配置工作模式

**命令格式**

```
work-mode [eips-subring | rrpp | standard]
```


**参数说明**

*无*


## 47.11. show eaps


**命令功能**

查看eaps 配置以及报文统计

**命令格式**

```
show eaps [domain]
```


**参数说明**

*无*


## 47.12. show eaps control-vlan


**命令功能**

查看控制vlan 以及其包含端口所属域环信息

**命令格式**

```
show eaps control-vlan [<vid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN ID | [1-4094] |


## 47.13. show eaps topology


**命令功能**

查看控制vlan 以及其包含端口所属域环信息

**命令格式**

```
show eaps topology [brief | domain <did> [ring <rid>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| did | 域ID | [0-15] |
| rid | 环ID | [0-15] |


## 47.14. 配置举例

组网
1 DUT1 11----------- 12 DUT 2 2
|_________________________|
配置
```
DUT1(config)#interface range ethernet 0/0/1 ethernet 0/0/11
DUT1(config-if-range)#no stp
DUT1(config-if-range)#exit
DUT1(config)#eaps
DUT1(config)#eaps domain 0
DUT1(config-eaps-domain-0)#control-vlan 100
DUT1(config-eaps-domain-0)#topo-collect
DUT1(config-eaps-domain-0)#ring 0 role master primary-port eth 0/0/1 secondary-port eth 0/0/11 level 0
DUT1(config-eaps-domain-0)#ring 0 enable
DUT2(config)#interface range ethernet 0/0/2 ethernet 0/0/12
DUT2(config-if-range)#no stp
DUT2(config-if-range)#exit
DUT2(config)#eaps
DUT2(config)#eaps domain 0
DUT2(config-eaps-domain-0)#control-vlan 100
DUT2(config-eaps-domain-0)#topo-collect
DUT2(config-eaps-domain-0)#ring 0 role transmit primary-port eth 0/0/12 secondary-port eth 0/0/2 level 0
DUT2(config-eaps-domain-0)#ring 0 enable
DUT1(config)#show eaps topology
domain 0 topology info:
ring ID    : 0
topo status: round
topo index: 1
host name  : DUT2
node role  : master
node status: COMPLETE
border     : no
base mac   : 00:0a:6a:00:03:ee
system oid : 1.3.6.1.4.1.54367.1.3.68
port     mac               role      block-status link-status
GE0/0/1  00:0a:6a:00:03:ee primary   unblock      up
GE0/0/11 00:0a:6a:00:03:ee secondary block        up
total nodes: 1
DUT2(config-eaps-domain-0)#show eaps topology
domain 0 topology information:
ring ID    : 0
topo status: not round
topo index: 1
host name  : DUT2
node role  : transit
node status: LINK-UP
border     : no
base mac   : 00:11:22:33:44:55
system oid : 1.3.6.1.4.1.13464.1.3.32
port     mac               role      block-status link-status
e0/0/12  00:11:22:33:44:55 primary   unblock      up
e0/0/2   00:11:22:33:44:55 secondary unblock      up
total nodes: 1
```


# 48. ERPS 配置

erps

**命令功能**

全局开启erps 功能。

**命令格式**

erps
```
no erps
```


**参数说明**

*无*

```
erps instance
```


**命令功能**

创建/删除并进入erps instance。

**命令格式**

```
(no) erps instance <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | instance id | 0-15 |

control-vlan

**命令功能**

在erps instance 模式配置/删除控制VLAN。

**命令格式**

```
(no) control-vlan <vlan id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan id | 配置控制vlan， | 该vlan 为未配置 |
| 的vlan | 2-4094 | 48.4. |

guard-timer

**命令功能**

在erps instance 模式配置/删除guard-timer。

**命令格式**

```
(no) guard-timer <times>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 100-2000ms，default：500ms | 48.5. |

mel

**命令功能**

在erps instance 模式配置/删除mel。

**命令格式**

```
(no) mel <level>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level | erps instance 下 | 关联cfm 的level 0-7， default：0 |

port0

**命令功能**

在erps instance 模式配置/删除port0 端口和模式。

**命令格式**

```
(no) port0 [eth-trunk id | ethernet portid] [neighbour | next-neighbour |owner]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| neighbour | rpl neighbour | owner |
| rpl-owner | next-neighbour | 下一个邻居 |
| port-id | 端口号 | id |

汇聚组号
port1

**命令功能**

在erps instance 模式配置/删除port1 端口和模式。

**命令格式**

```
(no) port1 [eth-trunk id | ethernet portid] [neighbour | next-neighbour |owner]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| neighbour | rpl neighbour | owner |
| rpl-owner | next-neighbour | 下一个邻居 |
| port-id | 端口号 | id |

汇聚组号
protected-instance

**命令功能**

在erps instance 模式配置/删除引用的实例。

**命令格式**

```
(no) protected-instance <id>
no protected-instance
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | mstp 创建的实例 | id |

1-64
ring

**命令功能**

在erps instance 模式配置ring 配置。

**命令格式**

```
ring [ id ] enable [ level level ]
ring [ id ] disable
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | Ring id | 1-239 |
| level | 环级别 | (0-主环, 1-子环 |

0-1

## 48.10. work-mode


**命令功能**

在erps instance 模式配置工作模式。

**命令格式**

```
work-mode [ non-revertive | revertive ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| revertive | 切换，默认为此 | 模式 |
| revertive | non-revertive | 不切换 |

non-revertive

## 48.11. wtr-timer


**命令功能**

在erps instance 模式工作模式切换等待时间。

**命令格式**

(no )wtr-timer <time>

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 默认为5 分钟 | 1-12 |


## 48.12. show erps


**命令功能**

```
show erps 查看erps 状态。
```


**命令格式**

```
show erps
```


**参数说明**

*无*


## 48.13. show erps control-vlan


**命令功能**

查看erps 控制vlan。

**命令格式**

```
show erps control-vlan <vlan id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | VLAN ID | 1-4094 |


## 48.14. show erps instance


**命令功能**

查看erps 某一实例状态。

**命令格式**

```
show erps instance < id >
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 实例id | 0-15 |


## 48.15. show erps statistics


**命令功能**

查看erps 统计。

**命令格式**

```
show erps statistics
```


**参数说明**

*无*


## 48.16. 配置举例

组网
DUT1 11/12---------11/12 DUT2
命令
1. 关闭erps 端口的stp 功能
```
dut1(config)#interface range ethernet 0/0/11 ethernet 0/0/12
dut1(config-if-range)#no stp
dut2(config)#interface range ethernet 0/0/11 ethernet 0/0/12
dut2(config-if-range)#no stp
2. dut1，dut2 开启erps，配置erps 端口角色
dut1(config)#erps
dut1(config)#erps instance 0
dut1(config-erps-instnace-0)#control-vlan 99
dut1(config-erps-instnace-0)#port0 eth 0/0/11 owner
dut1(config-erps-instnace-0)#port1 eth 0/0/12
dut1(config-erps-instnace-0)#protected-instance 0
dut1(config-erps-instnace-0)#ring enable
dut2(config)#erps
dut2(config)#erps instance 0
dut2(config-erps-instnace-0)#control-vlan 99
dut2(config-erps-instnace-0)#port0 eth 0/0/11 neighbour
dut2(config-erps-instnace-0)#port1 eth 0/0/12
dut2(config-erps-instnace-0)#protected-instance 0
dut2(config-erps-instnace-0)#ring enable
3. 待组网稳定后查看erps 状态
dut1(config)#show erps
ERPS state          : enable
Instance Id         : 0
Mel                 : 0
Work-mode           : revertive
WTR Timer           : 5 min
Guard Timer         : 500 ms
Holdoff Timer       : 0 s
Ring 1 info         :
Control vlan        : 99
Status              : enable
Protected-instance  : 0
Role                : Owner
Sub-ring            : No
Stm                 : Pending
--------------------------------------------------------------
port   portId   role    state       nodeId             BPR
--------------------------------------------------------------
port0  e0/0/11  Owner   Blocking    00:00:00:00:00:00  0
port1  e0/0/12  Common  Forwarding  00:00:00:00:00:00  0
Total 1 ring(s).
dut2(config-erps-inst-0)#s erps
ERPS state          : enable
Instance Id         : 0
Mel                 : 0
Work-mode           : revertive
WTR Timer           : 5 min
Guard Timer         : 500 ms
Holdoff Timer       : 0 s
Ring 1 info         :
Control vlan        : 99
Status              : enable
Protected-instance  : 0
Role                : Neighbour
Sub-ring            : No
Stm                 : Idle
--------------------------------------------------------------
port   portId    role       state       nodeId             BPR
--------------------------------------------------------------
port0  GE0/0/9   Neighbour  Blocking    00:0a:5e:00:00:33  0
port1  GE0/0/11  Common     Forwarding  00:0a:5e:00:00:33  0
Total 1 ring(s).
```


# 49. DHCP-Snooping 配置


## 49.1. dhcp-snooping


**命令功能**

在全局模式或vlan 模式（取消）使能dhcp-snooping

**命令格式**

```
dhcp-snooping
no dhcp-snooping
```


**参数说明**

*无*

```
dhcp-snooping fast-remove
```


**命令功能**

使能快速老化

**命令格式**

```
dhcp-snooping fast-remove
no dhcp-snooping fast-remove
```


**参数说明**

*无*

```
dhcp-snooping dhcp-server
```


**命令功能**

指定 dhcp server

**命令格式**

```
dhcp-snooping dhcp-server <ipaddress>
no dhcp-snooping dhcp-server [all | <ipaddress>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | Dhcp server ip | 无 |

```
dhcp-snooping max-learn-num
```


**命令功能**

在端口模式或vlan 模式配置最大学习数量

**命令格式**

```
dhcp-snooping max-learn-num value
no dhcp-snooping max-learn-num
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 具体限值 | 0-2048 |

```
dhcp-snooping trust
```


**命令功能**

在端口模式或vlan 模式配置(取消)使能trust

**命令格式**

```
dhcp-snooping trust
no dhcp-snooping trust
```


**参数说明**

*无*

```
show dhcp-snooping
```


**命令功能**

查看信息

**命令格式**

```
show dhcp-snooping vlan
show dhcp-snooping interface [ethernet <port-id>]
show dhcp-snooping clients
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | 50. DHCP-Option82 配置 |


## 50.1. dhcp-option82


**命令功能**

全局或VALN 或端口(取消)使能dhcp-option82

**命令格式**

```
dhcp-option82
no dhcp-option82
```


**参数说明**

*无*


## 50.2. dhcp-option82 device-id


**命令功能**

全局配置添加device-id 信息

**命令格式**

```
dhcp-option82 device-id
no dhcp-option82 device-id
```


**参数说明**

*无*


## 50.3. dhcp-option82 format


**命令功能**

全局配置添加device-id 信息

**命令格式**

```
dhcp-option82 format [normal | user-defined | verbose [node-identifier [hostname |
mac | user-defined <node-value>]]]
no dhcp-option82 format [verbose node-identifier]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| node-value | 自定义node 信息 | 1-60 个字符 |


## 50.4. dhcp-option82 information format


**命令功能**

全局配置option82 内容格式

**命令格式**

```
dhcp-option82 information format [ascii | hex]
no dhcp-option82 information format
```


**参数说明**

*无*


## 50.5. dhcp-option82 circuit-id


**命令功能**

VLAN 或端口下配置circuit-id 内容

**命令格式**

```
dhcp-option82 circuit-id user-defined <circuit-info>
no dhcp-option82 circuit-id user-defined
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| circuit-info | circuit-id 信息 | 1-128 个字符 |


## 50.6. dhcp-option82 remote-id


**命令功能**

VLAN 或端口下配置remote-id 内容

**命令格式**

```
dhcp-option82 remote-id user-defined <remote-info>
no dhcp-option82 remote-id user-defined
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| remote-info | remote-id 信息 | 1-128 个字符 |


## 50.7. dhcp-option82 strategy


**命令功能**

VLAN 或端口下配置处理option82 报文策略

**命令格式**

```
dhcp-option82 strategy [drop | keep | replace]
no dhcp-option82 strategy
```


**参数说明**

*无*


## 50.8. show dhcp-option82 interface


**命令功能**

查看dhcp-option82 端口下的配置

**命令格式**

```
show dhcp-option82 interface [ethernet <port-id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 取端口id | 数字形式字符串，不区分大小写，不支持空 |
| 格，长度范围是5-6。端口范围与交换机物 | 理端口相等 | 50.9. show dhcp-option82 vlan |


**命令功能**

查看dhcp-option82 vlan 下的配置

**命令格式**

```
show dhcp-option82 vlan [vlan-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | 取VLAN id | 数字形式字符串，不区分大小写，不支持空 |

格，长度范围是1-128。字符串范围1-4094

# 51. DHCP-Server 配置


## 51.1. dhcp-server


**命令功能**

全局配置dhcp-server

**命令格式**

```
dhcp-server ID ipaddress
no dhcp-server ID
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | Server 编号 | 1-256 |
| ipaddress | Server ip | 51.2. dhcp-server <id> |


**命令功能**

接口模式配置应用dhcp-server

**命令格式**

```
dhcp-server id
no dhcp-server id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | Server 编号 | 1-256 |

```
dhcp-server ip-pool name
```


**命令功能**

创建pool

**命令格式**

```
dhcp-server ip-pool name
no dhcp-server ip-pool name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Pool name | 1-32 个字符 |

```
gateway ipaddress mask
```


**命令功能**

在pool 模式下配置gateway

**命令格式**

```
gateway ipaddress mask
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | Ip address | DUT 应用该pool 的接口ip |
| mask | 子网掩码 | 51.5. |

```
setion id startip endip
```


**命令功能**

Pool 模式下配置地址池

**命令格式**

```
setion id startip endip
no section id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 地址段编号 | 0-7 |
| startip | 起始IP | endip |

线束IP
```
router ipaddress
```


**命令功能**

Pool 模式配置地址池分配给client 时的网关

**命令格式**

```
(no)router ipaddress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ipaddress | 网关地址 | 51.7. |

```
lease time
```


**命令功能**

pool 模式配置lease time

**命令格式**

```
(no)lease ddd:hh:mm
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ddd:hh:mm | 老化时间 | 默认24h |

dns-list

**命令功能**

pool 配置模式配置dns server

**命令格式**

```
(no)dns-list [fourth-ip |primary-ip|second-ip|third-ip] ipaddress
```


**参数说明**

*无*

domain-name

**命令功能**

pool 模式下配置domain name suffix

**命令格式**

```
(no)domain-name string
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | Domain name | 1-32 个字符 |


## 51.10. nbns-list ipaddress


**命令功能**

pool 模式下配置WINS server list

**命令格式**

```
(no)nbns-list [primary-ip|second-ip] ipaddress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | Wins server ip | 51.11. forbidden-ip ipaddress |


**命令功能**

pool 模式下配置不分配的ip

**命令格式**

```
(no)forbidden-ip ipaddress
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | Ip address | 51.12. option |


**命令功能**

pool 模式下配置option

**命令格式**

```
(no)option code ……
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| code | Option code | 4-254 |


## 51.13. unbind-client


**命令功能**

pool 模式下配置不匹配绑定表项的用户使用的IP

**命令格式**

```
(no)unbind-client section <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 地址段编号 | 0-7 |


## 51.14. dhcp-client bind ipaddress macaddress vid


**命令功能**

全局配置绑定用户

**命令格式**

```
(no)dhcp-client bind ipaddress macaddress vid
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 绑定的ip | Pool 中合法地址 |
| macaddress | 用户mac | 合法mac |
| vid | Vlan id | 1-4094 |


## 51.15. dhcp-client bind


**命令功能**

全局（取消）使能绑定用户功能

**命令格式**

```
(no)dhcp-client bind
```


**参数说明**

*无*


## 51.16. dhcp-client unbind-assign


**命令功能**

全局使能给未绑定用户分配IP

**命令格式**

```
(no)dhcp-client unbind-assign
```


**参数说明**

*无*


## 51.17. show dhcp-server


**命令功能**

查看配置

**命令格式**

```
show dhcp-server  <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | Server 编号 | 1-256 |


## 51.18. show dhcp-server clients


**命令功能**

查看客户端表项

**命令格式**

```
show dhcp-server clients [ip address <mask> |mac adress |ip pool name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip address | Ip address | 从地址池中学习到的ip 地址 |
| mask | 子网掩码 | mac adress |
| mac 地址 | ip pool name | 地址池 |

STRING<1-32>

## 51.19. show dhcp-server interface


**命令功能**

查看接口下的dhcp 配置

**命令格式**

```
show dhcp-server interface [supervlan-interface<superVLAN ID> |vlan-interface
<id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| superVLAN ID | number | 1-128 |
| id | vlan id | 1-4094 |


## 51.20. show dhcp-server ip-pool


**命令功能**

查看dhcp 地址池配置

**命令格式**

```
show dhcp-server ip-pool [<name>|brief]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Pool name | 1-32 个字符 |


## 51.21. show dhcp-client bind


**命令功能**

查看dhcp-client 绑定表项

**命令格式**

```
show dhcp-client bind [enter | A.B.C.D | H:H:H:H:H:H]
```


# 52. DHCP-Relay 配置


## 52.1. dhcp-relay


**命令功能**

全局或端口(取消)使能dhcp-relay

**命令格式**

```
dhcp-relay
no dhcp-relay
```


**参数说明**

*无*

```
dhcp-relay hide server-ip
```


**命令功能**

(取消)使能隐藏server

**命令格式**

```
dhcp-relay hide server-ip
no dhcp-relay hide server-ip
```


**参数说明**

*无*

```
dhcp-relay max-hops
```


**命令功能**

在全局模式配置max-hops

**命令格式**

```
dhcp-relay max-hops <number>
no dhcp-relay max-hops
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 取值 | 1-16 |

```
show dhcp-relay
```


**命令功能**

查看配置

**命令格式**

```
show dhcp-relay
```


**参数说明**

*无*


# 53. DHCPv6-Server 配置

```
dhcpv6-server
```


**命令功能**

全局(取消)使能dhcpv6-server

**命令格式**

```
dhcpv6-server
no dhcpv6-server
```


**参数说明**

*无*

```
dhcpv6-server apply pool
```


**命令功能**

接口下引用ipv6 地址池

**命令格式**

```
dhcpv6-server apply pool <pname> [enter | preference <pre-value> | rapid-commit]
no dhcpv6-server
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pname | 地址池名称 | 1-32 个字符 |
| pre-value | 优先级 | [0-255] |

```
ipv6 pool pname
```


**命令功能**

全局下配置ipv6 地址池

**命令格式**

```
ipv6 pool <pname>
no ipv6 pool [ pname ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pname | 地址池名称 | 1-32 个字符 |

address

**命令功能**

pool 下配置地址段

**命令格式**

```
address <start-address> <end-address> [preferred-lifetime <preferred-time> valid-
lifetime <valid-time>]
no address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-address | 起始地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| end-address | 结束地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| preferred-time | 首选时间 | [60-4294967295] |
| valid-liftetime | 有效时间 | [60-4294967295] |

```
address prefix
```


**命令功能**

pool 下配置地址前缀

**命令格式**

```
address prefix <address/prefix-lenth> [preferred-lifetime <preferred-time> valid-
lifetime <valid-time>]
no address prefix
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| address | IPv6 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| prefix-length | 前缀长度 | [1-128] |
| preferred-time | 首选时间 | [60-4294967295] |
| valid-liftetime | 有效时间 | [60-4294967295] |

```
dns-server [address | domain-name]
```


**命令功能**

pool 下配置dns-server

**命令格式**

```
dns-server [address <dns-addr> | domain-name <dns-domain>]
no dns-server [address [<dns-addr>] | domain-name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dns-addr | dns 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| dns-domain | dns 域名称 | 1-32 个字符 |

```
nis-server [address | domain-name]
```


**命令功能**

pool 下配置nis-server

**命令格式**

```
nis-server [address <nis-addr> | domain-name <nis-domain>]
no nis-server [address [<nis-addr>] | domain-name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| nis-addr | nis 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| nis-domain | nis 域名称 | 1-32 个字符 |

```
nisp-server [address | domain-name]
```


**命令功能**

pool 下配置nisp-server

**命令格式**

```
nisp-server [address <nisp-addr> | domain-name <nisp-domain>]
no nisp-server [address [<nisp-addr>] | domain-name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| nisp-addr | nisp 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| nisp-domain | nisp 域名称 | 1-32 个字符 |

```
sip-server [address | domain-name]
```


**命令功能**

pool 下配置sip-server

**命令格式**

```
sip-server [address <sip-addr> | domain-name <sip-domain>]
no sip-server [address [<sip-addr>] | domain-name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| sip-addr | sip 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| sip-domain | sip 域名称 | 1-32 个字符 |


## 53.10. ntp-server address


**命令功能**

pool 下配置ntp-server

**命令格式**

```
ntp-server [address <sip-addr>]
no ntp-server [address <sip-addr>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| sip-addr | sip 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |


## 53.11. static-bind address


**命令功能**

pool 下配置静态绑定地址

**命令格式**

```
static-bind address <addr-value> duid <duid-value> [iaid <iaid-value>] [preferred-
lifetime <preferred-time> valid-time <valid-time>]
no static-bind address <addr-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| addr-value | Ipv6 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| duid-value | duid 值 | 20-28 个字符 |
| iaid-value | iaid 值 | [0-4294967295] |
| preferred-time | 首选时间 | [60-4294967295] |
| valid-liftetime | 有效时间 | [60-4294967295] |


## 53.12. unassigned address


**命令功能**

pool 下配置禁止分配的地址

**命令格式**

```
unassigned address <addr-value>
no unassigned address [<addr-value>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| addr-value | Ipv6 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |


## 53.13. show dhcpv6-server


**命令功能**

查看dhcpv6-server 信息

**命令格式**

```
show dhcpv6-server [interface vlan-interface <vid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN ID | [1-4094] |


## 53.14. 配置举例

组网
```
DUT 1----------- PC
配置
DUT(config)#dhcpv6-server
DUT(config)#ipv6 pool pool1
DUT(config-ipv6-pool-pool1)#address prefix 2001:1000::0/112
DUT(config-ipv6-pool-pool1)#address 2001:1000::11 2001:1000::20
DUT(config-ipv6-pool-pool1)#ex
DUT(config)#interface vlan-interface 1
DUT(config-if-vlanInterface-1)#ipv6 address 2001:1000::1/112
DUT(config-if-vlanInterface-1)#ipv6 address auto link-local
DUT(config-if-vlanInterface-1)#dhcpv6-server apply pool pool1
```


# 54. DHCPv6-Relay 配置

```
dhcpv6-relay
```


**命令功能**

接口下开启dhcpv6 relay 功能

**命令格式**

```
dhcpv6-relay server-address <addr-value> [interface vlan-interface <vid>]
no dhcpv6-relay [server-address <addr-value>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| addr-value | Dhcpv6 server 地 | 址 |
| xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx | vid | VLAN ID |

[1-4094]
```
dhcpv6-relay max-hops
```


**命令功能**

全局下配置dhcpv6 relay 支持的最大的调数

**命令格式**

```
dhcpv6-relay max-hops <hops-value>
no dhcpv6-relay max-hops
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| hops-value | 跳数 | [1-32] |

```
show dhcpv6-relay
```


**命令功能**

查看dhcpv6 relay 配置

**命令格式**

```
show dhcpv6-relay [enter | interface vlan-interface if-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| if-id | 接口id | 1-4094 |


# 55. IGMP-Snooping 配置

igmp-snooping

**命令功能**

全局视图开启、关闭组播侦听

**命令格式**

igmp-snooping
```
no igmp-snooping
```


**参数说明**

*无*

```
igmp-snooping enable-vlan
```


**命令功能**

全局视图（取消）使能指定vlan id 的组播侦听

**命令格式**

```
igmp-snooping enable-vlan <vlan_list>
no igmp-snooping enable-vlan<vlan_list>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | VLAN 列表 | [1-128]范围内使用“,”和“-”的任意组合 |

例如：1,3,5-10
```
igmp-snooping host-aging-time
```


**命令功能**

全局视图配置动态组播端口成员老化时间

**命令格式**

```
igmp-snooping host-aging-time <time>
no igmp-snooping host-aging-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 老化时间(秒) | [0-1000000] |

```
igmp-snooping max-response-time
```


**命令功能**

全局视图配置查询最大响应时间

**命令格式**

```
igmp-snooping max-response-time <time>
no igmp-snooping max-response-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 最大响应时间(秒) | [1-100] |

```
igmp-snooping querier
```


**命令功能**

全局视图开启、关闭查询器

**命令格式**

```
igmp-snooping querier
no igmp-snooping querier
```


**参数说明**

*无*

```
igmp-snooping version
```


**命令功能**

全局视图配置IGMP 的版本

**命令格式**

```
igmp-snooping version <ver_num>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ver_num | IGMP 版本号, 默 | 认为IGMPv2 |

[2,3]
```
igmp-snooping querier-vlan
```


**命令功能**

全局视图配置具体vlan 内的查询功能

**命令格式**

```
igmp-snooping querier-vlan <vlan_list>
no igmp-snooping querier-vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vlan-id | VLAN 列表 | [1-128]范围内使用“,”和“-”的任意组合 |

例如：1,3,5-10
```
igmp-snooping query-interval
```


**命令功能**

全局视图配置查询报文的时间间隔

**命令格式**

```
igmp-snooping query-interval <time>
no ip igmp snooping query-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 查询报文发送间 | 隔(秒)，默认60s |

[1-30000]
```
igmp-snooping last-member-query-interval
```


**命令功能**

命令配置或恢复组播特定查询发送间隔

**命令格式**

```
igmp-snooping last-member-query-interval <time>
no igmp-snooping last-member-query-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 最大响应时间 | (秒)，默认1s |

[1-5]

## 55.10. igmp-snooping query-source


**命令功能**

全局视图配置发送组查询报文所使用的源地址

**命令格式**

```
igmp-snooping query-source <ipv4>
no igmp-snooping query-source
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ipv4 | 查询报文源地址 | IPv4 单播地址,格式为X:X:X:X |


## 55.11. igmp-snooping query-proxy


**命令功能**

全局（取消）使能query proxy(使能后将query 报文使用自己的mac 转发)

**命令格式**

```
igmp-snooping query-proxy
no igmp-snooping query-proxy
```


**参数说明**

*无*


## 55.12. igmp-snooping route-port forward


**命令功能**

全局视图配置混合路由端口功能

**命令格式**

```
igmp-snooping route-port forward
no igmp-snooping route-port forward
```


**参数说明**

*无*


## 55.13. igmp-snooping router-aging-time


**命令功能**

全局视图配置动态路由端口的老化时间

**命令格式**

```
igmp-snooping router-aging-time <time>
no igmp-snooping router-aging-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 路由端口老化时 | 间范围(秒) |

[10-1000000]，默认值300s

## 55.14. igmp-snooping route-port vlan


**命令功能**

全局视图配置静态路由端口

**命令格式**

```
(no)igmp-snooping route-port vlan <vid> [all|ethernet <port id> ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN id | [1-4094] |
| Port id | 端口号 | 端口号，格式device_id/slot_id/port_id |

例如：0/0/1

## 55.15. igmp-snooping preview


**命令功能**

全局视图(取消)使能组播预览功能

**命令格式**

```
igmp-snooping preview
no igmp-snooping preview
```


**参数说明**

*无*


## 55.16. igmp-snooping preview group-ip


**命令功能**

全局视图配置使用组播预览功能的组播组

**命令格式**

```
(no)igmp-snooping preview group-ip <ipv4> vlan <vid> ethernet <port id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipv4 | 组播组地址 | IPv4 组播地址，格式为X:X:X:X |
| vid | VLAN id | [1-4094] |
| port id | 端口号 | 端口号，格式device_id/slot_id/port_id |

例如：0/0/1

## 55.17. igmp-snooping preview [permit-times| time-once|time-

interval|time-reset] value

**命令功能**

全局视图配置预览次数、单次预览时长、每次预览之间的间隔时间、预览重置时长

**命令格式**

```
igmp-snooping preview permit-times <permit-times>
igmp-snooping preview time-once <time-once>
igmp-snooping preview time-interval <time-interval>
igmp-snooping preview time-reset <time-reset>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-once | 单次预览时长(秒) | [60-300] |
| time-interval | 预览间隔(秒) | [180-600] |
| time-reset | 预览重置时长(秒) | [1800-7200] |
| permit-times | 允许预览次数 | [1-10] |


## 55.18. igmp-snooping profile


**命令功能**

全局视图配置profile 索引，并且在profile 视图下配置profile 属性

**命令格式**

```
igmp-snooping profile <profile_id>
profile limit <type>
(no)ip range <start_ipv4> <end_ipv4> [vlan <vid>]
(no)mac range <start_mac> <end_mac> [vlan <vid>]
description <name>
no igmp-snooping profile [<profile_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| profile_id | Profile 索引 | [1-128] |
| type | Profile 类型 | [permit,deny]，默认值permit |
| start_ipv4 | 起始ipv4 组播地址 | IPv4 组播地址，格式x.x.x.x |
| 例如：225.0.0.1 | end_ipv4 | 结束ipv4 组播地址 |
| IPv4 组播地址，格式x.x.x.x | 例如：228.0.0.1 | start_mac |
| 起始mac 组播地址 | Mac 组播地址，格式x:x:x:x:x:x | 例如：01:00:5e:00:00:1 |
| end_mac | 结束mac 组播地址 | Mac 组播地址，格式x:x:x:x:x:x |
| 例如：01:00:5e:00:00:3 | name | Profile 的名字 |

String<1-32>

## 55.19. igmp-snooping profile refer


**命令功能**

端口视图、vlan 视图配置引用profile

**命令格式**

```
igmp-snooping profile refer <profile_id>
no igmp-snooping profile refer
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| profile_id | Profile 索引 | [1-128] |


## 55.20. igmp-snooping [permit | deny]p group all


**命令功能**

命令配置允许或拒绝所有组播组学习

**命令格式**

```
(no)igmp-snooping [permit | deny] group all
```


**参数说明**

*无*


## 55.21. igmp-snooping <type> group[-range]


**命令功能**

端口视图配置组播黑白名单

**命令格式**

```
igmp-snooping <type> group[-range] <mac> [multi-count <num>] vlan <vid>
no igmp-snooping <type> group [<mac> vlan <vid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Type | 名单类型 | [permit,deny] |
| mac | mac 组播地址 | Mac 组播地址，格式x:x:x:x:x:x |
| 例如：01:00:5e:00:00:1 | num | 组播个数 |
| [1-64] | vid | VLAN id 号 |

[1-4094]

## 55.22. igmp-snooping group-limit


**命令功能**

端口视图配置最大可学习的组播数

**命令格式**

```
igmp-snooping group-limit <num>
no igmp-snooping group-limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 组播组数目 | [0-1024]，默认值1024 |


## 55.23. igmp-snooping overflow-replace


**命令功能**

命令在全局及端口模式下配置学满组播组时动作行为

**命令格式**

```
(no)igmp-snooping overflow-replace
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| strategy | 行为策略 | [drop,replace]，默认值drop |


## 55.24. igmp-snooping fast-leave


**命令功能**

端口视图配置快递离开模式

**命令格式**

```
(no)igmp-snooping fast-leave
```


**参数说明**

*无*


## 55.25. igmp-snooping multicast vlan


**命令功能**

端口视图配置组播vlan。开启该功能后，不论端口接收到的IGMP 报文属于哪个
VLAN，交换机都会将其修改为组播VLAN。

**命令格式**

```
(no)igmp-snooping multicast vlan <vid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN id | [1-4094] |


## 55.26. igmp-snooping robust-count


**命令功能**

命令配置或恢复组播健壮系数

**命令格式**

```
igmp-snooping robust-count <count>
no igmp-snooping robust-count
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| count | 健壮系数值, 默认 | 为2 |

2-5

## 55.27. igmp-snooping forwarding-mode


**命令功能**

命令配置组播数据转发模式

**命令格式**

```
igmp-snooping forwarding-mode [ip |mac]
```


**参数说明**

*无*


## 55.28. igmp-snooping source-learning


**命令功能**

命令配置igmpv3 组播源学习

**命令格式**

```
(no)igmp-snooping source-learning
```


**参数说明**

*无*


## 55.29. igmp-snooping static-group proxy interval


**命令功能**

命令配置静态组播代理时间间隔

**命令格式**

```
igmp-snooping static-group proxy interval <time>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 组播代理时间间 | 隔 |

[30-300]

## 55.30. igmp-snooping static-group proxy


**命令功能**

命令(取消)使能静态组播代理

**命令格式**

```
(no)igmp-snooping static-group proxy
```


**参数说明**

*无*


## 55.31. igmp-snooping static-group


**命令功能**

命令配置静态组播组

**命令格式**

```
(no)igmp-snooping static-group ipv4 [source-ip <ip-address>] vlan<vid> ethernet<port-
id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipv4 | 组播组地址 | IPv4 组播地址，格式为X:X:X:X |
| vid | VLAN id | [1-4094] |
| port_id | 端口号 | 端口号，格式device_id/slot_id/port_id |
| 例如：0/0/1 | ip-address | ip 地址 |

例如:a.b.c.d

## 55.32. igmp-snooping drop [query | report]


**命令功能**

端口视图配置丢弃查询或者报告报文

**命令格式**

```
igmp-snooping drop [query | report]
```


**参数说明**

*无*


## 55.33. show igmp-snooping


**命令功能**

查看IGMP Snooping 的相关配置

**命令格式**

```
show igmp-snooping
```


**参数说明**

*无*


## 55.34. show igmp-snooping router-dynamic


**命令功能**

查看动态路由端口

**命令格式**

```
show igmp-snooping router-dynamic
```


**参数说明**

*无*


## 55.35. show igmp-snooping router-static


**命令功能**

查看静态路由端口

**命令格式**

```
show igmp-snooping router-static
```


**参数说明**

*无*


## 55.36. show igmp-snooping mcast-table


**命令功能**

命令查看组播表（详细）信息

**命令格式**

```
show ip igmp snooping mcast-table[ ethernet port-id | ip-address ipadd]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |
| 机：0/0/1-0/1/4 | ipadd | 组播ip 地址 |

32 位二进制数，格式为X:X:X:X

## 55.37. show igmp-snooping preview


**命令功能**

查看组播预览信息

**命令格式**

```
show igmp-snooping preview [status]
```


**参数说明**

*无*


## 55.38. show igmp-snooping profile


**命令功能**

查看当前profile 配置以及对profile 的引用配置

**命令格式**

```
show igmp-snooping profile [{<profile_list>|vlan [vid]|interface [ethernet <port id> [to
ethernet <port id>]] }]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| profile_list | Profile 索引号列 | 表 |
| String<1-128>，[1,128]范围取值的任意组 | 合，使用“,”和“-”连接 | 例如：2,4,7-9 |
| vid | VLAN 号 | [1-4094] |
| port id | 端口号 | 端口号，格式device_id/slot_id/port_id |

例如：0/0/1

## 55.39. show multicast


**命令功能**

查看组播表项

**命令格式**

```
show multicast mac-address <mac-address>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac | mac 组播地址 | Mac 组播地址，格式x:x:x:x:x:x |

例如：01:00:5e:00:00:1

## 55.40. show igmp-snooping statistics


**命令功能**

查看组播报文统计

**命令格式**

```
show igmp-snooping statistics {all | vlan<vid> [ethernet <port id> [to ethernet <port id>]]}
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN 号 | [1-4094] |
| port id | 端口号 | 端口号，格式device_id/slot_id/port_id |

例如：0/0/1

## 55.41. 配置举例

```
#组网
TC A ----------- 22 DUT 21 --------- TC B
|
PC
#开启组播侦听功能
DUT(config)#igmp-snooping
DUT(config)#igmp-snooping enable-vlan 1
#TC A 发送report 报文（加入组播组225.0.0.2）
#查看侦听到的组播成员端口
DUT(config)#show igmp-snooping mcast-table
Show IGMP-snooping multicast table:
Vlan ID: 1, Group IP: 225.1.1.1
Port: e0/0/1, Filter Mode: exclude, Static: false
Expire: 0, V1 Expire: 00:02:20, V2 Expire: 0, V3 Expire: 0
Forward Source(0): N/A
Block Source(0)  : N/A
Total entries: 1
DUT(config)#show igmp-snooping mcast-table ip-address 225.1.1.1
Show IGMP-snooping multicast table:
Vlan ID: 1, Group IP: 225.1.1.1
Port: e0/0/1, Filter Mode: exclude, Static: false
Expire: 0, V1 Expire: 00:02:10, V2 Expire: 0, V3 Expire: 0
Forward Source(0): N/A
Block Source(0)  : N/A
Total entries: 1
```


# 56. MLD-Snooping 配置

mld-snooping

**命令功能**

全局下（取消）使能mld-snooping

**命令格式**

mld-snooping
```
no mld-snooping
```


**参数说明**

*无*

```
mld-snooping host-aging-time
```


**命令功能**

全局下配置主机老化时间

**命令格式**

```
mld-snooping host-aging-time <time-value>
no mld-snooping host-aging-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 老化时间 | [10-1000000] |

```
mld-snooping max-response-time
```


**命令功能**

全局下配置通用组查询最大响应时间

**命令格式**

```
mld-snooping max-response-time <time-value>
no mld-snooping max-response-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 最大响应时间 | [1-100] |

```
mld-snooping [permit | deny]
```


**命令功能**

全局下配置允许或者拒绝加入组播组

**命令格式**

```
mld-snooping [permit | deny] [group all | vlan <vid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | Vlan id | [1-4094] |

```
mld-snooping querier
```


**命令功能**

全局下（取消）使能查询器

**命令格式**

```
mld-snooping querier
no mld-snoopin querier
```


**参数说明**

*无*

```
mld-snooping query-interval
```


**命令功能**

全局下配置最大响应时间

**命令格式**

```
mld-snooping query-interval <time-value>
no mld-snooping query-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 查询间隔时间 | [1-30000] |

```
mld-snooping query-max-response
```


**命令功能**

全局下配置特定组组查询最大响应时间

**命令格式**

```
mld-snooping query-max-response <time-value>
no mld-snooping query-max-response
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 最大响应时间 | [1-25] |

```
mld-snooping route-port forward
```


**命令功能**

全局下（取消）使能组播业务报文向路由端口转发

**命令格式**

```
mld-snooping route-port forward
no mld-snoopin route-port forward
```


**参数说明**

*无*

```
mld-snooping route-port
```


**命令功能**

全局下配静态路由端口

**命令格式**

```
(no)mld-snooping route-port vlan <vid> interface ethernet <pid> [to ethernet <pid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | Vlan id | [1-4094] |
| pid | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


## 56.10. mld-snooping router-port-age


**命令功能**

全局下配置路由端口老化时间

**命令格式**

```
mld-snooping router-port-age <time-value>
mld-snooping router-port-age [off|on]
no mld-snooping router-port-age
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 路由端口老化时 | 间 |

[10-1000000]

## 56.11. mld-snooping [permit | deny]


**命令功能**

端口下配置允许或者拒绝加入某组播组

**命令格式**

```
mld-snooping [permit | deny] group <mac-value> vlan <vid>
mld-snooping [permit | deny] group-range <mac-value> multi-count vlan <vid>
no mld-snooping [permit | deny] <mac-value> vlan <vid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac-value | ipv6 地址对应的 | 组播mac 地址 |
| xx:xx:xx:xx:xx:xx | vid | VLAN Id |

[1-4094]

## 56.12. mld-snooping fast-leave


**命令功能**

端口下（取消）使能组播成员快速离开

**命令格式**

```
mld-snooping fast-leave
no mld-snoopin fast-leave
```


**参数说明**

*无*


## 56.13. mld-snooping group-limit


**命令功能**

端口下配置组播组表项学习限制

**命令格式**

```
mld-snooping group-limit <count-value>
no mld-snooping group-limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| count-value | 限制个数 | [0-4096] |


## 56.14. mld-snooping multicast vlan


**命令功能**

端口下配置组播vlan

**命令格式**

```
mld-snooping multicast vlan <vid>
no mld-snooping multicast vlan
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN Id | [1-4094] |


## 56.15. show mld-snooping


**命令功能**

查看mld-snooping 配置

**命令格式**

```
show mld-snooping
```


**参数说明**

*无*


## 56.16. show multicast mld-snooping


**命令功能**

查看组播组

**命令格式**

```
show multicast mld-snooping [interface ethernet <pid> [to ethernet <pid>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| pid | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


## 56.17. show mld-snooping [router-dynamic | router-static]


**命令功能**

查看mld-snooping 路由端口信息

**命令格式**

```
show mld-snooping [router-dynamic | router-static]
```


**参数说明**

*无*


## 56.18. 配置举例

组网
```
Clinet----- 1 DUT1 2 ----- 2 DUT2
配置
DUT1(config)#mld-snooping
DUT1(config)#show multicast mld-snooping
show multicast table information
MAC Address      : 33:33:00:00:00:01
VLAN ID          : 1
Static port list :
MLD port list    : GE0/0/1
Total entries: 1.
DUT1(config)#
DUT2(config)#igmp-snooping querier
DUT1(config)#show mld-snooping router-dynamic
Port        VID        Age      Type
GE0/0/2     1         295    { QUERY }
Total Record: 1
DUT1(config)#
```


# 57. 静态二层组播配置

```
multicast mac-address
```


**命令功能**

配置MAC 格式静态二层组播。

**命令格式**

```
(no)multicast mac-address <mac> vlan <vid> interface [all | ethernet <port id> ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac | mac 组播地址 | Mac 组播地址，格式x:x:x:x:x:x |
| 例如：01:00:5e:00:00:1 | vid | VLAN 号 |
| [1-4094] | port id | 端口号 |
| 端口号，格式device_id/slot_id/port_id | 例如：0/0/1 | 57.2. |

```
show multicast
```


**命令功能**

查看组播表信息

**命令格式**

```
show multicast mac-address <mac>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mac | mac 组播地址，当地 | 址类型选择mac- |
| address 时有效 | Mac 组播地址，格式x:x:x:x:x:x | 例如：01:00:5e:00:00:1 |


**配置举例**

```
#组网拓扑
TC1----------DUT(21)--------TC2/TC3/TC4
#配置静态组播组成员
DUT(config)#multicast ip-address 224.0.0.5 vlan 5
DUT(config)#multicast mac-address 01:00:5e:00:00:10 vlan 5 interface ethernet 0/0/21
```


# 58. 管理超时配置

timeout

**命令功能**

特权模式下配置访问超时

**命令格式**

```
timeout <num>
no timeout
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 取值,默认20min | 1-480 min |

```
Show timeout
```


**命令功能**

特权模式下查看超时配置

**命令格式**

```
show timeout
```


# 59. 管理IP 限制配置

```
login-access-list telnet
```


**命令功能**

配置允许通过telnet 访问的网络地址

**命令格式**

```
(no)login-access-list telnet ipaddress wildcard
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 允许访问的网络 | 合法单播ip |
| wildcard | 网络反掩码 | 0.0.0.0-255.255.255.255 |

```
login-access-list ssh
```


**命令功能**

配置允许通过ssh 访问的网络地址

**命令格式**

```
(no)login-access-list ssh ipaddress wildcard
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 允许访问的网络 | 合法单播ip |
| wildcard | 网络反掩码 | 0.0.0.0-255.255.255.255 |

```
login-access-list snmp
```


**命令功能**

配置允许通过snmp 访问的网络地址

**命令格式**

```
(no)login-access-list snmp ipaddress wildcard
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 允许访问的网络 | 合法单播ip |
| wildcard | 网络反掩码 | 0.0.0.0-255.255.255.255 |

```
login-access-list web
```


**命令功能**

配置允许通过web 访问的网络地址

**命令格式**

```
(no)login-access-list web ipaddress wildcard
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 允许访问的网络 | 合法单播ip |
| wildcard | 网络反掩码 | 0.0.0.0-255.255.255.255 |

```
login-access-list privilege-limit
```


**命令功能**

配置允许同时Telnet 登陆并进入特权模式的用户数

**命令格式**

```
(no)login-access-list privilege-limit num
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 取值 | 0-5 |

```
show login-access-list
```


**命令功能**

查看配置信息

**命令格式**

```
show login-access-list
```


**参数说明**

*无*


# 60. Baud Speed 配置

baud-rate

**命令功能**

配置波特率

**命令格式**

```
baud-rate <speed>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| speed | 波特率 | 110-9216000 |


# 61. WEB 配置

```
http
```


**命令功能**

全局（取消）使能HTTP

**命令格式**

```
http enable [port port]
http disable
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port | 协议端口号 | [3-65535],默认80 |

```
http enable ssl
```


**命令功能**

全局（取消）使能HTTPS

**命令格式**

```
http enable ssl [port port]
http disable
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port | 协议端口号 | [3-65535] |

```
load server-certificate
```


**命令功能**

特权模式下下载HTTPS 协议需要使用的证书文件

**命令格式**

```
load server-certificate ftp [inet | inet6] <server-ip> <filename> <user> <password>
load server-certificate tftp [inet | inet6] <server-ip> <filename>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | 服务器IP 地址 | 合法的ip 地址 |
| filename | 证书文件名全称 | 1-64 个字符 |
| user | FTP 登录用户名 | 1-32 个字符 |
| password | FTP 登录密码 | 1-32 个字符 |

```
load private-key
```


**命令功能**

特权模式下下载HTTPS 协议需要使用的密钥文件

**命令格式**

```
load private-key ftp [inet | inet6] <server-ip> <filename> <user> <password>
load private-key tftp [inet | inet6] <server-ip> <filename>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | 服务器IP 地址 | 合法Ip |
| filename | 密钥文件名全称 | 1-64 个字符 |
| user | FTP 登录用户名 | 1-32 个字符 |
| password | FTP 登录密码 | 1-32 个字符 |

```
http timeout
```


**命令功能**

全局配置HTTP 超时时间

**命令格式**

```
http timeout <time-value>
no http timeout
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | HTTP 登录超时时 | 间 |

[60-36000]

**配置举例**

组网
PC-------------DUT
命令
```
DUT(config)#http enable //使能http 功能；
```


# 62. SSH 配置

ssh

**命令功能**

全局（取消）使能SSH

**命令格式**

ssh
```
no ssh
```


**参数说明**

*无*

```
ssh limit
```


**命令功能**

全局配置SSH 连接用户限制

**命令格式**

```
ssh limit <limit>
no ssh limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| limit | 登录用户个数限 | 制 |

[0-5]
```
crypto key generate[dss | ecdsa | rsa]
```


**命令功能**

特权模式下生成密钥

**命令格式**

```
crypto key generate [dss | ecdsa | rsa]
```


**参数说明**

*无*

```
crypto key zeroize [dss | ecdsa | rsa]
```


**命令功能**

特权模式下清除密钥

**命令格式**

```
crypto key zeroize [dss | ecdsa | rsa]
```


**参数说明**

*无*

```
stop vty
```


**命令功能**

特权模式下强制关闭虚拟终端

**命令格式**

```
stop vty [all | <Id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 虚拟终端ID | 0-5 |


**配置举例**

组网
```
PC------------ DUT
配置
DUT(config)#interface vlan-interface 1
DUT(config-if-vlanInterface-1)# ip address 192.168.1.11 255.255.255.0
DUT(config-if-vlanInterface-1)#exit
DUT(config)#ssh
DUT(config)#exit
DUT#crypto key generate rsa
#PC 使用Xshell 虚拟终端软件SSH 登录DUT
[D:\~]$ ssh 192.168.1.11
Connecting to 192.168.1.11:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.
WARNING! The remote SSH server rejected X11 forwarding request.
Password(1-32 chars):*****
Admin>
```


# 63. Telnet Server 配置

```
telnet enable
```


**命令功能**

使能功能

**命令格式**

```
telnet enable
```


**参数说明**

*无*

```
telnet disable
```


**命令功能**

取消使能功能

**命令格式**

```
telnet disable
```


**参数说明**

*无*

```
telnet limit
```


**命令功能**

配置Telnet 用户个数限制

**命令格式**

```
telnet limit <num>
no telnet limit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| num | 具体取值 | 0-5 |

```
stop vty
```


**命令功能**

特权模式下强制关闭虚拟终端

**命令格式**

```
stop vty [all | <Id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 虚拟终端ID | 0-5 |

```
show telnet limit
```


**命令功能**

查看telnet 服务限制登录个数

**命令格式**

```
show telnet limit
```


**参数说明**

*无*


**配置举例**

组网
PC--------------DUT
命令
```
DUT(config)#interface vlan-interface 1
DUT(config-if-vlanInterface-1)# ip address 192.168.1.61 255.255.255.0
DUT(config-if-vlanInterface-1)# ipv6 address 2001:1000::61/64
DUT(config)#telnet limit 2           //配置远程登录限制数
DUT(config)#telnet enable           //开启远程
PC 使用Xshell 虚拟终端 IPv4 地址telnet 登录DUT
[D:\~]$ telnet 2001:1000::61
Connecting to 2001:1000::61:23...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.
Linux 4.19.1 (DUT2) (11:07 on Monday, 06 September 2021)
Username(1-64 chars):admin
Password(1-128 chars):*****
DUT>
PC 使用Xshell 虚拟终端 IPv6 地址telnet 登录DUT
[D:\~]$ telnet 192.168.1.61
Connecting to 192.168.1.61:23...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.
Linux 4.19.1 (DUT2) (11:12 on Monday, 06 September 2021)
Username(1-64 chars):admin
Password(1-128 chars):*****
DUT>enable
DUT#show telnet limit             //查看远程登录个数
Telnet user limit is 2, current is 2.login is 2
```


# 64. Telnet Client 配置

Telnet

**命令功能**

特权模式下telnet 连接server

**命令格式**

```
telnet <ip> [<port>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 服务器IP 地址 | x.x.x.x，x∈[0-255] |


**配置举例**

组网
```
DUT----------- Server（192.168.1.11）
命令
DUT#telnet 192.168.1.11
Trying to connect to 192.168.1.11 ...
Connected to 192.168.1.11 successfully."Ctr+]" to exit.
Username(1-32 chars):admin
Password(1-32 chars):*****
Server>exit
The telnet client has exited..
DUT#
Telnet6 Client 配置
```


# 65. SNMP 管理配置

```
snmp-server contact
```


**命令功能**

配置系统contact

**命令格式**

```
snmp-server contact <value>
no snmp-server contact
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 具体取值 | STRING<1-255> |

```
snmp-server location
```


**命令功能**

配置系统location

**命令格式**

```
snmp-server location <value>
no snmp-server location
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | STRING<1-255> | 65.3. |

```
snmp-server name
```


**命令功能**

配置系统name

**命令格式**

```
snmp-server name <value>
no snmp-server name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 具体取值 | STRING<1-255> |

```
snmp-server max-packet-length
```


**命令功能**

配置系统max-packet-length

**命令格式**

```
snmp-server max-packet-length <value>
no snmp-server max-packet-length
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 具体取值 | 484-8000 |

```
snmp-server view
```


**命令功能**

配置试图

**命令格式**

```
snmp-server view <view-name > <oid> [exclude|include ]
no snmp-server view <view-name > <oid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| view-name | 视图名字 | STRING<1-32> |
| oid | mib 树oid | STRING<1-64> |
| exclude | 不包含配置的oid | incline |

只包含配置的oid
```
snmp-server community
```


**命令功能**

配置团体名

**命令格式**

```
snmp-server community <text> [rw|ro][deny|permit ] [view <view-name>]
no snmp-server community <text>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| text | 密文的团体名 | STRING<1-20> |
| rw | 可读写 | ro |
| 只读 | view-name | 视图名 |

STRING<1-32>
```
snmp-server group
```


**命令功能**

配置v3 的组

**命令格式**

```
snmp-server group <group-name> 3 [auth | noauthpriv| priv] [context < context-text>]
read <read-view> write <write-view> notify <notify-view>
no snmp-server group <group-name> 3 [auth | noauthpriv| priv] [context < context-
text>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-name | 组名 | STRING<1-32> |
| auth | 仅认证 | 无 |
| noauthpriv | 不认证不加密 | 无 |
| priv | 认证且加密 | 无 |
| context | 配置的context | STRING<1-32> |
| read-view | 读的视图,必须配 | 置 |
| STRING<1-32> | write-view | 写的视图,必须配 |
| 置 | STRING<1-32> | notify-view |
| 消息视图,必须配 | 置 | STRING<1-32> |

```
snmp-server user
```


**命令功能**

配置v3 用户

**命令格式**

```
snmp-server user <username> <groupname> [auth [ md5 | sha ] [auth-password
<authpassword> | auth-key <authkey> ] [ priv des priv-
key [ auth-key <privkey> | auth-password
<privpassword> ]]
snmp-server user <username> <groupname> remote <ip-address> [ udp-port <port-
num>] ] [ auth [ md5 | sha ]  [auth-password
<authpassword> | auth-key <authkey> ] [ priv des priv-
key [ auth-key <privkey> | auth-password
<privpassword> ] ]
no snmp-server user <username>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| groupname | 组名 | STRING<1-32> |
| username | 用户名 | STRING<1-32> |
| ip-address | 远端地址 | port-num |
| udp 端口号 | INTEGER<1-65535> | 65.9. |

```
snmp-server enable [traps|informs]
```


**命令功能**

使能traps/informs

**命令格式**

```
(no)snmp enable [traps|informs] [bridge | gbn | gbnsavecfg | interfaces | rmon |
snmp]
```


**参数说明**

*无*


## 65.10. snmp-server trap-source


**命令功能**

配置发送trap 消息的源

**命令格式**

```
snmp-server trap-source <ip-address>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | 接口ip 地址 | 合法ip |


## 65.11. snmp-server host


**命令功能**

配置通告目的主机

**命令格式**

```
snmp-server host <ipaddress> [version 1 | 2c | 3] <security-name> [ udp-port <port-
number> ] [ notify-type [bridge | gbn | gbnsavecfg |
interfaces | rmon | snmp ]]
no snmp-server host <ipaddress> <security-name> [1 | 2c | 3]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipaddress | 目的主机ip | 合法IP |
| security-name | 安全名 | 字符串 |


## 65.12. snmp-server engineid


**命令功能**

配置engineid

**命令格式**

```
snmp-server engineid remote <ip-address> [udp-port<udp-port>] <engine-id>
(no)snmp-server engineid local <engine-id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip address | udp-port |
| udp 端口号 | 1-65535 | engine-id |
| 引擎id | STRING<1-24> | 65.13. show snmp community |


**命令功能**

查看community 信息

**命令格式**

```
show snmp community
```


**参数说明**

*无*


## 65.14. show snmp contact


**命令功能**

查看contact 信息

**命令格式**

```
show snmp contact
```


**参数说明**

*无*


## 65.15. show snmp engineid


**命令功能**

查看engineid 信息

**命令格式**

```
show snmp engineid [local|remote]
```


**参数说明**

*无*


## 65.16. show snmp group


**命令功能**

查看组信息

**命令格式**

```
show snmp group <groupname >
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| groupname | 具体取值 | STRING<1-32> |


## 65.17. show snmp host


**命令功能**

查看通告信息主机

**命令格式**

```
show snmp host
```


**参数说明**

*无*


## 65.18. show snmp location


**命令功能**

查看location 信息

**命令格式**

```
show snmp location
```


**参数说明**

*无*


## 65.19. show snmp max-packet-length


**命令功能**

查看snmp 最大包长度

**命令格式**

```
show snmp max-packet-length
```


**参数说明**

*无*


## 65.20. show snmp name


**命令功能**

查看snmp 名字

**命令格式**

```
show snmp name
```


**参数说明**

*无*


## 65.21. show snmp notify


**命令功能**

查看notify

**命令格式**

```
show snmp notify
```


**参数说明**

*无*


## 65.22. show snmp user


**命令功能**

查看v3 用户信息

**命令格式**

```
show snmp user <user-name>
```


**参数说明**

*无*


## 65.23. show snmp view


**命令功能**

查看视图对应oid

**命令格式**

```
show snmp view
```


**参数说明**

*无*


## 65.24. 配置举例

```
#配置交换机的接口ip 地址
DUT2(config)#int vlan-interface 1
DUT2(config-if-vlanInterface-1)#ip add 192.168.1.10 255.0.0.0
DUT2(config-if-vlanInterface-1)#exit
#配置可读可写团体名且开启snmp 功能
DUT2(config)#snmp-server community 1234 rw permit
#配置告警主机
DUT2(config)#snmp-server host 192.168.1.1 version 1 1234
DUT2(config)#snmp-server enable traps
#安装MIB brower 软件，打开进行连接
#验证配置结果 查看snmp 团体
DUT2(config)#show snmp community
Show snmp community information
index  community  priority  state   view-name
1      1234       rw        permit  iso
#查看告警主机
DUT2(config)#show snmp host
Show SNMP trap host information
SNMP host ip  security  version
192.168.1.1   1234      1
```


# 66. 用户管理配置

```
username user_name
```


**命令功能**

创建用户

**命令格式**

```
username user_name privilege level password [0|7] password
no username user_name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user_name | 用户名 | STRING<1-64> |
| level | 权限 | INTEGER<0-15> |
| password | 密码 | STRING<1-128> |

```
username change-password
```


**命令功能**

修改密码

**命令格式**

```
username change-password
```


**参数说明**

*无*

```
username failmax [user_name] fail_times
```


**命令功能**

(取消)使能静默功能

**命令格式**

```
username failmax [user_name] fail_times
no username failmax [user_name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user_name | 用户名 | STRING<1-64> |
| fail_times | 次数 | 3-8 |

```
username silent-time
```


**命令功能**

配置静默时间，该时间内用户无法登录

**命令格式**

```
username silent-time <min>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| min | 时间 | 2-1440min |

```
username online-max user_name num
```


**命令功能**

配置同一用户同时在线个数

**命令格式**

```
(no)username online-max user_name num
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user_name | 用户名 | STRING<1-64> |
| num | 个数 | 1-100 |
| username user_name terminal [all | console | telnet | ssh | | web | none] | 命令功能 |

配置用户登录终端

**命令格式**

```
username user_name terminal [all | console | telnet | ssh| web | none]
```


**参数说明**

*无*

```
stop user_name
```


**命令功能**

特权模式强制用户下线

**命令格式**

```
stop user_name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user_name | 用户名 | STRING<1-32> |

```
show username
```


**命令功能**

查看用户信息

**命令格式**

```
show username [user_name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| user_name | 用户名 | STRING<1-64> |

```
show users
```


**命令功能**

查看在线用户信息

**命令格式**

```
show users
```


**参数说明**

*无*


## 66.10. show username silent


**命令功能**

查看静默用户

**命令格式**

```
show username silent
```


**参数说明**

*无*


## 66.11. 配置举例

```
#创建用户aa，查看用户
DUT2(config)#username aa password 0 123456
DUT2(config)#show username
display user information
User Name         Role
______________________________________________________________________________
admin             ADMIN
aa                NORMAL
```


# 67. 系统信息

```
show version
```


**命令功能**

查看版本信息

**命令格式**

```
show version
```


**参数说明**

*无*

```
show system
```


**命令功能**

查看运行信息

**命令格式**

```
show system
```


**参数说明**

*无*


# 68. Reboot 配置

reboot

**命令功能**

特权模式下重启系统

**命令格式**

reboot

**参数说明**

*无*

```
auto-reboot in hours hour minutes min
```


**命令功能**

配置单次自动重启

**命令格式**

```
auto-reboot in hours hour minutes min
no auto-reboot
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| hour | 小时 | [0-23] |
| min | 分钟 | [0-59] |
| auto-reboot at hh:mm:ss [YYYY/MM/DD| daily| fri| mon| | sat|sun|thu|tue|wed] | 命令功能 |

配置周期性自动重启

**命令格式**

```
auto-reboot at hh:mm:ss [YYYY/MM/DD| daily| fri| mon| sat|sun|thu|tue|wed]
no auto-reboot
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| hour | 小时 | [0-23] |
| min | 分钟 | [0-59] |
| hh:mm:ss | 时分秒 | yyyy/mm/dd |

年月日
```
show auto-reboot
```


**命令功能**

查看自动重启配置

**命令格式**

```
show auto-reboot
```


**参数说明**

*无*


**配置举例**

```
#每天12 点自动重启
DUT2(config)#auto-reboot at 12:00:00 daily
```


# 69. 系统调试配置

ping

**命令功能**

检测ipv4 主机是否可达

**命令格式**

```
ping [-s source_ip] [-c number ] [-i ttl][-l length] [-t timeout] dest-ip
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| source_ip | 源ip 地址 | 合法ip |
| number | 发包个数 | 1-2147483647 |
| timeout | 超时时间 | 1-60s |
| host-ip | 目的主机ip | 合法ip |
| ttl | TTL | 1-255 |
| length | 数据包长度 | 0-4064 |

ping6

**命令功能**

检测ipv6 主机是否可达

**命令格式**

ping6 [-h hop][-s len][-c count ][-a sourceip ][-w timeout] [-t] dest_ip

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| hop | 跳数 | 1-255 |
| len | 包长度 | 20-8100 bytes |
| count | 发包个数 | 1-2147483647 |
| sourceip | 源ip | timeout |
| 超时时间 | 1-60s | host-ip |

目的主机ip
tracert

**命令功能**

检测到目的主机所经过的路径

**命令格式**

```
tracert [-c] [-u] [-f] [-h ttl] [-w timeout] [-s <sourceip>] dst-ip
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ttl | 跳数 | 1-255 |
| -c | icmp 模式 | -u |
| udp 模式 | timeout | 超时时间 |
| 10-60s | host-ip | 目的主机ip |
| sourceip | 源ip | 69.4. |

hostname

**命令功能**

配置主机名

**命令格式**

```
hostname <name>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 设备名 | STRING<1-64> |

help

**命令功能**

查看帮助信息

**命令格式**

help

**参数说明**

*无*

```
screen-rows per-page
```


**命令功能**

特权模式下配置分屏显示的行数

**命令格式**

```
(no)screen-rows per-page number
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | Show 命令每屏显 | 示的行数，默认 |

INTEGER<0-256>,0 表示显示所有
```
show screen-rows per-page
```


**命令功能**

查看分屏配置信息

**命令格式**

```
show screen-rows per-page
```


**参数说明**

*无*

```
line width
```


**命令功能**

特权模式下配置每行命令最长可显示的字符

**命令格式**

```
(no)line width number
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 每行命令最长字 | 符数，默认78 |

INTEGER<78-256>
```
show line width
```


**命令功能**

查看line 配置信息

**命令格式**

```
show line width
```


**参数说明**

*无*


## 69.10. cls


**命令功能**

清屏

**命令格式**

cls

**参数说明**

*无*


## 69.11. terminal language [chinese|english]


**命令功能**

特权模式下配置终端显示语言

**命令格式**

```
terminal language [chinese | english ]
```


**参数说明**

*无*


## 69.12. show tech-support [nowait]


**命令功能**

查看tech-support 信息

**命令格式**

```
show tech-support [enter|nowat|product-sn]
```


**参数说明**

*无*


## 69.13. buildrun mode [continue|stop]


**命令功能**

特权模式下配置加载模式

**命令格式**

```
buildrun mode [continue|stop]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| continue | 关键字，表示加 | 载配置遇到失败 |
| 时，继续加载配 | 置 | 无 |
| stop | 关键字，表示加 | 载配置遇到失败 |
| 立即串止加载配 | 置 | 无 |


## 69.14. 配置模式（视图）切换


**命令功能**

配置视图（模式）切换，具体见 命令格式 中说明；

**命令格式**

登录后立即进入执行模式：Switch>
```
enable 从执行模式进入特权（enable）模式：Switch#
configure terminal 从特权（enable）模式进入全局模式：Switch(config)#
end 切换到enable 模式，也称特权模式
exit 退回到上一模式
quit 退出登录
```


**参数说明**

*无*


## 69.15. performance testing


**命令功能**

（取消）使能RFC2544 64Byte 测试；如果不使能测试64Byte 字节时无法线
速；

**命令格式**

```
(no)performance testing
```


**参数说明**

*无*


## 69.16. show memory


**命令功能**

查看内存信息

**命令格式**

```
show memory
```


**参数说明**

*无*


## 69.17. show cpu-utilization


**命令功能**

查看cpu 利用率

**命令格式**

```
show cpu-utilization
```


**参数说明**

*无*


# 70. 文件下载

```
load application ftp
```


**命令功能**

在特权模式下使用ftp 方式进行主机程序下载

**命令格式**

```
load application ftp inet[6] server-ip filename username password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip |
| filename | 主机程序文件 | STRING<1-64> |
| username | ftp 服务器用户名 | STRING<1-64> |
| password | ftp 服务器用户密 | 码 |

STRING<1-32>
```
load application tftp
```


**命令功能**

在特权模式下使用tftp 方式进行主机程序下载

**命令格式**

```
load application tftp inet[6] server-ip filename
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip 地址 |
| filename | 主机程序文件 | STRING<1-64> |

```
load application xmodem
```


**命令功能**

在特权模式下使用xmodem 方式进行主机程序下载

**命令格式**

```
load application xmodem
```


**参数说明**

*无*

```
load whole-bootrom ftp
```


**命令功能**

在特权模式下使用ftp 方式进行bootrom 程序下载

**命令格式**

```
load whole-bootrom ftp inet[6] server-ip filename username password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip |
| filename | 主机程序文件 | STRING<1-64> |
| username | ftp 服务器用户名 | STRING<1-64> |
| password | ftp 服务器用户密 | 码 |

STRING<1-32>
```
load whole-bootrom tftp
```


**命令功能**

在特权模式下使用tftp 方式进行bootrom 程序下载

**命令格式**

```
load whole-bootrom tftp inet[6] server-ip filename
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip 地址 |
| filename | 主机程序文件 | STRING<1-64> |

```
load whole-bootrom xmode
```


**命令功能**

特权模式下使用xmodem 方式进行bootrom 程序下载

**命令格式**

```
load whole-bootrom xmodem
```


**参数说明**

*无*

```
load configuration xmodem
```


**命令功能**

在特权模式下使用xmodem 方式进行配置文件下载

**命令格式**

```
load configuration xmodem
```


**参数说明**

*无*

```
load configuration tftp
```


**命令功能**

在特权模式下使用tftp 方式进行配置文件下载

**命令格式**

```
load configuration tftp inet[6] server-ip filename
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名.txt 格式 | STRING<1-64> |

```
load configuration ftp
```


**命令功能**

在特权模式下使用ftp 方式进行配置文件下载

**命令格式**

```
load configuration ftp inet[6] server-ip filename username password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | ftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名.txt 格式 | STRING<1-64> |
| username | ftp 服务器用户名 | STRING<1-32> |
| password | ftp 服务器用户密 | 码 |

STRING<1-32>

## 70.10. show running-config


**命令功能**

```
show running-config [module |perlines lines]命令在特权模式下查看当前配置反编译
```


**命令格式**

```
show running-config if
show running-config perlines 3
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| module | 各种不同业务类 | 型 |
| 根据交换机特性模块确定 | lines | 每次显示几行 |

0-4096

## 70.11. copy running-config startup-config


**命令功能**

在特权模式下保存当前配置

**命令格式**

```
copy running-config startup-config
```


**参数说明**


## 70.12. copy startup-config running-config


**命令功能**

在特权模式下加载启动配置

**命令格式**

```
copy startup-config running-config
```


**参数说明**

*无*


## 70.13. copy startup-config running-config


**命令功能**

在特权模式下加载启动配置

**命令格式**

```
copy startup-config running-config
```


**参数说明**

*无*


## 70.14. show startup-config [module_name] [perlines lines]


**命令功能**

在特权模式下查看启动配置

**命令格式**

```
show startup-config [module_name] [perlines lines]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| module_name | 功能模块名 | vlan 等,具体可根据帮助信息？获取 |
| lines | 每次显示的行数 | 0-4096,0 表示显示所有 |


## 70.15. clear startup-config [with user-info]


**命令功能**

在特权模式下清除启动配置

**命令格式**

```
clear startup-config [with user-info]
```


**参数说明**

*无*


## 70.16. 配置举例

DUT#load configuration tftp inet 192.168.1.11 sw.txt     //使用tftp 下载配置文件
DUT#load application tftp inet 192.168.1.11 test.img    //使用 ftp 升级

# 71. 文件上传

```
upload logging ftp
```


**命令功能**

在特权模式下使用ftp 方式上传日志文件

**命令格式**

```
upload logging ftp inet[6] server-ip filename username password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | ftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名 | STRING<1-64> |
| username | ftp 服务器用户名 | STRING<1-32> |
| password | ftp 服务器用户密 | 码 |

STRING<1-32>
```
upload logging tftp
```


**命令功能**

在特权模式下使用tftp 方式上传日志文件

**命令格式**

```
upload logging tftp inet[6] server-ip filename
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名 | STRING<1-64> |

```
upload configuration ftp
```


**命令功能**

在特权模式下使用ftp 方式上传配置文件

**命令格式**

```
upload configuration ftp inet[6] server-ip filename username password
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | ftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名 | STRING<1-64> |
| username | ftp 服务器用户名 | STRING<1-32> |
| password | ftp 服务器用户密 | 码 |

STRING<1-32>
```
upload configuration tftp
```


**命令功能**

命令在特权模式下使用tftp 方式进行配置文件上传

**命令格式**

```
upload configuration tftp inet[6] server-ip filename
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| server-ip | tftp 服务器ip 地址 | 合法ip 地址 |
| filename | 文件名 | STRING<1-64> |


**配置举例**

DUT#upload logging tftp inet 192.168.1.11 1.txt     //使用tftp 上传主机日志
DUT#upload logging ftp inet 192.168.1.11 1.txt admin admin    //使用ftp 上传主机日志
DUT#upload configuration tftp inet 192.168.1.11 zz.txt    //使用tftp 上传配置文件
DUT#upload configuration ftp inet 192.168.1.11 zz.txt admin admin     //使用ftp 上传配置文件

# 72. Syslog 配置

```
logging
```


**命令功能**

开关日志功能

**命令格式**

```
(no) logging
```


**参数说明**

*无*

```
logging sequence-numbers
```


**命令功能**

开关日志序列号

**命令格式**

```
(no)logging sequence-numbers
```


**参数说明**

*无*

```
logging timestamps
```


**命令功能**

命令配置（恢复）时间戳类型

**命令格式**

```
(no)logging timestamps [ notime | uptime | datetime ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| notime | 不显示时间戳 | 无 |
| uptime | 开机时间显示时 | 无 |
| 间戳 | datetime | 以绝对时间显示 |
| 时间戳 | 无 | 72.4. |

```
terminal monitor
```


**命令功能**

特权模式下（取消）使能输出到终端

**命令格式**

```
(no)terminal monitor
```


**参数说明**

*无*

```
logging monitor [all | monitor-num]
```


**命令功能**

全局模式下(取消)使能输出到vty

**命令格式**

```
(no) logging monitor [all | monitor-num]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| monitor-num | 终端号 | 0-5 |
| logging monitor [all|monitor-num ] [ level-value | none | | level-list start-level to end-level ] [ module module-name ] | 命令功能 |

配置vty 日志过滤规则

**命令格式**

```
logging monitor [all|monitor-num ] [ level-value | none | level-list start-level to end-level ]
[ module module-name ]
no logging monitor [all|monitor-num ] filter
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| monitor-num | 终端号 | 0-5 |
| level-value | 信息级别 | 0-7 |
| start-level | 信息级别 | 0-7 |
| end-level | 信息级别 | 0-7 |
| module-name | 模块名 | 交换机特性模块 |

```
logging buffered
```


**命令功能**

(取消)使能输出到buffer

**命令格式**

```
(no)logging buffered
```


**参数说明**

*无*

```
logging buffered [level-value | none | level-list start-level to
end-level ][module module-name]
```


**命令功能**

配置buffered 日志过滤规则

**命令格式**

```
logging buffered [level-value | none | level-list start-level to end-level ] [ module module-
name ]
no logging buffered filter
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level-value | 信息级别 | 0-7 |
| start-leve | 信息级别 | 0-7 |
| end-level | 信息级别 | 0-7 |
| module-name | 模块名 | 交换机特性模块 |

```
logging flash
```


**命令功能**

(取消)使能输出到flash

**命令格式**

```
(no)logging flash
```


**参数说明**

*无*


## 72.10. logging flash [level-value | none | level-list start-level to end-

```
level ][module module-name]
```


**命令功能**

配置flash 日志过滤规则

**命令格式**

```
logging flash [level-value | none | level-list [ start-leve to end-level | level-value ]] [module
module-name ]
no logging flash filter
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level-value | 信息级别 | 0-7 |
| start-leve | 信息级别 | 0-7 |
| end-level | 信息级别 | 0-7 |
| module-name | 模块名 | 交换机特性模块 |


## 72.11. logging snmp-agent


**命令功能**

(取消)使能输出到snmp 代理

**命令格式**

```
(no)logging snmp-agent
```


**参数说明**

*无*


## 72.12. logging snmp-agent [level-value | none | level-list [ start-

```
leve to end-level | level-value ]] [module module-name ]
```


**命令功能**

配置snmp-agent 日志过滤规则

**命令格式**

```
logging snmp-agent[level-value | none | level-list [ start-leve to end-level | level-value ]]
[module module-name ]
no logging snmp-agent filter
```


**参数说明**

*无*


## 72.13. logging ip-address


**命令功能**

配置日志服务器

**命令格式**

```
(no) logging ip-address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | Syslog 服务器IP | 地址 |

合法ip 地址

## 72.14. logging host [all | ip-address]


**命令功能**

（取消）使能日志服务器

**命令格式**

```
(no) logging host [all | ip-address]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | Syslog 服务器IP | 地址 |

合法ip 地址

## 72.15. logging host all | ip-address level-value | none | level-list

[start-level to end-level | level-value] [ module module-name ]

**命令功能**

配置过滤规则

**命令格式**

```
logging host [all | ip-address] [level-value | none | level-list start-level to end-level ]
[ module module-name ]
no logging host [all | ip-address] filter
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | Syslog 服务器IP | 地址 |
| 合法ip 地址 | level-value | 信息级别 |
| 0-7 | start-leve | 信息级别 |
| 0-7 | end-level | 信息级别 |
| 0-7 | module-name | 模块名 |

交换机特性模块

## 72.16. logging facility


**命令功能**

配置日志记录工具名称

**命令格式**

```
logging facility [ clock1 | clock2 | ftp | kernel | lineprinter | localuse0 | localuse1 | localuse2
| localuse3 | localuse4 | localuse5 | localuse6 |  localuse6 | localuse7 | logalert | logaudit | mail |
networkknews | ntp | security1 | security2 | syslogd | system | userlevel | uucp ]
no logging facility
```


**参数说明**

*无*


## 72.17. logging source


**命令功能**

配置日志报文的源IP

**命令格式**

```
(no)logging source [ip-address | loopback-interface if-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | 可配置有效的ip | 地址 |
| 合法Ip 地址 | if-id | 环回接口id |

0-1

## 72.18. show logging


**命令功能**

查看配置信息

**命令格式**

```
Show logging
```


**参数说明**

*无*


## 72.19. show logging filter [buffered | flash | host | snmp-agent |

```
monitor ]
```


**命令功能**

查看过滤规则

**命令格式**

```
show logging filter [buffered|flash|host|snmp-agent|monitor]
```


**参数说明**

*无*


## 72.20. show logging buffered


**命令功能**

查看buffer 日志

**命令格式**

```
Show logging buffered [ level-value | level-list [ start-level to end-level | value ]] [ module
module-name ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level-value | 信息级别 | 0-7 |
| start-leve | 信息级别 | 0-7 |
| end-level | 信息级别 | 0-7 |
| module-name | 模块名 | 交换机特性模块 |


## 72.21. show logging flash


**命令功能**

命令查看flash 中的日志信息

**命令格式**

```
Show logging flash [ level-value | level-list [ start-level to end-level | value ]] [ module
module-name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| level-value | 信息级别 | 0-7 |
| start-leve | 信息级别 | 0-7 |
| end-level | 信息级别 | 0-7 |
| module-name | 模块名 | 交换机特性模块 |


## 72.22. 配置举例

1.配置日志输出到控制台
```
#开启终端输出功能
DUT#terminal monitor
DUT#configure terminal
#开启终端显示功能
DUT(config)#logging monitor all
#开启日志功能（默认开启）
DUT(config)#logging
2.配置日志输出到日志服务器192.168.1.3
#配置日志服务器
DUT(config)#logging 192.168.1.3
#启用日志服务器
DUT(config)#logging host 192.168.1.3
#配置信息查看
DUT(config)#show logging
state: on;
logging sequence-numbers: on;
logging timestamps: datetime;
logging language: english
logging monitor:
Console:    state: on;  display: on;   0 logged;  0 lost;  0 overflow.
Telnet 1:   state: on;  display: off;  0 logged;  0 lost;  0 overflow.
Telnet 2:   state: on;  display: off;  0 logged;  0 lost;  0 overflow.
Telnet 3:   state: on;  display: off;  0 logged;  0 lost;  0 overflow.
Telnet 4:   state: on;  display: off;  0 logged;  0 lost;  0 overflow.
Telnet 5:   state: on;  display: off;  0 logged;  0 lost;  0 overflow.
logging buffered:  state: on;  182 logged;    0 lost;    57 overflow.
logging flash:  state: on;  76 logged;     0 lost;    0 overflow.
logging loghost:
logging facility: localuse7;logging source: off
logging SNMP Agent:  state: on;  0 logged;      0 lost;    0 overflow.
```


# 73.  告警配置

```
alarm cpu
```


**命令功能**

全局（取消）使能CPU alarm

**命令格式**

```
alarm cpu
no alarm cpu
```


**参数说明**

*无*

```
alarm cpu threshold
```


**命令功能**

配置CPU 繁忙或者空闲的阈值

**命令格式**

```
alarm cpu threshold [busy <percentage> | unbusy <percentage>]
no alarm cpu threshold
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| percentage | CPU 使用率 | [0-100] |

```
alarm all-packets
```


**命令功能**

全局或端口（取消）使能port alarm

**命令格式**

```
alarm all-packets
no alarm all-packets
```


**参数说明**

*无*

```
alarm all-packets threshold
```


**命令功能**

端口配置端口繁忙或者空闲的阈值

**命令格式**

```
alarm all-packets threshold [exceed <bandwidth> normal < bandwidth>]
no alarm cpu threshold
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| bandwidth | 带宽使用 | [0-1000] |

```
show alarm cpu
```


**命令功能**

查看CPU Alarm 配置

**命令格式**

```
show alarm cpu
```


**参数说明**

*无*

```
show alarm all-packets
```


**命令功能**

查看全局或者端口Port Alarm 配置

**命令格式**

```
show alarm all-packets [interface [eth <portId> [to eth <portId>]]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 例如：0/0/1 |


# 74. RMON 配置

```
rmon statistics
```


**命令功能**

在端口模式下创建统计组

**命令格式**

```
(no)rmon statistics index [ owner string ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |
| string | 描述字符串 | 1-127 字符 |

```
rmon history
```


**命令功能**

查在端口模式下创建历史组

**命令格式**

```
(no)rmon history index bucket bucket-num interval value [owner string ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |
| bucket-num | 录数目值 | 1-65535 |
| value | 抽样间隔值(秒) | 1-3600 |
| string | 描述字符串 | 1-127 字符 |

```
rmon alarm
```


**命令功能**

创建告警组

**命令格式**

```
(no)rmon alarm index mib-oid value [ absolute | delta ] rising threshold-value index falling
threshold-value index [ owner string ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |
| mib-oid | MIB 对象标识 | 1-127 字符 |
| value | 抽样间隔值(秒) | 1-3600 |
| threshold-value | 抽样统计的界限 | 值 |
| 1-2147483647 | string | 描述字符串 |

1-127 字符
```
rmon event
```


**命令功能**

创建事件表项

**命令格式**

```
(no)rmon event index [ description string ] [ log | log-trap | trap | none ] [ owner string ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |
| string | 描述字符串 | 1-127 字符 |

```
show rmon alarm
```


**命令功能**

告警组信息查看

**命令格式**

```
show rmon alarm [index]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |

```
show rmon event
```


**命令功能**

历史组信息查看

**命令格式**

```
show rmon event [index]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |

```
show rmon eventlog
```


**命令功能**

告警组信息查看

**命令格式**

```
show rmon eventlog [index]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| index | 表格索引 | 1-65535 |

```
show rmon history
```


**命令功能**

历史组信息查看

**命令格式**

```
show rmon history interface [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如28 口交换 |

机：0/0/1-0/1/4
```
show rmon statistics
```


**命令功能**

统计组信息查看

**命令格式**

```
show rmon statistics [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| port-id | 端口号 | 根据交换机物理端口来定，例如0/0/1 |


## 74.10. 配置举例

组网
```
PC----- DUT
配置
DUT(config)#int eth 0/0/1
DUT(config-if-ethernet-0/0/1)#rmon statistics 1
DUT(config-if-ethernet-0/0/1)#exit
DUT(config)#int eth 0/0/2
DUT(config-if-ethernet-0/0/2)#rmon history 10 buckets 5 interval 10
DUT(config-if-ethernet-0/0/1)#exit
DUT(config)#rmon event 1 log
DUT(config)#rmon alarm 1 1.3.6.1.2.1.16.1.1.1.5.1 10 absolute rising 10000 1 falling 500 1
```


# 75. LLDP

lldp

**命令功能**

全局（取消）使能LLDP

**命令格式**

```
(no)lldp
```


**参数说明**

*无*

```
lldp hello-time
```


**命令功能**

配置发送时间间隔

**命令格式**

```
(no)lldp hello-time <interval>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| interval | 时间间隔 | [5-32768] |

```
lldp hold-time
```


**命令功能**

配置 hold time

**命令格式**

```
(no)lldp hold-time <value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 取值 | [2-10] |

```
lldp trap
```


**命令功能**

（取消）使能LLDP trap

**命令格式**

```
lldp trap enable
lldp trap disable
```


**参数说明**

*无*

```
lldp [rxtx | rx | tx]
```


**命令功能**

端口模式配置收发类型

**命令格式**

```
lldp [rxtx | rx | tx]
no lldp
```


**参数说明**

```
lldp management-address
```


**命令功能**

配置管理地址信息

**命令格式**

```
lldp management-address [supervlan-interface | vlan-interface] <interfaceId>
no lldp management-address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| interfaceId | 接口ID | 超级接口[1-128] |

普通接口[1-4094]
```
show lldp
```


**命令功能**

查看LLDP 配置及收集的拓扑信息

**命令格式**

```
show lldp [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 合法端口，例如：0/0/1 |


**配置举例**

组网
DUT1 1----------- 18 DUT2

**命令格式**

```
DUT1(config)#interface vlan-interface 1
DUT1(config-if-vlanInterface-1)#ip address 192.168.1.11 255.255.255.0
DUT1(config-if-vlanInterface-1)#ex
DUT1(config)#lldp
DUT1(config)#interface eth 0/0/1
DUT1(config-if-ethernet-0/0/1)#lldp rxtx
DUT1(config-if-ethernet-0/0/1)#
DUT2(config)#interface vlan-interface 1
DUT2(config-if-vlanInterface-1)#ip address 192.168.1.12 255.255.255.0
DUT2(config-if-vlanInterface-1)#ex
DUT2(config)#lldp
DUT2(config)#interface eth 0/0/18
DUT2(config-if-ethernet-0/0/18)#lldp rxtx
DUT2(config-if-ethernet-0/0/18)#
DUT1(config-if-ethernet-0/0/1)#show lldp ethernet 0/0/1
System LLDP: enable
LLDP trap: disable
LLDP hello-time: 30(s)  LLDP hold-times: 4  LLDP TTL: 120(s)
GE0/0/1
Port LLDP: rxtx         Pkt Tx: 82          Pkt Rx: 116
Total neighbor count: 2
Neighbor (1):
TTL: 90(s)
Chassis ID: 00:e0:53:17:ee:e3
Port ID: GE0/0/18
System Name: S3052PETF-E
System Description: INTELLINET
Port Description: NULL
Management Address: 192.168.1.12
Port Vlan ID: 1
Port SetSpeed: auto
Port ActualSpeed: FULL-1000
Port Link Aggregation: support ,not in aggregation
```


# 76. UDLD

udld

**命令功能**

全局或端口下（取消）使能UDLD 功能

**命令格式**

```
(no)udld
```


**参数说明**

*无*

```
udld delaydown-time
```


**命令功能**

全局配置端口Down 延迟时间

**命令格式**

```
(no)udld delaydown-time <time-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | Down 延迟时间 | [1-5] |

```
udld error-down recover
```


**命令功能**

全局配置自动恢复Down 端口

**命令格式**

```
(no)udld error-down recover
```


**参数说明**

*无*

```
udld error-down recover-time
```


**命令功能**

全局配置自动恢复Down 端口时间

**命令格式**

```
(no)udld error-down recover-time time-value
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 自动恢复等待时 | 间 |

[30-86400]
```
udld message-interval
```


**命令功能**

全局配置端口Down 延迟时间

**命令格式**

```
(no)udld message-interval <time-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | UDLD 协议报文 | 发送间隔时间 |

[7-90]
```
udld reset
```


**命令功能**

全局或端口重启所有被UDLD 关闭的端口

**命令格式**

```
udld reset
```


**参数说明**

*无*

```
udld port shutdown
```


**命令功能**

端口下配置UDLD 关闭端口

**命令格式**

```
(no)udld port shutdown
```


**参数说明**

*无*

```
udld work-mode
```


**命令功能**

端口下配置UDLD 工作模式

**命令格式**

```
udld work-mode [aggressive | normal]
```


**参数说明**

*无*

```
udld unidirectional-shutdown [auto | manual]
```


**命令功能**

端口下配置UDLD shutdown 模式

**命令格式**

```
udld unidirectional-shutdown [auto | manual]
```


**参数说明**

*无*


## 76.10. show udld


**命令功能**

查看UDLD 配置

**命令格式**

```
show udld interface [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


# 77. 静态时间配置

```
clock set
```


**命令功能**

特权模式下配置系统时间

**命令格式**

```
clock set <HH:MM:SS YYYY/MM/DD>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| HH:MM:SS | 时分秒 | 合法值 |
| YYYY/MM/DD | 年月日 | 年：2000-2099 |

```
clock timezone
```


**命令功能**

配置时区

**命令格式**

```
clock timezone <zone-name hours-offset minutes-offset >
no clock timezone
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| zone-name | 时区名 | STRING<1-32> |
| hours-offset | 偏移小时 | -23 to 23 |
| minutes-offset | 偏移分钟 | INTEGER<0-59> |

```
show clock
```


**命令功能**

查看系统当前时间，时区信息

**命令格式**

```
show clock
```


**参数说明**

*无*


# 78. SNTP-Client 配置

```
sntp client
```


**命令功能**

全局模式下sntp 客户端使能开关。

**命令格式**

```
(no)sntp client
```


**参数说明**

*无*

```
sntp client mode
```


**命令功能**

全局模式下配置sntp 客户端工作方式。

**命令格式**

```
sntp client mode [anycast | broadcast | multicast | unicast]
no sntp client mode
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| anycast | 任意播 | 无 |
| broadcast | 广播 | 无 |
| multicast | 组播 | 无 |
| unicast | 单播 | 无 |

```
sntp client authenticate
```


**命令功能**

全局模式下配置sntp 客户端认证功能开关。

**命令格式**

```
sntp client authenticate
no sntp client authenticate
```


**参数说明**

*无*

```
sntp client authentication-key
```


**命令功能**

全局模式下配置sntp 信赖时钟源的认证密码

**命令格式**

```
(no)sntp client authentication-key <integer> md5 <key>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| integer | 密码号 | 1-4294967295 |
| key | 认证密码 | STRING<1-16> |

```
sntp client broadcastdelay
```


**命令功能**

全局模式下修改广播延时

**命令格式**

```
sntp client broadcastdelay <microseconds>
no sntp client broadcastdelay
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| microeconds | 具体取值 | 1-9999 |

```
sntp client poll-interval
```


**命令功能**

全局模式下配置轮询间隔

**命令格式**

```
sntp client poll-interval <seconds>
no sntp client poll-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 具体取值 | 64-1024s |

```
sntp client retransmit
```


**命令功能**

全局模式下配置重传次数

**命令格式**

```
sntp client retransmit <times>
no sntp client retransmit
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| times | 重传次数 | 1-10 |

```
sntp client retransmit-interval
```


**命令功能**

全局模式下配置重传间隔

**命令格式**

```
sntp client retransmit-interval <seconds>
no sntp client retransmit-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 重传间隔 | 3-30s |

```
sntp client summer-time dayly
```


**命令功能**

全局模式下按日期配置夏令时

**命令格式**

```
sntp client summer-time dayly <start-month start-day start-time end-month end-day
end-time >
no sntp client summer-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-month | 开始月份 | start-day |
| 开始日子 | start-time | 开始时间 |
| end-month | 结束月份 | end-day |
| 结束日子 | end-time | 结束时间 |


## 78.10. sntp client summer-time weekly


**命令功能**

全局模式下按星期配置sntp 夏令时

**命令格式**

```
sntp client summer-time weekly start-month start-week [ Fri |mon| sat | sun | thu | tue |
wed ] start-time end-month end-week [ Fri | mon | sat | sun | thu | tue | wed ] end-time
no sntp client summer-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-month | 开始月份 | 1-12 |
| start-week | 开始星期几 | 1-5 |
| start-time | 开始时间 | 合法时间 |
| end-month | 结束月份 | 1-12 |
| end-day | 结束星期几 | 1-5 |
| end-time | 结束时间 | 合法时间 |


## 78.11. sntp client valid-server


**命令功能**

全局模式下配置sntp 合法服务器

**命令格式**

```
sntp client valid-server <ip> < wildcard>
no sntp client valid-server [all | <ip> < wildcard> ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 服务器所在网段 | 合法地址 |
| wildcard | 通配符 | 0.0.0.0-255.255.255.255 |


## 78.12. sntp trusted-key


**命令功能**

全局模式下配置sntp 信任密码id

**命令格式**

```
(no)sntp trusted-key <key>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key | 密码序号 | 1-4294967295 |


## 78.13. sntp server key


**命令功能**

全局模式下配置sntp 信任密码id

**命令格式**

```
sntp server key <key>
no sntp server key
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key | 密码序号 | 1-4294967295 |


## 78.14. sntp server


**命令功能**

全局模式下配置主服务器ip

**命令格式**

```
sntp server <ip-address>
no sntp server
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | 合法ip 地址 |


## 78.15. sntp server backup


**命令功能**

全局模式下配置备份服务器ip

**命令格式**

```
sntp server backup <ip-address>
no sntp server backup
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | ip 地址 | 合法IP 地址 |


## 78.16. sntp client mode anycast key


**命令功能**

配置信任密码id

**命令格式**

```
sntp client mode anycast key <id>
no sntp client anycastkey <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | key 序号 | 1-4294967295 |


## 78.17. show sntp client


**命令功能**

查看sntp 客户端的运行信息

**命令格式**

```
show sntp client
```


**参数说明**

*无*


## 78.18. show sntp client summer-time


**命令功能**

查看sntp 夏令时状态

**命令格式**

```
show sntp client summer-time
```


**参数说明**

*无*


## 78.19. 配置举例

组网
```
SNTP Server  -------  DUT
命令
#开启sntp 客户端功能
DUT1(config)#sntp client
#配置sntp 工作模式为广播
DUT1(config)#sntp client mode broadcast
#配置sntp 合法服务器ip 地址范围
DUT1(config)#sntp client valid-server 192.168.1.0  0.0.0.255
#开启SNTP 服务器，发送模式为广播
#查看SNTP client 信息
DUT1(config)#show sntp client
Clock state  : synchronized    Current mode    : broadcast
Use server   : 192.168.1.110   State           : idle
Server state : synchronized    Server stratum  : 1
Authenticate : disable         Bcast delay     : 3ms
Last synchronized time: Fri Sep  3 07:21:19 2021
Summer-time is not set.
Valid server list:
Server address:192.168.1.0     wildcard:0.0.0.255
```


# 79. NTP 配置

```
ntp access
```


**命令功能**

全局配置访问控制ip 地址权限

**命令格式**

```
ntp access <ip> <mask> [permit | deny]
no ntp access [all | <ip> <mask>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 服务器ip | wmask |

掩码
```
ntp authentication
```


**命令功能**

```
ntp 认证功能开关
```


**命令格式**

```
ntp authentication
no ntp authentication
```


**参数说明**

*无*

```
ntp authentication-keyid
```


**命令功能**

```
ntp 认证密钥
```


**命令格式**

```
ntp authentication-keyid id md5 <md5-key>
no ntp authentication-keyid [all|<id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | key 序号 | 1-65535 |
| md5-key | md5 密码 | STRING<1-16> |

```
ntp max-dynamic-sessions
```


**命令功能**

```
ntp 最大动态会话数
```


**命令格式**

```
ntp max-dynamic-sessions <value>
no ntp max-dynamic-sessions
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 11-100 | 79.5. |

```
ntp reference-clock local
```


**命令功能**

```
ntp 参考时钟
```


**命令格式**

```
ntp reference-clock local
no ntp reference-clock local
```


**参数说明**

*无*

```
ntp unicast
```


**命令功能**

```
ntp 工作模式
```


**命令格式**

```
ntp unicast [peer | server] <ip> authentication-keyid <id>
no ntp unicast [peer | server] [all | <ip>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| peer | 关键字 | 对等体模式 |
| server | 关键字 | 单播服务器模式 |
| ip | 服务器ip | 合法ip |
| id | 标识号 | 1-65535 |

```
ntp broadcast server
```


**命令功能**

接口下配置ntp 广播模式服务器

**命令格式**

```
ntp broadcast server authentication-keyid <id>
no ntp broadcast
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | key 序号 | 1-65535 |

```
ntp broadcast client
```


**命令功能**

接口下配置ntp 广播模式客户端

**命令格式**

```
ntp broadcast client
no ntp broadcast
```


**参数说明**

*无*

```
ntp multicast server
```


**命令功能**

接口下配置ntp 组播模式服务器

**命令格式**

```
ntp multicast server authentication-keyid <id>
no ntp multicast
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | key 序号 | 1-65535 |


## 79.10. ntp multicast client


**命令功能**

接口下配置ntp 组播模式客户端

**命令格式**

```
ntp multicast client
no ntp multicast
```


**参数说明**

*无*


## 79.11. ntp receive


**命令功能**

开启（关闭）ntp 接收

**命令格式**

```
ntp ntp receive [enable | disable]
```


**参数说明**

*无*


## 79.12. show ntp access


**命令功能**

查看ntp 访问控制

**命令格式**

```
show ntp access
```


**参数说明**

*无*


## 79.13. show ntp authentication


**命令功能**

查看ntp 认证

**命令格式**

```
show ntp authentication
```


**参数说明**

*无*


## 79.14. show ntp broadcast


**命令功能**

查看ntp 广播模式

**命令格式**

```
show ntp broadcast [client | server] [supervlan-interface | vlan-interface] <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 1-128 | 79.15. show ntp max-dynamic-sessions |


**命令功能**

查看ntp 最大动态会话数

**命令格式**

```
show ntp max-dynamic-sessions
```


**参数说明**

*无*


## 79.16. show ntp multicast


**命令功能**

查看ntp 组播模式

**命令格式**

```
show ntp multicast [client | server] [supervlan-interface | vlan-interface] <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 1-128 | 79.17. show ntp receive |


**命令功能**

查看ntp 接收

**命令格式**

```
show ntp receive [supervlan-interface | vlan-interface] <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 接口id | 1-128 |


## 79.18. show ntp reference-clock


**命令功能**

查看ntp 参考时钟

**命令格式**

```
show ntp reference-clock
```


**参数说明**

*无*


## 79.19. show ntp sessions


**命令功能**

查看ntp 会话

**命令格式**

```
show ntp sessions
```


**参数说明**

*无*


## 79.20. show ntp status


**命令功能**

查看ntp 状态

**命令格式**

```
show ntp status
```


**参数说明**

*无*


## 79.21. show ntp unicast


**命令功能**

查看ntp 单播工作模式

**命令格式**

```
show ntp unicast [peer |server]
```


**参数说明**

*无*


# 80. IP 管理接口

```
interface internal-interface 0
```


**命令功能**

进入管理口配置模式。

**命令格式**

```
interface internal-interface <id>
no interface internal-interface <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 接口号，固定为0 | 80.2. |

```
ip address ip_address mask
```


**命令功能**

进入管理口配置模式。

**命令格式**

```
(no)ip address ip_address mask
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip_address | Ip 地址 | 合法ip |
| mask | 子网掩码 | 合法掩码 |


**配置举例**

```
# 配置管理接口地址192.168.1.100/24
DUT(config)#interface internal-interface 0
DUT1(config-if-internalInterface-0)#ip address 192.168.1.100 255.255.255.0
```


# 81. IF-Vlan 接口配置命令

```
interface vlan-interface
```


**命令功能**

配置普通VLAN 接口，同时进入接口配置模式

**命令格式**

```
interface vlan-interface vid
no interface vlan-interface vid
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | VLAN id | 1-4094 |

description

**命令功能**

接口模式下配置接口描述信息

**命令格式**

no)description string

**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | 描述信息 | 除？号以外任意字符，空格需要加上双引号 |

```
shutdown
```


**命令功能**

接口模式下开关接口，默认开启

**命令格式**

```
(no)shutdown
```


**参数说明**

*无*

```
ip address ip_address mask
```


**命令功能**

接口模式下配置接口静态ip 地址

**命令格式**

```
ip address ipaddress mask
no ip address [ipaddress mask]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip_address | 可配置有效的ip | 地址 |
| 合法Ip | mask | 配置接口掩码 |

255.0.0.0-255.255.255.252
```
ip address primary ip_address
```


**命令功能**

接口模式下切换接口主ip 地址

**命令格式**

```
(no)ip address primary ip_address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip_address | 需要配置的主 | ip，默认第一个配 |
| 置的ip 是接口主 | 接口Ip | ip |

```
ip address range start_ip end_ip
```


**命令功能**

接口模式下配置接口允许通信范围，默认所有ip 可通信

**命令格式**

```
(no)ip addres range start_ip end_ip
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-ip | 可配置有效的ip | 地址 |
| 合法ip | end-ip | 可配置有效的ip |
| 地址 | 合法ip | 81.7. |

```
ip address [dhcp | bootp]
```


**命令功能**

接口模式下(取消)使能dhcp&bootp client，即动态获取IP

**命令格式**

```
(no)ip address [dhcp | bootp]
```


**参数说明**

*无*

```
ipv6 address
```


**命令功能**

接口模式下配置接口ipv6 地址

**命令格式**

```
(no)ipv6 address X:X::X:X/M [eui-64]
(no)ipv6 address X:X::X:X link-local
(no)ipv6 address auto link-local
(no)ipv6 address autoconfig
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| X:X::X:X | Ipv6 地址 | 合法ipv6 地址 |
| M | 前缀长度 | 0-128 |

```
ipv6 forwarding
```


**命令功能**

(取消)使能ipv6 转发

**命令格式**

```
(no)ipv6 forwarding
```


**参数说明**

*无*


## 81.10. show ip dhcp lease


**命令功能**

查看接口动态地址

**命令格式**

```
show ip dhcp lease
```


**参数说明**

*无*


## 81.11. show ip interface vlan-interface vlan-id


**命令功能**

查看接口配置ip 地址信息

**命令格式**

```
show ip interface vlan-interface vlan-id
show ipv6 interface vlan-interface vlan-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Vlan-id | vlan 接口 | 1-4094 |


## 81.12. 配置举例

```
DUT(config)#int vlan-interface 1             //进入普通vlan 接口
DUT(config-if-vlanInterface-1)#ip address 1.1.1.1 255.0.0.0        //配置ip 地址
DUT(config-if-vlanInterface-1)#description zz       //接口描述
DUT(config-if-vlanInterface-1)#show ip interface       //查看接口信息
Show informations of interface
The mac-address of interface is 00:0a:6a:01:02:22
Interface description : zz
Interface name        : VLAN-IF1
Primary ipaddress     : 192.168.1.10/255.0.0.0
Secondary ipaddress   : 1.1.1.1/255.0.0.0
VLAN                  : 1
Interface status      : Up
Total entries: 1 interface.
```


# 82. SuperVlan 接口配置命令

```
interface supervlan-interface
```


**命令功能**

配置supervlan 接口，同时进入接口配置模式

**命令格式**

```
(no)interface supervlan-interface id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | number | 1-128 |

```
subvlan vid
```


**命令功能**

接口模式下配置supervlan 下属subvlan

**命令格式**

```
(no)subvlan [vid | vlan-list]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | vlan id | 1-4094 |
| vlan-list | 多个vlan | 数字形式字符串，不区分大小写，不支持空 |

格，长度范围是1-64。字符串范围1-4094
description

**命令功能**

接口模式下配置接口描述信息

**命令格式**

```
(no)description string
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | 描述信息 | 除？号以外任意字符，空格需要加上双引号 |

```
shutdown
```


**命令功能**

接口模式下开关接口，默认开启

**命令格式**

```
(no)shutdown
```


**参数说明**

*无*

```
ip address ip_address mask
```


**命令功能**

接口模式下配置接口静态ip 地址

**命令格式**

```
ip address ipaddress mask
no ip address [ipaddress mask]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip_address | 可配置有效的ip | 地址 |
| 合法Ip | mask | 配置接口掩码 |

255.0.0.0-255.255.255.252
```
ip address primary ip_address
```


**命令功能**

接口模式下切换接口主ip 地址

**命令格式**

```
(no)ip address primary ip_address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Ip_address | 需要配置的主 | ip，默认第一个配 |
| 置的ip 是接口主 | ip | 接口Ip |

```
ip address range start_ip end_ip
```


**命令功能**

接口模式下配置接口允许通信范围，默认所有ip 可通信

**命令格式**

```
(no)ip addres range start_ip end_ip
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| start-ip | 可配置有效的ip | 地址 |
| 合法ip | end-ip | 可配置有效的ip |
| 地址 | 合法ip | 82.8. |

```
ip address [dhcp | bootp]
```


**命令功能**

接口模式下(取消)使能dhcp&bootp client，即动态获取IP

**命令格式**

```
(no)ip address [dhcp | bootp]
```


**参数说明**

*无*

```
ipv6 address
```


**命令功能**

接口模式下配置接口ipv6 地址

**命令格式**

```
(no)ipv6 address X:X::X:X/M [eui-64]
(no)ipv6 address X:X::X:X link-local
(no)ipv6 address auto link-local
(no)ipv6 address autoconfig
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| X:X::X:X | Ipv6 地址 | 合法ipv6 地址 |
| M | 前缀长度 | 0-128 |


## 82.10. show ip dhcp lease


**命令功能**

查看接口动态地址

**命令格式**

```
show ip dhcp lease
```


**参数说明**

*无*


## 82.11. show ip interface supervlan-interface id


**命令功能**

查看接口配置ip 地址信息

**命令格式**

```
show ip interface supervlan-interface id
show ipv6 interface supervlan-interface id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | supervlan 接口 | 1-128 |


## 82.12. 配置举例

```
DUT(config)#int supervlan-interface 1                //进入supervlan 接口
DUT(config-if-superVLANInterface-1)#subvlan 1         //添加子vlan
DUT(config-if-superVLANInterface-1)#ip address 2.2.2.1 255.0.0.0
This ipaddress will be the primary ipaddress of this interface.
DUT(config-if-superVLANInterface-1)#description example
DUT(config-if-superVLANInterface-1)#show ip interface supervlan-interface 1      //查看supervlan 接口
Show informations of interface
The mac-address of interface is 00:0a:6a:01:02:22
Interface description : ss
Interface name        : superVLAN-IF1
Primary ipaddress     : 2.2.2.1/255.0.0.0
Secondary ipaddress   : None
VLAN                  : 1
Interface status      : Down
Total entries: 1 interface.
```


# 83. Loopback-Interface

```
interface loopback-interface
```


**命令功能**

创建环回接口，同时进入接口配置模式

**命令格式**

```
(no)interface loopback-interface <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 环回接口id | 0-1 |

description

**命令功能**

在接口模式下，配置接口描述符

**命令格式**

```
(no)description <string>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| string | 接口描述 | 1-31 |

```
ip address
```


**命令功能**

在接口配置模式下，配置接口IP 地址

**命令格式**

```
(no)ip address <ipadd> <mask>
no ip address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipadd | 接口IP 地址 | IPV4 地址 |
| mask | 掩码 | IPV4 地址 |

```
ip address primary
```


**命令功能**

在接口配置模式下，设置接口主IP 地址（IP 地址需已配置）

**命令格式**

```
ip address primary <ipadd>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipadd | 接口IP 地址 | IPV4 地址 |

```
ipv6 address
```


**命令功能**

在接口配置模式下，配置接口IPV6 地址

**命令格式**

```
(no)ipv6 address <X:X::X:X/M>
(no)ipv6 address <X:X::X:X/M> eui-64
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| X:X::X:X | 接口IPV6 地址 | IPV6 地址 |
| M | 前缀长度 | 0-128 |

```
show ip interface
```


**命令功能**

查看设备ip 接口信息

**命令格式**

```
show ip interface loopback-interface <id>
show ipv6 interface loopback-interface <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 环回接口id | 0-1 |


**配置举例**

组网
无
命令
```
#创建环回接口0
DUT1(config)#interface loopback-interface 0
#添加多个IPV4 地址
DUT1(config-if-loopBackInterface-0)#ip address 192.168.1.1 255.255.255.0
DUT1(config-if-loopBackInterface-0)#ip address 192.168.2.1 255.255.255.0
#配置其中一个IPV4 地址为主地址
DUT1(config-if-loopBackInterface-0)#ip address primary 192.168.1.1
#配置接口描述
DUT1(config-if-loopBackInterface-0)#description test
#查看设备IP 接口信息
DUT1(config-if-loopBackInterface-0)#show ip interface
Show informations of interface
The mac-address of interface is 44:18:47:00:00:00
Interface description : test
Interface name        : loopback0
Primary ipaddress     : 192.168.1.1/255.255.255.0
Secondary ipaddress   : 192.168.2.1/255.255.255.0
Interface status      : Up
Total entries: 1 interface.
```


# 84. ARP

```
arp ip mac [vlan vlan-id] [ethernet port-id]
```


**命令功能**

配置静态arp 表

**命令格式**

```
arp ip mac [vlan vlan-id] [ethernet port-id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | IP 地址 | 合法ip |
| mac | mac 地址 | 合法mac |
| vlan-id | vlan 号 | 1-4094 |
| port-id | 端口号 | 格式如0/0/1 |

```
arp aging-time
```


**命令功能**

配置arp 老化时间

**命令格式**

```
arp aging-time <time >
no arp aging-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time | 取值，默认20m | 3-2880 minutes |

```
arp bind dynamic
```


**命令功能**

将动态arp 变为静态

**命令格式**

```
arp bind dynamic [ip | all ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | IP 地址 | 合法ip |

```
no arp [dynamic | static | all | ip ]
```


**命令功能**

删除arp 表

**命令格式**

```
no arp [dynamic | static | all | ip ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | IP 地址 | 合法ip |

```
show arp [ dynamic | static | all | ip|mac]
```


**命令功能**

查看arp 表

**命令格式**

```
show arp [ dynamic | static | all | ip|mac ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | IP 地址 | 合法ip |
| mac | mac 地址 | 合法mac |

```
show arp aging-time
```


**命令功能**

查看arp 老化时间

**命令格式**

```
show arp aging-time
```


**参数说明**

*无*


**配置举例**

```
DUT(config)#arp 192.168.1.2 00:00:00:01:2:3 ethernet 0/0/1 vlan 1   //配置静态arp
DUT(config)#arp bind dynamic 192.168.1.111   //将动态arp 转换成静态表项
DUT(config)#show arp all
//查看arp 表项
Information of ARP
IpAddress                                Mac_Address        Vlan Port     Type
192.168.1.2                              00:00:00:01:02:03  1    0/0/1    static
192.168.1.111                            80:1f:02:4c:19:60  1    0/0/14   static
Total entries: 2, Printed entries: 2
```


# 85. ND

```
ipv6 neighbor ipv6-add mac [vlan vid ethernet portId]
```


**命令功能**

全局下配置静态IPv6 邻居

**命令格式**

```
ipv6 neighbor ipv6-add mac [vlan vid ethernet portId]
no ipv6 neighbor ipv6-add
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipv6-addr | IPv6 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| mac-adrr | MAC 地址 | xx:xx:xx:xx:xx:xx |
| vid | VLAN ID | [1-4094] |
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |

```
ipv6 neighbors max-learning-num
```


**命令功能**

配置最大可学习IPv6 邻居数

**命令格式**

```
(no)ipv6 neighbors max-learning-num <limit>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| limit | 最大邻居限制数 | 1-64 |

```
ipv6 nd dad attemps
```


**命令功能**

接口下配置DAD 检测次数

**命令格式**

```
ipv6 nd dad attemps <count-value>
no ipv6 nd dad attemps
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| count-value | DAD 检测次数 | [0-20] |

```
ipv6 nd ns retrans-time
```


**命令功能**

接口下配置NS 报文发送间隔时间

**命令格式**

```
ipv6 nd ns retrans-time <interval-value>
no ipv6 nd ns retrans-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| interval-value 间隔时间 | [1-3600] | 85.5. |

```
ipv6 nd reachable-time
```


**命令功能**

接口下配置邻居可达时间

**命令格式**

```
ipv6 nd reachable-time <time-value>
no ipv6 nd reachable-time
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 邻居可达时间 | [1-3600] |

```
show ipv6 nd [dad | ns retrans-time | reachable-time]
```


**命令功能**

查看ND 配置

**命令格式**

```
show ipv6 nd [dad | ns retrans-time | reachable-time]
```


**参数说明**

*无*

```
show ipv6 neighbors
```


**命令功能**

查看IPv6 邻居表项

**命令格式**

```
show ipv6 neighbors [<ipv6-addr> | <mac mac-addr> | dynamic | static | all]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipv6-addr | IPv6 地址 | xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx |
| mac-adrr | MAC 地址 | xx:xx:xx:xx:xx:xx |


**配置举例**

组网
```
PC----- 48 DUT
配置
DUT(config)#interface eth 0/0/1
DUT(config)#interface vlan-interface 4094
DUT(config-if-vlanInterface-4094)#ipv6 address 2001:1000::62/112
DUT(config-if-vlanInterface-4094)#exit
DUT(config)# ipv6 neighbor 2001:1000::111 00:00:00:13:40:20 vlan 4094 ethernet 0/0/1
DUT(config)#ping6 2001:1000::112
PING 2001:1000::112(2001:1000::112) 56 data bytes
64 bytes from 2001:1000::112: icmp_seq=1 ttl=128 time < 1ms
64 bytes from 2001:1000::112: icmp_seq=2 ttl=128 time < 1ms
64 bytes from 2001:1000::112: icmp_seq=3 ttl=128 time < 1ms
64 bytes from 2001:1000::112: icmp_seq=4 ttl=128 time < 1ms
64 bytes from 2001:1000::112: icmp_seq=5 ttl=128 time < 1ms
--- 2001:1000::112 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4094ms
rtt min/avg/max/mdev = 0/0/0/0 ms
DUT3(config)#show ipv6 neighbors all
Information of neighbors
IpAddress                                 Mac_Address         Vlan   Port     Type     Status
ExpireTime
2001:1000::111                            00:00:00:13:40:20   4094   0/0/1    static
PERMANENT    --
2001:1000::112                            80:1f:02:4c:19:60   4094   0/0/48   dynamic
REACHABLE    26 sec
Total entries: 2, Printed entries: 2
```


# 86. 静态路由

```
ip route
```


**命令功能**

配置静态路由表项。

**命令格式**

```
ip route dst-net mask next-hop [ distance distance]
no ip route dst-net mask [next-hop]
no ip route static all
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dst-net | 目标网络地址 | 0.0.0.0-223.255.255.254 |
| mask | 目标网络掩码 | 0.0.0.0-255.255.255.255 |
| next-hop | 下一跳ip 地址 | 必须三层接口配置子网vlan 地址 |
| distance | 管理距离值 | [1-255] |

```
show ip route
```


**命令功能**

查看路由表项

**命令格式**

```
show ip route [ip-address [ mask ]]
```


**参数说明**


**参数说明**

取值
ip-address
路由条目网络
0.0.0.0-255.255.255.255
mask
路由条目掩码
0.0.0.0-255.255.255.255
```
show ip route rib-stats
```


**命令功能**

查看路由统计信息

**命令格式**

```
show ip route rib-stats
```


**参数说明**

*无*

```
ipv6 route
```


**命令功能**

配置静态路由表项。

**命令格式**

```
(no)ipv6 route dst-net mask next-hop
(no)ipv6 route dst-net/len next-hop
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| dst-net | 目标ipv6 网络地 | 址 |
| 合法ip | mask | 目标网络掩码 |
| 合法掩码 | len | 掩码长度 |
| 0-128 | next-hop | 下一跳ipv6 地址 |

合法ip
```
show ipv6 route
```


**命令功能**

查看路由表项

**命令格式**

```
show ipv6 route
```


**参数说明**

*无*


# 87. RIP

```
router rip
```


**命令功能**

进入 rip 配置模式

**命令格式**

```
(no)router rip
```


**参数说明**

*无*

network

**命令功能**

Rip 配置模式启动指定ip 网段RIP 协议。

**命令格式**

```
(no)network ip-address
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip-address | 接口IP 地址 | 合法接口ip |

aggregate-addres

**命令功能**

Rip 模式配置聚合路由。

**命令格式**

```
(no)aggregate-address ip/m
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 聚合路由 | 如：192.168.0.0 |
| m | 掩码长度 | 0-32 |
| redistribute [static|connected|isis|ospf|bgp] [ metric value ] | [ route-map name] | 命令功能 |

Rip 模式配置引入外部路由

**命令格式**

```
redistribute [bgp|connected|isis|ospf|static] [ metric value ] [ route-map name]
no redistribute [bgp|connected|isis|ospf|static]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 引入路由的度量 | 0-16 |
| name | route-map 的名称 | STRING<1-32> |

```
default-information originate
```


**命令功能**

Rip 模式配置引入默认路由

**命令格式**

```
(no)default-information originate
```


**参数说明**

*无*

default-metric

**命令功能**

Rip 模式配置引入外部路由的默认metric 值

**命令格式**

```
default-metric value
no default-metric
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 默认metric 值 | [1,16] |

```
distance distance [ip/m [acl]]
```


**命令功能**

Rip 模式配置rip 路由的管理距离。

**命令格式**

```
distance distance [ip/m [acl]]
no distance [distance [ip/m [acl]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| distance | 管理距离 | [1,255] |
| ip/m | 匹配具体网段 | 如：192.168.0.0/16 |
| acl | ip acl 名 | 合法的值 |

distribute-list

**命令功能**

Rip 模式配置路由过滤

**命令格式**

```
(no)distribute-list [acl|prefix pre_name] [in | out]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl | ip acl 名 | STRING[1，32] |
| prefix | 前缀列表名 | STRING[1，32] |

```
ip access-list
```


**命令功能**

Rip 模式配置IP ACL 策略

**命令格式**

```
(no)ip access-list acl-list [permit | deny] ……
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl-list | 配置ip acl 的序列号或者ip acl | 名 |
| [1,99]为标准ACL； | [100,199]为扩展ACL； | [1300,1900]为标准ACL+扩展range |
| [2000,2699]为标准ACL+扩展range | STRING[1,32] IP ACL 名字 | 87.10. ip prefix-list |


**命令功能**

Rip 模式配置IP Prefix 策略。

**命令格式**

```
(no)ip prefix-list sequence-number
(no)ip prefix-list prefix-list [seq seq_id] [permit | deny] [ip/mask |any]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| prefix-list | 配置ip prefix 的name | STRING[1,32] |
| seq_id | 序列号 | INTEGER<1-2147483647> |
| ip/mask | 配置匹配的具体网段 | 如：192.168.1.0/24 |


## 87.11. key chain name


**命令功能**

RIP 模式配置密钥name，并进入keychain 配置模式

**命令格式**

```
(no)key chain name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Key-chain 名 | STRING[1,32] |


## 87.12. key chain


**命令功能**

Rip 配置模式配置认证管理密钥，并进入keychain 模式

**命令格式**

```
(no)key chain name
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Key-chain 名 | STRING[1,32] |


## 87.13. Key key_id


**命令功能**

keychain 模式配置密钥id，并进入key 模式

**命令格式**

```
(no)key key_id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key_id | Key 编号 | INTEGER<0-2147483647> |


## 87.14. Key key-string


**命令功能**

key 模式配置密钥id

**命令格式**

```
(no)key key-string
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| key-string | 密码 | STRING<1-16> |


## 87.15. accept-lifetime HH:MM:SS


**命令功能**

key 模式配置密钥accept life time

**命令格式**

```
(no)accept-lifetime HH:MM:SS day moth year HH:MM:SS day moth year
(no)accept-lifetime HH:MM:SS day moth year duration dura_key
(no)accept-lifetime HH:MM:SS day moth year infinite
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| day | 日 | <1-31> |
| moth | 月 | INTEGER<1-12> |
| year | 年 | INTEGER<1993-2035> |
| dura_key | Duration of the key | INTEGER<1-2147483646> |


## 87.16. send-lifetime HH:MM:SS


**命令功能**

key 模式配置密钥send life time

**命令格式**

```
(no)send-lifetime HH:MM:SS day moth year HH:MM:SS day moth year
(no)send-lifetime HH:MM:SS day moth year duration dura_key
(no)accept-lifetime HH:MM:SS day moth year infinite
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| day | 日 | <1-31> |
| moth | 月 | INTEGER<1-12> |
| year | 年 | INTEGER<1993-2035> |
| dura_key | Duration of the key | INTEGER<1-2147483646> |


## 87.17. ip rip authentication


**命令功能**

接口模式配置认证

**命令格式**

```
ip rip authentication mode [md5 key-chain chain_pass | text passwd string]
no ip rip authentication
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| md5 | 开启MD5 认证 | 无 |
| text | 开启明文认证 | 无 |
| chain_pass | Chain name | STRING<1-32> |
| string | 明文密码 | STRING(1-16 char) |


## 87.18. offset-list offset-list acl [in | out] metric


**命令功能**

Rip 模式配置路由偏移量

**命令格式**

```
(no)offset-list acl [in | out] metric [vlan-interface | supervlan-interface id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl | IP ACL 名 | STRING[1，32] |
| metric | Metric 值 | [0,16] |
| id | 接口号 | 普通接口[1,4094] |

超级接口[1,128]

## 87.19. passive-interface


**命令功能**

Rip 模式被动接口。

**命令格式**

```
(no)passive-interface [default | supervlan-interface vid | vlan-interface id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 接口号 | 普通接口[1,4094] |

超级接口[1,128]

## 87.20. route-map


**命令功能**

配置route-map 策略

**命令格式**

```
(no)route-map <name> [permit |deny] seq_num
(no)route-map <name> [in|out] [supervlan-interface|vlan-interface] id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 配置route-map 的名字 | STRING[1,32] |
| seq_num | Route-map 的序列号 | [1,65535] |
| id | 普通vlan 接口ID 号 | [普通接口[1,4094] |

超级接口[1,128]

## 87.21. timers basic


**命令功能**

Rip 模式配置定时器

**命令格式**

```
(no)timers basic <update><timeout><garbage>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| update | 配置RIP 路由update 时间 | [5,65535] |
| timeout | 配置RIP 路由timeout 时间 | [5,65535] |
| garbage | 配置RIP 路由garbage 时间 | [5,65535] |


## 87.22. version


**命令功能**

RIP 模式配置版本号

**命令格式**

```
version <version>
no version
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| version | 配置RIP 版本号 | 1,2 |


## 87.23. ip rip receive version


**命令功能**

接口模式配置接收报文的版本

**命令格式**

```
ip rip receive version version [bcast|mcast]
no ip rip receive version
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| version | 接收rip 报文的版本号 | 1,2 |


## 87.24. ip rip send version


**命令功能**

接口模式配置发送报文的版本

**命令格式**

```
ip rip send version version
no ip rip send version
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| version | 发送rip 报文的版本号 | 1,2 |


## 87.25. ip rip split-horizon


**命令功能**

接口模式配置水平分割

**命令格式**

```
ip rip split-horizon [poisoned-reverse]
no ip rip split-horizon [poisoned-reverse]
```


**参数说明**


## 87.26. show ip rip status


**命令功能**

查看rip 状态。

**命令格式**

```
show ip rip status
```


**参数说明**


## 87.27. show ip rip interface


**命令功能**

查看rip 接口状态。

**命令格式**

```
show ip rip interface [loopback-interface id|supervlan-interface id|vlan-interfaceid ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | Loopback 接口号 | 0,1 |
| Supervlan 的ID 号 | [1,128] | 普通vlan 接口ID 号 |

[1,4094]

## 87.28. show rip route-table


**命令功能**

查看 rip 路由信息

**命令格式**

```
show rip route-table [ip_address [mask]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip_address | Ip 地址 | 合法ip |
| mask | 掩码 | 合法掩码 |


## 87.29. show ip fdb


**命令功能**

查看 fdb 信息

**命令格式**

```
show ip fdb [ip_address [mask]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip_address | Ip 地址 | 合法ip |
| mask | 掩码 | 合法掩码 |


## 87.30. 配置举例

```
#组网
DUT1 ----------  DUT2
#配置RIP 进程
DUT1(config)#router rip
DUT1(config-router-rip)#network 192.168.1.10
DUT2(config)#router rip
DUT2(config-router-rip)#network 192.168.1.11
#查看rip 信息
DUT1(config-router-rip)#show ip rip status
Routing Protocol is "rip"
Sending updates every 30 seconds with +/-50%, next due in 18 seconds
Timeout after 180 seconds, garbage collect after 120 seconds
Default redistribution metric is 1
Outgoing update filter list for all interface is not set
Incoming update filter list for all interface is not set
Redistributing: connected
Default version control: send version 2, receive any version
Routing for Networks:
192.168.1.10
Routing Information Sources:
Gateway          BadPackets BadRoutes  Distance Last Update
192.168.1.11             0         0       120   00:00:16
Distance: (default is 120)
DUT1(config-router-rip)#
#发布直连路由
DUT1(config-router-rip)#redistribute connected
DUT2(config-router-rip)#redistribute connected
#查看从邻居学习的路由
DUT1(config-router-rip)#show ip route
IP route information
DestIp/Mask        Proto      Distance Metric   Nexthop         Interface
127.0.0.0/8        connected  0        1        *               N/A
192.168.1.0/24     connected  0        1        *               N/A
192.168.2.0/24     connected  0        1        *               N/A
192.168.3.0/24     rip        120      1        192.168.1.11    N/A
Total entries: 4. Printed entries: 4.
```


# 88. OSPF

```
router ospf
```


**命令功能**

全局视图配置ospf 进程

**命令格式**

```
(no)router ospf [<process_id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| process_id | 进程ID | [1-10] |

network

**命令功能**

ospf 视图配置接口的区域号

**命令格式**

```
(no)network <interface_address> <wildcard> area <area_id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| interface_address | 接口地址 | Ipv4 地址 |
| wildcard | 子网掩码，注意使用反码 | IPv4 地址 |
| 例如：0.0.0.255 | area_id | 区域编号 |
| IPv4 地址格式 | 例如：0.0.0.1 | 整数格式，取值[0-4294967295] |

例如：1
```
ip ospf authentication
```


**命令功能**

接口模式(取消)使能OSPF 认证。

**命令格式**

```
ip ospf authentication [message-digest|null] <ip>
no ip ospf authentication<ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 配置具体的ip 地址 | 合法ip |

```
ip ospf authentication-key
```


**命令功能**

接口模式配置明文密码。

**命令格式**

```
ip ospf authentication-key <key><ip>
no ip ospf authentication <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 配置具体的ip 地址 | 合法ip |
| key | 配置接口认证的密码 | STRING[1,8] |

```
ip ospf message-digest-key
```


**命令功能**

接口模式配置MD5 认证的密码

**命令格式**

```
ip ospf message-digest-key <id> md5<key><ip>
no ip ospf authentication <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 配置MD5 认证的密钥 | [1,255] |
| key | 配置接口认证的密码 | STRING[1,16] |
| ip | 配置具体的ip 地址 | 合法ip |

redistribute

**命令功能**

ospf 视图配置其它协议源的路由重发布到ospf 路由域。

**命令格式**

```
redistribute <protocol_type> [metric <metric-value> ] [metric-type <metric-type>]
[ route-map <name>]
no redistribute <protocol_type>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| protocol_type | 指定协议进行路由重发布 | [bgp,connected,isis,rip,static] |
| metric-value | 配置用于设置相应的重发布路 | 由的度量 |
| [0-16777214] | metric-type | 类型 |
| [1,2] | name | 配置route-map 的名称。 |

STRING<1-32>
```
area <id> authentication
```


**命令功能**

开启/关闭区域明文认证。

**命令格式**

```
(no)area <id> authenticatoin
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |

```
area <id> authentication message-digest
```


**命令功能**

开启/关闭区域MD5 认证

**命令格式**

```
(no)area <id> authentication message-digest
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |

```
area <id> default-cost
```


**命令功能**

配置发布默认路由的默认cost 值。

**命令格式**

```
(no)area <id> default-cost <cost>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |
| cost | 特殊区域发布默认路由的cost值 [0,16777214] | 88.10. area <id> filter-list prefix |


**命令功能**

配置区域间过滤策略。

**命令格式**

```
(no)area <id> filter-list prefix <prefix-list> [in |out]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |
| prefix-list | 前缀列表名 | STRING<1-32> |


## 88.11. area <id> nssa


**命令功能**

配置区域为NSSA 区域。

**命令格式**

```
(no)area <id> nssa <no-summary>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |


## 88.12. area <id> stub


**命令功能**

配置区域为STUB 区域

**命令格式**

```
(no)area <id> stub <no-summary>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |


## 88.13. area <id> range


**命令功能**

配置区域间聚合路由。

**命令格式**

```
area <id> range <ip1> [advertise |not-advertise|cost <cost>|substitute<ip2>]
no area <id> range <ip> [substitute]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |
| ip | 配置区域间聚合路由 | 例如：10.0.0.0/8 |
| advertise | 将聚合路由发布出去 | not-advertise |
| 将聚合路由不发布出去 | cost | 配置聚合路由的cost 值 |
| [0,16777215] | substitute | 聚合路由用另一网段替代 |


## 88.14. area <id> shortcut


**命令功能**

配置区域为shortcut 模式。

**命令格式**

```
area <id> shortcut <default| disable | enable>
no area <id> shortcut
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| default | 默认开启shortcut 模式 | 无 |
| disable | 关闭shortcut 模式 | 无 |
| enable | 开启shortcut 模式 | 无 |


## 88.15. area <id> virtual-link


**命令功能**

配置虚链路

**命令格式**

area<id>virtual-link<rid>[authentication-key<key>|message-digest-
key<kid>md5<key>|dead-interval<dead>|hello-interval<hello>|retransmit-
interval<retransmit>|transmit-delay<delay>]
```
no area <id> virtual-link <rid>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 区域编号 | IPv4 地址格式 |
| 例如：0.0.0.1 | 整数格式，取值[0-4294967295] | 例如：1 |
| rid | 配置虚链路对端的router id | 例如：2.2.2.2 |
| key | 配置认证密码                 STRING<1-8> | kid |
| 配置MD5 认证的密钥 | [1,255] | dead |
| 配置虚链路失效时间 | [1,65535] | hello |
| 配置虚链路hello 时间 | [1,65535] | retransmit |
| 配置虚链路重传时间 | [1,65535] | delay |
| 配置虚链路传输延迟时间 | [1,65535] | 88.16. auto-cost reference-bandwidth |


**命令功能**

配置接口默认cost 值计算方式

**命令格式**

```
(no)auto-cost reference-bandwidth <n>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| n | 配置cost 值计算参考值 | [1,4294967] |
| disable | 关闭shortcut 模式 | enable |

开启shortcut 模式

## 88.17. clear ip prefix-list


**命令功能**

清除匹配上前缀列表的统计值

**命令格式**

```
clear ip prefix-list <name> <ipv4>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 配置前缀列表名 | STRING[1,32] |
| ipv4 | 配置匹配具体的ip 网段 | 例：10.0.0.0/8 |


## 88.18. capability opaque


**命令功能**

配置支持opaque 的LSA。

**命令格式**

```
(no)capability opaque
```


**参数说明**

*无*


## 88.19. default-information originate


**命令功能**

配置引入默认路由

**命令格式**

```
default-information originate [always|metric<metric>|metric-type<metric-type>|route-
map<name>]
no default-information originate [always|metric|metric-type|route-map]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| metric | 配置引入默认路由的metric 值 | [0,16777214] |
| metric-type | 配置引入默认路由的类型值 | 1 和2 |
| name | route-map 的名字 | STRING[1,32] |


## 88.20. default-metric


**命令功能**

配置引入外部路由的默认metric 值。

**命令格式**

```
default-metric <metric>
no default-metric
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| metric | 配置引入外部路由的metric 值 | [0,16777214] |


## 88.21. distance


**命令功能**

配置ospf 路由的管理距离。

**命令格式**

```
distance <value><ipv4>[ospf external <value> |inter-area<value> |intra-area<value>]
no distance <value><ipv4>[ospf external <value> |inter-area<value> |intra-
area<value>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置管理距离的值 | [1,255] |
| ipv4 | 配置具体匹配网段的管理距离 | 例：10.0.0.0/8 |


## 88.22. distribute-list


**命令功能**

配置发布路策略

**命令格式**

```
(no)distribute-list <acl>out [bgp |connected|isis|rip|static]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl | 配置引用的acl 名 | STRING[1,32] |


## 88.23. ip access-list


**命令功能**

在OSPF 进程下配置IP ACL 策略。

**命令格式**

```
(no)ip access-list <acl-list> {permit | deny} [ip mask |any | host ip]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl-list | 配置ip acl 的序列号或者ip acl | 名 |
| [1,99]为标准ACL； | [100,199]为扩展ACL； | [1300,1900]为标准ACL+扩展range |
| [2000,2699]为标准ACL+扩展range | STRING[1,32] IP ACL 名字 | ip mask |
| 配置匹配的具体网段 | ip+ Wildcard mask 的格式 | 如：192.168.1.0 0.0.0.255 |
| any | 匹配所有的 | host ip |
| 匹配具体的主机地址 | 如：192.168.3.2 | 88.24. ip prefix-list |


**命令功能**

在OSPF 进程下配置IP Prefix 策略。

**命令格式**

```
(no)ip prefix-list <prefix-list>[seq <seq-num>] {permit | deny} [ip/mask |any]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| prefix-list | 配置ip prefix 的序列号 | STRING[1,32] |
| ip/mask | 配置匹配的具体网段 | ip+ mask 长度的格式 |
| 如：192.168.1.0/24 | any | 匹配所有的 |
| seq-num | 配置前缀列表的序列号 | [1,2147483647] |


## 88.25. log-adjacency-changes


**命令功能**

(取消)使能OSPF 日志信息。

**命令格式**

```
(no)log-adjacency-changes [ detail ]
```


**参数说明**

*无*


## 88.26. neighbor


**命令功能**

配置OSPF 的静态邻居。

**命令格式**

```
neighbor <ip> [poll-interval<interval>|priority<pri>]
no neighbor <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ip | 配置静态邻居的ip 地址 | interval |
| 配置静态邻居的轮询间隔时间 | [1,65535] | pri |
| 配置静态邻居的优先级 | [0,255] | 88.27. ospf abr-type |


**命令功能**

配置OSPF 的ABR 类型。

**命令格式**

```
ospf abr-type [cisco|ibm |shortcut|standard ]
no ospf abr-type
```


**参数说明**

*无*


## 88.28. ospf rfc1583compatibility


**命令功能**

配置兼容RFC1583 计算路由方式。

**命令格式**

```
(no)ospf rfc1583compatibility
```


**参数说明**

*无*


## 88.29. ospf router-id


**命令功能**

配置OSPF 的路由标识RID。

**命令格式**

```
ospf router-id <router-id>
no ospf router-id
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| router-id | 路由标识 | 0.0.0.1-255.255.255.255 |


## 88.30. passive-interface


**命令功能**

配置被动接口。

**命令格式**

```
(no)passive-interface [default | supervlan-interface <supervlan-id> <ip> |vlan-interface
<vlan-id> <ip> ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| supervlan-id | Supervlan 的ID 号 | [1,128] |
| ip | 匹配具体的ip 地址 | vlan-id |
| 普通vlan 接口ID 号 | [1,4094] | 88.31. refresh timer |


**命令功能**

配置刷新计时器

**命令格式**

```
refresh timer <timer>
no refresh timer
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| timer | 刷新计时器的时间 | [10,1800] |


## 88.32. route-map


**命令功能**

配置route-map 策略。

**命令格式**

```
route-map <name>[permit |deny]
no route-map<name>[permit |deny]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 配置route-map 的名字 | STRING[1，32] |


## 88.33. timers throttle spf


**命令功能**

配置SPF 算法的阀值。

**命令格式**

```
timers throttle spf <delay><init><max>
no timers throttle spf
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| delay | 配置SPF 算法的delay 时间 | [0，600000] |
| init | 配置SPF 算法的init hold 时间 | [0，600000] |
| max | 配置SPF 算法的max hold 时间 | [0，600000] |


## 88.34. ip ospf bfd


**命令功能**

接口模式(取消)使能BFD 功能。

**命令格式**

```
(no)ip ospf bfd
```


## 88.35. ip ospf cost


**命令功能**

接口模式配置接口的cost 值。

**命令格式**

```
ip ospf cost <cost> [<ip>]
no ip ospf cost [<ip>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| cost | 配置接口的cost 值 | [1,65535] |
| ip | 配置匹配具体ip | 合法Ip |


## 88.36. ip ospf dead-interval


**命令功能**

接口模式配置OSPF 失效时间。

**命令格式**

```
ip ospf dead-interval <value> [minimal hello-multiplier <num> ] <ip>
no ip ospf dead-interval <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的dead 时间 | [1,65535] |
| num | 配置dead 为hello 时间的倍数 | [1,10] |
| ip | 配置匹配具体ip | 88.37. ip ospf hello-interval |


**命令功能**

接口模式配置OSPFhello 时间。

**命令格式**

```
ip ospf hello-interval <value> <ip>
no ip ospf hello-interval <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的hello 时间 | [1,65535] |
| ip | 配置匹配具体ip | 合法ip |


## 88.38. ip ospf mtu-ignore


**命令功能**

接口模式(取消)使能忽略检查MTU 值。

**命令格式**

```
(no)ip ospf mtu-ignore <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的hello 时间 | [1,65535] |
| ip | 配置匹配具体ip | 合法ip |


## 88.39. ip ospf network


**命令功能**

接口模式配置网络类型。

**命令格式**

```
ip ospf network [broadcast|non-broadcast|point-to-multipoint|point-to-point]
no ip ospf network
```


**参数说明**

*无*


## 88.40. ip ospf priority


**命令功能**

接口模式接口的优先级。

**命令格式**

```
ip ospf priority <value> <ip>
no ip ospf priority <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的优先级 | [0,255] |
| ip | 配置匹配具体ip | 合法ip |


## 88.41. ip ospf retransmit-interval


**命令功能**

接口模式配置重传时间。

**命令格式**

```
ip ospf retransmit-interval <value> <ip>
no ip ospf retransmit-interval <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的重传时间 | [1,655535] |
| ip | 配置匹配具体ip | 合法Ip |


## 88.42. ip ospf transmit-delay


**命令功能**

接口模式配置传输延时时间。

**命令格式**

```
ip ospf transmit-delay <value> <ip>
no ip ospf transmit-delay <ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| value | 配置接口的传输延时时间 | [1,655535] |
| ip | 配置匹配具体ip | 88.43. show ip ospf |


**命令功能**

查看ospf 信息。

**命令格式**

```
show ip ospf <id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | OSPF 进程ID | [1,10] |


## 88.44. show ospf route-table


**命令功能**

查看ospf 路由表信息。

**命令格式**

```
show ospf route-table
```


**参数说明**

*无*


## 88.45. show ip ospf border-routers


**命令功能**

查看ospf 边界路由器信息。

**命令格式**

```
show ip ospf border-routers
```


**参数说明**

*无*


## 88.46. show ip ospf database


**命令功能**

查看ospf LSA 数据库信息。

**命令格式**

```
show ip ospf database [asbr-summary|external |network|nssa-external|opaque-area
|opaque-as|opaque-link|router|summary]
```


**参数说明**

*无*


## 88.47. show ip ospf interface


**命令功能**

查看ospf 接口信息。

**命令格式**

```
show ip ospf interface [vlan-interface<vid>|supervlan-interface<s-vid>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| vid | 普通vlan 接口的ID 号 | [1,4094] |
| s-vid | Supervlan 接口的ID 号 | [1,128] |


## 88.48. show ip ospf neighbor


**命令功能**

查看ospf 邻居信息。

**命令格式**

```
show ip ospf neighbor
```


**参数说明**

*无*


## 88.49. show ip ospf virtual-link


**命令功能**

查看ospf 虚链路信息。

**命令格式**

```
show ip ospf virtual-link
```


**参数说明**

*无*


## 88.50. 配置举例

```
#组网
DUT1 ----------  DUT2
#配置OSPF 进程1
DUT1(config-router-ospf-1)#router ospf 1
DUT1(config-router-ospf-1)#network 192.168.1.10 0.0.0.255 area 0.0.0.1
DUT2(config-router-ospf-1)#router ospf 1
DUT2(config-router-ospf-1)#network 192.168.1.11 0.0.0.255 area 0.0.0.1
#查看邻居信息
DUT1(config)#show ip ospf 1 neighbor
Type: D - Dynamic, S - Static
Type  Neighbor ID    Pri State      Dead Time Address     Interface     RXmtL RqstL DBsmL
D   192.168.1.11     1 Full/DR      34.258s 192.168.1.11    VLAN-IF1      0     0     0
#查看从邻居学习的路由
DUT1(config-router-ospf-1)#show ip route
IP route information
DestIp/Mask        Proto      Distance Metric   Nexthop         Interface
127.0.0.0/8        connected  0        1        *               N/A
192.168.1.0/24     connected  0        1        *               N/A
192.168.2.0/24     connected  0        1        *               N/A
192.168.3.0/24     ospf       110      1        192.168.1.11    N/A
Total entries: 4. Printed entries: 4.
```


# 89. VRRP


## 89.1. vrrp vrid<vrid> virtual-ip


**命令功能**

接口模式下配置虚拟ip 地址

**命令格式**

```
vrrp vrid <vrid> virtual-ip <ip-address>
no vrrp vrid [<vrid> [virtual-ip <ip-address>]]
no vrrp vrid all
```


**参数说明**


**参数说明**

取值
vrid
id
1-255
ip-address
ip
合法ip

## 89.2. vrrp vrid<vrid> priority


**命令功能**

接口模式下配置优先级

**命令格式**

```
vrrp vrid <vrid> priority < priority>
no vrrp <vrid>priority
```


**参数说明**


**参数说明**

取值
vrid
id
1-255
priority
优先级
1-254

## 89.3. vrrp vrid<vrid> preempt-mode


**命令功能**

接口模式下配置抢占参数

**命令格式**

```
vrrp vrid <vrid> preempt-mode [delay <delay> ]
no vrrp vrid <vrid> preempt-mode
```


**参数说明**


**参数说明**

取值
vrid
id
1-255
delay
抢占延时
0-255

## 89.4. vrrp vrid<vrid> advertise-interval


**命令功能**

接口模式下配置vrrp 报文发送周期

**命令格式**

```
vrrp vrid <vrid> advertise-interval<time>
no vrrp vrid <vrid> advertise-interval
```


**参数说明**


**参数说明**

取值
vrid
虚拟id
1-255
time
具体参数
1-255s default：1s

## 89.5. vrrp vrid<vrid>track


**命令功能**

接口模式下配置vrrp 监视端口

**命令格式**

```
vrrp vrid <vrid>track [vlan-interface <vlan-if>|supervlan-if <supervlan-if>] [reduced
<priority>]
no vrrp vrid <vrid>track [vlan-interface <vlan-if>|supervlan-if <supervlan-if>|all]
```


**参数说明**


**参数说明**

取值
vrid
id
1-255
priority
优先级
1-254

## 89.6. vrrp ping-enable


**命令功能**

全局模式下(取消)使能VRRP ping 功能。

**命令格式**

```
vrrp ping-enable
no vrrp ping-enable
```


**参数说明**

*无*


## 89.7. show vrrp status


**命令功能**

查看vrrp 信息

**命令格式**

```
show vrrp status[ vlan-interface <id> | supervlan-interface <id>] [vrid ]
```


**参数说明**


**参数说明**

取值
id
普通vlan 号或者
supervlan 号
1-4094
1-128
vrid
1-255

## 89.8. show vrrp statistics


**命令功能**

查看vrrp 数据统计信息

**命令格式**

```
show vrrp statistics[ vlan-interface <id> | supervlan-interface <id>] [vrid ]
```


**参数说明**


**参数说明**

取值
id
普通vlan 号或者
supervlan 号
vrid
1-255

## 89.9. 配置举例

```
#组网
(12.1.1.1)DUT1      DUT2(12.1.1.2)
\        /
SW
步骤1 创建VLAN 并配置各接口所属VLAN，配置各VLANIF 接口的IP 地址
步骤2 交换机配置VRRP。
#DUT1 配置
DUT1(config)# interface vlan-interface 1
DUT1(config-if-vlanInterface-1)# vrrp vrid 1 virtual-ip 192.168.1.254
#DUT2 配置
DUT2(config)# interface vlan-interface 1
DUT2(config-if-vlanInterface-1)#vrrp vrid 1 virtual-ip 192.168.1.254
#DUT1 查看vrrp 状态
DUT1(config)# show vrrp status
Show informations of VRRP status
Virtual IP Ping: Enable
VLAN-IF1 | Virtual Router 1
State                     : Master
Virtual IP                : 192.168.1.254
Priority                  : 100
Preempt Mode              : YES
Delay Time (secs)         : 0
Advertise Interval (secs) : 1
track interfaces:
Total entries:1
```


# 90. 路由策略


## 90.1. IP ACL


**命令功能**

路由模式下配置访问控制列表

**命令格式**

```
(no)ip access-list Id {permit | deny} {any | ipv4 wildcard-mask | host ipv4} [{any | ipv4
wildcard-mask | host ipv4}]
(no)ip access-list name {any | ipv4/lenv4 [exact-match]}
(no)ip access-list name {permit | deny} {any | ipv6/lenv6 [exact-match]}
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | IP ACL ID | [1-99,100-199,1300-1999,2000-2699] |
| name | IP ACL 名称 | 1-32 个字符 |
| ipv4 | IPv4 地址 | X.X.X.X，X∈[0-255] |
| wildcard-mask | 反掩码 | X.X.X.X，X∈[0-255] |
| lenv4 | 地址前缀长度 | [0-32] |
| ipv6 | IPv6 地址 | XXXX.XXXX.XXXX.XXXX.XXXX.XXXX. |
| XXXX.XXXX，X∈[0-F] | lenv6 | 地址前缀长度 |

[0-128]

## 90.2. Prefix-list


**命令功能**

路由模式下创建或者删除地址前缀列表

**命令格式**

```
ip prefix-list name [seq num] {permit | deny} {any | ipv4/lenv4 [ge glenv4] [le llenv4]}
no ip prefix-list name [[seq num] {permit | deny} {any | ipv4/lenv4 [ge glenv4] [le
llenv4]}]
Ripng 路由模式下配置
ip prefix-list name [seq num] {permit | deny} {any | ipv6/lenv6 [ge glenv6] [le llenv6]}
no ip prefix-list name [[seq num] {permit | deny} {any | ipv6/lenv6 [ge glenv6] [le
llenv6]}]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Prefix-list 名称 | 1-32 个字符 |
| ipv4 | IPv4 地址 | X.X.X.X，X∈[0-255] |
| lenv4 | IPv4 地址前缀长 | 度 |
| [0-32] | glenv4 | 掩码最小长度 |
| [0-32] | llenv4 | 掩码最大长度 |
| [0-32] | ipv6 | IPv6 地址 |
| XXXX.XXXX.XXXX.XXXX.XXXX.XXXX. | XXXX.XXXX，X∈[0-F] | lenv6 |
| 地址前缀长度 | [0-128] | glenv6 |
| 掩码最小长度 | [0-128] | llenv6 |
| 掩码最大长度 | [0-128] | 90.3. Prefix-list sequence-number |


**命令功能**

路由模式下（取消）使能地址前缀列表规则编号

**命令格式**

```
ip prefix-list sequence-number
no ip prefix-list sequence-number
```


**参数说明**

*无*


## 90.4. As-path ACL


**命令功能**

BGP 路由模式下创建或者删除as-path acl

**命令格式**

```
ip as-path access-list Id {permit | deny} regular-expression
no ip as-path access-list Id {permit | deny} regular-expression
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | ACL ID | [1-199] |
| regular-expression | 正则表达式 | 1-64 个字符 |


## 90.5. 控制路由发布


**命令功能**

路由模式下控制路由发布

**命令格式**

Rip 路由模式下配置
```
distribute-list [prefix] name direction [vlan-interface interfaceId | supervlan-interface
superInterfaceId]
no distribute-list [prefix] name direction [vlan-interface interfaceId | supervlan-
interface superInterfaceId]
BGP 路由模式下配置
neighbor neighborName distribute-list {aclId | aclName} direction
no neighbor neighborName distribute-list {aclId | aclName} direction
neighbor neighborName prefix-list prefixListName direction
no neighbor neighborName prefix-list prefixListName direction
neighbor neighborName filter-list aspathaclId direction
no neighbor neighborName filter-list aspathaclId direction
OSPF 路由模式下配置
distribute-list aclName out routeType
no distribute-list aclName out routeType
area {Id | addressId} filter-list prefix prefixlistName direction
no area {Id | addressId} filter-list prefix prefixlistName direction
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | IP ACL 或者 | Prefix-list 的名称 |
| 1-32 个字符 | direction | 出入方向 |
| [in,out] | interfaceId | 普通接口ID |
| [1-4094] | superInterfaceId | 超级接口ID |
| [1-128] | neighborName | 邻居名 |
| 1-32 个字符 | aclId | IP ACL ID |
| [1-199,1300-1999] | aclName | IP ACL 名称 |
| 1-32 个字符 | prefixlistName | Prefix-list 名称 |
| 1-32 个字符 | aspathaclId | As-path ACL ID |
| [1-199] | routeType | 路由类型 |
| [bgp,connected,isis,rip,static] | Id | 数字格式的区域 |
| ID | [0-4294967295] | addressId |
| IP 地址格式的区 | 域ID | X.X.X.X，X∈[0-255] |


## 90.6. route-map


**命令功能**

路由模式下配置route-map 路由策略

**命令格式**

```
route-map name {permit | deny} Id
no route-map name [{permit | deny} Id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 策略名称 | 1-32 个字符 |
| Id | 节点ID | [1-65535] |


## 90.7. match


**命令功能**

```
Route map 模式下配置匹配条件
```


**命令格式**

```
(no)match {ip | ipv6} address [prefix-list] {Id | name}
(no)match as-path aspathId
(no)match interface { vlan-interface interfaceId | supervlan-interface superInterfaceId }
(no)match metric metric
(no)match origin { egp | igp | incomplete}
(no)match peer peerAddress
(no)match probability percentage
(no)match tag tagValue
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | IP ACL ID | [1-199,1300-2699] |
| name | IP ACL 或者 | prefix-list 名称 |
| 1-32 个字符 | aspathId | as-path ACL ID |
| [1-199] | interfaceId | 普通接口ID |
| [1-4094] | superInterfaceId | 超级接口ID |
| [1-128] | metric | metric 数值 |
| [0-4294967295] | peerAddress | 对等体地址 |
| X.X.X.X，X∈[0-255] | percentage | 百分比 |
| [0-100] | tagValue | 标签值 |

[0-65535]

## 90.8. set


**命令功能**

```
Route map 模式下配置匹配成功之后的行为
```


**命令格式**

```
(no)set {ip next-hop ipv4 | ipv6 next-hop {global | local} ipv6}
(no)set local-preference preference
(no)set metric-type type {type-1 | type-2}
(no)set metric metric
(no)set origin { egp | igp | incomplete}
(no)set tag tagValue
(no)set weight weightValue
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| ipv4 | IPv4 地址 | X.X.X.X，X∈[0-255] |
| ipv6 | IPv6 地址 | XXXX.XXXX.XXXX.XXXX.XXXX.XXXX. |
| XXXX.XXXX，X∈[0-F] | preference | 偏好度 |
| [0-4294967295] | metric | metric 数值 |
| [0-4294967295] | tagValue | 标签值 |
| [0-65535] | weightValue | 权值 |

[0-4294967295]

## 90.9. on-match goto


**命令功能**

Route-map 模式下配置匹配成功后跳转到指定序列

**命令格式**

```
(no)on-match [next | goto Id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 节点ID | [1-65535] |


## 90.10. call route-map


**命令功能**

Route-map 模式下配置再匹配其他route-map

**命令格式**

```
call name
no call
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 路由策略名称 | 1-32 个字符 |


## 90.11. route-map 应用


**命令功能**

Rip 或者Ripng 路由模式下（取消）应用路由策略

**命令格式**

```
(no)route-map name [in|out] [ vlan-interface Id | supervlan-interface s_id ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | 策略名称 | 1-32 个字符 |
| id | 普通接口ID | [1-4094] |
| s_id | 超级接口ID | [1-128] |


## 90.12. show ip access-list


**命令功能**

路由模式下查看IP ACL 配置信息

**命令格式**

```
show ip access-list [Id | name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | IP ACLID | [1-99,100-199,1300-1999,2000-2699] |
| name | IP ACL 名称 | 1-32 个字符 |


## 90.13. show ip prefix-list


**命令功能**

路由模式下查看prefix list 配置信息

**命令格式**

```
show ip prefix-list
show ip prefix-list summary [name]
show ip prefix-list detail [name]
show ip prefix-list name [seq num | address/len [first-match | longer]]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| name | Prefix-list 名称 | 1-32 个字符 |
| num | Prefix-list 规则编 | 号 |
| [1-2147483647] | address | 网络地址 |
| X.X.X.X，X∈[0-255] | len | 地址前缀长度 |

[0-32]

## 90.14. show ip as-path access-list


**命令功能**

路由模式下查看As-path ACL 配置信息

**命令格式**

```
show ip as-path access-list [Id]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | As-path ACLID | [1-199] |


## 90.15. show route-map


**命令功能**

路由模式下查看route map 配置信息

**命令格式**

```
show route-map [name]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Name | 路由策略名称 | 1-32 个字符 |


# 91. 策略路由


## 91.1. traffic policy-based-route


**命令功能**

全局下配置基于ACL 的策略路由

**命令格式**

```
(no)traffic policy-based-route {hybrid-acl hId [subitem subId] | ip-acl iId [subitem
subId] mac-acl mId [subitem subId]} next-hop {ipv4 | ipv6 ipv6}
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| hId | Hybrid-acl Id | [2000-2999] |
| iId | IP-acl Id | [1-999] |
| mId | MAC-acl Id | [1000-1999] |
| subId | 规则ID | [0-127] |
| ipv4 | IPv4 地址 | X.X.X.X，X∈[0-255] |
| ipv6 | IPv6 地址 | XXXX.XXXX.XXXX.XXXX.XXXX.XXXX. |

XXXX.XXXX，X∈[0-F]

## 91.2. show traffic policy-based-route


**命令功能**

查看策略路由配置

**命令格式**

```
show traffic policy-based-route
```


**参数说明**

*无*


# 92. BFD

bfd

**命令功能**

全局（取消）使能BFD

**命令格式**

```
bfd enable
bfd disable
```


**参数说明**

*无*

```
bfd demand
```


**命令功能**

接口下（取消）使能BFD 查询模式

**命令格式**

```
bfd demand start
bfd demand off
```


**参数说明**

*无*

```
bfd detect-multiplier
```


**命令功能**

接口下配置检测次数

**命令格式**

```
bfd detect-multiplier <counts>
no bfd detect-multiplier
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| counts | 检测次数 | [3-50] |

```
bfd min-receive-interval
```


**命令功能**

接口下配置最小接收时间间隔

**命令格式**

```
bfd min-receive-interval <time-value>
no bfd min-receive-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 最小接收时间间 | 隔 |

[200-1000]
```
bfd min-transmit-interval
```


**命令功能**

接口下配置最小发送时间间隔

**命令格式**

```
bfd min-transmit-interval <time-value>
no bfd min-transmit-interval
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 最小接收时间间 | 隔 |

[200-1000]
```
bfd session init-mode
```


**命令功能**

接口下配置会话模式

**命令格式**

```
bfd session init-mode [active | passive]
no bfd session init-mode
```


**参数说明**

*无*

```
show bfd interface
```


**命令功能**

查看接口BFD 配置

**命令格式**

```
show bfd interface [verbose]
```


**参数说明**

*无*

```
show bfd session
```


**命令功能**

查看BFD 会话配置

**命令格式**

```
show bfd session [verbose]
```


**参数说明**

*无*


# 93. IP-def-cpu

```
ip dlf cpu
```


**命令功能**

全局（取消）使能

**命令格式**

```
(no)ip dlf cpu
```


**参数说明**

*无*

```
ip host-dlf cpu
```


**命令功能**

接口下（取消）使能

**命令格式**

```
(no)ip host-dlf cpu
```


**参数说明**

*无*

```
show ip dlf cpu
```


**命令功能**

查看全局配置

**命令格式**

```
show ip dlf cpu
```


**参数说明**

*无*

```
show ip host-dlf cpu
```


**命令功能**

查看接口配置

**命令格式**

```
show ip host-dlf cpu
```


**参数说明**

*无*


# 94. IGMP


## 94.1. ip multicast-routing


**命令功能**

全局(取消)使能组播路由协议

**命令格式**

```
(no)ip multicast-routing
```


**参数说明**

*无*

```
ip igmp
```


**命令功能**

在三层接口(取消)使能igmp

**命令格式**

```
(no)ip igmp
```


**参数说明**

*无*

```
ip igmp version
```


**命令功能**

在三层接口配置igmp 版本

**命令格式**

```
(no)ip igmp version <number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 版本号 | 1-3 |

```
ip igmp access-group
```


**命令功能**

三层接口配置组播过滤功能

**命令格式**

```
(no)ip igmp access-group <acl-number> [all| ethernet <port-number>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl-number | 关联的acl 号 | 1-999 |
| port-number | 端口号 | all |

所有端口
```
ip igmp create-group
```


**命令功能**

三层接口配置静态组播路由表，主要是跟ip igmp static-group 命令配合使用

**命令格式**

```
(no)ip igmp create-group <group>[to <group>] <source> [*|source-ip]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group | 组地址 | 合法地址 |
| * | 所有源 | 无 |
| source-ip | 具体源地址 | 合法ip |

```
ip igmp static-group
```


**命令功能**

三层接口配置静态组播组

**命令格式**

```
(no)ip igmp static-group [ * | group ] [all| ethernet port-id] sourcelist [ * | source-ip ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group | 组地址 | 合法组播 |
| port-id | 端口时配置 | 合法端口号 |
| source-ip | 指定源 | 具体ip |

```
ip igmp last-member-query-interval
```


**命令功能**

三层接口配置最后成员查询发送间隔

**命令格式**

```
(no)ip igmp last-member-query-interval <seconds>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 间隔时间 | 1-25s，default：1s |

```
ip igmp limit-group
```


**命令功能**

三层接口限制组播组最大数

**命令格式**

```
ip igmp limit-group <number>
no ip igmp limit-group
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 0-1024 | 94.9. |

```
ip igmp query-max-response-time
```


**命令功能**

三层接口配置最大查询响应时间

**命令格式**

```
(no)ip igmp query-max-response-time <seconds>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 具体取值 | 1-3000s，default：10s |


## 94.10. ip igmp query-interval


**命令功能**

三层接口配置发送通用查询报文间隔

**命令格式**

```
(no)ip igmp query-interval <seconds>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| seconds | 间隔时间 | 15-30000，default：125s |


## 94.11. ip igmp ssm-mapping


**命令功能**

三层接口开启igmp ssm 映射，主要是跟mroute igmp 命令配合使用

**命令格式**

```
(no)ip igmp ssm-mapping
```


**参数说明**


## 94.12. mroute igmp


**命令功能**

进入router-igmp 配置模式

**命令格式**

```
mroute igmp
```


**参数说明**

*无*


## 94.13. ssm-mapping <group><mask><source-ip>


**命令功能**

router-igmp 模式下配置ssm-mapping 映射表

**命令格式**

```
(no)ssm-mapping <group> <mask> <source-ip>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group | 组地址 | 224.0.0.1-239.255.255.254 |
| mask | 掩码长度 | 0-32 |
| source-ip | 具体源地址 | 合法ip |


## 94.14. ip igmp robustness-varible


**命令功能**

三层接口配置查询器健壮性变量。

**命令格式**

```
(no)ip igmp robustness-varible <number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 取值 | 2-7 |


## 94.15. show ip igmp groups


**命令功能**

查看组信息

**命令格式**

```
show ip igmp groups [dynamic|static|group-ip]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-ip | 组地址 | 合法组播地址 |


## 94.16. show ip igmp interface


**命令功能**

查看三层接口的igmp 信息

**命令格式**

```
show ip igmp interface [vlan-interface <id>|supervlan-interface <id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 三层接口i | 普通接口1-4094 |

超级接口1-128

## 94.17. show ip igmp ssm-mapping


**命令功能**

查看三层接口的igmp ssm-mapping 信息

**命令格式**

```
show ip igmp ssm-mapping [group-ip]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-ip | 组地址 | 224.0.0.1-239.255.255.254 |


## 94.18. 配置举例

```
#组网：
TC1--------(if1)DUT(if2)--------TC2
步骤1 创建VLAN 并配置各接口所属VLAN，配置各VLANIF 接口的IP 地址。
步骤2 交换机全局使能主播路由功能，三层接口下使能IGMP 功能和PIM-DM 功能。
#DUT 配置
DUT(config)#ip multicast-routing
DUT(config)#int vlan 1
DUT(config-if-vlanInterface-1)#ip pim dense-mode
DUT(config)#int vlan 2
DUT(config-if-vlanInterface-2)#ip pim dense-mode
DUT(config-if-vlanInterface-2)#ip igmp
步骤3 TC1 发送225.0.1.1 的组播流，TC2 发送225.0.1.1 的report 报文，查看TC2 能收到组播流。
DUT#show ip igmp groups
IGMP Connected Group Membership
Group Address: 225.0.1.1
Vlan: 2, port: 0/0/10, Uptime: 00:00:57
Expires: 00:03:27, Last Reporter: 10.1.1.2
V1 Expires: 00:00:00, V2 Expires: 00:03:27, Self: False
FilterMode: EXCLUDE, Static: False
Forward Source(0): none
Block Source(0): none
Current State(IGMP_MS_NORMAL2)
Total Groups: 1, Total group members: 1
```


# 95. PIM


## 95.1. ip multicast-routing


**命令功能**

全局(取消)使能组播路由协议

**命令格式**

```
(no)ip multicast-routing
```


**参数说明**

```
ip pim mode [ dense-mode | sparse-mode ]
```


**命令功能**

在三层接口使能pim 协议

**命令格式**

```
(no)ip pim [ dense-mode | sparse-mode ]
```


**参数说明**

*无*

```
ip pim neighbor-limit
```


**命令功能**

在三层接口配置neighbor-limit

**命令格式**

```
(no)ip pim neighbor-limit <number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 限制数量 | 1-128 |

```
ip pim neighbor-policy
```


**命令功能**

三层接口配置邻居过滤功能

**命令格式**

```
(no)ip pim neighbor-policy <acl-number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl-number | acl 号 | 1-999 |

```
ip pim query-interval
```


**命令功能**

三层接口配置邻居发现报文发送间隔

**命令格式**

```
(no)ip pim query-interval <number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | 报文发送周期 | 1-65535 |

```
ip pim bsr-border
```


**命令功能**

三层接口(取消)使能bsr border

**命令格式**

```
(no)ip bsr-border
```


**参数说明**

*无*

```
mroute pim
```


**命令功能**

进入 pim 配置模式

**命令格式**

```
(no)mroute pim
```


**参数说明**

```
bsr-candidate vlan-interface if-id hash-len pri
```


**命令功能**

```
pim 模式下配置bsr-candidate
```


**命令格式**

```
bsr-candidate vlan-interface <if-id> <hash-len> <pri>
no bsr-candidate
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| If-id | 接口id | Interface id 相同 |
| Hash-len | Hash mask length | 0-32 |
| pri | priority | 0-255 |

rp-candidate

**命令功能**

Pim 模式下配置候选rp

**命令格式**

```
rp-candidate vlan-interface <if-id> group-list <number> <priority>
no rp-candidate
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | Acl id | 1-999 |
| Priority | 优先级 | 0-255 |


## 95.10. static-rp


**命令功能**

Pim 模式下配置静态rp

**命令格式**

```
static-rp a.b.c.d [preferred ]
no static-rp
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| A.b.c.d | Rp ip | 合法ip |


## 95.11. source-policy


**命令功能**

Pim 模式下配置组播源过滤

**命令格式**

```
(no)source-policy <number>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| number | Acl id | 1-999 |


## 95.12. spt-threshold


**命令功能**

Pim 模式配置stp 切换方式

**命令格式**

spt-threshold ｛immediately |infinity｝
```
no spt-threshold
```


**参数说明**

*无*


## 95.13. ssm


**命令功能**

Pim 模式配置ssm 组播范围

**命令格式**

```
(no) ssm [default|range access-list]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| acl-list | 关联的acl 号 | 1-999 |


## 95.14. show ip pim bsr


**命令功能**

查看BSR 的信息

**命令格式**

```
show ip pim bsr
```


**参数说明**

*无*


## 95.15. show ip pim interface


**命令功能**

查看运行PIM 的接口信息

**命令格式**

```
show ip pim interface  [vlan-interface <id>|supervlan-interface <id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 三层接口id | 普通接口1-4094 |

超级接口1-128

## 95.16. show ip pim neighbor


**命令功能**

查看运行PIM 邻居信息

**命令格式**

```
show ip pim neighbor [vlan-interface <id>|supervlan-interface <id>]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| id | 三层接口id | 普通接口1-4094 |

超级接口1-128

## 95.17. show ip pim rp-info


**命令功能**

查看当前的RP 信息

**命令格式**

```
show ip pim rp-info [group-ip]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| group-ip | 组地址 | 224.0.0.1-239.255.255.254 |


## 95.18. show ip pim ssm


**命令功能**

查看配置的SSM 组地址范围

**命令格式**

```
show ip pim ssm range
```


**参数说明**

*无*


## 95.19. show ip mroute


**命令功能**

查看组播路由信息

**命令格式**

```
show ip mroute [static |dynamic|a.b.c.d]
```


**参数说明**

*无*


# 96. EFM

efm

**命令功能**

端口下（取消）使能EFM 功能

**命令格式**

```
(no)efm
```


**参数说明**

*无*

```
efm mode
```


**命令功能**

端口下配置工作模式

**命令格式**

```
efm mode [active | passive]
```


**参数说明**

*无*

```
efm pdu-timeout
```


**命令功能**

端口下配置OAMPDU 报文发送间隔时间

**命令格式**

```
efm pdu-timeoute <time-value>
no efm pdu-timeout
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 发送间隔时间 | [1-60] |

```
efm link-timeout
```


**命令功能**

端口下配置连接超时时间

**命令格式**

```
(no)efm link-timeout <time-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 连接超时时间 | [3-300] |

```
efm remote-response-timeout
```


**命令功能**

端口下配置响应超时时间

**命令格式**

```
(no)efm remote-response-timeoute <time-value>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| time-value | 响应超时时间 | [1-10] |

```
efm remote-failure
```


**命令功能**

端口下配置紧急链路事件类型

**命令格式**

```
(no)efm remote-failure [critical-event | dying-gasp | link-fault]
```


**参数说明**

*无*

```
efm link-monitor error-frame
```


**命令功能**

端口下配置链路事件类型error-frame

**命令格式**

```
efm link-monitor error-frame [window <window> | threshold <threshold>]
no efm link-monitor error-frame [window | threshold ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| window | 窗口大小 | [10-600] |
| threshold | 阈值 | [1-4294967295] |

```
efm link-monitor error-frame-seconds
```


**命令功能**

端口下配置链路事件类型error-frame-seconds

**命令格式**

```
efm link-monitor error-frame-seconds [window <window> | threshold old <threshold>]
no efm link-monitor error-frame-seconds [window | threshold ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| window | 窗口大小 | [100-9000] |
| threshold | 阈值 | [1-900] |

```
efm link-monitor error-frame-period
```


**命令功能**

端口下配置链路事件类型error-frame-period

**命令格式**

```
efm link-monitor error-frame-period [window <window> | threshold <threshold>]
no efm link-monitor error-frame-period [window | threshold ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| window | 窗口大小 | [1-4294967295] |
| threshold | 阈值 | [1-4294967295] |


## 96.10. efm link-monitor error-symbol-period


**命令功能**

端口下配置链路事件类型error-frame-period

**命令格式**

```
efm link-monitor error-symbol-period [window high <high> low <low> | threshold old
high <t-high> low <t-low>]
no efm link-monitor error-symbol-period [window | threshold ]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| high | 窗口高 | [0-4294967295] |
| low | 窗口低 | [0-4294967295] |
| t-high | 阈值高 | [0-4294967295] |
| t-low | 阈值低 | [0-4294967295] |


## 96.11. efm remote-loopback


**命令功能**

端口下（取消）使能远端环回功能

**命令格式**

```
(no)efm remote-loopback
```


**参数说明**

*无*


## 96.12. efm remote-loopback process


**命令功能**

端口下使能处理远端环回报文

**命令格式**

```
efm remote-loopback d
```


**参数说明**

*无*


## 96.13. efm remote-loopback ignore


**命令功能**

端口下取消使能不处理远端环回报文

**命令格式**

```
efm remote-loopback ignore
```


**参数说明**

*无*


## 96.14. efm remote-loopback start


**命令功能**

端口下执行远端环回检测

**命令格式**

```
efm remote-loopbak start
```


**参数说明**

*无*


## 96.15. efm remote-loopback stop


**命令功能**

端口下结束执行远端环回检测

**命令格式**

```
efm remote-loopbak stop
```


**参数说明**

*无*


## 96.16. efm variable-retrieval


**命令功能**

端口下（取消）使能远端MIB 获取

**命令格式**

```
(no)efm variable-retrieval
```


**参数说明**

*无*


## 96.17. show efm discover


**命令功能**

查看发现信息

**命令格式**

```
show efm discover interface [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


## 96.18. show efm port


**命令功能**

端口查看获取的远端设备端口MIB 变量值

**命令格式**

```
show efm port <portlist> remote-mib <variable>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portlist | 端口列表 | 1-64 个字符串 |
| variable | 变量 | [autonegadminstate, phyadminstate] |


## 96.19. show efm remote-mib


**命令功能**

端口查看获取的远端设备全局MIB 变量值

**命令格式**

```
show efm remote-mib <variable>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| variable | 变量 | [fecability, fecmode] |


## 96.20. show efm status


**命令功能**

查看EFM 协议运行状态

**命令格式**

```
show efm status interface [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |


## 96.21. show efm summary


**命令功能**

查看EFM 概要信息

**命令格式**

```
show efm summary
```


**参数说明**

*无*


## 96.22. show efm statistics


**命令功能**

查看EFM 协议报文统计信息

**命令格式**

```
show efm statistics interface [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 合法端口号，例如：0/0/1 |


## 96.23. clear efm statistics


**命令功能**

清除EFM 协议报文统计信息

**命令格式**

```
clear efm statistics interface [eth <portId> [to eth <portId>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| portId | 端口号 | 合法端口号，例如：0/0/1 |


# 97. CFM

```
cfm md
```


**命令功能**

全局下创建或者删除维护域

**命令格式**

```
(no)cfm md <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 域ID | [1-4294967295] |

```
cfm md format type name level
```


**命令功能**

维护域下配置域名称以及等级

**命令格式**

```
cfm md format [none | <type> name <name>] level <level>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| type | 名称类型 | [dns-name, mac-uint,string] |
| name | 维护域名称 | 根据type 类型填写的字符串 |
| level | 维护域等级 | [0-7] |

```
cfm ma
```


**命令功能**

维护域下配置维护集

**命令格式**

```
(no)cfm ma <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护集名称 | [1-4294967295] |

```
cfm mep Id direction
```


**命令功能**

维护集下配置维护点方向以及相应端口

**命令格式**

```
cfm mep <Id> direction <direction> [primary-vlan <vid>] interface [ethernet <pId> |
channel-group <lagId>]
no cfm mep <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| direction | 维护点方向 | [up,down] |
| vid | VLAN ID | [1-4094] |
| pId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合端口ID | [1-16] |

```
cfm mep Id priority
```


**命令功能**

维护集下配置维护点优先级

**命令格式**

```
(no)cfm mep <Id> priority <priority>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| priority | 维护点优先级 | [0-7] |

```
cfm mep Id state [enable | disable]
```


**命令功能**

维护集下配置维护点管理状态

**命令格式**

```
cfm mep <Id> state [enable | disable]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |

```
cfm mep Id cc [enable | disable]
```


**命令功能**

维护集下配置维护点连续性检测

**命令格式**

```
cfm mep <Id> cc [enable | disable]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |

```
cfm mip
```


**命令功能**

维护集下配置中间点

**命令格式**

```
cfm mip <Id> interface [ethernet <pId> | channel-group <lagId>]
no cfm mip <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| pId | 端口号 | 堆叠号/槽口号/端口号，例如：0/0/1 |
| lagId | 聚合端口ID | [1-16] |

```
cfm rmep
```


**命令功能**

维护集下配置远端点

**命令格式**

```
(no)cfm rmep <Id> mep <Id>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |


## 97.10. cfm loopback


**命令功能**

维护集下配置链路跟踪功能

**命令格式**

```
cfm loopback mep <Id> [dst-mac <mac> | dst-mep <Id>] count <counts> data <content>
length <len> priority <priority>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| mac | MAC 地址 | xx:xx:xx:xx:xx:xx |
| counts | 报文个数 | [1-1024] |
| content | 报文内容 | 1-400 个字符 |
| len | 报文长度 | [1-1500] |
| priority | 报文优先级 | [0-7] |


## 97.11. cfm linktrace


**命令功能**

维护集下配置环回检测功能

**命令格式**

```
cfm linktrace mep <Id> [dst-mac <mac> | dst-mep <Id>] flag <flag> timeout [timeout] ttl
[ttl]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| mac | MAC 地址 | xx:xx:xx:xx:xx:xx |
| flag | MIP CCM | Database 标签 |
| [unuse-mpdb, use-mpdb] | timeout | 超时时间 |
| [3-60] | ttl | 生存时间值 |

[1-255]

## 97.12. cfm eth-2dm


**命令功能**

维护集下配置帧时延测量功能

**命令格式**

```
cfm eth-2dm mep <Id> [dst-mac <mac> | dst-mep <Id>] count <counts> interval <interval>
priority <priority> timeout <timeout>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| mac | MAC 地址 | xx:xx:xx:xx:xx:xx |
| counts | 测量次数 | [1-1024] |
| interval | 间隔时间 | [1-30] |
| priority | 报文优先级 | [0-7] |
| timeout | 超时时间 | [3-60] |


## 97.13. cfm eth-slm


**命令功能**

维护集下配置帧丢失率测量功能

**命令格式**

```
cfm eth-slm mep <Id> [dst-mac <mac> | dst-mep <Id>] count <counts> interval <interval>
priority <priority> timeout <timeout>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| Id | 维护点ID | [1-8191] |
| mac | MAC 地址 | xx:xx:xx:xx:xx:xx |
| counts | 测量次数 | [1-1024] |
| interval | 间隔时间 | [1-30] |
| priority | 报文优先级 | [0-7] |
| timeout | 超时时间 | [3-60] |


## 97.14. cfm cc


**命令功能**

维护集下配置连续性检测时间间隔

**命令格式**

```
cfm cc interval <interval>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| interval | 时间间隔 | [1,10,60,600] |


## 97.15. show cfm md


**命令功能**

查看维护域信息

**命令格式**

```
show cfm md [<mdId> [ma <maid>]]
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| mdId | 维护域ID | [1-4294967295] |
| maid | 维护集ID | [1-4294967295] |


## 97.16. show cfm ma


**命令功能**

查看维护集信息

**命令格式**

```
show cfm ma
```


**参数说明**

*无*


## 97.17. show cfm mp


**命令功能**

查看维护点信息

**命令格式**

```
show cfm mp <location>
```


**参数说明**

| 参数 | 参数说明 | 取值 |
|------|----------|------|
| location | 位置 | [local,remote] |


## 97.18. show cfm cc


**命令功能**

查看连续性检测统计数据

**命令格式**

```
show cfm cc [database]
```


**参数说明**

*无*


## 97.19. show cfm errors


**命令功能**

查看错误统计数据

**命令格式**

```
show cfm cc errors
```


**参数说明**

*无*

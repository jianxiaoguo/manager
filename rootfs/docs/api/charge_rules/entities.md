# 计费规则

## charge_rule 计费规则

name                |type   |comments
--------------------|-------|---------------------------------------------------
uuid                |string | id
name                |string | 规则名称
resource_type       |string | 计费项，`cpu/memory/volume/network`
price_unit          |string    | 单价单位，`cpu:1m,memory:1M1,volume:1Mi,network:1000bytes`
price               |float  | 单价
created             |date   | 创建时间
updated             |date   | 更新时间

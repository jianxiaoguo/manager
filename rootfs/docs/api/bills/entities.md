# 账单

## bills 账单
name                |type   |comments
--------------------|-------|---------------------------------------------------
uuid                |string | 流水号
owner_id            |string | 用户
cluster_id          |string | 集群id
app_id              |string | app id
resource_type       |string | 计费项，`cpu/memory/volume/network`
price_unit          |int    | 单价单位，`cpu:1m,memory:1M1,volume:1Mi,network:1000bytes`
price               |float  | 单价
quantity            |float  | 用量
total_price         |float  | 总价
detail              |json   | 账单详细
created             |date   | 创建时间
updated             |date   | 更新时间

### detail 账单详细
name                |type   |comments
--------------------|-------|---------------------------------------------------
resource_type       |string | 计费项，`cpu/memory/volume/network`
price_unit          |int    | 单价单位，`cpu:1m,memory:1M1,volume:1Mi,network:1000bytes`
price               |float  | 单价
quantity            |float  | 用量
total_price         |float  | 总价

# 账单

## bills 账单
name                |type   |comments
--------------------|-------|---------------------------------------------------
uuid                |string | 流水号
owner_id            |string | 用户
cluster_id          |string | 集群id
app_id              |string | app id
resource_type       |string | 计费项，`cpu/memory/volume/network`
price_unit          |string | 单价单位，`cpu:1m/day,memory:1M/day,volume:1M/day,network:1000bytes/hour`
price               |float  | 单价
quantity            |float  | 用量
start_time          |date   | 计费开始时间
end_time            |date   | 计费结束时间
total_price         |float  | 总价
created             |date   | 创建时间
updated             |date   | 更新时间

### detail 账单详细
name                |type   |comments
--------------------|-------|---------------------------------------------------
resource_type       |string | 计费项，`cpu/memory/volume/network`
price_unit          |string | 单价单位，`cpu:1m/day,memory:1M/day,volume:1M/day,network:1000bytes/hour`
price               |float  | 单价
quantity            |float  | 用量
total_price         |float  | 总价

# 计费

## ChargeRule 计费规则

name                |type   |comments
--------------------|-------|---------------------------------------------------
name                |string |规则名称
resource_type       |int    |资源类型，`1-cpu，2-mem，3-network(rx\tx), 4-volume, pod数`
calc_unit           |int    |计费单位，`元/nanocores，元/MiB` 

计费模式 
时长计费（月、年）
容量占用计费

## balance 余额

name                |type   |comments
--------------------|-------|---------------------------------------------------
account             |string |账户
balance             |int    |余额


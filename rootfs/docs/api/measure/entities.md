## Measure


## measure

### config limit
name              |type    |comments
------------------|--------|-----------------------
uuid              |string  | id
cluster_id        |string  | 集群id
app_id            |string  | app id
container_type    |string  | container type
cpu               |int     | m cores
memory            |int     | Mi
owner_id          |string  | 用户
timestamp         |string  | 时间戳
created           |date    | 创建时间
updated           |date    | 更新时间

### volume
name              |type    |comments
------------------|--------|-----------------------
uuid              |string  | id
cluster_id        |string  | 集群id
app_id            |string  | app id
name              |string  | container type
size              |int     | Mi
owner_id          |string  | 用户
timestamp         |float   | 时间戳
created           |date    | 创建时间
updated           |date    | 更新时间

### network
name              |type    |comments
------------------|--------|-----------------------
uuid              |string  | id
cluster_id        |string  | 集群id
app_id            |string  | app id
pod_name          |string  | pod_name
rx_bytes          |int     | bytes
tx_bytes          |int     | bytes
timestamp         |float   | 时间戳
created           |date    | 创建时间
updated           |date    | 更新时间

### instance
name              |type    |comments
------------------|--------|-----------------------
uuid              |string  | id
cluster_id        |string  | 集群id
app_id            |string  | app id
container_type    |string  | container type
container_count   |int     | replicas number
timestamp         |float   | 时间戳
created           |date    | 创建时间
updated           |date    | 更新时间

### resource
name              |type    |comments
------------------|--------|-----------------------
uuid              |string  | id
cluster_id        |string  | 集群id
app_id            |string  | app id
name              |string  | resource name
plan              |string  | resource plan
timestamp         |float   | 时间戳
created           |date    | 创建时间
updated           |date    | 更新时间

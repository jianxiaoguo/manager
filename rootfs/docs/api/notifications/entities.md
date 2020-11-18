# 消息

## Notifications

name        |type  |NN |comments
------------|------|---|---------------------
message_id  |string| T |
user_id     |string| T |
code        |int   | T |
sender_type |int   | T |
sender      |string| T |
body        |string| T |
created　　　|double| T |

## body
|name               |type      |comments  |
|-------------------|----------|----------|
|code               |int       |  消息code |


## UnReadCount

name     |type  |NN |comments
---------|------|---|---------------------
user_id  |string| T |
msg_count|int   | T |


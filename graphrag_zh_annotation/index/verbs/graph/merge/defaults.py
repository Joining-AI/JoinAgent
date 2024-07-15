# 导入一个叫做 BasicMergeOperation 的类型，它帮助我们处理合并操作
from .typing import BasicMergeOperation

# 这是微软公司的版权信息，告诉我们代码的归属和使用的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文件是用来定义一些默认值的，比如处理节点、边的操作和连接字符串时用的分隔符
"""A file containing DEFAULT_NODE_OPERATIONS, DEFAULT_EDGE_OPERATIONS and DEFAULT_CONCAT_SEPARATOR values definition."""

# 再次导入 BasicMergeOperation 类型，确保我们能正确使用它
from .typing import BasicMergeOperation

# 定义一个字典，叫 DEFAULT_NODE_OPERATIONS
# "*" 表示所有节点，默认操作是替换（Replace）
DEFAULT_NODE_OPERATIONS = {
    "*": {
        "operation": BasicMergeOperation.Replace,
    }
}

# 另一个字典，叫 DEFAULT_EDGE_OPERATIONS
# "*" 依然代表所有边，但这里还特别指定了 "weight" 的操作是求和（sum）
DEFAULT_EDGE_OPERATIONS = {
    "*": {
        "operation": BasicMergeOperation.Replace,
    },
    "weight": "sum",
}

# 定义一个变量，叫 DEFAULT_CONCAT_SEPARATOR
# 它是一个逗号（,），用于在合并字符串时作为分隔符
DEFAULT_CONCAT_SEPARATOR = ","


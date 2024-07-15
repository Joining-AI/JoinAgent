# 导入了一个叫做Protocol的东西，它帮助我们定义接口
from typing import Protocol

# 导入了pandas库，它用于处理数据，就像电子表格一样
import pandas as pd

# 这一段是版权声明，告诉我们这段代码是由微软公司在2024年写的
# 并且遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了下面的代码是干什么的
# "TableEmitter"协议，用于把表格发送到某个地方
"""

TableEmitter protocol for emitting tables to a destination.

"""

# 这里定义了一个协议类（Protocol），叫TableEmitter
class TableEmitter(Protocol):
    # 这个类也是关于发送表格的协议
    """TableEmitter协议，用于向目的地发送表格"""

    # 定义了一个异步方法（能等待的任务）叫做emit
    async def emit(self, name: str, data: pd.DataFrame) -> None:
        # 这个方法的作用是把一个叫做"name"的名字和一个pandas数据框（data）发送出去
        # 数据框就像是一个电子表格
        """将数据框发射（保存或发送）到存储中。"""


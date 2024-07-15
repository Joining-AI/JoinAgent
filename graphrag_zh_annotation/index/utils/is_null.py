# 导入math模块，这个模块里有很多数学相关的函数
import math
# 导入typing模块中的Any类型，它代表任何类型的值
from typing import Any

# 这是一个版权声明，表示这段代码是微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个文档字符串描述了一个叫做is_null的工具函数
"""定义is_null实用工具函数。"""

# 再次导入math模块和Any类型，确保它们在函数内部也可以使用
import math
from typing import Any


# 定义一个名为is_null的函数，它接收一个参数value，返回值类型是布尔型（True或False）
def is_null(value: Any) -> bool:
    # 定义一个内部函数is_none，检查value是否是None（没有值）
    def is_none() -> bool:
        # 如果value等于None，返回True，否则返回False
        return value is None

    # 定义另一个内部函数is_nan，检查value是否是"不是数字"（Not a Number）
    def is_nan() -> bool:
        # 如果value是浮点数并且它的值是NaN（不是数字），返回True，否则返回False
        return isinstance(value, float) and math.isnan(value)

    # 检查value是否是None或者是不是数字（NaN），如果满足任一条件，返回True，否则返回False
    return is_none() or is_nan()


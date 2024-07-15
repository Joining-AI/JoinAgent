# 导入必要的库，让程序能处理数据和类型检查
from typing import cast
import pandas as pd  # 用于数据操作的库
from datashaper import TableContainer, VerbInput, verb  # 数据操作工具库
from .typing import Replacement  # 自定义的替换类型

# 这是微软公司的版权信息，告诉我们这个代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含replace和_apply_replacements方法

# 类型转换函数，确保数据类型正确
from typing import cast

# 导入pandas库，用于处理表格数据
import pandas as pd

# 从datashaper库中导入TableContainer、VerbInput和verb装饰器
from datashaper import TableContainer, VerbInput, verb

# 导入自定义的替换类型
from .typing import Replacement


# 使用verb装饰器，创建一个名为"text_replace"的操作
@verb(name="text_replace")
def text_replace(
    input: VerbInput,  # 输入的数据
    column: str,  # 需要替换的文本所在的列名
    to: str,  # 替换后文本保存的新列名
    replacements: list[dict[str, str]],  # 一系列替换规则，每个规则包含要找的模式和替换后的文本
    **_kwargs: dict,  # 其他可能的参数，这里我们忽略它们
) -> TableContainer:  # 返回处理后的数据容器
    """
    用一组替换规则替换文本中的内容。

    如何使用：


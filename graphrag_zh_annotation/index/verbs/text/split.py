# 导入必要的库，它们帮助我们处理数据和定义函数
from typing import cast  # 类型转换工具
import pandas as pd  # 数据处理库
from datashaper import TableContainer, VerbInput, verb  # 数据操作库

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含一个叫做 "text_split" 的方法定义

# 使用 typing 库中的 cast 工具
from typing import cast

# 引入 pandas 库来处理数据
import pandas as pd

# 从 datashaper 库中导入 TableContainer, VerbInput 和 verb 函数
from datashaper import TableContainer, VerbInput, verb


# 定义一个名为 "text_split" 的函数，它是一个数据操作（verb）
@verb(name="text_split")
def text_split(
    # 输入参数，表示要处理的数据
    input: VerbInput,
    # 指定要分割的列的名称
    column: str,
    # 输出新列的名称
    to: str,
    # 分隔符，默认是逗号
    separator: str = ",",
    # 其他可能的参数，但在这里我们忽略它们
    **_kwargs: dict,
) -> TableContainer:
    """
    根据分隔符将文本分割成字符串列表。这个函数会在数据中创建一个新的列，其中包含分割后的字符串列表。

    **使用方法**：


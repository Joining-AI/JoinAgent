# 导入必要的库
from typing import cast  # 类型转换工具
import pandas as pd  # 数据处理库
from datashaper import TableContainer, VerbInput, verb  # 数据操作库
from graphrag.index.utils import gen_md5_hash  # 生成MD5哈希的函数

# 代码版权信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含genid方法

# 从typing导入cast
from typing import cast

# 导入pandas库
import pandas as pd

# 从datashaper库导入TableContainer, VerbInput和verb装饰器
from datashaper import TableContainer, VerbInput, verb

# 从graphrag.index.utils导入gen_md5_hash函数
from graphrag.index.utils import gen_md5_hash


# 使用verb装饰器定义genid函数，用于生成唯一ID
@verb(name="genid")
def genid(
    # 输入参数
    input: VerbInput,  # 输入的数据
    to: str,  # 输出ID的列名
    method: str = "md5_hash",  # 生成ID的方法，默认为"md5_hash"
    hash: list[str] = [],  # 用于MD5哈希的列名列表，默认为空
    **_kwargs: dict,  # 其他关键字参数，这里不使用
) -> TableContainer:  # 返回一个包含生成ID后的数据的TableContainer对象

    """
    为表格数据的每一行生成一个唯一的ID。

    **用法示例**：
    - JSON格式:


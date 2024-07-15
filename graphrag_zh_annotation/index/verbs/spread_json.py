# 导入logging模块，用于记录程序运行中的信息和错误
import logging

# 导入pandas库，它用于处理表格数据
import pandas as pd

# 从datashaper库中导入TableContainer、VerbInput和verb装饰器
from datashaper import TableContainer, VerbInput, verb

# 从graphrag.index.utils库中导入is_null函数，检查值是否为空
from graphrag.index.utils import is_null

# 这是微软公司的版权信息和许可声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含一个名为spread_json的方法

# 导入logging模块，用于处理日志信息
import logging

# 导入pandas库，它用于处理表格数据
import pandas as pd

# 从datashaper库中导入类和装饰器
from datashaper import TableContainer, VerbInput, verb

# 从graphrag.index.utils库中导入is_null函数
from graphrag.index.utils import is_null

# 默认要复制的列名列表
DEFAULT_COPY = ["level"]

# 使用verb装饰器定义一个名为'spread_json'的函数，用于展开JSON格式的数据
@verb(name="spread_json")
def spread_json(
    # 输入参数，类型为VerbInput
    input: VerbInput,
    # 要展开的列名
    column: str,
    # 可选的复制列名列表，默认为None
    copy: list[str] | None = None,
    # 其他关键字参数，这里忽略
    **_kwargs: dict,
) -> TableContainer:
    """
    将包含元组的列展开成多个单独的列。

    例如：
    原始数据：
    id|json|b
    1|{"x":5,"y":6}|b

    展开后：
    id|x|y|b
    --------
    1|5|6|b
    """

    # 如果copy参数未设置，则使用默认值
    if copy is None:
        copy = DEFAULT_COPY

    # 获取输入数据
    data = input.get_input()

    # 创建一个空列表，用于存储处理后的行
    results = []

    # 遍历数据框的每一行
    for _, row in data.iterrows():
        # 尝试进行展开操作
        try:
            # 从原始行中复制指定列到新字典
            cleaned_row = {col: row[col] for col in copy}

            # 如果json列有值，就将其转换为字典，否则设为空字典
            rest_row = row[column] if row[column] is not None else {}
            if is_null(rest_row):
                rest_row = {}

            # 合并复制的列和展开的json列
            results.append({**cleaned_row, **rest_row})  # type: ignore
        # 捕获并记录异常，然后重新抛出异常
        except Exception:
            logging.exception("处理行时出错：%s", row)
            raise

    # 创建一个新的数据框，使用原数据的索引
    data = pd.DataFrame(results, index=data.index)

    # 返回一个新的TableContainer对象，包含展开后的数据
    return TableContainer(table=data)


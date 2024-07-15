# 导入必要的工具模块
from typing import cast
import pandas as pd  # 用于处理数据的库
from datashaper import TableContainer, VerbInput, verb  # 用于操作数据的库

# 这两行是版权信息，表示代码由微软公司编写，遵循MIT许可证

# 定义一个名为"concat_override"的函数
@verb(name="concat_override")  # 这是一个特殊标记，告诉datashaper这个函数是用来处理数据的
def concat(  # 这个函数叫做concat，用于合并数据
    input: VerbInput,  # input参数是一个特殊类型的数据输入对象
    columnwise: bool = False,  # columnwise参数是一个布尔值，默认为False，决定是否按列合并
    **_kwargs: dict,  # 其他任意参数，这里用不到，所以用**_kwargs接收并忽略
) -> TableContainer:  # 函数返回一个TableContainer对象，里面包含合并后的数据

    # 将输入的VerbInput转换为pandas的DataFrame，这样可以方便地处理数据
    input_table = cast(pd.DataFrame, input.get_input())

    # 获取除主要输入外的其他数据，也转换为DataFrame列表
    others = cast(list[pd.DataFrame], input.get_others())

    # 如果columnwise为True，则按列合并数据
    if columnwise:
        output = pd.concat([input_table, *others], axis=1)  # 沿着列（水平）合并

    # 否则，按行合并数据，并忽略原有的索引
    else:
        output = pd.concat([input_table, *others], ignore_index=True)  # 沿着行（垂直）合并

    # 最后，将合并后的数据放入TableContainer中并返回
    return TableContainer(table=output)


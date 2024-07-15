# 这段代码是用来将数据框（DataFrame）中的一列包含元组的数据拆分成多列的

from typing import cast  # 引入cast函数，用于类型转换
import pandas as pd  # 引入pandas库，用于处理数据
from datashaper import TableContainer, VerbInput, verb  # 引入datashaper库中的几个类和装饰器

# 版权声明，这个代码是微软公司的，遵循MIT许可证

# 定义一个模块，里面有一个方法unzip
# from typing import cast 不再重复注释
# import pandas as pd 不再重复注释
# from datashaper import TableContainer, VerbInput, verb 不再重复注释


# 这是一个待办事项，检查是否已经有了类似的功能
# 这个函数会把一列数据，可能是元组形式，变成多列
@verb(name="unzip")  # 使用verb装饰器，给函数命名"unzip"
def unzip(  # 定义unzip函数
    input: VerbInput,  # 输入参数，是一个VerbInput对象
    column: str,  # 指定要拆分的列名
    to: list[str],  # 指定拆分后新列的名字列表
    **_kwargs: dict  # 其他可能的参数，这里不使用
) -> TableContainer:  # 函数返回值是一个TableContainer对象
    """将数据框中包含元组的列拆分为多个单独的列."""
    # 将输入的VerbInput对象转换为pandas DataFrame
    table = cast(pd.DataFrame, input.get_input())

    # 创建一个新的DataFrame，将原数据框中指定列的元组拆分出来
    table[to] = pd.DataFrame(table[column].tolist(), index=table.index)

    # 返回一个新的TableContainer对象，包含拆分后的数据框
    return TableContainer(table=table)


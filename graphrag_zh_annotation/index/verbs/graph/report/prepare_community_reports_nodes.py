# 导入必要的工具库，它们帮助我们处理数据和定义函数
from typing import cast  # 类型转换工具
import pandas as pd  # 数据处理库
from datashaper import TableContainer, VerbInput, verb  # 数据操作库

# 从另一个文件导入一些预定义的常量，这些常量代表节点的属性
from graphrag.index.graph.extractors.community_reports.schemas import (
    NODE_DEGREE,  # 节点度数
    NODE_DESCRIPTION,  # 节点描述
    NODE_DETAILS,  # 节点详细信息
    NODE_ID,  # 节点ID
    NODE_NAME,  # 节点名称
)

# 这是微软公司的版权信息，告诉我们这个代码不能随便用，需要遵守MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了一些方法的定义，比如创建图、获取节点属性等

# 使用类型注解工具cast
from typing import cast

# 引入pandas库，用于数据处理
import pandas as pd

# 引入datashaper库，用于数据操作
from datashaper import TableContainer, VerbInput, verb

# 从graphrag库中导入节点属性的常量
from graphrag.index.graph.extractors.community_reports.schemas import (
    NODE_DEGREE,
    NODE_DESCRIPTION,
    NODE_DETAILS,
    NODE_ID,
    NODE_NAME,
)

# 定义一个空字符串，表示没有描述
_MISSING_DESCRIPTION = "No Description"

# 定义一个函数，名字叫prepare_community_reports_nodes，它接受一些输入并返回处理后的数据
@verb(name="prepare_community_reports_nodes")  # 这是给函数添加一个标签，方便其他地方调用
def prepare_community_reports_nodes(
    input: VerbInput,  # 输入的数据
    to: str = NODE_DETAILS,  # 指定合并后新列的名字，默认是NODE_DETAILS
    id_column: str = NODE_ID,  # 节点ID列的名字，默认是NODE_ID
    name_column: str = NODE_NAME,  # 节点名称列的名字，默认是NODE_NAME
    description_column: str = NODE_DESCRIPTION,  # 节点描述列的名字，默认是NODE_DESCRIPTION
    degree_column: str = NODE_DEGREE,  # 节点度数列的名字，默认是NODE_DEGREE
    **_kwargs,  # 其他任意参数
) -> TableContainer:  # 函数返回的数据类型
    # 将输入的数据转成DataFrame（一种表格形式的数据结构）
    node_df = cast(pd.DataFrame, input.get_input())

    # 如果描述列有缺失值，就用"No Description"替换
    node_df = node_df.fillna(value={description_column: _MISSING_DESCRIPTION})

    # 创建一个新的列，将四个列的值合并成一个字典
    node_df[to] = node_df.apply(
        # 对每一行数据应用以下操作
        lambda x: {  # 创建一个字典
            id_column: x[id_column],  # 字典键是列名，值是对应行的值
            name_column: x[name_column],
            description_column: x[description_column],
            degree_column: x[degree_column],
        },
        axis=1,  # 按照行进行操作
    )

    # 最后，将处理后的DataFrame封装成TableContainer并返回
    return TableContainer(table=node_df)


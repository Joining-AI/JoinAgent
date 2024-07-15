# 导入必要的库，让程序可以处理数据
from typing import cast
import pandas as pd  # 用于数据操作的库
from datashaper import TableContainer, VerbInput, verb  # 数据处理相关的库

# 从graphrag库中导入一些常量，它们是边缘属性的名称
from graphrag.index.graph.extractors.community_reports.schemas import (
    EDGE_DEGREE,
    EDGE_DESCRIPTION,
    EDGE_DETAILS,
    EDGE_ID,
    EDGE_SOURCE,
    EDGE_TARGET,
)

# 这是微软公司的版权信息，告诉我们这个代码的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了几个方法的定义，用于处理图的数据

# 使用cast函数来确保类型正确，这是编程中的一个辅助工具
from typing import cast

# 导入pandas库，它用于处理数据
import pandas as pd

# 导入datashaper库中的TableContainer, VerbInput和verb，这些是用来处理数据的工具
from datashaper import TableContainer, VerbInput, verb

# 从graphrag库中导入边缘属性的常量
from graphrag.index.graph.extractors.community_reports.schemas import (
    EDGE_DEGREE,
    EDGE_DESCRIPTION,
    EDGE_DETAILS,
    EDGE_ID,
    EDGE_SOURCE,
    EDGE_TARGET,
)

# 定义一个没有描述时的默认值
_MISSING_DESCRIPTION = "No Description"

# 定义一个名为"prepare_community_reports_edges"的函数，它会处理边的信息
@verb(name="prepare_community_reports_edges")
def prepare_community_reports_edges(
    # 输入的数据
    input: VerbInput,
    # 输出的目标列名，默认为EDGE_DETAILS
    to: str = EDGE_DETAILS,
    # 边的ID列名，默认为EDGE_ID
    id_column: str = EDGE_ID,
    # 边的起点列名，默认为EDGE_SOURCE
    source_column: str = EDGE_SOURCE,
    # 边的终点列名，默认为EDGE_TARGET
    target_column: str = EDGE_TARGET,
    # 描述列名，默认为EDGE_DESCRIPTION
    description_column: str = EDGE_DESCRIPTION,
    # 度数（连接数量）列名，默认为EDGE_DEGREE
    degree_column: str = EDGE_DEGREE,
    # 其他可能的参数，但在这里我们忽略它们
    **_kwargs,
) -> TableContainer:
    # 获取输入数据，如果description_column有缺失值，用_NO_DESCRIPTION填充
    edge_df: pd.DataFrame = cast(pd.DataFrame, input.get_input()).fillna(
        value={description_column: _MISSING_DESCRIPTION}
    )
    # 创建一个新的列，将每条边的信息打包成字典
    edge_df[to] = edge_df.apply(
        # 对每行数据应用以下操作
        lambda x: {
            # 将列名和对应的值放入字典
            id_column: x[id_column],
            source_column: x[source_column],
            target_column: x[target_column],
            description_column: x[description_column],
            degree_column: x[degree_column],
        },
        # 按照每行（axis=1）操作
        axis=1,
    )
    # 返回处理后的数据
    return TableContainer(table=edge_df)


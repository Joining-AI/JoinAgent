# 导入logging模块，它用于在程序中记录信息和错误
import logging

# 使用typing模块中的cast函数，它帮助确保数据类型正确
from typing import cast

# 导入pandas库，它用于处理数据，比如表格
import pandas as pd

# 导入datashaper库，它帮助我们操作和描述数据
from datashaper import TableContainer, VerbInput, verb

# 导入graphrag库中关于社区报告的模式定义
import graphrag.index.graph.extractors.community_reports.schemas as schemas

# 这一行是版权声明，告诉我们这个代码由微软公司编写，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了一些方法的定义，比如创建图、获取节点属性、获取边属性和获取属性列映射
"""A module containing create_graph, _get_node_attributes, _get_edge_attributes and _get_attribute_column_mapping methods definition."""

# 初始化日志记录器，用于记录程序运行时的信息
log = logging.getLogger(__name__)

# 定义一个名为"restore_community_hierarchy"的函数，它是一个verb，可能用于处理数据或图形
@verb(name="restore_community_hierarchy")

# 定义一个名为 restore_community_hierarchy 的函数，它接受一些参数
def restore_community_hierarchy(
    输入: VerbInput,  # 这个参数用来获取数据
    名称列: str = schemas.NODE_NAME,  # 默认的列名，用于存储节点名称
    社区列: str = schemas.NODE_COMMUNITY,  # 默认的列名，用于存储节点所属社区
    级别列: str = schemas.NODE_LEVEL,  # 默认的列名，用于存储节点级别
    **_kwargs,  # 其他任意参数，但在这里我们不需要它们
) -> TableContainer:  # 函数返回一个 TableContainer 对象

    """这个函数从节点数据中恢复社区层级结构。"""

    # 将输入数据转换成 DataFrame（一种表格数据结构）
    节点数据框: pd.DataFrame = cast(pd.DataFrame, 输入.get_input())

    # 按照社区列和级别列对数据框进行分组，然后将名称列中的值聚合为列表
    社区层级数据框 = (
        节点数据框.groupby([社区列, 级别列])
        .agg({名称列: list})  # 对每个组，将名称列转为列表
        .reset_index()  # 重置索引以便处理
    )

    # 创建一个字典，用于存储不同级别的社区及其对应的名称
    社区级别字典 = {}

    # 遍历社区层级数据框的每一行
    for _, 行 in 社区层级数据框.iterrows():
        当前级别 = 行[级别列]
        名称 = 行[名称列]
        社区 = 行[社区列]

        # 如果当前级别在字典中不存在，就创建一个新的字典项
        if 社区级别字典.get(当前级别) is None:
            社区级别字典[当前级别] = {}
        # 将社区和对应的名称存入字典
        社区级别字典[当前级别][社区] = 名称

    # 获取所有级别的列表，并按升序排序
    级别列表 = sorted(社区级别字典.keys())

    # 初始化一个空列表，用于存储社区层级关系
    社区层级结构 = []

    # 遍历级别列表，从低到高（不包括最高级）
    for idx in range(len(级别列表) - 1):
        当前级别 = 级别列表[idx]
        日志.debug("当前级别: %s", 当前级别)
        下一级别 = 级别列表[idx + 1]

        # 获取当前级别和下一级别的社区字典
        当前级别社区 = 社区级别字典[当前级别]
        下一级别社区 = 社区级别字典[下一级别]

        # 输出当前级别的社区数量
        日志.debug(
            "当前级别 %s 的社区数量: %s",
            当前级别,
            len(当前级别社区),
        )

        # 遍历当前级别的每个社区
        for 当前社区 in 当前级别社区:
            当前实体 = 当前级别社区[当前社区]

            # 在下一级别的社区中查找子社区
            已找到实体数 = 0
            for 下一级别社区名 in 下一级别社区:
                下一级别实体 = 下一级别社区[下一级别社区名]
                # 如果下一级别的实体集合是当前级别实体的子集
                if set(下一级别实体).issubset(set(当前实体)):
                    # 将层级关系保存到社区层级结构列表
                    社区层级结构.append({
                        社区列: 当前社区,
                        schemas.COMMUNITY_LEVEL: 当前级别,
                        schemas.SUB_COMMUNITY: 下一级别社区名,
                        schemas.SUB_COMMUNITY_SIZE: len(下一级别实体),
                    })

                    # 增加已找到的实体数
                    已找到实体数 += len(下一级别实体)
                    # 如果已经找到所有当前级别的实体，就跳出循环
                    if 已找到实体数 == len(当前实体):
                        break

    # 将社区层级结构列表转换成 DataFrame 并返回
    return TableContainer(table=pd.DataFrame(社区层级结构))


# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，用来创建数据模型
from pydantic import BaseModel, Field

# 导入一些默认的配置参数，它们来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这段文字是版权信息，告诉我们这个代码是由微软公司写的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了接下来的代码是关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 创建一个新的类ClusterGraphConfig，它继承自BaseModel
class ClusterGraphConfig(BaseModel):
    # 这个类是用来定义图聚类的配置

    # 定义一个变量max_cluster_size，它是一个整数
    # Field()是用来添加描述和默认值的
    max_cluster_size: int = Field(
        description="能使用的最大聚类大小。", default=defs.MAX_CLUSTER_SIZE
    )
    # 定义一个变量strategy，它可以是字典或者None
    strategy: dict | None = Field(
        description="要使用的聚类策略。", default=None
    )

    # 定义一个方法，返回确定的聚类策略
    def resolved_strategy(self) -> dict:
        # 从graphrag.index.verbs.graph.clustering导入一个类型
        from graphrag.index.verbs.graph.clustering import GraphCommunityStrategyType

        # 如果strategy有值，就返回它；否则，返回一个新的字典
        return self.strategy or {
            "type": GraphCommunityStrategyType.leiden,  # 使用Leiden算法作为默认策略
            "max_cluster_size": self.max_cluster_size,  # 策略中的最大聚类大小与上面的变量相同
        }


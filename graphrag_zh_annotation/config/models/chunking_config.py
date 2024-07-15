# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，用于创建数据模型
from pydantic import BaseModel, Field

# 导入默认配置的模块，它在graphrag.config包下的defaults文件里
import graphrag.config.defaults as defs

# 这是微软公司的版权声明和许可信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为"Parameterization settings for the default configuration."的文档字符串

# 创建一个类，叫做ChunkingConfig，它是BaseModel的子类，用于存储关于分块配置的信息
class ChunkingConfig(BaseModel):

    # 定义一个属性size，它是整数类型，默认值从defs模块中的CHUNK_SIZE获取，描述是分块大小
    size: int = Field(description="要使用的分块大小。", default=defs.CHUNK_SIZE)

    # 定义一个属性overlap，也是整数类型，默认值从defs模块中的CHUNK_OVERLAP获取，描述是分块重叠部分
    overlap: int = Field(description="要使用的分块重叠。", default=defs.CHUNK_OVERLAP)

    # 定义一个属性group_by_columns，是一个包含字符串的列表，默认值从defs模块中的CHUNK_GROUP_BY_COLUMNS获取，描述是按哪些列进行分块
    group_by_columns: list[str] = Field(
        description="要使用的按列分块。", default=defs.CHUNK_GROUP_BY_COLUMNS
    )

    # 定义一个属性strategy，可以是字典或None，描述是分块策略，如果设置了就覆盖默认的分词策略，初始默认值是None
    strategy: dict | None = Field(
        description="要使用的分块策略，可覆盖默认的分词策略。",
        default=None,
    )

    # 定义一个方法，返回解决后的分块策略
    def resolved_strategy(self) -> dict:
        # 引入ChunkStrategyType枚举，它在graphrag.index.verbs.text.chunk模块中
        from graphrag.index.verbs.text.chunk import ChunkStrategyType

        # 如果strategy有值，就直接返回；否则，创建一个默认的基于tokens的策略
        return self.strategy or {
            "type": ChunkStrategyType.tokens,
            "chunk_size": self.size,
            "chunk_overlap": self.overlap,
            "group_by_columns": self.group_by_columns,
        }


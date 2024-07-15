# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们创建数据模型
from pydantic import BaseModel, Field

# 导入一些默认设置，它们来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这段文字是版权信息，表示代码由微软公司拥有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为GlobalSearchConfig的数据模型类
class GlobalSearchConfig(BaseModel):

    # 这个类用于描述缓存的默认配置

    # temperature属性：可以是浮点数或None，用于生成令牌时的温度值
    temperature: float | None = Field(
        description="生成令牌时用到的温度值。",
        default=defs.LLM_TEMPERATURE,
    )

    # top_p属性：可以是浮点数或None，用于生成令牌时的top-p值
    top_p: float | None = Field(
        description="生成令牌时用到的top-p值。",
        default=defs.LLM_TOP_P,
    )

    # n属性：可以是整数或None，用于生成的完成数量
    n: int | None = Field(
        description="要生成的完成数量。",
        default=defs.LLM_N,
    )

    # max_tokens属性：整数，最大上下文大小以令牌计
    max_tokens: int = Field(
        description="最大的上下文大小（以令牌计算）。",
        default=defs.GLOBAL_SEARCH_MAX_TOKENS,
    )

    # data_max_tokens属性：整数，数据llm的最大令牌数
    data_max_tokens: int = Field(
        description="数据llm的最大令牌数。",
        default=defs.GLOBAL_SEARCH_DATA_MAX_TOKENS,
    )

    # map_max_tokens属性：整数，映射llm的最大令牌数
    map_max_tokens: int = Field(
        description="映射llm的最大令牌数。",
        default=defs.GLOBAL_SEARCH_MAP_MAX_TOKENS,
    )

    # reduce_max_tokens属性：整数，减少llm的最大令牌数
    reduce_max_tokens: int = Field(
        description="减少llm的最大令牌数。",
        default=defs.GLOBAL_SEARCH_REDUCE_MAX_TOKENS,
    )

    # concurrency属性：整数，并发请求的数量
    concurrency: int = Field(
        description="同时进行的请求数量。",
        default=defs.GLOBAL_SEARCH_CONCURRENCY,
    )


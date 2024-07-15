# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们定义和验证数据模型
from pydantic import BaseModel, Field

# 导入一些默认设置，这些设置来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这段代码的版权信息，表示2024年微软公司的作品，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个类，叫LocalSearchConfig，它是BaseModel的子类，用于存储配置信息
class LocalSearchConfig(BaseModel):

    # 这个类里有一个属性，叫做"text_unit_prop"，它是个浮点数
    # 有描述：文本单位比例，默认值从defs模块导入
    text_unit_prop: float = Field(description="文本单位比例。", default=defs.LOCAL_SEARCH_TEXT_UNIT_PROP)

    # 另一个属性，"community_prop"，也是浮点数
    # 有描述：社区比例，默认值同样从defs模块导入
    community_prop: float = Field(description="社区比例。", default=defs.LOCAL_SEARCH_COMMUNITY_PROP)

    # "conversation_history_max_turns"是整数，描述是对话历史的最大轮数
    # 默认值来自defs模块
    conversation_history_max_turns: int = Field(description="对话历史最大轮数。", default=defs.LOCAL_SEARCH_CONVERSATION_HISTORY_MAX_TURNS)

    # "top_k_entities"，整数，表示顶级映射实体的数量
    # 默认值从defs模块获取
    top_k_entities: int = Field(description="顶级映射实体数量。", default=defs.LOCAL_SEARCH_TOP_K_MAPPED_ENTITIES)

    # "top_k_relationships"，整数，表示顶级映射关系的数量
    # 默认值同样来自defs模块
    top_k_relationships: int = Field(description="顶级映射关系数量。", default=defs.LOCAL_SEARCH_TOP_K_RELATIONSHIPS)

    # "max_tokens"，整数，描述最大令牌数
    # 默认值从defs模块导入
    max_tokens: int = Field(description="最大令牌数。", default=defs.LOCAL_SEARCH_MAX_TOKENS)

    # "llm_max_tokens"，整数，表示LLM（可能是一种语言模型）的最大令牌数
    # 默认值从defs模块获取
    llm_max_tokens: int = Field(description="LLM最大令牌数。", default=defs.LOCAL_SEARCH_LLM_MAX_TOKENS)


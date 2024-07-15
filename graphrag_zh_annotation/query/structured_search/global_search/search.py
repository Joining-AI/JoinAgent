# 导入必要的库，让Python可以做更多的事情
import asyncio  # 异步编程工具
import json  # 处理JSON格式数据
import logging  # 记录程序运行日志
import time  # 处理时间
from dataclasses import dataclass  # 定义数据类
from typing import Any  # 定义类型提示，用于任何类型

import pandas as pd  # 数据分析库
import tiktoken  # 一个可能的授权或令牌处理库
from graphrag.index.utils.json import clean_up_json  # 清理JSON数据的函数
from graphrag.query.context_builder.builders import GlobalContextBuilder  # 创建全局上下文的类
from graphrag.query.context_builder.conversation_history import ConversationHistory  # 对话历史记录类
from graphrag.query.llm.base import BaseLLM  # 基础语言模型类
from graphrag.query.llm.text_utils import num_tokens  # 计算文本中单词数的函数
from graphrag.query.structured_search.base import BaseSearch, SearchResult  # 基础搜索类和搜索结果类
from graphrag.query.structured_search.global_search.callbacks import GlobalSearchLLMCallback  # 全局搜索的语言模型回调类
from graphrag.query.structured_search.global_search.map_system_prompt import MAP_SYSTEM_PROMPT  # 映射系统提示的常量
from graphrag.query.structured_search.global_search.reduce_system_prompt import (
    GENERAL_KNOWLEDGE_INSTRUCTION,  # 通用知识指令
    NO_DATA_ANSWER,  # 没有数据的答案
    REDUCE_SYSTEM_PROMPT,  # 减少系统提示的常量
)

# 这段代码是微软公司写的，用的是MIT许可证
# 它实现了一个叫做GlobalSearch的功能

# 导入需要的库
import asyncio  # 异步编程工具
import json  # 处理JSON数据
import logging  # 记录日志
import time  # 处理时间
from dataclasses import dataclass  # 创建数据类的工具
from typing import Any  # 定义类型提示

import pandas as pd  # 数据处理库
import tiktoken  # 可能是一个特定的令牌库
from graphrag.index.utils.json import clean_up_json  # 清理JSON数据的函数
from graphrag.query.context_builder.builders import GlobalContextBuilder  # 构建全局上下文的类
from graphrag.query.context_builder.conversation_history import ConversationHistory  # 对话历史类
from graphrag.query.llm.base import BaseLLM  # 基础语言模型类
from graphrag.query.llm.text_utils import num_tokens  # 计算文本中单词数量的函数
from graphrag.query.structured_search.base import BaseSearch, SearchResult  # 基础搜索和搜索结果类
from graphrag.query.structured_search.global_search.callbacks import GlobalSearchLLMCallback  # 全局搜索回调函数
from graphrag.query.structured_search.global_search.map_system_prompt import MAP_SYSTEM_PROMPT  # 映射系统提示
from graphrag.query.structured_search.global_search.reduce_system_prompt import (
    GENERAL_KNOWLEDGE_INSTRUCTION,  # 通用知识指令
    NO_DATA_ANSWER,  # 没有数据的答案
    REDUCE_SYSTEM_PROMPT,  # 减少系统提示
)

# 定义默认的映射语言模型参数
DEFAULT_MAP_LLM_PARAMS = {
    "max_tokens": 1000,  # 最大单词数
    "temperature": 0.0,  # 温度参数，用于生成多样性的回答，默认为无多样性
}

# 定义默认的减少语言模型参数
DEFAULT_REDUCE_LLM_PARAMS = {
    "max_tokens": 2000,  # 最大单词数
    "temperature": 0.0,  # 温度参数，用于生成多样性的回答，默认为无多样性
}

# 初始化日志记录器
log = logging.getLogger(__name__)

# 定义一个数据类，表示全局搜索的结果
@dataclass
class GlobalSearchResult(SearchResult):
    # 继承自SearchResult类
    map_responses: list[SearchResult]  # 映射阶段的搜索结果列表
    reduce_context_data: str | list[pd.DataFrame] | dict[str, pd.DataFrame]  # 减少阶段的数据，可以是字符串、DataFrame列表或字典
    reduce_context_text: str | list[str] | dict[str, str]  # 减少阶段的文本，可以是字符串、字符串列表或字典




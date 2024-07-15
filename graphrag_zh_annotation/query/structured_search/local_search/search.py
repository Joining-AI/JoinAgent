# 导入日志模块，用于记录程序运行情况
import logging

# 导入时间模块，用于获取当前时间
import time

# 从typing模块导入Any类型，表示可以是任何类型的数据
from typing import Any

# 导入tiktoken模块，可能是一个用于处理特定令牌的库
import tiktoken

# 从graphrag的查询上下文构建器模块中导入本地上下文构建器
from graphrag.query.context_builder.builders import LocalContextBuilder

# 从对话历史模块中导入ConversationHistory类
from graphrag.query.context_builder.conversation_history import ConversationHistory

# 从基础语言模型模块中导入BaseLLM和BaseLLMCallback基类
from graphrag.query.llm.base import BaseLLM, BaseLLMCallback

# 从文本工具模块中导入num_tokens函数，用于计算文本中的令牌数
from graphrag.query.llm.text_utils import num_tokens

# 从结构化搜索的基础模块中导入BaseSearch和SearchResult类
from graphrag.query.structured_search.base import BaseSearch, SearchResult

# 从本地搜索的系统提示模块中导入LOCAL_SEARCH_SYSTEM_PROMPT常量
from graphrag.query.structured_search.local_search.system_prompt import LOCAL_SEARCH_SYSTEM_PROMPT

# 版权声明（2024年微软公司）
# 使用MIT许可证授权

# 定义一个名为"LocalSearch"的实现
# （这部分代码被注释掉了，所以不会被执行）

# 导入日志模块并设置日志记录器，名字为当前模块名
log = logging.getLogger(__name__)

# 定义默认的语言模型参数字典，包括最大令牌数和温度参数
DEFAULT_LLM_PARAMS = {
    "max_tokens": 1500,  # 最大允许的令牌数
    "temperature": 0.0,  # 温度参数，用于控制生成结果的随机性，0.0表示最确定的结果
}




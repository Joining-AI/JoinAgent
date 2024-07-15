# 导入基础抽象类和方法
from abc import ABC, abstractmethod  # 引入抽象基类和抽象方法，用于定义接口

# 导入数据处理库
import pandas as pd  # 引入Pandas库，用于处理表格数据

# 从graphrag库的查询上下文构建模块导入对话历史类
from graphrag.query.context_builder.conversation_history import ConversationHistory

# 版权信息
# Copyright (c) 2024 Microsoft Corporation.  # 表示代码版权属于微软公司
# Licensed under the MIT License  # 表示代码遵循MIT许可证

# 定义全局搜索上下文构建器的基类
class GlobalContextBuilder(ABC):
    """这是一个用于创建全局搜索上下文的基础类。"""

    # 定义一个抽象方法，需要子类实现
    @abstractmethod
    def build_context(
        self, conversation_history: ConversationHistory | None = None, **kwargs
    ) -> tuple[str | list[str], dict[str, pd.DataFrame]]:
        """构建全局搜索模式下的上下文。返回一个字符串或字符串列表，以及一个键为字符串、值为Pandas DataFrame的字典。"""


# 定义局部搜索上下文构建器的基类
class LocalContextBuilder(ABC):
    """这是一个用于创建局部搜索上下文的基础类。"""

    # 定义一个抽象方法，需要子类实现
    @abstractmethod
    def build_context(
        self,
        query: str,  # 接收一个查询字符串作为参数
        conversation_history: ConversationHistory | None = None,
        **kwargs,
    ) -> tuple[str | list[str], dict[str, pd.DataFrame]]:
        """构建局部搜索模式下的上下文。返回一个字符串或字符串列表，以及一个键为字符串、值为Pandas DataFrame的字典。"""


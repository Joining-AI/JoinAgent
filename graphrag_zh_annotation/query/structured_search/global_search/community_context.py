# 导入各种工具，让我们的程序能识别不同类型的变量
from typing import Any

# 导入一个用于处理数据的库，叫做pandas
import pandas as pd

# 导入一个可能用于处理令牌或认证的库，tiktoken
import tiktoken

# 从graphrag的model模块导入两个类：CommunityReport和Entity，它们代表报告和实体
from graphrag.model import CommunityReport, Entity

# 从graphrag查询的context_builder社区上下文模块导入一个函数：build_community_context，用于构建社区上下文
from graphrag.query.context_builder.community_context import build_community_context

# 从graphrag查询的context_builder对话历史模块导入ConversationHistory类，可能用来记录对话历史
from graphrag.query.context_builder.conversation_history import ConversationHistory

# 从graphrag查询的结构化搜索基础模块导入GlobalContextBuilder类，用于构建全局搜索上下文
from graphrag.query.structured_search.base import GlobalContextBuilder

# 这里是微软公司的版权信息，告诉我们代码由微软创建，使用了MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个文件的作用，是关于构建全局搜索提示的上下文数据的算法
"""Contains algorithms to build context data for global search prompt."""

# 这是一个名为GlobalCommunityContext的类，它从GlobalContextBuilder类继承
class GlobalCommunityContext(GlobalContextBuilder):
    # 这个类是用来构建全局搜索的社区上下文的
    """GlobalSearch community context builder."""

    # 初始化方法，当创建这个类的实例时会运行
    def __init__(
        self,
        # 传入一个包含社区报告的列表
        community_reports: list[CommunityReport],
        # 可选地，传入一个实体列表
        entities: list[Entity] | None = None,
        # 可选地，传入一个用于编码的token编码器
        token_encoder: tiktoken.Encoding | None = None,
        # 设置随机数种子，用于确保可重复性，默认值是86
        random_state: int = 86,
    ):
        # 将传入的参数保存为类的属性
        self.community_reports = community_reports
        self.entities = entities
        self.token_encoder = token_encoder
        self.random_state = random_state

    # 这个方法用来构建上下文数据
    def build_context(
        self,
        # 可选地，传入对话历史对象
        conversation_history: ConversationHistory | None = None,
        # 默认情况下，使用社区摘要
        use_community_summary: bool = True,
        # 列分隔符，默认是"|"
        column_delimiter: str = "|",
        # 是否打乱数据，默认是True
        shuffle_data: bool = True,
        # 是否包含社区排名，默认是False
        include_community_rank: bool = False,
        # 最小社区排名，默认是0
        min_community_rank: int = 0,
        # 社区排名的名称，默认是"rank"
        community_rank_name: str = "rank",
        # 是否包含社区权重，默认是True
        include_community_weight: bool = True,
        # 社区权重的名称，默认是"occurrence"
        community_weight_name: str = "occurrence",
        # 是否归一化社区权重，默认是True
        normalize_community_weight: bool = True,
        # 最大令牌数，默认是8000
        max_tokens: int = 8000,
        # 上下文名称，默认是"Reports"
        context_name: str = "Reports",
        # 是否只使用对话历史中的用户回合，默认是True
        conversation_history_user_turns_only: bool = True,
        # 对话历史的最大回合数，默认是5
        conversation_history_max_turns: int | None = 5,
        # 其他任意参数
        **kwargs: Any,
    ) -> tuple[str | list[str], dict[str, pd.DataFrame]]:
        # 准备社区报告数据表的批次作为全局搜索的上下文数据
        """Prepare batches of community report data table as context data for global search."""
        
        # 初始化对话历史上下文为空字符串
        conversation_history_context = ""
        # 初始化最终上下文数据为空字典
        final_context_data = {}

        # 如果有对话历史，构建对话历史上下文
        if conversation_history:
            # 使用对话历史对象的build_context方法
            (
                conversation_history_context,
                conversation_history_context_data,
            ) = conversation_history.build_context(
                # 只包含用户回合
                include_user_turns_only=conversation_history_user_turns_only,
                # 最大问答回合数
                max_qa_turns=conversation_history_max_turns,
                # 列分隔符
                column_delimiter=column_delimiter,
                # 最大令牌数
                max_tokens=max_tokens,
                # 不使用最近偏见
                recency_bias=False,
            )
            # 如果对话历史上下文不为空，则将其添加到最终上下文数据中
            if conversation_history_context != "":
                final_context_data = conversation_history_context_data

        # 构建社区上下文和数据
        community_context, community_context_data = build_community_context(
            # 使用当前类的属性
            community_reports=self.community_reports,
            entities=self.entities,
            token_encoder=self.token_encoder,
            use_community_summary=use_community_summary,
            column_delimiter=column_delimiter,
            shuffle_data=shuffle_data,
            include_community_rank=include_community_rank,
            min_community_rank=min_community_rank,
            community_rank_name=community_rank_name,
            include_community_weight=include_community_weight,
            community_weight_name=community_weight_name,
            normalize_community_weight=normalize_community_weight,
            max_tokens=max_tokens,
            single_batch=False,
            context_name=context_name,
            random_state=self.random_state,
        )

        # 如果社区上下文是列表，将对话历史和社区上下文合并
        if isinstance(community_context, list):
            # 每个社区上下文前加上对话历史上下文和换行符
            final_context = [
                f"{conversation_history_context}\n\n{context}"
                for context in community_context
            ]
        # 否则，直接将两者合并
        else:
            final_context = f"{conversation_history_context}\n\n{community_context}"

        # 更新最终上下文数据
        final_context_data.update(community_context_data)
        # 返回合并后的上下文和数据
        return (final_context, final_context_data)


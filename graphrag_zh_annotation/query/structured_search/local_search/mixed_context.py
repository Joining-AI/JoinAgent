# 导入logging模块，用于记录程序运行时的信息
import logging

# 类型注解模块，帮助我们指定函数参数和返回值的数据类型
from typing import Any

# 导入pandas库，这是一个处理数据的工具，像电子表格一样
import pandas as pd

# 导入tiktoken，这个可能是用来处理特定令牌或访问令牌的库
import tiktoken

# 从graphrag.model导入多个类，这些类可能定义了数据结构
from graphrag.model import CommunityReport, Covariate, Entity, Relationship, TextUnit

# 从graphrag.query.context_builder的子模块导入函数，这些函数用于构建查询上下文
from graphrag.query.context_builder.community_context import build_community_context
from graphrag.query.context_builder.conversation_history import ConversationHistory
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey, map_query_to_entities
from graphrag.query.context_builder.local_context import (
    build_covariates_context,
    build_entity_context,
    build_relationship_context,
    get_candidate_context,
)
from graphrag.query.context_builder.source_context import (
    build_text_unit_context,
    count_relationships,
)

# 从graphrag.query.input.retrieval的子模块导入函数，这些函数用于获取查询输入数据
from graphrag.query.input.retrieval.community_reports import get_candidate_communities
from graphrag.query.input.retrieval.text_units import get_candidate_text_units

# 从graphrag.query.llm的子模块导入基类，用于处理文本嵌入
from graphrag.query.llm.base import BaseTextEmbedding
from graphrag.query.llm.text_utils import num_tokens

# 从graphrag.query.structured_search的子模块导入基类，用于结构化搜索
from graphrag.query.structured_search.base import LocalContextBuilder

# 从graphrag.vector_stores导入基类，可能用于存储向量数据
from graphrag.vector_stores import BaseVectorStore

# 这行代码是版权信息，表示这段代码属于微软公司，2024年的版权。
# Copyright (c) 2024 Microsoft Corporation.

# 这行代码表示代码遵循MIT许可证。
# Licensed under the MIT License

# 这是一个文档字符串，描述了这段代码的作用。
"""这是用来构建本地搜索提示上下文数据的算法。"""

# 导入日志模块，用于记录程序运行信息。
import logging

# 导入pandas库，它是一个用于数据处理的库。
from typing import Any

# 导入pandas的DataFrame类，用于数据操作。
import pandas as pd

# 导入tiktoken库，可能是一个用于文本处理的库。
import tiktoken

# 从graphrag.model导入一些类，它们可能是数据结构。
from graphrag.model import CommunityReport, Covariate, Entity, Relationship, TextUnit

# 从graphrag.query.context_builder.community_context导入一个函数，用于构建社区上下文。
from graphrag.query.context_builder.community_context import build_community_context

# 从graphrag.query.context_builder.conversation_history导入一个类，用于处理对话历史。
from graphrag.query.context_builder.conversation_history import ConversationHistory

# 从graphrag.query.context_builder.entity_extraction导入两个类，用于处理实体和存储键。
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey, map_query_to_entities

# 从graphrag.query.context_builder.local_context导入几个函数，用于构建不同的上下文。
from graphrag.query.context_builder.local_context import (
    build_covariates_context,
    build_entity_context,
    build_relationship_context,
    get_candidate_context,
)

# 从graphrag.query.context_builder.source_context导入两个函数，用于处理文本单元和关系计数。
from graphrag.query.context_builder.source_context import (
    build_text_unit_context,
    count_relationships,
)

# 从graphrag.query.input.retrieval.community_reports导入一个函数，用于获取候选社区。
from graphrag.query.input.retrieval.community_reports import get_candidate_communities

# 从graphrag.query.input.retrieval.text_units导入一个函数，用于获取候选文本单元。
from graphrag.query.input.retrieval.text_units import get_candidate_text_units

# 从graphrag.query.llm.base导入一个基类，可能与语言模型有关。
from graphrag.query.llm.base import BaseTextEmbedding

# 从graphrag.query.llm.text_utils导入一个函数，用于计算令牌数量。
from graphrag.query.llm.text_utils import num_tokens

# 从graphrag.query.structured_search.base导入一个基类，可能与结构化搜索有关。
from graphrag.query.structured_search.base import LocalContextBuilder

# 从graphrag.vector_stores导入一个基类，用于向量存储。
from graphrag.vector_stores import BaseVectorStore

# 定义一个全局变量log，用于记录日志信息。
log = logging.getLogger(__name__)




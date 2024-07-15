# 导入两个特殊类型的模块，它们帮助我们定义数据结构
from typing_extensions import NotRequired, TypedDict

# 这是一个版权声明，表示代码由微软公司拥有，2024年
# 并遵循MIT许可证的规定，但对我们理解代码内容并不重要

# 这段文字描述了这个代码的作用，是关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 再次导入NotRequired和TypedDict，确保它们在类定义中可用
from typing_extensions import NotRequired, TypedDict


# 定义一个名为LocalSearchConfigInput的数据类
# 类似于一个字典，但有特定的键和类型
class LocalSearchConfigInput(TypedDict):

    # 这个类里定义了一些配置参数，都是可选的（因为用了NotRequired）
    
    # text_unit_prop：可以是浮点数、字符串或None，但不是必须的
    text_unit_prop: NotRequired[float | str | None]

    # community_prop：同样可以是浮点数、字符串或None，也是可选的
    community_prop: NotRequired[float | str | None]

    # conversation_history_max_turns：可以是整数、字符串或None，也是可选的
    conversation_history_max_turns: NotRequired[int | str | None]

    # top_k_entities：可以是整数、字符串或None，可选
    top_k_entities: NotRequired[int | str | None]

    # top_k_relationships：同上，可选
    top_k_relationships: NotRequired[int | str | None]

    # max_tokens：可以是整数、字符串或None，可选
    max_tokens: NotRequired[int | str | None]

    # llm_max_tokens：最后一个是相同的，可选
    llm_max_tokens: NotRequired[int | str | None]


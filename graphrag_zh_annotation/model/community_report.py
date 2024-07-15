# 导入一个叫做 'dataclass' 的工具，它帮助我们创建带有默认值和自动方法的类
from dataclasses import dataclass
# 导入 'Any' 类型，它在编程中代表任何类型的数据
from typing import Any
# 从当前文件的子模块 'named' 导入 'Named' 类
from .named import Named

# 这段文字是版权信息，说明代码由微软公司拥有，且遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个代码包包含了一个名为 'CommunityReport' 的模型
"""A package containing the 'CommunityReport' model."""

# 再次导入 'dataclass' 和 'Any'，确保它们已经准备好了
from dataclasses import dataclass
from typing import Any

# 从 'named' 子模块再次导入 'Named'，这可能是因为需要在下面的代码中使用
from .named import Named

# 使用 '@dataclass' 装饰器定义一个新类，这个类会有一些默认值和特殊的方法
# 这个类的名字会在接下来的代码中定义
@dataclass

# 定义一个名为CommunityReport的类，它继承自Named（这个可能是另一个类，但在这里我们不详细解释）
class CommunityReport(Named):
    # 这个类是用来描述一个社区的总结报告，由一个AI系统（LLM）生成的

    # 报告关联的社区ID
    community_id: str
    """The ID of the community this report is associated with."""

    # 报告的简短总结
    summary: str = ""
    """Summary of the report."""

    # 报告的完整内容
    full_content: str = ""
    """Full content of the report."""

    # 报告的排名，用于排序（可选）。数值越大，报告越重要
    rank: float | None = 1.0
    """Rank of the report, used for sorting (optional). Higher means more important"""

    # 报告摘要的语义（即文本）嵌入（可选）
    summary_embedding: list[float] | None = None
    """The semantic (i.e. text) embedding of the report summary (optional)."""

    # 报告全文的语义（即文本）嵌入（可选）
    full_content_embedding: list[float] | None = None
    """The semantic (i.e. text) embedding of the full report content (optional)."""

    # 与报告关联的额外属性字典（可选）
    attributes: dict[str, Any] | None = None
    """A dictionary of additional attributes associated with the report (optional)."""

    # 这是一个类方法，可以从字典中创建一个新的社区报告对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],          # 从这个字典中获取数据
        id_key: str = "id",         # 字典中的ID键，默认是"id"
        title_key: str = "title",    # 标题键，默认是"title"
        community_id_key: str = "community_id",  # 社区ID键，默认是"community_id"
        short_id_key: str = "short_id",   # 短ID键，默认是"short_id"
        summary_key: str = "summary",    # 摘要键，默认是"summary"
        full_content_key: str = "full_content",  # 全文键，默认是"full_content"
        rank_key: str = "rank",        # 排名键，默认是"rank"
        summary_embedding_key: str = "summary_embedding",  # 摘要嵌入键，默认是"summary_embedding"
        full_content_embedding_key: str = "full_content_embedding",  # 全文嵌入键，默认是"full_content_embedding"
        attributes_key: str = "attributes",  # 属性键，默认是"attributes"
    ) -> "CommunityReport":
        # 使用字典中的数据创建并返回一个新的CommunityReport对象
        return CommunityReport(
            id=d[id_key],
            title=d[title_key],
            community_id=d[community_id_key],
            short_id=d.get(short_id_key),  # 如果短ID键存在，则获取，否则返回None
            summary=d[summary_key],
            full_content=d[full_content_key],
            rank=d[rank_key],
            summary_embedding=d.get(summary_embedding_key),  # 如果摘要嵌入键存在，则获取，否则返回None
            full_content_embedding=d.get(full_content_embedding_key),  # 如果全文嵌入键存在，则获取，否则返回None
            attributes=d.get(attributes_key),  # 如果属性键存在，则获取，否则返回None
        )


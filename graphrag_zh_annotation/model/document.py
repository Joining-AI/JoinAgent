# 导入一个叫做"dataclass"的工具，它能帮助我们创建类时自动添加一些默认的方法
from dataclasses import dataclass, field
# 导入"Any"类型，这个类型可以代表任何其他类型的数据
from typing import Any
# 从当前文件夹下的"named"模块导入"Named"类
from .named import Named

# 这段文字是版权信息，说明代码由微软公司编写，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档，描述了包含'Document'模型的包
"""A package containing the 'Document' model."""

# 再次导入"dataclass"和"field"，确保代码清晰
from dataclasses import dataclass, field
# 再次导入"Any"类型
from typing import Any

# 使用装饰器"@dataclass"来定义一个新类，这个类叫做'Document'
@dataclass
# 定义一个类，叫'Document'，它继承自'Named'类
class Document(Named):
    # 这里使用'field'来定义类的一个属性，名叫'content'，初始值是None
    content: Any = field(default=None)

# 定义一个名为Document的类，它继承自Named（假设Named是另一个类）
class Document(Named):
    # 这是一个协议，表示系统中的文档
    """A protocol for a document in the system."""

    # 文档的类型，默认是"text"
    type: str = "text"
    """Type of the document."""

    # 文档中文本单元的ID列表，初始化为空列表
    text_unit_ids: list[str] = field(default_factory=list)
    """list of text units in the document."""

    # 文档的原始文本内容，初始化为空字符串
    raw_content: str = ""
    """The raw text content of the document."""

    # 文档的摘要（可选）
    summary: str | None = None
    """Summary of the document (optional)."""

    # 摘要的语义嵌入（可选）
    summary_embedding: list[float] | None = None
    """The semantic embedding for the document summary (optional)."""

    # 原始内容的语义嵌入（可选）
    raw_content_embedding: list[float] | None = None
    """The semantic embedding for the document raw content (optional)."""

    # 结构化的属性字典，如作者等（可选）
    attributes: dict[str, Any] | None = None
    """A dictionary of structured attributes such as author, etc (optional)."""

    # 类方法，从字典数据创建一个新的Document对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],  # 输入的字典数据
        id_key: str = "id",  # ID对应的键，默认是"id"
        short_id_key: str = "short_id",  # 短ID对应的键，默认是"short_id"
        title_key: str = "title",  # 标题对应的键，默认是"title"
        type_key: str = "type",  # 类型对应的键，默认是"type"
        raw_content_key: str = "raw_content",  # 原始内容对应的键，默认是"raw_content"
        summary_key: str = "summary",  # 摘要对应的键，默认是"summary"
        summary_embedding_key: str = "summary_embedding",  # 摘要嵌入对应的键，默认是"summary_embedding"
        raw_content_embedding_key: str = "raw_content_embedding",  # 原始内容嵌入对应的键，默认是"raw_content_embedding"
        text_units_key: str = "text_units",  # 文本单元对应的键，默认是"text_units"
        attributes_key: str = "attributes",  # 属性对应的键，默认是"attributes"
    ) -> "Document":
        # 使用给定的键从字典中获取值，创建并返回一个新的Document对象
        return Document(
            id=d[id_key],
            short_id=d.get(short_id_key),
            title=d[title_key],
            type=d.get(type_key, "text"),  # 如果字典中没有"type"键，则默认为"text"
            raw_content=d[raw_content_key],
            summary=d.get(summary_key),
            summary_embedding=d.get(summary_embedding_key),
            raw_content_embedding=d.get(raw_content_embedding_key),
            text_unit_ids=d.get(text_units_key, []),  # 如果字典中没有"text_units"键，则默认为空列表
            attributes=d.get(attributes_key),
        )


# 导入一个叫做"dataclass"的东西，它能帮助我们创建类并自动添加一些方法
from dataclasses import dataclass
# 导入"Any"，这是一个类型提示，表示这个位置可以放任何类型的值
from typing import Any
# 从另一个文件（当前文件的父级目录）导入了"Identified"类
from .identified import Identified

# 这是一段版权信息，告诉我们这个代码是微软公司2024年的作品，使用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个代码包包含了一个叫做'TextUnit'模型的东西
"""A package containing the 'TextUnit' model."""

# 再次导入"dataclass"和"Any"，这是因为Python有时候需要再次声明
from dataclasses import dataclass
from typing import Any

# 从".identified"导入"Identified"类，这是Python的一种导入方式，表示导入同一目录下别的文件的类

# 使用"dataclass"装饰器来定义一个新类，这个类叫"TextUnit"
@dataclass

# 定义一个名为TextUnit的类，它继承自Identified类（这个类在这里没有显示，但它是存在的）
class TextUnit(Identified):
    # 这个类是用来表示文档数据库中的一个文本单元的协议
    """A protocol for a TextUnit item in a Document database."""

    # 这个单元的文本内容
    text: str
    """The text of the unit."""

    # 文本单元的嵌入表示，可能不存在
    text_embedding: list[float] | None = None
    """The text embedding for the text unit (optional)."""

    # 与文本单元相关的实体ID列表，可能不存在
    entity_ids: list[str] | None = None
    """List of entity IDs related to the text unit (optional)."""

    # 与文本单元相关的关系ID列表，可能不存在
    relationship_ids: list[str] | None = None
    """List of relationship IDs related to the text unit (optional)."""

    # 与文本单元相关的不同类型的协变量字典，可能不存在
    covariate_ids: dict[str, list[str]] | None = None
    "Dictionary of different types of covariates related to the text unit (optional)."

    # 文本中的单词数量，可能不存在
    n_tokens: int | None = None
    """The number of tokens in the text (optional)."""

    # 文本单元出现的文档ID列表，可能不存在
    document_ids: list[str] | None = None
    """List of document IDs in which the text unit appears (optional)."""

    # 与文本单元关联的其他属性字典，可能不存在
    attributes: dict[str, Any] | None = None
    """A dictionary of additional attributes associated with the text unit (optional)."""

    # 类方法，从字典数据创建一个新的文本单元对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],  # 输入的字典数据
        id_key: str = "id",  # 字典中ID键的默认值
        short_id_key: str = "short_id",  # 字典中短ID键的默认值
        text_key: str = "text",  # 字典中文本键的默认值
        text_embedding_key: str = "text_embedding",  # 字典中文本嵌入键的默认值
        entities_key: str = "entity_ids",  # 字典中实体ID键的默认值
        relationships_key: str = "relationship_ids",  # 字典中关系ID键的默认值
        covariates_key: str = "covariate_ids",  # 字典中协变量ID键的默认值
        n_tokens_key: str = "n_tokens",  # 字典中文本单词数键的默认值
        document_ids_key: str = "document_ids",  # 字典中文档ID键的默认值
        attributes_key: str = "attributes",  # 字典中其他属性键的默认值
    ) -> "TextUnit":
        # 使用输入字典中的数据创建并返回一个TextUnit对象
        return TextUnit(
            id=d[id_key],
            short_id=d.get(short_id_key),
            text=d[text_key],
            text_embedding=d.get(text_embedding_key),
            entity_ids=d.get(entities_key),
            relationship_ids=d.get(relationships_key),
            covariate_ids=d.get(covariates_key),
            n_tokens=d.get(n_tokens_key),
            document_ids=d.get(document_ids_key),
            attributes=d.get(attributes_key),
        )


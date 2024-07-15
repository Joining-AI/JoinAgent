# 导入dataclass模块，它帮助我们创建带有默认值和顺序的类
from dataclasses import dataclass
# 导入Any类型，这是一个特殊的类型，表示可以接受任何类型的数据
from typing import Any
# 导入Identified类，这个类可能是从别的文件导入的，它可能包含了某些特殊功能
from .identified import Identified

# 这是一个注释，告诉我们这段代码的版权属于微软公司，2024年
# 并且使用了MIT许可证，这是一种允许他人自由使用、修改和分享代码的许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个包包含了一个名为'Relationship'的模型
"""A package containing the 'Relationship' model."""

# 再次导入dataclass和Any，确保代码的可读性，即使前面已经导入过
from dataclasses import dataclass
from typing import Any

# 从.identified导入Identified类，这里的"."表示当前目录下的文件或模块
from .identified import Identified

# 使用dataclass装饰器定义一个新类，这个类叫做Relationship
# @dataclass
@dataclass
class Relationship:
    # 类的属性在这里定义，比如：
    name: str  # 一个字符串类型的属性，表示关系的名称
    type: Any  # 一个任意类型的属性，可能用来存储不同类型的关联信息

# 定义一个名为Relationship的类，它继承自Identified类（这个类我们暂时不解释）
class Relationship(Identified):
    # 这个类是用来表示两个实体之间的关系，可以用于任何类型的关系
    """A relationship between two entities. This is a generic relationship, and can be used to represent any type of relationship between any two entities."""

    # 定义一个变量source，用来存储来源实体的名字
    source: str
    """The source entity name."""

    # 定义一个变量target，用来存储目标实体的名字
    target: str
    """The target entity name."""

    # 定义一个变量weight，表示关系的权重，默认是1.0
    weight: float | None = 1.0
    """The edge weight."""

    # 定义一个变量description，用来描述这个关系，可选的
    description: str | None = None
    """A description of the relationship (optional)."""

    # 定义一个变量description_embedding，存储关系描述的语义嵌入，也是可选的
    description_embedding: list[float] | None = None
    """The semantic embedding for the relationship description (optional)."""

    # 定义一个列表text_unit_ids，存储关系出现的文本单元ID，可选的
    text_unit_ids: list[str] | None = None
    """List of text unit IDs in which the relationship appears (optional)."""

    # 定义一个列表document_ids，存储关系出现的文档ID，可选的
    document_ids: list[str] | None = None
    """List of document IDs in which the relationship appears (optional)."""

    # 定义一个字典attributes，存储与关系相关的额外属性，可选的，并会在搜索提示中包含
    attributes: dict[str, Any] | None = None
    """Additional attributes associated with the relationship (optional). To be included in the search prompt"""

    # 定义一个类方法from_dict，它接收一个字典并根据字典内容创建一个新的Relationship对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],
        # 这些参数是字典中对应键的默认名称，可以根据实际情况调整
        id_key: str = "id",
        short_id_key: str = "short_id",
        source_key: str = "source",
        target_key: str = "target",
        description_key: str = "description",
        weight_key: str = "weight",
        text_unit_ids_key: str = "text_unit_ids",
        document_ids_key: str = "document_ids",
        attributes_key: str = "attributes",
    ) -> "Relationship":
        # 创建并返回一个新的Relationship对象，其属性值来自给定字典中的相应键
        return Relationship(
            id=d[id_key],
            short_id=d.get(short_id_key),
            source=d[source_key],
            target=d[target_key],
            description=d.get(description_key),
            weight=d.get(weight_key, 1.0),  # 如果字典中没有weight，则默认为1.0
            text_unit_ids=d.get(text_unit_ids_key),
            document_ids=d.get(document_ids_key),
            attributes=d.get(attributes_key),
        )


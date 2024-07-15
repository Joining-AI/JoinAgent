# 导入一个叫做 dataclass 的工具，它能帮助我们创建类时自动添加默认的构造函数和一些方法
from dataclasses import dataclass
# 导入 Any 类型，这是一个特殊的类型，代表任何类型的值都可以
from typing import Any
# 从当前文件的父目录下的 named 模块导入 Named 类
from .named import Named

# 这是一段版权信息，告诉我们这段代码是微软公司2024年的版权，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个包包含了 'Entity' 模型
"""A package containing the 'Entity' model."""

# 再次导入 dataclass 和 Any，这是为了确保代码的清晰，即使前面已经导入过
from dataclasses import dataclass
from typing import Any

# 从 named 模块再次导入 Named 类，这样在后面的代码中我们可以直接使用它
from .named import Named

# 使用 @dataclass 装饰器，定义一个叫做 Entity 的类，它会有一些自动创建的属性和方法
@dataclass

# 定义一个名为Entity的类，它继承自Named（这个类没有显示在这里，但可能是定义了名字属性的类）
class Entity(Named):
    # 这是一个协议，表示系统中的一个实体
    """A protocol for an entity in the system."""

    # 实体的类型，可以是任何字符串，但可能为空
    type: str | None = None
    """Type of the entity (can be any string, optional)."""

    # 实体的描述，也是可选的
    description: str | None = None
    """Description of the entity (optional)."""

    # 实体描述的语义嵌入，即文本的数学表示，可能为空
    description_embedding: list[float] | None = None
    """The semantic (i.e. text) embedding of the entity (optional)."""

    # 实体名字的语义嵌入，与上面类似，可选
    name_embedding: list[float] | None = None
    """The semantic (i.e. text) embedding of the entity (optional)."""

    # 实体的图嵌入，可能来自node2vec算法，也是可选的
    graph_embedding: list[float] | None = None
    """The graph embedding of the entity, likely from node2vec (optional)."""

    # 实体所在的社区ID列表，可选
    community_ids: list[str] | None = None
    """The community IDs of the entity (optional)."""

    # 实体出现的文本单元ID列表，可选
    text_unit_ids: list[str] | None = None
    """List of text unit IDs in which the entity appears (optional)."""

    # 实体出现的文档ID列表，可选
    document_ids: list[str] | None = None
    """List of document IDs in which the entity appears (optional)."""

    # 实体的排名，用于排序，可选。数值越大，表示实体越重要
    rank: int | None = 1
    """Rank of the entity, used for sorting (optional). Higher rank indicates more important entity. This can be based on centrality or other metrics."""

    # 关联到实体的其他属性，如开始时间、结束时间等，可选
    attributes: dict[str, Any] | None = None
    """Additional attributes associated with the entity (optional), e.g. start time, end time, etc. To be included in the search prompt."""

    # 这是一个类方法，用于从字典中创建一个新的实体对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],
        # 指定字典中用于获取ID的键
        id_key: str = "id",
        short_id_key: str = "short_id",
        title_key: str = "title",
        type_key: str = "type",
        description_key: str = "description",
        description_embedding_key: str = "description_embedding",
        name_embedding_key: str = "name_embedding",
        graph_embedding_key: str = "graph_embedding",
        community_key: str = "community",
        text_unit_ids_key: str = "text_unit_ids",
        document_ids_key: str = "document_ids",
        rank_key: str = "degree",
        attributes_key: str = "attributes",
    ) -> "Entity":
        # 使用字典中的数据创建并返回一个Entity对象
        return Entity(
            id=d[id_key],
            title=d[title_key],
            short_id=d.get(short_id_key),
            type=d.get(type_key),
            description=d.get(description_key),
            name_embedding=d.get(name_embedding_key),
            description_embedding=d.get(description_embedding_key),
            graph_embedding=d.get(graph_embedding_key),
            community_ids=d.get(community_key),
            rank=d.get(rank_key, 1),  # 如果字典中没有rank_key，则默认为1
            text_unit_ids=d.get(text_unit_ids_key),
            document_ids=d.get(document_ids_key),
            attributes=d.get(attributes_key),
        )


# 导入数据类模块，用于创建具有默认值的数据类
from dataclasses import dataclass
# 导入类型模块，用于定义变量的可能类型
from typing import Any
# 从另一个名为"named"的模块导入名为"Named"的类
from .named import Named

# 以下代码的版权属于微软公司，并遵循MIT许可证

# 这是一个包含'Community'模型的包的文档字符串

# 再次导入数据类和类型模块，确保代码的可读性
from dataclasses import dataclass
from typing import Any

# 从命名模块导入"Named"类

# 使用数据类装饰器创建一个名为"Community"的新类，它继承自"Named"类
@dataclass
class Community(Named):
    # 社区级别，初始为空字符串
    level: str = ""

    # 与社区相关的实体ID列表（可选），默认为None
    entity_ids: list[str] | None = None

    # 与社区相关的关系ID列表（可选），默认为None
    relationship_ids: list[str] | None = None

    # 与社区相关的不同类型的协变量字典（可选），如索赔数据，初始为None
    covariate_ids: dict[str, list[str]] | None = None

    # 关联到社区的其他属性字典（可选），用于搜索提示，初始为None
    attributes: dict[str, Any] | None = None

    # 类方法，用于从字典中创建一个新的社区对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],  # 字典数据
        id_key: str = "id",  # 默认的ID键名
        title_key: str = "title",  # 默认的标题键名
        short_id_key: str = "short_id",  # 默认的短ID键名
        level_key: str = "level",  # 默认的级别键名
        entities_key: str = "entity_ids",  # 默认的实体ID键名
        relationships_key: str = "relationship_ids",  # 默认的关系ID键名
        covariates_key: str = "covariate_ids",  # 默认的协变量键名
        attributes_key: str = "attributes",  # 默认的属性键名
    ) -> "Community":
        # 根据字典中的键值创建并返回新的Community对象
        return Community(
            id=d[id_key],
            title=d[title_key],
            short_id=d.get(short_id_key),
            level=d[level_key],
            entity_ids=d.get(entities_key),
            relationship_ids=d.get(relationships_key),
            covariate_ids=d.get(covariates_key),
            attributes=d.get(attributes_key),
        )


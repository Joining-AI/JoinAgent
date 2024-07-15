# 导入数据类模块，用于创建带有默认值的数据类
from dataclasses import dataclass
# 导入Any类型，表示可以是任何类型
from typing import Any
# 导入Identified类，可能是在同一个文件夹下的另一个类
from .identified import Identified

# 这段代码的版权信息和许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个包含'Covariate'模型的包的描述
# "Covariate"可能是一个术语，代表某种数据类型或概念

# 再次导入dataclass和Any，确保模块在需要的地方被导入
from dataclasses import dataclass
from typing import Any

# 再次导入Identified类
from .identified import Identified

# 使用数据类装饰器定义一个名为Covariate的新类，它继承自Identified类
@dataclass
class Covariate(Identified):
    """
    系统中协变量的协议。

    协变量是与主体（如实体）相关联的元数据，例如实体声明。
    每个主体可能与多种类型的协变量相关联。
    """

    # 主体ID，是一个字符串
    subject_id: str
    # 主体类型，默认为"entity"，也是一个字符串
    subject_type: str = "entity"
    # 协变量类型，默认为"claim"，同样是一个字符串
    covariate_type: str = "claim"
    # 协变量信息出现的文本单元ID列表（可选），可能为空
    text_unit_ids: list[str] | None = None
    # 协变量信息出现的文档ID列表（可选），可能为空
    document_ids: list[str] | None = None
    # 协变量的属性字典，可能为空
    attributes: dict[str, Any] | None = None

    # 类方法，从字典中创建一个新的Covariate对象
    @classmethod
    def from_dict(
        cls,
        d: dict[str, Any],  # 传入的字典数据
        id_key: str = "id",  # 字典中的ID键，默认为"id"
        subject_id_key: str = "subject_id",  # 主体ID键，默认为"subject_id"
        subject_type_key: str = "subject_type",  # 主体类型键，默认为"subject_type"
        covariate_type_key: str = "covariate_type",  # 协变量类型键，默认为"covariate_type"
        short_id_key: str = "short_id",  # 短ID键，默认为"short_id"
        text_unit_ids_key: str = "text_unit_ids",  # 文本单元ID键，默认为"text_unit_ids"
        document_ids_key: str = "document_ids",  # 文档ID键，默认为"document_ids"
        attributes_key: str = "attributes",  # 属性键，默认为"attributes"
    ) -> "Covariate":
        """从字典数据创建一个新的协变量对象并返回."""
        # 使用字典中的键值创建Covariate实例并返回
        return Covariate(
            id=d[id_key],
            short_id=d.get(short_id_key),
            subject_id=d[subject_id_key],
            subject_type=d.get(subject_type_key, "entity"),
            covariate_type=d.get(covariate_type_key, "claim"),
            text_unit_ids=d.get(text_unit_ids_key),
            document_ids=d.get(document_ids_key),
            attributes=d.get(attributes_key),
        )


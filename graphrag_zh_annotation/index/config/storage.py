# 这段代码定义了数据存储配置的模型，让十岁的孩子理解，我会用简单语言注释每一行

# 导入未来注解，这在Python3.7以下版本是必要的，但在这里是为了兼容性
from __future__ import annotations

# 导入泛型、字面量和类型变量，这些都是Python处理数据类型的工具
from typing import Generic, Literal, TypeVar

# 导入一个用于数据验证的库Pydantic，以及它的"Field"类
from pydantic import BaseModel, Field as pydantic_Field

# 从另一个模块导入存储类型的枚举
from graphrag.config.enums import StorageType

# 定义一个类型变量T，它可以在多个类中代表不同的类型
T = TypeVar("T")

# 这个模块包含三个数据存储配置的类

# 定义一个基类，表示管道（pipeline）的存储配置，使用Pydantic的BaseModel，并且是泛型类
class PipelineStorageConfig(BaseModel, Generic[T]):
    # 存储配置的类型，由子类具体指定
    type: T

# 定义一个子类，表示文件存储配置，继承自PipelineStorageConfig，类型为StorageType.file的字面量
class PipelineFileStorageConfig(PipelineStorageConfig[Literal[StorageType.file]]):
    # 文件存储的类型，固定为"file"
    type: Literal[StorageType.file] = StorageType.file
    # 存储的根目录，可以是任何字符串或没有（None）
    base_dir: str | None = pydantic_Field(
        # 描述：存储的根目录
        description="The base directory for the storage.",
        # 默认值：没有设置
        default=None
    )

# 定义另一个子类，表示内存存储配置，继承自PipelineStorageConfig，类型为StorageType.memory的字面量
class PipelineMemoryStorageConfig(PipelineStorageConfig[Literal[StorageType.memory]]):
    # 内存存储的类型，固定为"memory"
    type: Literal[StorageType.memory] = StorageType.memory

# 定义一个名为PipelineBlobStorageConfig的类，它继承自PipelineStorageConfig，并且泛型参数是Literal[StorageType.blob]
class PipelineBlobStorageConfig(PipelineStorageConfig[Literal[StorageType.blob]]):
    # 这个类用来表示管道的blob存储配置
    """Represents the blob storage configuration for the pipeline."""

    # 类中有一个属性叫type，它的值是固定的StorageType.blob
    type: Literal[StorageType.blob] = StorageType.blob
    # 这个属性表示存储的类型

    # 定义一个属性connection_string，它可能是字符串或None
    # 使用pydantic的Field来设置描述和默认值（默认为None）
    connection_string: str | None = pydantic_Field(
        description="用于存储的blob存储连接字符串。",
        default=None
    )
    # 这个属性是存储的blob连接字符串

    # 定义一个属性container_name，它必须是字符串
    # 同样使用Field设置描述和默认值（默认为None）
    container_name: str = pydantic_Field(
        description="用于存储的容器名称。",
        default=None
    )
    # 这个属性是存储的容器名称

    # 定义一个属性base_dir，它可能是字符串或None
    # Field描述和默认值（默认为None）
    base_dir: str | None = pydantic_Field(
        description="存储的基目录。",
        default=None
    )
    # 这个属性是存储的基目录

    # 定义一个属性storage_account_blob_url，可能是字符串或None
    # Field描述和默认值（默认为None）
    storage_account_blob_url: str | None = pydantic_Field(
        description="存储帐户的blob URL。",
        default=None
    )
    # 这个属性是存储帐户的blob URL


# 定义一个元组PipelineStorageConfigTypes，它包含了三种类型的配置类
PipelineStorageConfigTypes = (
    PipelineFileStorageConfig | PipelineMemoryStorageConfig | PipelineBlobStorageConfig
)


# 导入两个特殊类型的模块，帮助我们定义数据结构
from typing_extensions import NotRequired, TypedDict
# 导入一个枚举类型，关于存储的类型
from graphrag.config.enums import StorageType

# 这是微软公司的版权声明
# Licensed under the MIT License

# 这段代码描述的是配置参数，特别是默认设置

# 定义一个类（像字典的数据结构），用于存储有关存储的配置信息
class StorageConfigInput(TypedDict):
    # 'type' 字段可以是存储类型、字符串或空，但不是必须的
    type: NotRequired[StorageType | str | None]
    # 'base_dir' 字段可以是字符串或空，但不是必须的
    base_dir: NotRequired[str | None]
    # 'connection_string' 字段可以是字符串或空，但不是必须的
    connection_string: NotRequired[str | None]
    # 'container_name' 字段可以是字符串或空，但不是必须的
    container_name: NotRequired[str | None]
    # 'storage_account_blob_url' 字段可以是字符串或空，但不是必须的
    storage_account_blob_url: NotRequired[str | None]


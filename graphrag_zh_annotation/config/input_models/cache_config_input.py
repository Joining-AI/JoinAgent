# 导入一些特殊类型的定义，帮助我们更好地说明变量的类型
from typing_extensions import NotRequired, TypedDict

# 导入一个名为CacheType的枚举类型，它包含关于缓存的特定选项
from graphrag.config.enums import CacheType

# 这是一个版权声明，告诉我们这段代码由微软公司在2024年编写
# 并且它遵循MIT许可证的规则

# 这段文字描述了这个代码的作用，是关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 使用typing_extensions库中的NotRequired和TypedDict来创建一个新的字典类
# 字典里的键值对会有特定的类型

# 定义一个名为CacheConfigInput的类，它是TypedDict的一个子类
class CacheConfigInput(TypedDict):
    # 这个类用于描述关于缓存的默认配置
    """The default configuration section for Cache."""

    # 键为'type'，值可以是CacheType枚举、字符串或None，但不是必须的（NotRequired）
    type: NotRequired[CacheType | str | None]

    # 键为'base_dir'，值可以是字符串或None，但不是必须的
    base_dir: NotRequired[str | None]

    # 键为'connection_string'，值可以是字符串或None，但不是必须的
    connection_string: NotRequired[str | None]

    # 键为'container_name'，值可以是字符串或None，但不是必须的
    container_name: NotRequired[str | None]

    # 键为'storage_account_blob_url'，值可以是字符串或None，但不是必须的
    storage_account_blob_url: NotRequired[str | None]


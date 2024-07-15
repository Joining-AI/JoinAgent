# 导入一个叫做 Any 的类型提示，用于表示任何类型的值
from typing import Any
# 导入一个叫 PipelineCache 的类，它来自同一目录下的 pipeline_cache 模块
from .pipeline_cache import PipelineCache

# 这是微软公司的版权信息和许可证声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了一个叫做 NoopPipelineCache 的实现

# 再次导入 Any 类型提示和 PipelineCache 类，确保它们在类定义中可用
from typing import Any
from .pipeline_cache import PipelineCache

# 定义一个名为 NoopPipelineCache 的类，它是 PipelineCache 类的子类
class NoopPipelineCache(PipelineCache):
    # 这个类是一个空操作（No-op）的缓存实现，通常用于测试
    """一个不执行任何操作的缓存实现，通常在测试时很有用。"""

    # 定义一个异步方法 get，用于获取指定键的值
    async def get(self, key: str) -> Any:
        # 参数：key - 要获取值的键
        # 返回：输出 - 给定键的值
        """根据给定的键获取值。
        
        参数：
            - key - 要获取的值的键。
            - as_bytes - 是否以字节形式返回值。

        返回：
            - 输出 - 给定键的值。
        """
        # 返回 None，因为这是一个不执行任何操作的实现
        return None

    # 定义一个异步方法 set，用于设置指定键的值
    async def set(
        self, key: str, value: str | bytes | None, debug_data: dict | None = None
    ) -> None:
        # 参数：key - 要设置的键
        #       value - 要设置的值
        """为给定的键设置值。

        参数：
            - key - 要设置值的键。
            - value - 要设置的值。
        """
        # 这个方法不执行任何操作，因为它是空操作的实现
        pass

    # 定义一个异步方法 has，用于检查指定键是否存在于缓存中
    async def has(self, key: str) -> bool:
        # 参数：key - 要检查的键
        # 返回：输出 - 如果键在缓存中则为 True，否则为 False
        """检查给定的键是否在缓存中。

        参数：
            - key - 要检查的键。

        返回：
            - 输出 - 如果键在缓存中则为 True，否则为 False。
        """
        # 总是返回 False，因为这个缓存不存储任何内容
        return False

    # 定义一个异步方法 delete，用于从缓存中删除指定键
    async def delete(self, key: str) -> None:
        # 参数：key - 要删除的键
        """从缓存中删除给定的键。

        参数：
            - key - 要删除的键。
        """
        # 这个方法不执行任何操作，因为它是空操作的实现
        pass

    # 定义一个异步方法 clear，用于清空缓存
    async def clear(self) -> None:
        """清空整个缓存。
        """
        # 这个方法不执行任何操作，因为它是空操作的实现
        pass

    # 定义一个方法 child，用于创建一个带有指定名称的子缓存
    def child(self, name: str) -> PipelineCache:
        # 参数：name - 子缓存的名称
        # 返回：一个新的 PipelineCache 对象，实际上是返回自身，因为这是一个空操作的实现
        """使用给定的名称创建一个子缓存。

        参数：
            - name - 创建子缓存时使用的名称。
        """
        # 返回当前对象本身，表示没有实际的子缓存
        return self


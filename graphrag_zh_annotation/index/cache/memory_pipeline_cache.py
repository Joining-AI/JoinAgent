# 导入一个叫做 Any 的类型提示，它代表任何类型的数据
from typing import Any

# 导入名为 PipelineCache 的类，它来自同一目录下的 'pipeline_cache' 模块
from .pipeline_cache import PipelineCache

# 这是一个版权信息，表示代码归 Microsoft Corporation 所有，时间是 2024 年
# 注：实际年份可能需要更新，这里以示例为准
# Licensed under the MIT License 表示代码遵循 MIT 许可证，允许他人自由使用和修改

"""
# 这是一个文档字符串，描述了这个模块的内容。它告诉人们这个模块有一个叫做 'InMemoryCache' 的模型
# 在这里，我们没有实际的 'InMemoryCache' 代码，但根据名字，我们可以猜测它可能是一个在内存中存储数据的类
"""

# 再次导入 Any 类型提示，虽然之前已经导入过，但这里可能是为了确保代码清晰，或者因为其他部分可能需要它
from typing import Any

# 这是一个名为InMemoryCache的类，它继承自PipelineCache
class InMemoryCache(PipelineCache):
    # 这个类是用来在内存中存储数据的缓存类
    """In memory cache class definition."""

    # 定义了一个字典变量，用来存放键值对
    _cache: dict[str, Any]
    # 定义了一个字符串变量，表示缓存的名字
    _name: str

    # 这是InMemoryCache类的初始化方法
    def __init__(self, name: str | None = None):
        # 初始化时，设置缓存为空字典
        self._cache = {}
        # 如果没有提供名字，则设为空字符串，否则用提供的名字
        self._name = name or ""

    # 这个方法用来获取特定键的值
    async def get(self, key: str) -> Any:
        """获取给定键的值。
        
        参数：
            - key - 要获取的键。
            
        返回：
            - 输出 - 给定键对应的值。
        """
        # 创建一个缓存键，然后从字典中获取该键的值并返回
        key = self._create_cache_key(key)
        return self._cache.get(key)

    # 这个方法用来设置特定键的值
    async def set(self, key: str, value: Any, debug_data: dict | None = None) -> None:
        """设置给定键的值。
        
        参数：
            - key - 要设置的键。
            - value - 要设置的值。
        """
        # 创建一个缓存键，然后将键值对存入字典
        key = self._create_cache_key(key)
        self._cache[key] = value

    # 这个方法检查给定键是否存在于缓存中
    async def has(self, key: str) -> bool:
        """如果给定的键在存储中存在，返回True。
        
        参数：
            - key - 检查的键。
            
        返回：
            - 输出 - 如果键存在，返回True，否则返回False。
        """
        # 创建一个缓存键，然后检查字典中是否存在该键
        key = self._create_cache_key(key)
        return key in self._cache

    # 这个方法删除给定键
    async def delete(self, key: str) -> None:
        """从存储中删除给定的键。
        
        参数：
            - key - 要删除的键。
        """
        # 创建一个缓存键，然后从字典中删除该键
        key = self._create_cache_key(key)
        del self._cache[key]

    # 这个方法清空整个缓存
    async def clear(self) -> None:
        """清除存储的所有内容。"""
        # 直接清空字典
        self._cache.clear()

    # 这个方法创建一个子缓存，子缓存有给定的名字
    def child(self, name: str) -> PipelineCache:
        """创建一个具有给定名称的子缓存对象。"""
        # 返回一个新的InMemoryCache实例，名字是传入的名字
        return InMemoryCache(name)

    # 这个方法为给定的键创建一个缓存键
    def _create_cache_key(self, key: str) -> str:
        """根据给定的键创建一个缓存键。"""
        # 在原键前加上缓存的名字，形成新的缓存键
        return f"{self._name}{key}"

# 定义一个函数叫做create_memory_cache，它不会接收任何输入参数，并返回一个PipelineCache类型的值。
def create_memory_cache() -> PipelineCache:

    # 这个函数的作用是创建一个内存中的缓存。缓存就像一个临时的存储空间，能快速取回之前保存的数据。
    """Create a memory cache."""

    # 现在我们创建一个名为InMemoryCache的对象，这个对象代表了内存中的缓存。
    # InMemoryCache是一个特定类型的缓存，它把数据存在程序的内存里。
    return InMemoryCache()


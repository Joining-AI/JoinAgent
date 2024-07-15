# 导入一个叫做Any的类型，这个类型可以代表任何数据类型
from typing import Any

# 从.file_pipeline_storage模块导入FilePipelineStorage类，这是一个关于文件处理的类
from .file_pipeline_storage import FilePipelineStorage

# 从.typing模块导入PipelineStorage，这可能是一个用来存储管道数据的接口或基类
from .typing import PipelineStorage

# 这是一个版权信息，表示这段代码是微软公司2024年的作品
# 注：实际年份可能需要更新，这里假设是未来的年份
# Licensed under the MIT License 表示代码遵循MIT许可证，允许他人自由使用、修改和分享

# 这是一个文档字符串，描述了这个模块包含了一个名为'InMemoryStorage'的模型
# "A module containing 'InMemoryStorage' model."

# 再次导入Any类型，虽然之前已经导入过，但这里再次引入是为了确保代码的清晰性
from typing import Any

# 定义一个叫做MemoryPipelineStorage的类，它继承自FilePipelineStorage
class MemoryPipelineStorage(FilePipelineStorage):
    """这是一个用来存储数据在内存中的类定义。"""

    # _storage 是一个字典，用于保存数据
    _storage: dict[str, Any]

    # 初始化方法，当创建新对象时会运行
    def __init__(self):
        """初始化方法，设置根目录为 '.output'"""
        # 调用父类的初始化方法
        super().__init__(root_dir=".output")
        # 创建一个空字典来保存数据
        self._storage = {}

    # 获取指定键(key)的值，可以以字节或字符串形式返回
    async def get(
        self, key: str, as_bytes: bool | None = None, encoding: str | None = None
    ) -> Any:
        """获取键为key的值。

        参数：
            - key - 要获取的值的键。
            - as_bytes - 是否将值作为字节返回。

        返回：
            - output - 指定键的值。
        """
        # 首先尝试从内存中获取值，如果不存在则从父类中获取
        return self._storage.get(key) or await super().get(key, as_bytes, encoding)

    # 设置指定键(key)的值
    async def set(
        self, key: str, value: str | bytes | None, encoding: str | None = None
    ) -> None:
        """设置键为key的值。

        参数：
            - key - 要设置值的键。
            - value - 要设置的新值。
        """
        # 将值存入内存字典
        self._storage[key] = value

    # 检查指定键(key)是否存在
    async def has(self, key: str) -> bool:
        """检查键是否存在于存储中。

        参数：
            - key - 要检查的键。

        返回：
            - output - 如果键存在返回True，否则返回False。
        """
        # 首先检查内存中是否有键，如果没有再从父类中检查
        return key in self._storage or await super().has(key)

    # 删除指定键(key)
    async def delete(self, key: str) -> None:
        """从存储中删除键。

        参数：
            - key - 要删除的键。
        """
        # 从内存字典中删除键
        del self._storage[key]

    # 清除所有存储的数据
    async def clear(self) -> None:
        """清除存储的所有内容。"""
        # 清空内存字典
        self._storage.clear()

    # 创建一个新的子存储实例
    def child(self, name: str | None) -> "PipelineStorage":
        """创建一个子存储对象实例。"""
        return self

# 定义一个函数，用于创建内存存储对象
def create_memory_storage() -> PipelineStorage:
    """创建内存存储对象。"""
    # 返回MemoryPipelineStorage的实例
    return MemoryPipelineStorage()


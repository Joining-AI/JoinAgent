# 导入json模块，它帮助我们处理数据，像JavaScript的对象一样
import json

# from typing import Any 这行代码告诉Python，这里的Any可以代表任何类型的数据
from typing import Any

# 从graphrag.index.storage导入PipelineStorage类，这是一个用来存储东西的工具
from graphrag.index.storage import PipelineStorage

# 从当前文件夹下的pipeline_cache模块导入PipelineCache类，这个类可能用来缓存数据
from .pipeline_cache import PipelineCache

# 这行代码是版权信息，说明代码由微软公司创建，使用了MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个注释，告诉我们这个模块包含一个叫做'FilePipelineCache'的模型
# "A module containing 'FilePipelineCache' model."

# 定义一个名为JsonPipelineCache的类，它继承自PipelineCache
class JsonPipelineCache(PipelineCache):
    # 这个类是关于文件管道缓存的
    """File pipeline cache class definition."""

    # 定义两个成员变量，_storage用来存储数据，_encoding用来指定字符编码
    _storage: PipelineStorage
    _encoding: str

    # 初始化方法，当创建JsonPipelineCache对象时会调用
    def __init__(self, storage: PipelineStorage, encoding="utf-8"):
        # 将传入的storage对象赋值给成员变量
        self._storage = storage
        # 如果没有指定编码，默认使用utf-8
        self._encoding = encoding

    # 获取方法，用于从缓存中获取数据
    async def get(self, key: str) -> str | None:
        # 检查key是否存在
        if await self.has(key):
            # 尝试从存储中获取数据并解码
            try:
                data = await self._storage.get(key, encoding=self._encoding)
                # 使用json库将字符串转换为字典
                data = json.loads(data)
                # 返回字典中的"result"键对应的值
                return data.get("result")
            # 如果解码时出错，删除这个key
            except UnicodeDecodeError:
                await self._storage.delete(key)
                return None
            # 如果解析json时出错，也删除这个key
            except json.decoder.JSONDecodeError:
                await self._storage.delete(key)
                return None
        # 如果key不存在，返回None
        return None

    # 设置方法，用于将数据存入缓存
    async def set(self, key: str, value: Any, debug_data: dict | None = None) -> None:
        # 如果value为空，直接返回
        if value is None:
            return
        # 创建一个字典，包含"result"键和value，以及可能的debug_data
        data = {"result": value, **(debug_data or {})}
        # 将数据序列化为json字符串并存储
        await self._storage.set(key, json.dumps(data), encoding=self._encoding)

    # 检查方法，用于检查key是否存在于缓存中
    async def has(self, key: str) -> bool:
        # 返回key在存储中是否存在
        return await self._storage.has(key)

    # 删除方法，用于从缓存中删除数据
    async def delete(self, key: str) -> None:
        # 如果key存在，就删除它
        if await self.has(key):
            await self._storage.delete(key)

    # 清除方法，用于清空整个缓存
    async def clear(self) -> None:
        # 调用存储对象的clear方法来清空缓存
        await self._storage.clear()

    # 子对象方法，用于创建JsonPipelineCache的子对象
    def child(self, name: str) -> "JsonPipelineCache":
        # 返回一个新的JsonPipelineCache对象，它的存储对象是当前对象的子存储
        return JsonPipelineCache(self._storage.child(name), encoding=self._encoding)


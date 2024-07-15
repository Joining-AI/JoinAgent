# 导入日志模块，用于记录程序运行信息
import logging

# 导入操作系统模块，处理文件和目录操作
import os

# 导入正则表达式模块，进行文本模式匹配
import re

# 导入shutil模块，提供高级文件操作，如复制、移动等
import shutil

# 导入迭代器抽象基类，确保某些对象可以迭代
from collections.abc import Iterator

# 导入Path模块，方便地处理文件路径
from pathlib import Path

# 类型注解，导入Any表示任意类型，cast用于类型转换
from typing import Any, cast

# 异步文件操作模块
import aiofiles

# 从aiofiles导入异步删除文件函数
from aiofiles.os import remove

# 从aiofiles导入异步检查文件或目录是否存在函数
from aiofiles.ospath import exists

# 导入数据形状模块，用于显示进度条
from datashaper import Progress

# 导入进度报告器，跟踪任务进度
from graphrag.index.progress import ProgressReporter

# 从当前模块的typing子模块导入PipelineStorage类型定义
from .typing import PipelineStorage

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块包含了'FileStorage'和'FilePipelineStorage'两个模型的定义
# 注释中的三个引号开始和结束表示这是一个多行字符串，通常用于文档说明

# 初始化日志模块，获取当前模块的日志记录器
log = logging.getLogger(__name__)

# 这个代码定义了一个名为FilePipelineStorage的类，它用来管理文件存储。
class FilePipelineStorage(PipelineStorage):
    # 类的描述
    """File storage class definition."""

    # 定义了两个变量，一个是根目录（_root_dir），另一个是编码（_encoding）
    _root_dir: str
    _encoding: str

    # 初始化方法，当创建类的实例时会执行
    def __init__(self, root_dir: str | None = None, encoding: str | None = None):
        # 如果没有提供根目录，就设为空字符串
        self._root_dir = root_dir or ""
        # 如果没有提供编码，就设为"utf-8"
        self._encoding = encoding or "utf-8"
        # 创建或确认根目录存在
        Path(self._root_dir).mkdir(parents=True, exist_ok=True)

    # 查找方法，根据文件模式和自定义过滤函数在存储中查找文件
    def find(
        self,
        file_pattern: re.Pattern[str],
        base_dir: str | None = None,
        progress: ProgressReporter | None = None,
        file_filter: dict[str, Any] | None = None,
        max_count=-1,
    ) -> Iterator[tuple[str, dict[str, Any]]]:
        # 定义一个内部函数，用于检查文件是否符合过滤条件
        def item_filter(item: dict[str, Any]) -> bool:
            # 如果没有提供过滤器，所有文件都符合条件
            if file_filter is None:
                return True

            # 检查文件名是否与过滤器中的模式匹配
            return all(re.match(value, item[key]) for key, value in file_filter.items())

        # 计算搜索路径
        search_path = Path(self._root_dir) / (base_dir or "")
        # 打印日志信息，显示正在查找的路径和模式
        log.info("search %s for files matching %s", search_path, file_pattern.pattern)
        # 获取所有文件
        all_files = list(search_path.rglob("**/*"))
        # 初始化计数器
        num_loaded = 0
        num_total = len(all_files)
        num_filtered = 0
        # 遍历所有文件
        for file in all_files:
            # 匹配文件名和模式
            match = file_pattern.match(f"{file}")
            # 如果匹配成功
            if match:
                # 提取匹配组
                group = match.groupdict()
                # 检查文件是否通过过滤器
                if item_filter(group):
                    # 获取相对路径
                    filename = f"{file}".replace(self._root_dir, "")
                    # 去掉开头的路径分隔符
                    if filename.startswith(os.sep):
                        filename = filename[1:]
                    # 返回文件名和匹配组
                    yield (filename, group)
                    num_loaded += 1
                    # 如果达到最大数量，停止查找
                    if max_count > 0 and num_loaded >= max_count:
                        break
                else:
                    num_filtered += 1
            else:
                num_filtered += 1
            # 更新进度报告（如果提供了）
            if progress is not None:
                progress(_create_progress_status(num_loaded, num_filtered, num_total))

    # 获取方法，根据键获取文件内容
    async def get(
        self, key: str, as_bytes: bool | None = False, encoding: str | None = None
    ) -> Any:
        # 获取文件路径
        file_path = join_path(self._root_dir, key)

        # 如果文件存在于存储中
        if await self.has(key):
            # 读取文件内容并返回
            return await self._read_file(file_path, as_bytes, encoding)
        # 如果文件存在于输入中但尚未写入存储
        elif await exists(key):
            return await self._read_file(key, as_bytes, encoding)

        # 文件不存在，返回None
        return None

    # 内部方法，读取文件内容
    async def _read_file(
        self,
        path: str | Path,
        as_bytes: bool | None = False,
        encoding: str | None = None,
    ) -> Any:
        # 根据需要以二进制或文本模式打开文件
        read_type = "rb" if as_bytes else "r"
        encoding = None if as_bytes else (encoding or self._encoding)

        # 异步读取文件内容并返回
        async with aiofiles.open(
            path,
            cast(Any, read_type),
            encoding=encoding,
        ) as f:
            return await f.read()

    # 设置方法，将值写入文件
    async def set(self, key: str, value: Any, encoding: str | None = None) -> None:
        # 判断值是否为字节类型
        is_bytes = isinstance(value, bytes)
        # 根据需要以二进制或文本模式写入文件
        write_type = "wb" if is_bytes else "w"
        encoding = None if is_bytes else encoding or self._encoding
        # 异步写入文件
        async with aiofiles.open(
            join_path(self._root_dir, key), cast(Any, write_type), encoding=encoding
        ) as f:
            await f.write(value)

    # 检查方法，检查文件是否存在
    async def has(self, key: str) -> bool:
        # 检查文件路径是否存在
        return await exists(join_path(self._root_dir, key))

    # 删除方法，删除文件
    async def delete(self, key: str) -> None:
        # 如果文件存在，删除它
        if await self.has(key):
            await remove(join_path(self._root_dir, key))

    # 清除方法，删除存储中的所有文件
    async def clear(self) -> None:
        # 遍历根目录下的所有文件和子目录
        for file in Path(self._root_dir).glob("*"):
            # 如果是目录，递归删除
            if file.is_dir():
                shutil.rmtree(file)
            # 如果是文件，删除它
            else:
                file.unlink()

    # 创建子存储实例的方法
    def child(self, name: str | None) -> "PipelineStorage":
        # 如果没有提供子目录名，返回当前实例
        if name is None:
            return self
        # 创建新的FilePipelineStorage实例，根目录为当前目录下新子目录
        return FilePipelineStorage(str(Path(self._root_dir) / Path(name)))

# 定义一个函数，把文件路径和文件名组合在一起，不管在什么操作系统上都能用。
def join_path(file_path: str, file_name: str) -> Path:
    """把路径和文件名合成为一个完整的路径"""
    # 使用Path对象来处理路径，先将文件名的目录部分和文件名分开，然后与原始路径连接
    return Path(file_path) / Path(file_name).parent / Path(file_name).name

# 定义另一个函数，创建一个基于文件的存储系统。
def create_file_storage(out_dir: str | None) -> PipelineStorage:
    """创建一个存储数据到文件的工具"""
    # 打印一条信息，告诉用户我们将在哪里创建文件存储
    log.info("创建文件存储在 %s", out_dir)
    # 返回一个FilePipelineStorage对象，它会把数据存储在指定的目录里
    return FilePipelineStorage(out_dir)

# 私有（内部）函数，用来创建进度状态报告。
def _create_progress_status(
    num_loaded: int, num_filtered: int, num_total: int
) -> Progress:
    # 创建一个Progress对象，表示加载了多少文件，过滤了多少，总共有多少
    return Progress(
        # 设置总项目数
        total_items=num_total,
        # 设置已完成的项目数（加载的加上被过滤的）
        completed_items=num_loaded + num_filtered,
        # 描述加载了多少文件，过滤了多少
        description=f"{num_loaded} 个文件已加载 ({num_filtered} 个被过滤)",
    )


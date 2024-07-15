# 导入日志模块，用于记录程序运行情况
import logging

# 从collections.abc模块导入Awaitable和Callable，它们是Python中关于异步操作和可调用对象的抽象基类
from collections.abc import Awaitable, Callable

# 导入Path模块，用于处理文件路径
from pathlib import Path

# 导入typing模块的cast函数，用于类型转换
from typing import cast

# 导入pandas库，用于数据处理
import pandas as pd

# 从graphrag.config模块导入InputConfig和InputType，它们可能定义了输入配置和输入类型的类
from graphrag.config import InputConfig, InputType

# 从graphrag.index.config模块导入PipelineInputConfig，可能是管道输入配置的类
from graphrag.index.config import PipelineInputConfig

# 从graphrag.index.progress模块导入NullProgressReporter和ProgressReporter，用于报告进度
from graphrag.index.progress import NullProgressReporter, ProgressReporter

# 从graphrag.index.storage模块导入BlobPipelineStorage和FilePipelineStorage，可能是存储相关类
from graphrag.index.storage import BlobPipelineStorage, FilePipelineStorage

# 从当前目录下的.csv子模块导入input_type并重命名为csv，以及load函数并重命名为load_csv
from .csv import input_type as csv
from .csv import load as load_csv

# 从当前目录下的.text子模块导入input_type并重命名为text，以及load函数并重命名为load_text
from .text import input_type as text
from .text import load as load_text

# 这一行是版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含load_input方法的定义
"""A module containing load_input method definition."""

# 初始化日志模块，获取当前模块的日志记录器
log = logging.getLogger(__name__)

# 创建一个字典，键是数据类型（text或csv），值是加载对应类型数据的函数
# 这样可以根据数据类型调用相应的加载函数，返回一个等待异步执行的pandas DataFrame
loaders: dict[str, Callable[..., Awaitable[pd.DataFrame]]] = {
    text: load_text,
    csv: load_csv,
}

# 定义一个异步函数load_input，它接收三个参数：config（配置信息），progress_reporter（进度报告器）和root_dir（根目录）
async def load_input(
    config: PipelineInputConfig | InputConfig,  # 输入可以是PipelineInputConfig或InputConfig类型
    progress_reporter: ProgressReporter | None = None,  # 进度报告器，如果不给定则默认为None
    root_dir: str | None = None,  # 根目录字符串，如果不给定则默认为None
) -> pd.DataFrame:  # 函数返回一个pandas DataFrame

    # 如果root_dir没有给定，则设置为空字符串
    root_dir = root_dir or ""

    # 使用日志打印信息，加载输入数据，根目录是config的base_dir
    log.info("loading input from root_dir=%s", config.base_dir)

    # 如果progress_reporter没有给定，就设置为NullProgressReporter，即不进行进度报告
    progress_reporter = progress_reporter or NullProgressReporter()

    # 如果config不存在，抛出一个ValueError，并附带错误信息
    if config is None:
        msg = "No input specified!"
        raise ValueError(msg)

    # 使用匹配表达式，根据config的type属性选择不同的处理方式
    match config.type:
        # 如果是Blob类型
        case InputType.blob:
            # 打印日志，使用Blob存储输入
            log.info("using blob storage input")

            # 检查Blob存储需要的参数是否齐全
            if config.container_name is None:
                msg = "Container name required for blob storage"
                raise ValueError(msg)
            if (
                config.connection_string is None
                and config.storage_account_blob_url is None
            ):
                msg = "Connection string or storage account blob url required for blob storage"
                raise ValueError(msg)

            # 创建BlobPipelineStorage对象
            storage = BlobPipelineStorage(
                connection_string=config.connection_string,
                storage_account_blob_url=config.storage_account_blob_url,
                container_name=config.container_name,
                path_prefix=config.base_dir,
            )
        # 如果是File类型
        case InputType.file:
            # 打印日志，使用文件存储输入
            log.info("using file storage for input")

            # 创建FilePipelineStorage对象
            storage = FilePipelineStorage(
                root_dir=str(Path(root_dir) / (config.base_dir or ""))
            )
        # 其他未知类型
        case _:
            # 打印日志，使用文件存储输入
            log.info("using file storage for input")

            # 创建FilePipelineStorage对象
            storage = FilePipelineStorage(
                root_dir=str(Path(root_dir) / (config.base_dir or ""))
            )

    # 检查config的file_type是否在loaders字典中
    if config.file_type in loaders:
        # 创建进度条子任务
        progress = progress_reporter.child(
            f"Loading Input ({config.file_type})", transient=False
        )
        # 获取对应file_type的加载器
        loader = loaders[config.file_type]
        # 异步调用加载器加载数据
        results = await loader(config, progress, storage)
        # 将结果转换为DataFrame并返回
        return cast(pd.DataFrame, results)

    # 如果file_type未知，抛出一个ValueError，并附带错误信息
    msg = f"Unknown input type {config.file_type}"
    raise ValueError(msg)


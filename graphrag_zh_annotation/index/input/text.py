# 导入日志模块，用来记录程序运行情况
import logging

# 导入正则表达式模块，用于匹配文件名
import re

# 导入Path模块，方便处理文件路径
from pathlib import Path

# 导入类型提示模块，让代码更清晰
from typing import Any

# 导入pandas库，用于处理数据
import pandas as pd

# 导入自定义配置类
from graphrag.index.config import PipelineInputConfig

# 导入进度报告类
from graphrag.index.progress import ProgressReporter

# 导入存储管理类
from graphrag.index.storage import PipelineStorage

# 导入生成MD5哈希值的工具函数
from graphrag.index.utils import gen_md5_hash

# 版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个包含加载方法定义的模块

# 定义一个正则表达式模式，用于匹配特定格式的文件名
DEFAULT_FILE_PATTERN = re.compile(
    r".*[\\/](?P<source>[^\\/]+)[\\/](?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_(?P<author>[^_]+)_\d+\.txt"
)

# 输入类型为文本
input_type = "text"

# 获取当前模块的日志记录器
log = logging.getLogger(__name__)

# 异步加载函数，从目录中加载文本输入
async def load(
    config: PipelineInputConfig,  # 加载配置
    progress: ProgressReporter | None,  # 进度报告器，可能为空
    storage: PipelineStorage,  # 存储管理器
) -> pd.DataFrame:  # 返回一个数据框

    # 内部异步函数，加载单个文件
    async def load_file(
        path: str,  # 文件路径
        group: dict | None = None,  # 可选的分组信息，默认为空字典
        _encoding: str = "utf-8",  # 编码方式，默认为UTF-8
    ) -> dict[str, Any]:  # 返回一个键值对字典

        # 如果没有分组信息，创建一个空字典
        if group is None:
            group = {}

        # 从存储中获取文件内容
        text = await storage.get(path, encoding="utf-8")

        # 更新字典，添加文本内容
        new_item = {**group, "text": text}

        # 生成MD5哈希作为唯一ID
        new_item["id"] = gen_md5_hash(new_item, new_item.keys())

        # 设置文件名作为标题
        new_item["title"] = str(Path(path).name)

        # 返回更新后的字典
        return new_item

    # 查找符合配置文件模式的文件
    files = list(
        storage.find(
            re.compile(config.file_pattern),  # 根据配置的文件模式查找
            progress=progress,  # 使用进度报告器
            file_filter=config.file_filter,  # 使用配置的文件过滤器
        )
    )

    # 如果没找到任何文件，抛出错误
    if len(files) == 0:
        msg = f"No text files found in {config.base_dir}"
        raise ValueError(msg)

    # 打印找到的文件信息
    found_files = f"found text files from {config.base_dir}, found {files}"
    log.info(found_files)

    # 异步加载每个文件，将结果放入数据框
    return pd.DataFrame([await load_file(file, group) for file, group in files])


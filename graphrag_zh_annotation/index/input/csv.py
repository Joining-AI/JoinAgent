# 导入logging模块，用于记录程序运行日志
import logging

# 导入正则表达式模块，用于处理和匹配字符串
import re

# 导入BytesIO，它是Python中的一个内存I/O流对象，用于处理字节数据
from io import BytesIO

# 从typing模块导入cast函数，用于类型转换
from typing import cast

# 导入pandas库，用于数据处理和分析
import pandas as pd

# 从graphrag.index.config导入两个配置类：PipelineCSVInputConfig和PipelineInputConfig
from graphrag.index.config import PipelineCSVInputConfig, PipelineInputConfig

# 从graphrag.index.progress导入ProgressReporter类，可能用于报告进度信息
from graphrag.index.progress import ProgressReporter

# 从graphrag.index.storage导入PipelineStorage类，可能用于存储数据管道
from graphrag.index.storage import PipelineStorage

# 从graphrag.index.utils导入gen_md5_hash函数，用于生成MD5哈希值
from graphrag.index.utils import gen_md5_hash

# 这是版权信息，表示代码归微软公司所有
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个模块的文档字符串，描述了这个模块包含的内容
"""这是一个包含加载方法定义的模块。"""

# 创建一个日志器，名为当前模块的名称，用于记录程序运行时的信息
log = logging.getLogger(__name__)

# 定义一个默认的文件模式正则表达式，用于匹配以.csv结尾的文件名
DEFAULT_FILE_PATTERN = re.compile(r"(?P<filename>[^\\/]).csv$")

# 定义一个变量input_type，其值为"csv"，可能代表数据的输入格式
input_type = "csv"

# 这个函数叫做load，它会加载csv文件并做一些处理。它需要三个参数：
# config：包含有关如何加载文件的信息，
# progress：报告加载进度的对象（如果没有，就传入None），
# storage：用于从某个存储获取文件的对象。

async def load(
    config: PipelineInputConfig,
    progress: ProgressReporter | None,
    storage: PipelineStorage,
) -> pd.DataFrame:
    """从目录加载csv输入文件"""
    # 把config转换成PipelineCSVInputConfig类型，方便后面操作
    csv_config = cast(PipelineCSVInputConfig, config)
    # 打印信息，告诉我们要从哪个目录加载csv文件
    log.info("Loading csv files from %s", csv_config.base_dir)

    # 定义一个内部的异步函数load_file，它会加载单个文件并返回数据
    async def load_file(path: str, group: dict | None) -> pd.DataFrame:
        # 如果group是None，就赋值一个空字典
        if group is None:
            group = {}
        # 从storage中获取文件内容，以字节形式存入BytesIO对象
        buffer = BytesIO(await storage.get(path, as_bytes=True))
        # 使用pandas读取csv文件，如果config中有编码信息就用它，否则用"latin-1"
        data = pd.read_csv(buffer, encoding=config.encoding or "latin-1")

        # 检查额外的键是否在数据中，如果有就添加
        additional_keys = group.keys()
        if len(additional_keys) > 0:
            data[[*additional_keys]] = data.apply(
                lambda _row: pd.Series([group[key] for key in additional_keys]), axis=1
            )

        # 如果数据中没有"id"列，就生成一个
        if "id" not in data.columns:
            data["id"] = data.apply(lambda x: gen_md5_hash(x, x.keys()), axis=1)

        # 如果有source_column配置且数据中没有"source"列，就添加
        if csv_config.source_column is not None and "source" not in data.columns:
            if csv_config.source_column not in data.columns:
                log.warning(
                    "source_column %s not found in csv file %s",
                    csv_config.source_column,
                    path,
                )
            else:
                data["source"] = data.apply(
                    lambda x: x[csv_config.source_column], axis=1
                )

        # 同理，处理"text"列
        if csv_config.text_column is not None and "text" not in data.columns:
            if csv_config.text_column not in data.columns:
                log.warning(
                    "text_column %s not found in csv file %s",
                    csv_config.text_column,
                    path,
                )
            else:
                data["text"] = data.apply(lambda x: x[csv_config.text_column], axis=1)

        # 处理"title"列
        if csv_config.title_column is not None and "title" not in data.columns:
            if csv_config.title_column not in data.columns:
                log.warning(
                    "title_column %s not found in csv file %s",
                    csv_config.title_column,
                    path,
                )
            else:
                data["title"] = data.apply(lambda x: x[csv_config.title_column], axis=1)

        # 处理"timestamp"列，需要指定格式
        if csv_config.timestamp_column is not None:
            fmt = csv_config.timestamp_format
            if fmt is None:
                # 提示必须提供时间戳格式
                raise ValueError("Must specify timestamp_format if timestamp_column is specified")

            # 如果时间戳列不存在，就警告
            if csv_config.timestamp_column not in data.columns:
                log.warning(
                    "timestamp_column %s not found in csv file %s",
                    csv_config.timestamp_column,
                    path,
                )
            else:
                # 将时间戳列转换为日期时间格式
                data["timestamp"] = pd.to_datetime(data[csv_config.timestamp_column], format=fmt)

            # 从时间戳中提取年、月、日、小时、分钟、秒
            for col_name in ["year", "month", "day", "hour", "minute", "second"]:
                if col_name not in data.columns:
                    data[col_name] = data.apply(lambda x: x["timestamp"].__getattribute__(col_name), axis=1)

        # 返回处理后的数据
        return data

    # 根据config创建文件匹配模式，如果没有就用默认模式
    file_pattern = (
        re.compile(config.file_pattern)
        if config.file_pattern is not None
        else DEFAULT_FILE_PATTERN
    )
    # 在存储中查找匹配的文件，使用progress报告进度，并根据config筛选文件
    files = list(
        storage.find(
            file_pattern,
            progress=progress,
            file_filter=config.file_filter,
        )
    )

    # 如果没找到任何文件，抛出错误
    if len(files) == 0:
        msg = f"No CSV files found in {config.base_dir}"
        raise ValueError(msg)

    # 异步加载每个文件，将结果保存到列表中
    files = [await load_file(file, group) for file, group in files]
    # 打印信息，显示加载了多少csv文件
    log.info("loading %d csv files", len(files))

    # 合并所有文件的数据
    result = pd.concat(files)
    # 计算未过滤的csv行总数并打印
    total_files_log = f"Total number of unfiltered csv rows: {len(result)}"
    log.info(total_files_log)

    # 最后返回合并后的数据
    return result


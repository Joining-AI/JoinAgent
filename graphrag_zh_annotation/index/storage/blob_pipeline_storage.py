# 导入logging模块，用于记录程序运行日志
import logging

# 导入正则表达式库re，用于处理字符串模式匹配
import re

# 从collections.abc导入Iterator接口，定义迭代器行为
from collections.abc import Iterator

# 从pathlib库导入Path类，用于处理文件路径
from pathlib import Path

# 从typing库导入Any类型，表示可以是任何类型的变量
from typing import Any

# 从azure.identity库导入DefaultAzureCredential，用于获取Azure服务的身份验证凭证
from azure.identity import DefaultAzureCredential

# 从azure.storage.blob库导入BlobServiceClient，用于操作Azure Blob存储服务
from azure.storage.blob import BlobServiceClient

# 从datashaper库导入Progress类，用于显示数据处理进度
from datashaper import Progress

# 从graphrag.index.progress导入ProgressReporter类，用于报告进度
from graphrag.index.progress import ProgressReporter

# 从当前模块的typing子模块导入PipelineStorage类型
from .typing import PipelineStorage

# 注释：版权所有2024年微软公司，遵循MIT许可证

# 定义一个名为"Azure Blob Storage实现的PipelineStorage"的模块
# 这个模块用于与Azure Blob存储进行交互

# 初始化logging模块的日志记录器，名字为本文件的名字
log = logging.getLogger(__name__)



# 定义一个函数create_blob_storage，它接受四个参数
def create_blob_storage(
    # 连接字符串，可以是字符串或者None
    connection_string: str | None,
    # 存储账户的blob URL，也可以是字符串或None
    storage_account_blob_url: str | None,
    # 容器名称，必须是字符串
    container_name: str,
    # 基本目录，可以是字符串或None
    base_dir: str | None,
) -> PipelineStorage:
    # 打印日志信息，告诉我们要在哪个容器创建blob存储
    log.info("Creating blob storage at %s", container_name)

    # 检查容器名称是否为空
    if container_name is None:
        # 如果为空，抛出一个错误
        msg = "No container name provided for blob storage."
        raise ValueError(msg)

    # 检查连接字符串和存储账户的blob URL都为空
    if connection_string is None and storage_account_blob_url is None:
        # 如果都为空，抛出一个错误
        msg = "No storage account blob url provided for blob storage."
        raise ValueError(msg)

    # 创建BlobPipelineStorage对象，用到上面提供的参数
    # 这个对象代表了与blob存储的交互方式
    return BlobPipelineStorage(
        # 使用提供的连接字符串
        connection_string,
        # 使用提供的容器名称
        container_name,
        # 设置路径前缀（基本目录）
        path_prefix=base_dir,
        # 使用提供的存储账户blob URL
        storage_account_blob_url=storage_account_blob_url,
    )

# 定义一个函数，名为validate_blob_container_name，接收一个字符串参数container_name
def validate_blob_container_name(container_name: str):
    """
    检查传入的blob容器名称是否符合Azure（一个云服务）的规定。

    - 名称长度必须在3到63个字符之间。
    - 必须以字母或数字开头。
    - 名称中的所有字母必须是小写。
    - 只能包含字母、数字或连字符（-）。
    - 不允许有连续的连字符。
    - 不能以连字符结尾。

    参数:
    ------
    container_name (str)
        需要验证的blob容器名称。

    返回值:
    --------
        bool: 如果有效则返回True，否则返回False。
    """
    # 检查名称的长度
    if len(container_name) < 3 或 len(container_name) > 63:
        # 如果长度不对，返回一个错误信息
        return ValueError(
            f"容器名称必须在3到63个字符之间。提供的名称长度为{len(container_name)}个字符。"
        )

    # 检查名称是否以字母或数字开头
    if not container_name[0].isalnum():
        # 如果不是，返回一个错误信息
        return ValueError(
            f"容器名称必须以字母或数字开头。起始字符为{container_name[0]}。"
        )

    # 使用正则表达式检查名称是否只包含有效的字符（小写字母、数字和连字符）
    if not re.match("^[a-z0-9-]+$", container_name):
        # 如果不匹配，返回一个错误信息
        return ValueError(
            f"容器名称必须只包含以下内容：
            \n- 小写字母
            \n- 数字
            \n- 或连字符
            \n提供的名称为{container_name}。"
        )

    # 检查名称中是否有连续的连字符
    if "--" in container_name:
        # 如果有，返回一个错误信息
        return ValueError(
            f"容器名称不能包含连续的连字符。提供的名称为{container_name}。"
        )

    # 检查名称是否以连字符结尾
    if container_name[-1] == "-":
        # 如果是，返回一个错误信息
        return ValueError(
            f"容器名称不能以连字符结尾。提供的名称为{container_name}。"
        )

    # 如果通过了所有检查，返回True表示名称有效
    return True

# 定义一个函数，叫_create_progress_status，它需要3个整数作为输入参数
# num_loaded: 已加载的文件数量
# num_filtered: 被过滤掉的文件数量
# num_total: 总共的文件数量
def _create_progress_status(num_loaded, num_filtered, num_total):
    # 创建一个Progress对象，它会告诉我们在进度方面的一些信息
    # total_items: 设置总项目数为总数num_total
    # completed_items: 设置已完成的项目数为已加载和被过滤的文件数之和
    # description: 设置描述信息，显示已加载和被过滤的文件数
    return Progress(
        total_items=num_total,            # 总文件数
        completed_items=num_loaded + num_filtered,  # 已处理（加载+过滤）的文件数
        description=f"{num_loaded} files loaded ({num_filtered} filtered)",  # 显示加载和过滤的文件数
    )


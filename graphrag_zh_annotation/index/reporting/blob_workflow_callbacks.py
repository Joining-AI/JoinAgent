# 导入json模块，它帮助我们将数据转换成一种叫做JSON的格式，电脑能轻松理解
import json

# 导入datetime和timezone模块，它们用来处理日期和时间
from datetime import datetime, timezone

# 导入pathlib模块，它让我们可以方便地处理文件路径
from pathlib import Path

# 从typing模块导入Any，这是一个类型提示，表示变量可能包含任何类型的数据
from typing import Any

# 导入DefaultAzureCredential，这是Azure身份验证的一种方式，让我们可以安全地连接到Azure服务
from azure.identity import DefaultAzureCredential

# 导入BlobServiceClient，这是Azure存储库的一部分，用于与Azure Blob存储交互
from azure.storage.blob import BlobServiceClient

# 导入NoopWorkflowCallbacks，这是一个数据处理工具，它不做任何操作，只是个占位符
from datashaper import NoopWorkflowCallbacks

# 这是程序的开头，它包含一个版权声明和许可证信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个文档字符串，描述了这个程序的功能，它是写入Blob存储的报告器
"""
A reporter that writes to a blob storage.
"""

# 定义一个类，叫做BlobWorkflowCallbacks，它继承自NoopWorkflowCallbacks
class BlobWorkflowCallbacks(NoopWorkflowCallbacks):
    # 这个类用来向一个叫做“blob存储”的地方报告信息
    """A reporter that writes to a blob storage."""

    # 这些是类的属性，用来保存一些信息
    _blob_service_client: BlobServiceClient  # 存储服务客户端
    _container_name: str  # 容器的名字
    _max_block_count: int = 25000  # 每个blob能有的最大块数，这里是25000

    # 这个方法叫做构造函数，用来创建BlobWorkflowCallbacks的实例
    def __init__(
        self,
        connection_string: str | None,  # 存储账户连接字符串
        container_name: str,  # 容器名字
        blob_name: str = "",  # blob的默认名字
        base_dir: str | None = None,  # 基础目录
        storage_account_blob_url: str | None = None,  # 存储账户blob的URL
    ):  # type: ignore
        # 如果没有提供容器名字，就抛出错误
        if container_name is None:
            msg = "No container name provided for blob storage."
            raise ValueError(msg)
        # 如果没有提供连接字符串和存储账户blob URL，也抛出错误
        if connection_string is None and storage_account_blob_url is None:
            msg = "No storage account blob url provided for blob storage."
            raise ValueError(msg)

        # 保存连接字符串和存储账户blob URL
        self._connection_string = connection_string
        self._storage_account_blob_url = storage_account_blob_url

        # 根据是否有连接字符串来创建BlobServiceClient
        if self._connection_string:
            self._blob_service_client = BlobServiceClient.from_connection_string(
                self._connection_string
            )
        else:
            # 如果没有连接字符串，但有存储账户blob URL，就用这个URL创建BlobServiceClient
            if storage_account_blob_url is None:
                msg = "Either connection_string or storage_account_blob_url must be provided."
                raise ValueError(msg)

            self._blob_service_client = BlobServiceClient(
                storage_account_blob_url,
                credential=DefaultAzureCredential(),  # 使用默认的认证方式
            )

        # 如果blob名字为空，就设置一个默认的名字，包含当前日期和时间
        if blob_name == "":
            blob_name = f"report/{datetime.now(tz=timezone.utc).strftime('%Y-%m-%d-%H:%M:%S:%f')}.logs.json"

        # 将blob名字和基础目录结合，保存为一个字符串
        self._blob_name = str(Path(base_dir or "") / blob_name)
        self._container_name = container_name  # 保存容器名字

        # 获取blob客户端，用来操作特定的blob
        self._blob_client = self._blob_service_client.get_blob_client(
            self._container_name, self._blob_name
        )

        # 如果blob不存在，就创建它
        if not self._blob_client.exists():
            self._blob_client.create_append_blob()

        # 初始化块计数器
        self._num_blocks = 0  # refresh block counter

    # 这个方法用来写日志到blob
    def _write_log(self, log: dict[str, Any]):
        # 当块计数接近25000时，创建新的文件
        if (
            self._num_blocks >= self._max_block_count
        ):  # 检查是否超过25000块
            # 重新初始化类，创建新的blob
            self.__init__(
                self._connection_string,
                self._container_name,
                storage_account_blob_url=self._storage_account_blob_url,
            )

        # 获取blob客户端，写入日志
        blob_client = self._blob_service_client.get_blob_client(
            self._container_name, self._blob_name
        )
        blob_client.append_block(json.dumps(log) + "\n")  # 将日志转为JSON并添加换行符

        # 更新块计数
        self._num_blocks += 1

    # 当发生错误时，报告错误
    def on_error(
        self,
        message: str,  # 错误信息
        cause: BaseException | None = None,  # 错误原因
        stack: str | None = None,  # 错误堆栈
        details: dict | None = None,  # 错误详情
    ):
        # 将错误信息写入日志
        self._write_log({
            "type": "error",
            "data": message,
            "cause": str(cause),
            "stack": stack,
            "details": details,
        })

    # 当发生警告时，报告警告
    def on_warning(self, message: str, details: dict | None = None):
        # 将警告信息写入日志
        self._write_log({"type": "warning", "data": message, "details": details})

    # 当需要记录普通日志时
    def on_log(self, message: str, details: dict | None = None):
        # 将普通日志信息写入日志
        self._write_log({"type": "log", "data": message, "details": details})


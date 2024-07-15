# 导入Path模块，用于处理文件路径
from pathlib import Path
# 导入cast函数，用于类型转换
from typing import cast
# 导入WorkflowCallbacks类，用于数据流程回调
from datashaper import WorkflowCallbacks
# 导入ReportingType枚举，表示报告类型
from graphrag.config import ReportingType
# 导入不同类型的报告配置
from graphrag.index.config import PipelineBlobReportingConfig, PipelineFileReportingConfig, PipelineReportingConfig
# 导入不同类型的回调类
from .blob_workflow_callbacks import BlobWorkflowCallbacks
from .console_workflow_callbacks import ConsoleWorkflowCallbacks
from .file_workflow_callbacks import FileWorkflowCallbacks

# 版权声明和许可信息
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义加载管道报告器的方法
def load_pipeline_reporter(config=None, root_dir=None) -> WorkflowCallbacks:
    """根据给定的管道配置创建一个报告器"""
    
    # 如果没有提供配置，就使用默认的PipelineFileReportingConfig，报告目录为'reports'
    config = config or PipelineFileReportingConfig(base_dir="reports")

    # 根据配置的类型进行匹配
    match config.type:
        # 如果是文件报告类型
        case ReportingType.file:
            # 类型转换为PipelineFileReportingConfig
            config = cast(PipelineFileReportingConfig, config)
            # 创建并返回FileWorkflowCallbacks实例，路径为root_dir（如果提供）或空字符串与配置的base_dir组合
            return FileWorkflowCallbacks(str(Path(root_dir or "") / (config.base_dir or "")))
        # 如果是控制台报告类型
        case ReportingType.console:
            # 返回ConsoleWorkflowCallbacks实例
            return ConsoleWorkflowCallbacks()
        # 如果是Blob（云存储）报告类型
        case ReportingType.blob:
            # 类型转换为PipelineBlobReportingConfig
            config = cast(PipelineBlobReportingConfig, config)
            # 创建并返回BlobWorkflowCallbacks实例，包含连接字符串、容器名和可选的基础目录和存储账户URL
            return BlobWorkflowCallbacks(
                config.connection_string,
                config.container_name,
                base_dir=config.base_dir,
                storage_account_blob_url=config.storage_account_blob_url,
            )
        # 其他未知类型
        case _:
            # 构造错误消息并抛出ValueError
            msg = f"未知的报告类型：{config.type}"
            raise ValueError(msg)


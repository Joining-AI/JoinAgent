# 导入模块，这些模块帮助我们处理不同类型的存储
from .blob_pipeline_storage import BlobPipelineStorage, create_blob_storage
# BlobPipelineStorage 是用于云存储的类
# create_blob_storage 是创建云存储的函数

from .file_pipeline_storage import FilePipelineStorage
# FilePipelineStorage 是用于文件系统存储的类

from .load_storage import load_storage
# load_storage 是加载存储的函数

from .memory_pipeline_storage import MemoryPipelineStorage
# MemoryPipelineStorage 是用于内存中存储的类

from .typing import PipelineStorage
# PipelineStorage 是一个类型定义，表示存储管道的类型

# 这是微软公司的一个程序，遵循MIT许可证
# 注释：这是索引引擎存储包的主文件

# 再次导入之前的部分，确保在本文件的"所有公开内容"列表中
from .blob_pipeline_storage import BlobPipelineStorage, create_blob_storage
from .file_pipeline_storage import FilePipelineStorage
from .load_storage import load_storage
from .memory_pipeline_storage import MemoryPipelineStorage
from .typing import PipelineStorage

# __all__ 列表告诉别人这个模块导出哪些内容
# 这里包括了各种存储类和函数
__all__ = [
    "BlobPipelineStorage",
    "FilePipelineStorage",
    "MemoryPipelineStorage",
    "PipelineStorage",
    "create_blob_storage",
    "load_storage",
]


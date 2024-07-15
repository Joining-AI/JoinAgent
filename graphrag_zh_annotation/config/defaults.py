# 导入一个叫做AsyncType的特殊类型，它来自一个叫做datashaper的库
from datashaper import AsyncType

# 从当前文件夹下的enums模块中导入多个枚举类型
# 枚举类型是用来定义一组相关的常量，这里包括：
# CacheType: 有关缓存的类型
# InputFileType: 输入文件的类型
# InputType: 输入数据的类型
# LLMType: 可能是指大型语言模型的类型
# ReportingType: 报告或输出类型的分类
# StorageType: 存储方式的类型
# TextEmbeddingTarget: 文本嵌入的目标，可能与处理文本数据相关
from .enums import (
    CacheType,
    InputFileType,
    InputType,
    LLMType,
    ReportingType,
    StorageType,
    TextEmbeddingTarget,
)

# 这段代码是Python写的，它设置了一些默认的配置参数。
# 注意：这是示例解释，尽量简化了，有些细节可能未涵盖。

# 这两行是版权信息和许可证说明
# Copyright (c) 2024 Microsoft Corporation. 表明代码由微软公司拥有版权
# Licensed under the MIT License 表明使用的是MIT许可证，允许他人自由使用、修改和分发代码

# 导入所需模块
from datashaper import AsyncType  # 引入异步类型定义
from .enums import (  # 引入一系列枚举类型
    CacheType, InputFileType, InputType, LLMType, ReportingType, StorageType, TextEmbeddingTarget,
)

# 定义一些常量
ASYNC_MODE = AsyncType.Threaded  # 异步模式，使用线程处理
ENCODING_MODEL = "cl100k_base"  # 文本编码模型的名称

# 以下是一些关于语言模型（LLM）的参数
LLM_TYPE = LLMType.OpenAIChat  # 使用的语言模型类型
LLM_MODEL = "gpt-4-turbo-preview"  # 具体的语言模型名字
# ... 更多LLM相关参数，如最大令牌数、温度、top_p等

# 文本嵌入参数
EMBEDDING_TYPE = LLMType.OpenAIEmbedding  # 嵌入类型
EMBEDDING_MODEL = "text-embedding-3-small"  # 嵌入模型
EMBEDDING_BATCH_SIZE = 16  # 批次大小
# ... 更多文本嵌入参数

# 缓存、文件处理和其他参数
CACHE_TYPE = CacheType.file  # 缓存类型
CACHE_BASE_DIR = "cache"  # 缓存目录
# ... 更多关于文件处理的参数

# 报告、社区报告、实体提取等参数
CLAIM_DESCRIPTION = "..."  # 描述信息
CLAIM_MAX_GLEANINGS = 1  # 最大提取信息数
# ... 更多相关参数

# 输入文件类型、输入目录、编码等
INPUT_FILE_TYPE = InputFileType.text  # 文件类型
INPUT_TYPE = InputType.file  # 输入类型
INPUT_BASE_DIR = "input"  # 输入文件目录
# ... 更多输入处理参数

# 并行处理、节点2向量、报告生成等参数
PARALLELIZATION_STAGGER = 0.3  # 并行处理延迟
PARALLELIZATION_NUM_THREADS = 50  # 并行处理线程数
# ... 更多并行处理和报告生成参数

# 本地搜索和全局搜索参数
LOCAL_SEARCH_TEXT_UNIT_PROP = 0.5  # 本地搜索文本单元比例
LOCAL_SEARCH_CONVERSATION_HISTORY_MAX_TURNS = 5  # 对话历史最大轮数
GLOBAL_SEARCH_MAX_TOKENS = 12_000  # 全局搜索最大令牌数
# ... 更多搜索相关参数

# 存储类型和目录
STORAGE_TYPE = StorageType.file  # 存储类型
STORAGE_BASE_DIR = "output/${timestamp}/artifacts"  # 存储目录


# 导入未来的注解功能，让Python 3.7以下版本支持一些新特性
from __future__ import annotations

# 导入枚举类（Enum），用于创建一组特定的、不可变的值
from enum import Enum

# 这段代码是微软公司写的，遵循MIT许可证
# """这是一个模块，里面包含了PipelineCacheConfig, PipelineFileCacheConfig和PipelineMemoryCacheConfig类。"""

# 再次导入未来的注解功能，确保所有地方都能正确处理注解
from __future__ import annotations

# 定义一个名为CacheType的枚举类，它继承自str和Enum
class CacheType(str, Enum):
    # 枚举成员'file'，表示文件类型的缓存配置
    file = "file"  # 文件缓存类型
    # 枚举成员'memory'，表示内存类型的缓存配置
    memory = "memory"  # 内存缓存类型
    # 枚举成员'none'，表示无缓存配置
    none = "none"  # 无缓存类型
    # 枚举成员'blob'，表示云存储（如Azure Blob）类型的缓存配置
    blob = "blob"  # 云存储缓存类型

    # 当打印或显示这个枚举成员时，返回一个好看的字符串形式
    def __repr__(self):
        return f'"{self.value}"'


# 定义一个名为InputFileType的枚举类，它继承自str和Enum
class InputFileType(str, Enum):
    # 枚举成员'csv'，表示CSV格式的输入文件
    csv = "csv"  # CSV输入类型
    # 枚举成员'text'，表示文本格式的输入文件
    text = "text"  # 文本输入类型

    # 同样，当打印或显示这个枚举成员时，返回一个好看的字符串形式
    def __repr__(self):
        return f'"{self.value}"'


# 定义一个名为InputType的枚举类，它继承自str和Enum
class InputType(str, Enum):
    # 枚举成员'file'，表示文件存储方式的输入
    file = "file"  # 文件存储输入类型
    # 枚举成员'blob'，表示云存储（如Azure Blob）方式的输入
    blob = "blob"  # 云存储输入类型

    # 同样，当打印或显示这个枚举成员时，返回一个好看的字符串形式
    def __repr__(self):
        return f'"{self.value}"'


# 定义一个名为StorageType的枚举类，它继承自str和Enum
class StorageType(str, Enum):
    # 枚举成员'file'，表示文件存储类型
    file = "file"  # 文件存储类型
    # 枚举成员'memory'，表示内存存储类型
    memory = "memory"  # 内存存储类型
    # 枚举成员'blob'，表示云存储（如Azure Blob）类型
    blob = "blob"  # 云存储类型

    # 同样，当打印或显示这个枚举成员时，返回一个好看的字符串形式
    def __repr__(self):
        return f'"{self.value}"'

# 定义一个名为ReportingType的类，它同时继承自str和Enum
class ReportingType(str, Enum):
    # 这个类是用来设置报告配置类型的
    # 下面是三种不同的报告类型

    # 文件报告类型
    file = "file"  # 表示报告将保存在文件中
    # 控制台报告类型
    console = "console"  # 表示报告会显示在电脑屏幕上（控制台）
    # Blob报告类型
    blob = "blob"  # 通常指云存储中的文件，这里也是报告的一种形式

    # 定义一个特殊方法，返回类实例的字符串表示
    def __repr__(self):
        # 返回一个引号包围的值字符串
        return f'"{self.value}"'


# 定义一个名为TextEmbeddingTarget的类，同样继承自str和Enum
class TextEmbeddingTarget(str, Enum):
    # 这个类用来定义文本嵌入的目标

    # 所有文本
    all = "all"  # 表示使用所有文本
    # 必要的文本
    required = "required"  # 只使用必要的文本

    # 同样定义一个返回字符串的方法
    def __repr__(self):
        # 返回一个引号包围的值字符串
        return f'"{self.value}"'


# 定义一个名为LLMType的类，也继承自str和Enum
class LLMType(str, Enum):
    # 这个类定义了不同类型的大型语言模型（LLM）

    # 嵌入相关
    OpenAIEmbedding = "openai_embedding"  # 使用OpenAI的嵌入技术
    AzureOpenAIEmbedding = "azure_openai_embedding"  # 使用Azure的OpenAI嵌入技术

    # 原始完成
    OpenAI = "openai"  # 使用OpenAI的原始完成服务
    AzureOpenAI = "azure_openai"  # 使用Azure的OpenAI完成服务

    # 聊天完成
    OpenAIChat = "openai_chat"  # 使用OpenAI的聊天服务
    AzureOpenAIChat = "azure_openai_chat"  # 使用Azure的OpenAI聊天服务

    # 调试模式
    StaticResponse = "static_response"  # 固定响应，用于调试

    # 再次定义一个返回字符串的方法
    def __repr__(self):
        # 返回一个引号包围的值字符串
        return f'"{self.value}"'


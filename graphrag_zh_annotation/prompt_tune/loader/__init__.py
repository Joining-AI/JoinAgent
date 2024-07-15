# 导入函数和常量，这些来自同一目录下的 'config' 和 'input' 模块
from .config import read_config_parameters  # 从 'config' 导入读取配置参数的函数
from .input import MIN_CHUNK_OVERLAP, MIN_CHUNK_SIZE, load_docs_in_chunks  # 从 'input' 导入最小块重叠、最小块大小和分块加载文档的函数

# 这是微软公司2024年的版权信息
# 使用的是 MIT 许可证，允许别人自由使用、修改和分享代码，只要保留原始许可信息

# 这段代码的描述：这是一个关于微调配置和数据加载的模块

# 再次从 'config' 和 'input' 导入，以便其他文件能通过这个模块直接访问这些常量和函数
from .config import read_config_parameters
from .input import MIN_CHUNK_OVERLAP, MIN_CHUNK_SIZE, load_docs_in_chunks

# '__all__' 是一个列表，告诉其他导入这个模块的代码可以使用以下这些名字
__all__ = [  # 这里列出了可以公开访问的项目
    "MIN_CHUNK_OVERLAP",  # 最小块重叠
    "MIN_CHUNK_SIZE",  # 最小块大小
    "load_docs_in_chunks",  # 分块加载文档的函数
    "read_config_parameters",  # 读取配置参数的函数
]


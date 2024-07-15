# 导入一些有用的函数，让我们的代码能用上它们
from .dicts import dict_has_keys_with_types  # 检查字典是否包含特定类型的关键字
from .hashing import gen_md5_hash           # 创建一个MD5哈希值，用来检查数据的独特性
from .is_null import is_null                 # 检查某个东西是否是空的或不存在的
from .json import clean_up_json              # 清理和格式化JSON数据
from .load_graph import load_graph           # 加载图形数据，可能是一个网络或关系图
from .string import clean_str                # 清理字符串，去掉不需要的字符
from .tokens import num_tokens_from_string, string_from_tokens  # 分割和组合字符串成单词
from .topological_sort import topological_sort  # 对有依赖关系的项目进行排序
from .uuid import gen_uuid                  # 生成一个唯一的标识符，像身份证号一样

# 这一行是微软公司的版权声明，说明这个代码是他们的，并且遵循MIT许可证

# 这个字符串是文档注释，描述这个文件包含的是一些工具方法

# 这里列出所有对外公开的函数，这样别人在使用时可以方便地看到有哪些可用功能
__all__ = [
    "clean_str",       # 清理字符串的函数
    "clean_up_json",   # 清理JSON的函数
    "dict_has_keys_with_types",  # 检查字典键类型的函数
    "gen_md5_hash",    # 生成MD5哈希的函数
    "gen_uuid",        # 生成唯一标识符的函数
    "is_null",         # 检查是否为空的函数
    "load_graph",      # 加载图形数据的函数
    "num_tokens_from_string",  # 计算字符串中单词数的函数
    "string_from_tokens",     # 从单词列表创建字符串的函数
    "topological_sort",   # 进行拓扑排序的函数
]


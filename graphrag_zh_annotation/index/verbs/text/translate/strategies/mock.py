# 导入不同模块，它们帮助我们处理数据和任务
from typing import Any  # 用于指定函数参数和返回值类型的工具
from datashaper import VerbCallbacks  # 一个用于报告任务进度的库
from graphrag.index.cache import PipelineCache  # 用于存储和检索数据的缓存系统
from .typing import TextTranslationResult  # 自定义的数据类型，表示文本翻译的结果

# 这段文字是版权信息，说明代码由微软公司编写，遵循MIT许可证

# 定义一个模块，包含run和_summarize_text方法的定义
# ...

# 不要忽略这行，它是一个编码规范注释，告诉检查器async是必要的
async def run(  # noqa RUF029 async is required for interface
    input: str | list[str],  # 输入可以是一个字符串或字符串列表
    _args: dict[str, Any],  # 一个字典，存放额外的参数，这里用下划线开头表示是内部使用的
    _reporter: VerbCallbacks,  # 用于报告任务进度的对象
    _cache: PipelineCache,  # 用于缓存的类实例
) -> TextTranslationResult:  # 函数返回一个TextTranslationResult对象
    """运行文本提取流程。"""
    # 如果输入是字符串，将其转换为单元素列表
    input = [input] if isinstance(input, str) else input
    # 对输入列表中的每个文本进行翻译，将结果存储在列表中
    translations = [_translate_text(text) for text in input]
    # 返回翻译后的结果
    return TextTranslationResult(translations=translations)


# 定义一个内部函数，用于翻译单个文本
def _translate_text(text: str) -> str:
    """将一个文本翻译成另一种形式。"""
    # 翻译操作，这里简单地在文本后添加" translated"
    return f"{text} translated"


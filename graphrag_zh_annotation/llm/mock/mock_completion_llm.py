# 导入logging模块，用于记录程序运行时的信息
import logging

# 从typing_extensions库导入Unpack，它是一个类型注解工具
from typing_extensions import Unpack

# 从graphrag.llm.base导入基类BaseLLM
from graphrag.llm.base import BaseLLM

# 从graphrag.llm.types导入一些数据类型定义
from graphrag.llm.types import CompletionInput, CompletionOutput, LLMInput

# 版权声明，这段代码由微软公司2024年编写，遵循MIT许可证

# 定义一个LLM静态响应方法的文档字符串
"""LLM Static Response 方法定义。"""

# 初始化日志记录器，用于打印程序运行信息
log = logging.getLogger(__name__)

# 定义一个MockCompletionLLM类，继承自BaseLLM
# 这个类是为了测试用途，它处理CompletionInput和CompletionOutput类型的输入和输出
class MockCompletionLLM(BaseLLM[CompletionInput, CompletionOutput]):
    # 初始化函数，当创建MockCompletionLLM对象时调用
    def __init__(self, responses: list[str]):
        # 存储一系列的响应字符串
        self.responses = responses
        # 初始化一个错误处理变量
        self._on_error = None

    # 定义一个异步执行LLM的方法
    async def _execute_llm(self, input: CompletionInput, **kwargs: Unpack[LLMInput]) -> CompletionOutput:
        # 当执行LLM时，返回响应列表的第一个元素作为输出
        return self.responses[0]


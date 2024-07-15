# 导入一些特殊类型的定义，帮助我们更好地理解代码中的数据结构
from typing_extensions import Unpack
# 导入graphrag库中关于LLM（可能是一种语言模型）的类型定义
from graphrag.llm.types import LLM, CompletionInput, CompletionLLM, CompletionOutput, LLMInput, LLMOutput
# 导入一个辅助函数，用于尝试将字符串解析成JSON对象
from .utils import try_parse_json_object

# 这段代码的版权信息，表示由微软公司2024年创建，遵循MIT许可证
# 注释：这部分不是代码，而是说明文件归属和许可的文本，小孩可以跳过

# 定义一个名为JsonParsingLLM的类，它是LLM的一个子类，专门处理与JSON相关的任务
class JsonParsingLLM(LLM[CompletionInput, CompletionOutput]):
    # 这个类有一个内部变量，用来存储另一个名为CompletionLLM的对象
    _delegate: CompletionLLM

    # 类的初始化方法，当创建JsonParsingLLM实例时会调用
    def __init__(self, delegate: CompletionLLM):
        # 将传入的CompletionLLM对象赋值给内部变量
        self._delegate = delegate

    # 定义一个异步方法，这是调用LLM的主要方式
    async def __call__(
        # 接收一个CompletionInput对象作为输入参数
        self, input: CompletionInput,
        # 接收任意数量的关键字参数，类型为LLMInput
        **kwargs: Unpack[LLMInput],
    ) -> LLMOutput[CompletionOutput]:
        # 调用内部的CompletionLLM对象，传入输入参数和关键字参数
        result = await self._delegate(input, **kwargs)
        
        # 检查关键字参数中是否有"json"，并且返回结果中json字段是否为空，输出字段是否不为空
        if kwargs.get("json") and result.json is None and result.output is not None:
            # 如果满足条件，尝试将输出字段解析为JSON对象并赋值给结果的json字段
            result.json = try_parse_json_object(result.output)
        
        # 返回处理后的结果
        return result


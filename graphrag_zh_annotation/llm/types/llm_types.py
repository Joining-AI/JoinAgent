# 导入一个叫做 TypeAlias 的东西，它能帮我们给数据类型起个新名字
from typing import TypeAlias

# 导入了一个叫做 LLM 的东西，它来自当前文件夹里的 llm 模块
from .llm import LLM

# 这里是微软公司写的代码，2024年的，用的是 MIT 许可证，你可以用，但要遵守规则哦

# 这个模块是关于 LLM（可能是一种语言模型）的类型定义

# 我们定义了一个新名字 EmbeddingInput，它代表一个包含很多字符串的列表
EmbeddingInput: TypeAlias = list[str]

# 另外一个名字 EmbeddingOutput，它代表一个包含很多浮点数列表的列表
EmbeddingOutput: TypeAlias = list[list[float]]

# CompletionInput 是一个单独的字符串
CompletionInput: TypeAlias = str

# CompletionOutput 也是一个单独的字符串
CompletionOutput: TypeAlias = str

# 现在我们定义 EmbeddingLLM，它是一个 LLM，但它需要的输入是 EmbeddingInput 类型的，输出是 EmbeddingOutput 类型的
EmbeddingLLM: TypeAlias = LLM[EmbeddingInput, EmbeddingOutput]

# 同样，CompletionLLM 也是一个 LLM，但它需要的输入是 CompletionInput 类型的，输出是 CompletionOutput 类型的
CompletionLLM: TypeAlias = LLM[CompletionInput, CompletionOutput]


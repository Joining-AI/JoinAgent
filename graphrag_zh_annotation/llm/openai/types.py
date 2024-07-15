# 导入两个特殊的Python库，它们让我们能和OpenAI的服务进行互动。
from openai import (
    AsyncAzureOpenAI,  # 这个是用于连接微软Azure上的OpenAI服务的异步（同时进行）版本
    AsyncOpenAI,      # 这个是用于连接OpenAI标准服务的异步版本
)

# 这段文字是版权声明，说明代码由微软公司创作，2024年的时候。
# 它遵循的是MIT许可证，这意味着你可以自由使用，但需要遵守一些规则。

# 这是一个描述OpenAI语言模型基础类的注释。
# "LLMs"代表"大型语言模型"，就是能理解和生成人类语言的智能程序。

# 我们定义了一个变量，叫做OpenAIClientTypes。
# 它表示可以是AsyncOpenAI或AsyncAzureOpenAI中的任何一种类型。
OpenAIClientTypes = AsyncOpenAI | AsyncAzureOpenAI


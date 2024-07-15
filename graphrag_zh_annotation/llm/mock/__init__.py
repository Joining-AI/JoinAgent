# 导入两个模拟（假装）语言模型的类
from .mock_chat_llm import MockChatLLM  # 模拟聊天式语言模型
from .mock_completion_llm import MockCompletionLLM  # 模拟完成式语言模型

# 这是微软公司2024年的版权信息
# 并且代码遵循MIT许可证

# 这段文字是对这个代码文件的描述，说这里是模拟语言模型的实现

# 再次导入之前导入的两个模拟语言模型类，以便于在其他地方使用
from .mock_chat_llm import MockChatLLM
from .mock_completion_llm import MockCompletionLLM

# 这个列表告诉别人，这个模块中可以公开使用的有两个东西
# "MockChatLLM" 和 "MockCompletionLLM"，它们都是模拟语言模型的类
__all__ = [
    "MockChatLLM",
    "MockCompletionLLM",
]


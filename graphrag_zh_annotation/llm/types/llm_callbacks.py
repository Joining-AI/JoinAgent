# 导入Callable模块，这是一个Python内置的抽象基类，表示可以调用的对象
from collections.abc import Callable

# 导入LLMInvocationResult模块，这个是程序内部定义的一个类
from .llm_invocation_result import LLMInvocationResult

# 这是版权信息，说明代码由微软公司2024年创建，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这个代码的作用，它是OpenAI DataShaper包的类型定义
"""Typing definitions for the OpenAI DataShaper package."""

# 再次导入Callable模块，确保我们知道如何定义可调用的函数
from collections.abc import Callable

# 定义一个类型：ErrorHandlerFn，它是一个函数，接收三种可能的参数：
# 1. 可能的异常对象（可能是None）
# 2. 可能的字符串（也可能是None）
# 3. 可能的字典（同样可能是None），并且不返回任何值
ErrorHandlerFn = Callable[[BaseException | None, str | None, dict | None], None]
# 这个函数用于处理错误情况

# 定义一个类型：LLMInvocationFn，它也是一个函数，接收一个LLMInvocationResult类型的对象作为参数，不返回任何值
LLMInvocationFn = Callable[[LLMInvocationResult], None]
# 这个函数用于处理LLM（可能是大型语言模型）调用的结果

# 定义一个类型：OnCacheActionFn，它接收两个参数：
# 1. 一个字符串
# 2. 可能的字符串（可能是None），不返回任何值
OnCacheActionFn = Callable[[str, str | None], None]
# 这个函数在缓存有操作时被调用

# 定义一个类型：IsResponseValidFn，它是一个函数，接收一个字典作为参数并返回一个布尔值
# 如果字典表示的响应有效，返回True；否则，返回False
IsResponseValidFn = Callable[[dict], bool]
# 这个函数用来检查LLM的响应是否有效


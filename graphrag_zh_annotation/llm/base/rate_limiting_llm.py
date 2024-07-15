# 导入必要的库，让程序能执行特定任务
import asyncio  # 异步编程库
import logging  # 记录程序运行日志
from collections.abc import Callable  # 定义可调用对象的抽象基类
from typing import Any, Generic, TypeVar  # 类型注解，用于更清晰地描述代码中的数据类型

# 从tenacity库导入用于重试的工具
from tenacity import (
    AsyncRetrying,  # 异步重试工具
    retry_if_exception_type,  # 如果出现特定异常则重试
    stop_after_attempt,  # 在尝试一定次数后停止
    wait_exponential_jitter,  # 指定等待时间，以指数方式增长并带有随机抖动
)

# 从typing_extensions导入Unpack，用于类型注解
from typing_extensions import Unpack

# 导入自定义错误和限流器
from graphrag.llm.errors import RetriesExhaustedError  # 重试次数耗尽错误
from graphrag.llm.limiting import LLMLimiter  # 限流器
from graphrag.llm.types import (  # 定义的数据结构
    LLM,  # 限流管理器
    LLMConfig,  # 限流配置
    LLMInput,  # 输入数据
    LLMInvocationFn,  # 调用函数
    LLMInvocationResult,  # 调用结果
    LLMOutput,  # 输出数据
)

# 定义泛型变量
TIn = TypeVar("TIn")  # 输入数据的类型
TOut = TypeVar("TOut")  # 输出数据的类型
TRateLimitError = TypeVar("TRateLimitError", bound=BaseException)  # 限流错误的类型，是异常的子类

# 定义错误消息
_CANNOT_MEASURE_INPUT_TOKENS_MSG = "不能测量输入的令牌数"  # 当无法计算输入数据量时的提示
_CANNOT_MEASURE_OUTPUT_TOKENS_MSG = "不能测量输出的令牌数"  # 当无法计算输出数据量时的提示

# 初始化日志记录器，用于记录程序运行信息
log = logging.getLogger(__name__)  # 获取当前模块的日志记录器




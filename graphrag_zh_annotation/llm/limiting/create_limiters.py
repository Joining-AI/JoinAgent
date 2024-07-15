# 导入日志模块，它帮助我们记录程序运行的信息
import logging

# 导入一个异步限流器库，用于控制请求速度
from aiolimiter import AsyncLimiter

# 从 graphrag.llm.types 模块中导入 LLMConfig 类型，这可能是配置信息
from graphrag.llm.types import LLMConfig

# 从当前目录下的 llm_limiter 模块导入 LLMLimiter 类
from .llm_limiter import LLMLimiter

# 从当前目录下的 tpm_rpm_limiter 模块导入 TpmRpmLLMLimiter 类
from .tpm_rpm_limiter import TpmRpmLLMLimiter

# 这一行是版权信息，表示代码由微软公司拥有，遵循 MIT 许可证

# 定义一个名为 log 的日志对象，用于记录程序中的信息
log = logging.getLogger(__name__)

# 这里是一个文档字符串，描述了这个模块的作用，创建 OpenAI API 请求的限流器

# 定义一个函数，用于创建限速器
def create_tpm_rpm_limiters(
    # 接受一个 LLMConfig 类型的参数，代表配置信息
    configuration: LLMConfig,
) -> LLMLimiter:
    # 从配置中获取每分钟允许的令牌数（TPM）
    tpm = configuration.tokens_per_minute
    # 从配置中获取每分钟允许的请求数（RPM）
    rpm = configuration.requests_per_minute

    # 使用 TpmRpmLLMLimiter 类创建限流器，如果 TPM 或 RPM 为 0，则不设置限流
    # 如果值为 0，用 None 替换，否则用 AsyncLimiter 创建限流器
    return TpmRpmLLMLimiter(
        None if tpm == 0 else AsyncLimiter(tpm or 50_000),
        None if rpm == 0 else AsyncLimiter(rpm or 10_000),
    )


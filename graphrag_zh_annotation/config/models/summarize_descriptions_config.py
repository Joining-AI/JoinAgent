# 导入一个叫做Path的模块，它帮助我们处理文件路径
from pathlib import Path
# 导入一个叫做Field的类，它是Pydantic库里的，用于设置和验证配置参数
from pydantic import Field
# 导入默认配置的模块
import graphrag.config.defaults as defs
# 导入LLMConfig类，这是另一个配置类
from .llm_config import LLMConfig

# 这是微软公司的版权信息，用的是MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个参数化配置的文档字符串
"""

Parameterization settings for the default configuration.

"""

# 再次导入Path模块，确保它在代码中可用
from pathlib import Path
# 再次导入Field类，确保它在代码中可用
from pydantic import Field
# 导入默认配置的模块
import graphrag.config.defaults as defs
# 导入LLMConfig类
from .llm_config import LLMConfig

# 创建一个叫SummarizeDescriptionsConfig的类，它继承自LLMConfig
class SummarizeDescriptionsConfig(LLMConfig):
    # 这个类是关于描述摘要的配置部分
    """Configuration section for description summarization."""

    # 定义一个名为prompt的变量，它可以是字符串或None，用于描述摘要提示
    prompt: str | None = Field(
        description="用于描述摘要的提示。",
        default=None
    )
    # 定义一个名为max_length的变量，它是整数，表示摘要的最大长度
    max_length: int = Field(
        description="描述摘要的最大长度。",
        default=defs.SUMMARIZE_DESCRIPTIONS_MAX_LENGTH,
    )
    # 定义一个名为strategy的变量，它可以是字典或None，用于覆盖策略
    strategy: dict | None = Field(
        description="要使用的覆盖策略。",
        default=None
    )

    # 定义一个方法，返回解析后的描述摘要策略
    def resolved_strategy(self, root_dir: str) -> dict:
        # 引入SummarizeStrategyType枚举类型
        from graphrag.index.verbs.entities.summarize import SummarizeStrategyType

        # 如果strategy有值，就返回它；否则返回一个默认策略
        return self.strategy or {
            "type": SummarizeStrategyType.graph_intelligence,
            # 使用LLM模型的序列化信息
            "llm": self.llm.model_dump(),
            # 使用并行化模型的序列化信息
            **self.parallelization.model_dump(),
            # 如果prompt有值，读取其文本内容，否则为None
            "summarize_prompt": (Path(root_dir) / self.prompt).read_text()
            if self.prompt
            else None,
            # 添加摘要的最大长度
            "max_summary_length": self.max_length,
        }


# 导入一个叫做Path的模块，它帮助我们处理文件路径
from pathlib import Path

# 导入一个叫做Field的类，它是Pydantic库中的，用于定义配置参数
from pydantic import Field

# 导入默认设置的模块
import graphrag.config.defaults as defs

# 从当前目录导入llm_config模块
from .llm_config import LLMConfig

# 这是一个版权声明，告诉我们这个代码是微软公司的，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个配置类，专门用于社区报告的设置
class CommunityReportsConfig(LLMConfig):
    # 这个类继承自LLMConfig

    # 定义一个参数prompt，可以是字符串或None，描述是用来提取社区报告的提示
    prompt: str | None = Field(description="用于提取社区报告的提示", default=None)

    # 定义一个参数max_length，是整数，描述是社区报告的最大长度（以令牌计）
    max_length: int = Field(description="社区报告的最大令牌长度", default=defs.COMMUNITY_REPORT_MAX_LENGTH)

    # 定义一个参数max_input_length，是整数，描述是生成报告时的最大输入长度（以令牌计）
    max_input_length: int = Field(description="生成报告时的最大输入令牌长度", default=defs.COMMUNITY_REPORT_MAX_INPUT_LENGTH)

    # 定义一个参数strategy，可以是字典或None，描述是覆盖策略
    strategy: dict | None = Field(description="要使用的覆盖策略", default=None)

    # 定义一个方法，返回解析后的社区报告提取策略
    def resolved_strategy(self, root_dir) -> dict:
        # 导入一个类型枚举，用于报告策略
        from graphrag.index.verbs.graph.report import CreateCommunityReportsStrategyType

        # 如果有设置策略，就返回策略；否则，返回一个默认的策略字典
        return self.strategy or {
            "type": CreateCommunityReportsStrategyType.graph_intelligence,
            "llm": self.llm.model_dump(),  # 使用模型的保存信息
            **self.parallelization.model_dump(),  # 添加并行化设置信息
            # 如果有prompt，读取其文本内容，否则设为None
            "extraction_prompt": (Path(root_dir) / self.prompt).read_text() if self.prompt else None,
            "max_report_length": self.max_length,  # 设置最大报告长度
            "max_input_length": self.max_input_length,  # 设置最大输入长度
        }


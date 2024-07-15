# 导入一个叫做Path的工具，它帮助我们处理文件路径
from pathlib import Path

# 导入Field模块，它是Pydantic库的一部分，用于定义数据模型的字段
from pydantic import Field

# 导入默认配置的模块
import graphrag.config.defaults as defs

# 从当前目录下的llm_config模块导入LLMConfig类
from .llm_config import LLMConfig

# 这是一个版权声明，表示代码由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个参数配置类，用于设置默认配置
class ClaimExtractionConfig(LLMConfig):
    # 这个类是关于提取主张（claim）的配置部分
    """配置段，用于设置主张提取功能。"""

    # 是否启用主张提取，值可以是True或False
    enabled: bool = Field(description="是否启用主张提取。")

    # 提取主张时使用的提示文本，可以是任何字符串或没有值（None）
    prompt: str | None = Field(description="主张提取的提示文本。", default=None)

    # 对主张的描述，默认值来自graphrag.config.defaults模块
    description: str = Field(description="主张的描述。", default=defs.CLAIM_DESCRIPTION)

    # 最多提取的实体数量，默认值也来自graphrag.config.defaults模块
    max_gleanings: int = Field(description="最多提取的实体数量。", default=defs.CLAIM_MAX_GLEANINGS)

    # 用于覆盖的策略字典，如果没有设定则为None
    strategy: dict | None = Field(description="要使用的覆盖策略。", default=None)

    # 这个方法用于获取解析后的主张提取策略
    def resolved_strategy(self, root_dir: str) -> dict:
        # 导入一个枚举类型，用于定义策略类型
        from graphrag.index.verbs.covariates.extract_covariates import ExtractClaimsStrategyType

        # 如果设置了自定义策略，就返回它；否则使用默认策略
        return self.strategy or {
            "type": ExtractClaimsStrategyType.graph_intelligence,
            # 使用LLMConfig类中的模型信息
            "llm": self.llm.model_dump(),
            # 使用并行化配置中的模型信息
            **self.parallelization.model_dump(),
            # 如果有提示文本，读取文件内容；如果没有，则为None
            "extraction_prompt": (Path(root_dir) / self.prompt).read_text() if self.prompt else None,
            # 添加主张的描述
            "claim_description": self.description,
            # 添加最大提取实体数
            "max_gleanings": self.max_gleanings,
        }


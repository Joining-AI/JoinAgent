# 导入Path模块，帮助我们处理文件路径
from pathlib import Path

# 导入Field，它是Pydantic库中的一个类，用于定义数据模型的字段
from pydantic import Field

# 导入默认配置的常量
import graphrag.config.defaults as defs

# 导入LLMConfig，这是另一个配置类
from .llm_config import LLMConfig

# 这段代码的版权信息，表示由微软公司拥有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为EntityExtractionConfig的类，它是LLMConfig的子类，用于设置实体提取的参数
class EntityExtractionConfig(LLMConfig):
    # 这个类用于实体提取的配置
    """Configuration section for entity extraction."""

    # 定义一个prompt字段，可以是字符串或None，描述是使用的实体提取提示，初始值为None
    prompt: str | None = Field(description="The entity extraction prompt to use.", default=None)

    # 定义一个entity_types字段，是一个包含字符串的列表，描述是要使用的实体类型，默认值来自defs模块
    entity_types: list[str] = Field(description="The entity extraction entity types to use.", default=defs.ENTITY_EXTRACTION_ENTITY_TYPES)

    # 定义一个max_gleanings字段，是整数，描述是最大提取的实体数量，默认值来自defs模块
    max_gleanings: int = Field(description="The maximum number of entity gleanings to use.", default=defs.ENTITY_EXTRACTION_MAX_GLEANINGS)

    # 定义一个strategy字段，可以是字典或None，描述是覆盖默认的实体提取策略，默认值为None
    strategy: dict | None = Field(description="Override the default entity extraction strategy", default=None)

    # 定义一个方法，返回解析后的实体提取策略
    def resolved_strategy(self, root_dir: str, encoding_model: str) -> dict:
        # 导入ExtractEntityStrategyType枚举，用于确定实体提取策略类型
        from graphrag.index.verbs.entities.extraction import ExtractEntityStrategyType

        # 如果有自定义的策略就返回，否则使用默认策略
        return self.strategy or {
            "type": ExtractEntityStrategyType.graph_intelligence,  # 策略类型
            "llm": self.llm.model_dump(),  # 使用的模型信息
            **self.parallelization.model_dump(),  # 并行处理的模型信息
            # 提取提示文本，如果prompt存在就读取文件，否则为None
            "extraction_prompt": (Path(root_dir) / self.prompt).read_text() if self.prompt else None,
            "max_gleanings": self.max_gleanings,  # 最大提取数量
            # 模型已预先分块
            "encoding_name": encoding_model,  # 编码模型名称
            "prechunked": True,  # 标记为预分块
        }


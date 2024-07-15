# 导入一个叫做Field的工具，它帮助我们设置配置参数
from pydantic import Field

# 引入默认配置的模块
import graphrag.config.defaults as defs

# 引入一个枚举类型，用于文本嵌入的目标选择
from graphrag.config.enums import TextEmbeddingTarget

# 引入一个名为LLMConfig的配置类
from .llm_config import LLMConfig

# 版权声明，由微软公司在2024年拥有，遵循MIT许可证

# 这个模块是关于文本嵌入配置的参数设定
"""

Parameterization settings for the default configuration.

"""

# 再次导入Field，确保我们有这个工具
from pydantic import Field

# 引入默认配置
import graphrag.config.defaults as defs

# 引入文本嵌入目标的枚举类型
from graphrag.config.enums import TextEmbeddingTarget

# 引入LLMConfig类
from .llm_config import LLMConfig


# 定义一个TextEmbeddingConfig类，它是LLMConfig的子类，专门处理文本嵌入的设置
class TextEmbeddingConfig(LLMConfig):
    # 文本嵌入的批次大小，默认值在defs模块中查找
    batch_size: int = Field(description="使用的批次大小。", default=defs.EMBEDDING_BATCH_SIZE)
    
    # 每个批次的最大令牌数，默认值也在defs模块中
    batch_max_tokens: int = Field(description="每个批次的最大令牌数。", default=defs.EMBEDDING_BATCH_MAX_TOKENS)
    
    # 文本嵌入的目标，可以是'all'或'required'，默认值在defs中
    target: TextEmbeddingTarget = Field(description="要使用的目标。", default=defs.EMBEDDING_TARGET)
    
    # 要跳过的特定嵌入列表，默认为空
    skip: list[str] = Field(description="要跳过的嵌入列表。", default=[])
    
    # 向量存储配置，可能是字典或None，默认为None
    vector_store: dict | None = Field(description="向量存储配置。", default=None)
    
    # 重写策略，可能是字典或None，默认为None
    strategy: dict | None = Field(description="要使用的重写策略。", default=None)

    # 返回解决后的文本嵌入策略
    def resolved_strategy(self) -> dict:
        # 引入TextEmbedStrategyType来确定策略类型
        from graphrag.index.verbs.text.embed import TextEmbedStrategyType

        # 如果有自定义策略就返回，否则用默认的OpenAI策略
        return self.strategy or {
            "type": TextEmbedStrategyType.openai,
            "llm": self.llm.model_dump(),  # 使用LLM模型的信息
            **self.parallelization.model_dump(),  # 使用并行化模型的信息
            "batch_size": self.batch_size,  # 包含批次大小
            "batch_max_tokens": self.batch_max_tokens,  # 包含批次最大令牌数
        }


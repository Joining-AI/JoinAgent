# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库
from pydantic import BaseModel, Field

# 导入一些默认的配置参数，它们来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这段文字是关于这个代码的描述，它说这是默认配置的参数设置
# """Parameterization settings for the default configuration."""

# 定义一个名为EmbedGraphConfig的类，它是BaseModel的子类
class EmbedGraphConfig(BaseModel):
    # 这个类是关于Node2Vec（一种图嵌入方法）的默认配置
    """The default configuration section for Node2Vec."""

    # 定义一个布尔变量，表示是否启用Node2Vec
    enabled: bool = Field(
        # 描述这个变量的作用
        description="A flag indicating whether to enable node2vec.",
        # 设置默认值，从defs模块获取
        default=defs.NODE2VEC_ENABLED,
    )

    # 定义一个整数变量，表示进行多少次随机游走
    num_walks: int = Field(
        description="The node2vec number of walks.",
        default=defs.NODE2VEC_NUM_WALKS,
    )

    # 定义一个整数变量，表示每次随机游走的长度
    walk_length: int = Field(
        description="The node2vec walk length.",
        default=defs.NODE2VEC_WALK_LENGTH,
    )

    # 定义一个整数变量，表示窗口大小（在学习词向量时用到）
    window_size: int = Field(
        description="The node2vec window size.",
        default=defs.NODE2VEC_WINDOW_SIZE,
    )

    # 定义一个整数变量，表示训练迭代次数
    iterations: int = Field(
        description="The node2vec iterations.",
        default=defs.NODE2VEC_ITERATIONS,
    )

    # 定义一个整数变量，用于设置随机数生成器的种子
    random_seed: int = Field(
        description="The node2vec random seed.",
        default=defs.NODE2VEC_RANDOM_SEED,
    )

    # 定义一个字典或None变量，用于覆盖默认的图嵌入策略
    strategy: dict | None = Field(
        description="The graph embedding strategy override.",
        default=None,
    )

    # 定义一个方法，返回解决后的Node2Vec策略
    def resolved_strategy(self) -> dict:
        # 引入一个枚举类型，用于确定图嵌入策略
        from graphrag.index.verbs.graph.embed import EmbedGraphStrategyType

        # 如果有自定义策略，就返回；否则返回默认的Node2Vec策略
        return self.strategy or {
            "type": EmbedGraphStrategyType.node2vec,
            "num_walks": self.num_walks,
            "walk_length": self.walk_length,
            "window_size": self.window_size,
            "iterations": self.iterations,
            "random_seed": self.random_seed,  # 注意这里应该是random_seed，不是iterations
        }


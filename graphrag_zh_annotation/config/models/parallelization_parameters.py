# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们创建数据模型
from pydantic import BaseModel, Field

# 导入默认配置，这些是预先设置好的值，来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这是一个版权声明，告诉我们这个代码的版权属于微软公司，并且遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了这是一个关于LLM参数的模型
"""LLM Parameters model."""

# 创建一个继承自BaseModel的类，叫做ParallelizationParameters
class ParallelizationParameters(BaseModel):

    # 这个类有一个属性叫做stagger，它是一个浮点数
    # Field是用来设置这个属性的描述和默认值的
    stagger: float = Field(
        # 这是stagger的描述，说明它的用途
        description="用于LLM服务的交错值。",
        # 这是stagger的默认值，从defs模块中获取
        default=defs.PARALLELIZATION_STAGGER,
    )

    # 这个类还有一个属性叫做num_threads，它是一个整数
    num_threads: int = Field(
        # 这是num_threads的描述，说明它的用途
        description="用于LLM服务的线程数量。",
        # 这是num_threads的默认值，同样从defs模块中获取
        default=defs.PARALLELIZATION_NUM_THREADS,
    )


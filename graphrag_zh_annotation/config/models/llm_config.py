# 导入一个叫做AsyncType的类，它来自datashaper库
from datashaper import AsyncType

# 导入BaseModel和Field这两个工具，它们来自pydantic库，用于创建数据模型
from pydantic import BaseModel, Field

# 导入默认配置的模块，它在graphrag.config包的defaults子模块里
import graphrag.config.defaults as defs

# 导入LLM参数的模块，它在这个文件的同一目录下的llm_parameters.py文件里
from .llm_parameters import LLMParameters

# 导入并行化参数的模块，也在同一目录下
from .parallelization_parameters import ParallelizationParameters

# 这是微软公司的版权信息，表示代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为LLMConfig的类，它是BaseModel的子类，用于设置LLM（可能是一种语言模型）配置
class LLMConfig(BaseModel):
    # 定义一个属性，叫llm，它是一个LLMParameters对象，描述了要使用的LLM配置
    # 如果没有指定，默认使用一个空的LLMParameters对象
    llm: LLMParameters = Field(description="LLM的配置", default=LLMParameters())

    # 定义另一个属性，叫parallelization，它是一个ParallelizationParameters对象，描述并行化配置
    # 如果没有指定，默认使用一个空的ParallelizationParameters对象
    parallelization: ParallelizationParameters = Field(
        description="并行处理的配置", default=ParallelizationParameters()
    )

    # 定义一个异步模式属性，async_mode，它是一个AsyncType对象，描述要使用的异步模式
    # 如果没有指定，默认使用defaults模块中定义的ASYNC_MODE
    async_mode: AsyncType = Field(description="使用的异步模式", default=defs.ASYNC_MODE)


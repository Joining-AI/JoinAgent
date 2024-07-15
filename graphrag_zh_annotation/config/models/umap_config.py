# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们创建数据模型
from pydantic import BaseModel, Field

# 导入defaults模块，它来自graphrag.config这个包，里面有一些默认设置
import graphrag.config.defaults as defs

# 这是微软公司2024年的版权信息，代码遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这段文字描述了下面的代码是关于默认配置的参数设置
"""Parameterization settings for the default configuration."""

# 创建一个新的类叫UmapConfig，它继承自BaseModel
class UmapConfig(BaseModel):
    # 这个类是用来设置UMAP（一种数据可视化方法）的配置
    """Configuration section for UMAP."""

    # 定义一个变量enabled，类型是布尔值（True或False）
    enabled: bool = Field(
        # 这个变量的描述是：一个标志，用来表示是否开启UMAP
        description="A flag indicating whether to enable UMAP.",
        # 默认值来自于defs模块中的UMAP_ENABLED
        default=defs.UMAP_ENABLED,
    )


# 导入一个叫做BaseModel和Field的工具，它们来自pydantic库，帮助我们创建数据模型
from pydantic import BaseModel, Field

# 导入一些默认设置，它们来自graphrag.config.defaults模块
import graphrag.config.defaults as defs

# 这段文字是代码的描述，告诉我们这是关于默认配置的参数设置
# """Parameterization settings for the default configuration."""

# 创建一个新类，叫SnapshotsConfig，它继承自BaseModel
class SnapshotsConfig(BaseModel):

    # 这个类里面有一个属性，叫做graphml，它是一个布尔值（True或False）
    # 有一个描述，说它用来标记是否保存GraphML格式的快照
    # 默认值从defs模块中的SNAPSHOTS_GRAPHML获取
    graphml: bool = Field(description="是否保存GraphML快照", default=defs.SNAPSHOTS_GRAPHML)

    # 另一个属性，raw_entities，也是一个布尔值，表示是否保存原始实体的快照
    # 同样，它的描述和默认值也是从defs模块获取
    raw_entities: bool = Field(description="是否保存原始实体快照", default=defs.SNAPSHOTS_RAW_ENTITIES)

    # 最后一个属性，top_level_nodes，表示是否保存顶级节点的快照
    # 依然，描述和默认值来自defs模块
    top_level_nodes: bool = Field(description="是否保存顶级节点快照", default=defs.SNAPSHOTS_TOP_LEVEL_NODES)


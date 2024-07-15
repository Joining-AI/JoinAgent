# 导入一些工具函数，帮助处理数据和文本
from .covariates import extract_covariates   # 提取相关变量的函数
from .entities import entity_extract, summarize_descriptions  # 提取实体和总结描述的函数
from .genid import genid  # 生成唯一ID的函数
from .graph import (  # 图形相关的函数集合
    cluster_graph,  # 聚类图形
    create_community_reports,  # 创建社区报告
    create_graph,  # 创建图形
    embed_graph,  # 嵌入图形
    layout_graph,  # 布局图形
    merge_graphs,  # 合并图形
    unpack_graph,  # 解包图形
)
from .overrides import aggregate, concat, merge  # 数据聚合、连接和合并的函数
from .snapshot import snapshot  # 获取快照的函数
from .snapshot_rows import snapshot_rows  # 获取快照行的函数
from .spread_json import spread_json  # 扩展JSON数据的函数
from .text import chunk, text_embed, text_split, text_translate  # 处理文本的函数
from .unzip import unzip  # 解压缩文件的函数
from .zip import zip_verb  # 压缩文件或操作的函数

# Microsoft公司2024年的版权信息，遵循MIT许可证

# 这是一个模块，定义了一个名为get_default_verbs的方法（未显示在这里）

# 将以下所有导入的函数公开，以便在其他地方可以使用它们
__all__ = [
    "aggregate",  # 聚合函数
    "chunk",  # 分块函数
    "cluster_graph",  # 聚类图形函数
    "concat",  # 连接函数
    "create_community_reports",  # 创建社区报告函数
    "create_graph",  # 创建图形函数
    "embed_graph",  # 嵌入图形函数
    "entity_extract",  # 提取实体函数
    "extract_covariates",  # 提取相关变量函数
    "genid",  # 生成唯一ID函数
    "layout_graph",  # 布局图形函数
    "merge",  # 合并函数
    "merge_graphs",  # 合并图形函数
    "snapshot",  # 获取快照函数
    "snapshot_rows",  # 获取快照行函数
    "spread_json",  # 扩展JSON函数
    "summarize_descriptions",  # 总结描述函数
    "text_embed",  # 文本嵌入函数
    "text_split",  # 文本分割函数
    "text_translate",  # 文本翻译函数
    "unpack_graph",  # 解包图形函数
    "unzip",  # 解压缩函数
    "zip_verb",  # 压缩函数
]


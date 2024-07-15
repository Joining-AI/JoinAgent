# 导入两个特殊的东西，它们来自graphrag.index.config模块
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这是一个特殊的文字，叫做版权声明，意思是这个代码是微软公司在2024年写的
# 并且它遵循MIT许可证的规定

# 这里写了一个文档字符串，描述了这个模块（文件）里有什么特别的方法
# 文档字符串是用来解释代码功能的

from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep  # 再次导入，确保我们能用这两个工具

# 定义一个变量，名字叫workflow_name，它的值是一个字符串，内容是"create_base_entity_graph"
workflow_name = "create_base_entity_graph"

# 定义一个函数，名为build_steps，它接受一个名为config的参数，类型是PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    这个函数用来创建实体图的基础表格。

    # 依赖项
    * `workflow:create_base_extracted_entities`
    """
    # 从config中获取"cluster_graph"的配置，如果没有就用默认值{"strategy": {"type": "leiden"}}
    clustering_config = config.get(
        "cluster_graph",
        {"strategy": {"type": "leiden"}},
    )

    # 从config中获取"embed_graph"的配置，如果没有就用默认的node2vec策略
    embed_graph_config = config.get(
        "embed_graph",
        {
            "strategy": {
                "type": "node2vec",
                "num_walks": config.get("embed_num_walks", 10),  # 漫步次数
                "walk_length": config.get("embed_walk_length", 40),  # 漫步长度
                "window_size": config.get("embed_window_size", 2),  # 窗口大小
                "iterations": config.get("embed_iterations", 3),  # 迭代次数
                "random_seed": config.get("embed_random_seed", 86),  # 随机种子
            }
        },
    )

    # 检查是否开启graphml快照功能，如果config中没有设置或设置为False，则默认关闭
    graphml_snapshot_enabled = config.get("graphml_snapshot", False) or False

    # 检查是否开启图嵌入功能，如果config中没有设置或设置为False，则默认关闭
    embed_graph_enabled = config.get("embed_graph_enabled", False) or False

    # 创建并返回一个步骤列表
    return [
        # 第一步：聚类图，输入来自"workflow:create_summarized_entities"
        {
            "verb": "cluster_graph",
            "args": {
                **clustering_config,
                "column": "entity_graph",
                "to": "clustered_graph",
                "level_to": "level",
            },
            "input": ({"source": "workflow:create_summarized_entities"}),
        },
        # 第二步（可选）：如果开启了graphml快照，保存聚类图快照
        {
            "verb": "snapshot_rows",
            "enabled": graphml_snapshot_enabled,
            "args": {
                "base_name": "clustered_graph",
                "column": "clustered_graph",
                "formats": [{"format": "text", "extension": "graphml"}],
            },
        },
        # 第三步（可选）：如果开启了图嵌入，进行图嵌入操作
        {
            "verb": "embed_graph",
            "enabled": embed_graph_enabled,
            "args": {
                "column": "clustered_graph",
                "to": "embeddings",
                **embed_graph_config,
            },
        },
        # 第四步（可选）：如果开启了graphml快照，保存嵌入后的图快照
        {
            "verb": "snapshot_rows",
            "enabled": graphml_snapshot_enabled,
            "args": {
                "base_name": "embedded_graph",
                "column": "entity_graph",
                "formats": [{"format": "text", "extension": "graphml"}],
            },
        },
        # 第五步：选择要保留的列，如果开启了图嵌入则包含"level", "clustered_graph", "embeddings"，否则只包含"level", "clustered_graph"
        {
            "verb": "select",
            "args": {
                "columns": (
                    ["level", "clustered_graph", "embeddings"]
                    if embed_graph_enabled
                    else ["level", "clustered_graph"]
                ),
            },
        },
    ]


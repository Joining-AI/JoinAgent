# 导入两个类：PipelineWorkflowConfig和PipelineWorkflowStep，它们来自graphrag.index.config模块。
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 这一行是版权信息，表示代码归2024年的微软公司所有。
# Licensed under the MIT License意味着这个代码可以使用MIT许可证，允许他人自由使用、修改和分享。

# 这是一个文档字符串，描述了这个模块包含的内容。它告诉人们这个模块里有一个叫做build_steps的方法定义。
"""这是一个模块，里面有一个方法叫做build_steps的定义。"""

# 从graphrag.index.config模块再次导入PipelineWorkflowConfig和PipelineWorkflowStep类，虽然已经导入过，但这里可能是为了代码清晰或有特殊用途。
from graphrag.index.config import PipelineWorkflowConfig, PipelineWorkflowStep

# 定义一个变量，名字叫workflow_name，它的值是"create_final_nodes"。这可能是一个工作流程的名字。
workflow_name = "create_final_nodes"

# 定义一个名为 build_steps 的函数，它接受一个名为 config 的参数，类型是 PipelineWorkflowConfig
def build_steps(
    config: PipelineWorkflowConfig,
) -> list[PipelineWorkflowStep]:
    """
    创建文档图的基础表格。

    这个函数依赖于另一个操作：`workflow:create_base_entity_graph`
    """
    
    # 从 config 中获取 "snapshot_top_level_nodes" 参数，如果没有设置则默认为 False
    snapshot_top_level_nodes = config.get("snapshot_top_level_nodes", False)
    
    # 从 config 中获取 "layout_graph_enabled" 参数，如果没有设置则默认为 True
    layout_graph_enabled = config.get("layout_graph_enabled", True)

    # 定义一个列表，里面是一系列的操作（字典）
    _compute_top_level_node_positions = [
        # 解压 "positioned_graph" 列中的数据
        {"verb": "unpack_graph", "args": {"column": "positioned_graph", "type": "nodes"}, "input": {"source": "laid_out_entity_graph"}},
        # 过滤 level 为特定值的节点（根据 config.get("level_for_node_positions", 0)）
        {"verb": "filter", "args": {...},},
        # 选择 id, x, y 列
        {"verb": "select", "args": {"columns": ["id", "x", "y"]},},
        # 如果 snapshot_top_level_nodes 为真，则保存这些节点
        {"verb": "snapshot", "enabled": snapshot_top_level_nodes, "args": {...},},
        # 重命名 id 为 top_level_node_id
        {"id": "_compute_top_level_node_positions", "verb": "rename", "args": {"columns": {"id": "top_level_node_id"}},},
        # 将 top_level_node_id 转换为字符串类型
        {"verb": "convert", "args": {"column": "top_level_node_id", "to": "top_level_node_id", "type": "string"},},
    ]

    # 获取 layout_graph 配置，如果没有设置则使用默认配置
    layout_graph_config = config.get(
        "layout_graph",
        {
            "strategy": {
                "type": "umap" if layout_graph_enabled else "zero",
            },
        },
    )

    # 返回一系列的操作步骤
    return [
        # 对图进行布局，得到 node_positions 和 positioned_graph
        {"id": "laid_out_entity_graph", "verb": "layout_graph", "args": {...}, "input": {"source": "workflow:create_base_entity_graph"}},
        # 解压 positioned_graph 中的节点数据
        {"verb": "unpack_graph", "args": {"column": "positioned_graph", "type": "nodes"}},
        # 删除没有 x 和 y 坐标的节点
        {"id": "nodes_without_positions", "verb": "drop", "args": {"columns": ["x", "y"]}},
        # 添加之前定义的计算顶级节点位置的操作
        *_compute_top_level_node_positions,
        # 根据 id 和 top_level_node_id 进行连接操作
        {"verb": "join", "args": {"on": ["id", "top_level_node_id"]}, "input": {...}},
        # 重命名 "label" 为 "title"，"cluster" 为 "community"
        {"verb": "rename", "args": {"columns": {"label": "title", "cluster": "community"}}},
    ]


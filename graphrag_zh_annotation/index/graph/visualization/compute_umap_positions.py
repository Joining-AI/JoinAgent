# 导入一些有用的库，它们可以帮助我们处理图形和数据
import graspologic as gc  # 用于图论和网络分析的库
import matplotlib.pyplot as plt  # 用于绘制图形
import networkx as nx  # 用于创建和操作图的库
import numpy as np  # 用于数学计算的库
import umap  # 用于降维和可视化数据的库

# 从当前模块导入自定义的数据类型
from .typing import NodePosition

# 这是微软公司的版权信息，表示代码遵循MIT许可证
# "A module containing compute_umap_positions and visualize_embedding method definition."
# 这是一个模块，包含两个方法：计算UMAP位置和可视化嵌入结果

# 定义一个名为get_zero_positions的函数
def get_zero_positions(
    # 输入参数，分别是节点标签（名字）、节点类别（可选）和节点大小（可选）
    node_labels: list[str],  # 节点的名字列表
    node_categories: list[int] | None = None,  # 每个节点的类别列表，如果没有则设为None
    node_sizes: list[int] | None = None,  # 每个节点的大小列表，如果没有则设为None
    three_d: bool | None = False,  # 是否在3D空间中定位，如果未设置则默认为False
) -> list[NodePosition]:  # 返回值类型，是一个包含节点位置信息的列表

    # 初始化一个空列表，用于存储每个节点的位置信息
    embedding_position_data: list[NodePosition] = []

    # 遍历每个节点
    for index, node_name in enumerate(node_labels):
        # 如果没有提供节点类别，就设为1
        node_category = 1 if node_categories is None else node_categories[index]
        # 如果没有提供节点大小，就设为1
        node_size = 1 if node_sizes is None else node_sizes[index]

        # 根据是否在3D空间中定位，决定添加2D还是3D的位置信息
        if not three_d:
            # 在2D空间中，添加节点位置信息到列表
            embedding_position_data.append(
                NodePosition(
                    label=str(node_name),  # 节点的名字
                    x=0,  # x坐标
                    y=0,  # y坐标
                    cluster=str(int(node_category)),  # 所属类别
                    size=int(node_size),  # 节点大小
                )
            )
        else:
            # 在3D空间中，添加节点位置信息到列表
            embedding_position_data.append(
                NodePosition(
                    label=str(node_name),  # 节点的名字
                    x=0,  # x坐标
                    y=0,  # y坐标
                    z=0,  # z坐标
                    cluster=str(int(node_category)),  # 所属类别
                    size=int(node_size),  # 节点大小
                )
            )

    # 返回包含所有节点位置信息的列表
    return embedding_position_data

# 定义一个函数，叫compute_umap_positions，它接受一些参数
def compute_umap_positions(
    # 这是一个包含数字的数组，表示每个节点的嵌入信息
    embedding_vectors: np.ndarray,
    # 这是一个字符串列表，每个字符串代表一个节点的标签
    node_labels: list[str],
    # 这是一个整数列表，如果有的话，表示每个节点的类别
    node_categories: list[int] | None = None,
    # 这是一个整数列表，如果有的话，表示每个节点的大小
    node_sizes: list[int] | None = None,
    # 这是一个浮点数，控制UMAP中点之间的最小距离
    min_dist: float = 0.75,
    # 这是一个整数，表示每个点的邻居数量
    n_neighbors: int = 25,
    # 这是一个浮点数，影响UMAP中的空间分布
    spread: int = 1,
    # 这是一个字符串，表示计算距离时使用的度量方式
    metric: str = "euclidean",
    # 这是一个整数，表示要降维到的维度，通常是2或3
    n_components: int = 2,
    # 这是一个随机种子，确保每次运行结果可复现
    random_state: int = 86,
) -> list[NodePosition]:
    """这个函数用UMAP算法将高维数据降到2D或3D。"""
    
    # 使用UMAP库进行降维处理
    embedding_positions = umap.UMAP(
        min_dist=min_dist,
        n_neighbors=n_neighbors,
        spread=spread,
        n_components=n_components,
        metric=metric,
        random_state=random_state,
    ).fit_transform(embedding_vectors)

    # 创建一个空列表，用来存储每个节点的位置信息
    embedding_position_data: list[NodePosition] = []

    # 遍历节点标签和它们对应的嵌入位置
    for index, node_name in enumerate(node_labels):
        # 获取当前节点的嵌入位置
        node_points = embedding_positions[index]  # 忽略类型检查错误
        # 如果没有类别信息，设置为1，否则取节点类别
        node_category = 1 if node_categories is None else node_categories[index]
        # 如果没有大小信息，设置为1，否则取节点大小
        node_size = 1 if node_sizes is None else node_sizes[index]

        # 检查降维后的维度，如果是2D
        if len(node_points) == 2:
            # 创建并添加一个NodePosition对象，包含标签、x、y坐标、类别和大小
            embedding_position_data.append(
                NodePosition(
                    label=str(node_name),
                    x=float(node_points[0]),
                    y=float(node_points[1]),
                    cluster=str(int(node_category)),
                    size=int(node_size),
                )
            )
        # 如果是3D
        else:
            # 创建并添加一个NodePosition对象，包含标签、x、y、z坐标、类别和大小
            embedding_position_data.append(
                NodePosition(
                    label=str(node_name),
                    x=float(node_points[0]),
                    y=float(node_points[1]),
                    z=float(node_points[2]),
                    cluster=str(int(node_category)),
                    size=int(node_size),
                )
            )

    # 返回所有节点的位置信息列表
    return embedding_position_data

# 定义一个名为visualize_embedding的函数，接收两个参数：graph和umap_positions
def visualize_embedding(graph, umap_positions: list[dict]):
    """这个函数的作用是将嵌入数据用UMAP降维到2D，并画出可视化图。"""

    # 清除当前图形
    plt.clf()

    # 获取当前图形的容器，并设置大小和分辨率
    figure = plt.gcf()
    figure.set_size_inches(10, 10)  # 图形尺寸设为10x10英寸
    figure.set_dpi(400)  # 设置分辨率，让图像更清晰

    # 创建字典，存储每个节点的标签及其在2D空间的位置
    node_position_dict = {
        str(position["label"]): (position["x"], position["y"])
        for position in umap_positions
    }

    # 创建另一个字典，存储每个节点的标签及其类别
    node_category_dict = {
        str(position["label"]): position["category"]
        for position in umap_positions
    }

    # 计算每个节点的大小
    node_sizes = [position["size"] for position in umap_positions]

    # 根据节点类别获取颜色
    node_colors = gc.layouts.categorical_colors(node_category_dict)  # 忽略类型检查

    # 创建两个列表，分别存储节点标签和对应的颜色
    vertices = []
    node_color_list = []
    for node in node_position_dict:
        vertices.append(node)
        node_color_list.append(node_colors[node])

    # 使用networkx绘制网络图的节点
    nx.draw_networkx_nodes(
        graph,  # 绘制的网络图
        pos=node_position_dict,  # 节点位置
        nodelist=vertices,  # 要绘制的节点列表
        node_color=node_color_list,  # 节点颜色
        alpha=1.0,  # 透明度，1表示完全不透明
        linewidths=0.01,  # 节点边框宽度
        node_size=node_sizes,  # 节点大小
        node_shape="o",  # 节点形状为圆形
        ax=ax,  # 当前的图形轴
    )

    # 显示图像
    plt.show()


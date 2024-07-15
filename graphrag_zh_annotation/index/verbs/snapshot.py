# 导入所需工具包，让程序能处理表格和操作数据
from datashaper import TableContainer, VerbInput, verb
from graphrag.index.storage import PipelineStorage

# 这段代码的版权信息，由微软公司所有，遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，里面有一个方法用于保存数据快照

# 使用datashaper库里的verb装饰器，创建一个名为"snapshot"的方法
@verb(name="snapshot")
# 定义一个异步函数（需要等待完成）来获取数据快照
async def snapshot(
    # 输入参数，是一个包含数据的特殊对象
    input: VerbInput,
    # 快照的名字
    name: str,
    # 可以保存的文件格式列表
    formats: list[str],
    # 用来存储数据的工具
    storage: PipelineStorage,
    # 其他可能的参数，但这里我们忽略它们
    **_kwargs: dict,
) -> TableContainer:
    """这个函数会把表格数据全部保存下来。"""
    # 获取输入数据
    data = input.get_input()

    # 遍历每种指定的文件格式
    for fmt in formats:
        # 如果格式是"parquet"，用它来保存数据
        if fmt == "parquet":
            # 等待保存为parquet文件，并在名字后加".parquet"
            await storage.set(name + ".parquet", data.to_parquet())
        # 如果格式是"json"，则保存为json文件
        elif fmt == "json":
            # 保存为json文件，以记录形式，每条记录占一行
            await storage.set(
                name + ".json", data.to_json(orient="records", lines=True)
            )

    # 最后，返回一个包含原始数据的表格容器
    return TableContainer(table=data)


# 这段代码是用来读取配置参数的，可以从设置文件或环境变量中获取这些参数。

# 导入Path模块，它帮助我们处理文件路径
from pathlib import Path
# 导入create_graphrag_config函数，这个函数用于创建配置对象
from graphrag.config import create_graphrag_config
# 导入ProgressReporter类，用于报告进度
from graphrag.index.progress.types import ProgressReporter

# 这是微软公司的版权声明和许可证信息，告诉别人这段代码的来源和使用许可
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这个模块是关于配置加载、解析和处理的
"""

Config loading, parsing and handling module.
"""

# 同样的，从pathlib模块导入Path
from pathlib import Path
# 从graphrag.config导入create_graphrag_config
from graphrag.config import create_graphrag_config
# 从graphrag.index.progress.types导入ProgressReporter类

# 定义一个函数，名为read_config_parameters，用来读取配置参数
def read_config_parameters(root: str, reporter: ProgressReporter):
    # 参数：
    # - root: 存放参数的根目录
    # - reporter: 用于报告进度的对象
    """
    从设置文件或环境变量中读取配置参数。

    参数:
    - root: 参数所在的根目录。
    - reporter: 进度报告器。
    """
    # 将输入的字符串root转换为Path对象
    _root = Path(root)
    # 指向settings.yaml文件的路径
    settings_yaml = _root / "settings.yaml"
    # 如果settings.yaml不存在，尝试settings.yml
    if not settings_yaml.exists():
        settings_yaml = _root / "settings.yml"
    # 指向settings.json文件的路径
    settings_json = _root / "settings.json"

    # 如果settings.yaml存在，就从这个文件读取
    if settings_yaml.exists():
        # 通过reporter报告正在从哪个文件读取
        reporter.info(f"Reading settings from {settings_yaml}")
        # 打开文件并以只读方式读取
        with settings_yaml.open("r") as file:
            # 导入yaml模块，用于解析yaml格式的数据
            import yaml
            # 安全地加载yaml文件内容
            data = yaml.safe_load(file)
            # 使用加载的数据和根目录创建配置对象
            return create_graphrag_config(data, root)

    # 如果settings.json存在，就从这个文件读取
    if settings_json.exists():
        # 通过reporter报告正在从哪个文件读取
        reporter.info(f"Reading settings from {settings_json}")
        # 打开文件并以只读方式读取
        with settings_json.open("r") as file:
            # 导入json模块，用于解析json格式的数据
            import json
            # 读取文件内容并转化为字典
            data = json.loads(file.read())
            # 使用加载的数据和根目录创建配置对象
            return create_graphrag_config(data, root)

    # 如果两个文件都不存在，那么从环境变量中读取配置
    reporter.info("Reading settings from environment variables")
    # 直接用根目录创建配置对象
    return create_graphrag_config(root_dir=root)


# 导入json模块，它帮助我们处理JSON格式的数据
import json

# 导入pathlib的Path类，用来操作文件路径
from pathlib import Path

# 导入yaml模块，用于读写YAML格式的配置文件
import yaml

# 从pyaml_env库导入parse_config函数，这个函数会将环境变量合并到YAML配置中
from pyaml_env import parse_config as parse_config_with_env

# 从graphrag.config导入create_graphrag_config和read_dotenv函数，它们是关于配置文件的创建和读取环境变量的
from graphrag.config import create_graphrag_config, read_dotenv

# 从graphrag.index.config导入PipelineConfig类，这可能是一个配置管道的类
from graphrag.index.config import PipelineConfig

# 从当前目录下的create_pipeline_config模块导入create_pipeline_config函数，用于创建管道配置
from .create_pipeline_config import create_pipeline_config

# 这行是版权信息，表示2024年微软公司拥有版权
# 注释：根据MIT许可证，这个代码可以自由使用

# 这是一个模块，包含了read_dotenv、load_pipeline_config、_parse_yaml和_create_include_constructor四个方法的定义
# 这些方法都是用来处理配置文件和环境变量的

# 定义一个名为load_pipeline_config的函数，它接受一个参数config_or_path，这个参数可以是文件路径或配置对象
def load_pipeline_config(config_or_path: str | PipelineConfig) -> PipelineConfig:
    """这个函数用来从文件路径或配置对象加载管道配置"""
    
    # 如果传入的参数已经是PipelineConfig类型，就直接赋值给变量config
    if isinstance(config_or_path, PipelineConfig):
        config = config_or_path
    # 如果传入的参数是"default"，创建默认的管道配置
    elif config_or_path == "default":
        config = create_pipeline_config(create_graphrag_config(root_dir="."))
    else:
        # 检查配置文件所在的目录下是否有.env文件，如果有，读取它
        read_dotenv(str(Path(config_or_path).parent))

        # 如果文件名以.json结尾，打开文件并用json加载配置
        if config_or_path.endswith(".json"):
            with Path(config_or_path).open(encoding="utf-8") as f:
                config = json.load(f)
        # 如果文件名以.yml或.yaml结尾，解析yaml文件
        elif config_or_path.endswith((".yml", ".yaml")):
            config = _parse_yaml(config_or_path)
        # 如果文件类型无效，抛出错误
        else:
            msg = f"无效的配置文件类型：{config_or_path}"
            raise ValueError(msg)

        # 验证配置
        config = PipelineConfig.model_validate(config)
        # 如果没有设置root_dir，将配置文件的父目录作为root_dir
        if not config.root_dir:
            config.root_dir = str(Path(config_or_path).parent.resolve())

    # 如果配置中有extends属性（表示继承其他配置）
    if config.extends is not None:
        # 如果extends是字符串，将其转换为列表
        if isinstance(config.extends, str):
            config.extends = [config.extends]
        # 遍历要继承的每个配置
        for extended_config in config.extends:
            # 加载要继承的配置
            extended_config = load_pipeline_config(extended_config)
            # 合并配置
            merged_config = {
                **json.loads(extended_config.model_dump_json()),  # 继承的配置
                **json.loads(config.model_dump_json(exclude_unset=True)),  # 当前配置，不包含未设置的值
            }
            # 验证合并后的配置
            config = PipelineConfig.model_validate(merged_config)

    # 返回最终的配置
    return config

# 定义一个辅助函数，用于解析支持!include指令的yaml文件
def _parse_yaml(path: str):
    """解析yaml文件，支持!include指令"""
    # 创建一个yaml安全加载器
    loader_class = yaml.SafeLoader

    # 如果!include构造函数不存在，添加它
    if "!include" not in loader_class.yaml_constructors:
        loader_class.add_constructor("!include", _create_include_constructor())

    # 使用加载器和环境变量解析配置
    return parse_config_with_env(path, loader=loader_class, default_value="")

# 定义一个函数，它的任务是创建一个处理"!include"指令的构造器。
def _create_include_constructor():
    """创建一个用于处理'!include'指令的构造函数。"""

    # 再定义一个内部函数，这个函数叫做handle_include，它接受两个参数：一个加载器和一个节点。
    def handle_include(loader: yaml.Loader, node: yaml.Node):
        """根据节点包含的文件名，将文件内容引入进来。"""
        
        # 把加载器的文件名（当前文件）和节点中的值（要包含的文件名）组合成完整路径。
        filename = str(Path(loader.name).parent / node.value)

        # 检查要包含的文件是否以.yml或.yaml结尾。
        if filename.endswith((".yml", ".yaml")):
            # 如果是YAML文件，就解析它并返回解析后的内容。
            return _parse_yaml(filename)

        # 如果不是YAML文件，就以UTF-8编码打开文件，读取内容并返回。
        with Path(filename).open(encoding="utf-8") as f:
            return f.read()

    # 最后，返回handle_include函数，这样外部就可以使用这个构造器来处理"!include"指令了。
    return handle_include


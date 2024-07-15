# 导入模块：这个代码是连接到一个叫做 "graphrag.config.defaults" 的部分
# 这个模块里有一些预设的设置或参数，就像一个工具箱里的默认工具
import graphrag.config.defaults as defs

# 这段代码是Python程序，用于初始化一个命令行工具的配置。
# 它定义了一些默认设置和变量，这些设置和变量与一个名为"graphrag"的软件如何连接和使用AI服务有关。

# 第一部分是版权声明，说明这是微软公司的代码，使用了MIT许可证。
# """Content for the init CLI command.""" 是这个命令的描述。

# 导入了一个名为"defaults"的模块，里面有一些预设的配置值。
import graphrag.config.defaults as defs

# 接下来定义了一个字符串变量INIT_YAML，它是一个YAML格式的配置文件模板。
# YAML是一种用来存储数据的格式，易于人类阅读和编写。
INIT_YAML = f"""
encoding_model: cl100k_base  # 用的AI模型名称
skip_workflows: []  # 不执行的工作流程列表，目前为空
llm:  # 语言模型相关设置
  api_key: ${{GRAPHRAG_API_KEY}}  # API密钥，需要替换
  type: {defs.LLM_TYPE.value}  # 语言模型的类型
  model: {defs.LLM_MODEL}  # 使用的语言模型
  model_supports_json: true  # 如果模型支持JSON格式，则为真
  # ... 更多设置，如最大令牌数、超时时间等，可以根据需要调整

# ...（更多配置项，包括并行化设置、异步模式、嵌入设置、分块设置、输入设置、缓存设置、存储设置、报告设置、实体提取、总结描述、主张提取、社区报告、聚类图、嵌入图、UMAP、快照、本地搜索和全局搜索设置）
"""

# 最后，定义了一个字符串变量INIT_DOTENV，它是一个环境变量设置模板。
# 这里的GRAPHRAG_API_KEY需要替换为实际的API密钥。
INIT_DOTENV = """
GRAPHRAG_API_KEY=<API_KEY>
"""

# 这个代码的作用是提供一个模板，让用户根据自己的需求和环境设置来填入具体的参数，以便于"graphrag"工具能正确地连接和使用AI服务。


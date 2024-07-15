# 导入一个叫做NotRequired的特殊类型，它表示某个参数可以不用提供
from typing_extensions import NotRequired

# 从graphrag.config.enums模块中导入一个枚举类型TextEmbeddingTarget
from graphrag.config.enums import TextEmbeddingTarget

# 从当前文件夹下的llm_config_input.py文件中导入LLMConfigInput类
from .llm_config_input import LLMConfigInput

# 这是微软公司的版权信息，告诉我们代码的使用权
# 根据MIT许可证，你可以自由地使用这段代码

# 这个模块定义了一些配置参数的设置

# 现在我们创建一个新的类TextEmbeddingConfigInput，它是LLMConfigInput类的子类
class TextEmbeddingConfigInput(LLMConfigInput):
    # 这个类是关于文本嵌入（一种处理文本的技术）的配置部分

    # 下面是类的一些属性，它们都是可选的（可以用NotRequired来表示）

    # batch_size：可以是整数、字符串或None，表示每次处理的数据量
    batch_size: NotRequired[int | str | None]

    # batch_max_tokens：可以是整数、字符串或None，表示每个批次最大处理的单词数量
    batch_max_tokens: NotRequired[int | str | None]

    # target：可以是TextEmbeddingTarget枚举类型、字符串或None，表示嵌入的目标
    target: NotRequired[TextEmbeddingTarget | str | None]

    # skip：可以是一个字符串列表、单个字符串或None，表示要跳过的特定内容
    skip: NotRequired[list[str] | str | None]

    # vector_store：可以是一个字典或None，用于存储嵌入向量的地方
    vector_store: NotRequired[dict | None]

    # strategy：可以是一个字典或None，表示处理策略的详细设定
    strategy: NotRequired[dict | None]


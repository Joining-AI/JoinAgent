# 导入两个基础类
from graphrag.query.llm.base import BaseLLMCallback
from graphrag.query.structured_search.base import SearchResult

# 这是微软公司的版权信息，表示代码由他们编写
# 并且遵循MIT许可证的规定

# 定义一个模块，关于全局搜索的LLM回调函数
"""GlobalSearch LLM Callbacks."""

# 从基类BaseLLMCallback导入
from graphrag.query.llm.base import BaseLLMCallback
# 从基类SearchResult导入
from graphrag.query.structured_search.base import SearchResult


# 创建一个新的类，叫GlobalSearchLLMCallback，它继承自BaseLLMCallback
class GlobalSearchLLMCallback(BaseLLMCallback):
    # 类的描述：全局搜索的LLM回调函数
    """GlobalSearch LLM Callbacks."""

    # 初始化方法，当创建这个类的实例时会执行
    def __init__(self):
        # 调用父类的初始化方法
        super().__init__()
        # 创建一个空列表，用来存储响应的上下文
        self.map_response_contexts = []
        # 创建另一个空列表，用来存储响应的结果
        self.map_response_outputs = []

    # 当开始处理地图响应时调用的方法
    def on_map_response_start(self, map_response_contexts: list[str]):
        # 把传入的地图响应上下文列表存到类变量里
        self.map_response_contexts = map_response_contexts

    # 当结束处理地图响应时调用的方法
    def on_map_response_end(self, map_response_outputs: list[SearchResult]):
        # 把传入的地图响应结果列表存到类变量里
        self.map_response_outputs = map_response_outputs


# 导入两个Python库，用于定义类型
from typing import Any, Protocol

# 这段代码的版权属于微软公司，2024年
# 并且遵循MIT许可证

# 这是一个文档字符串，描述了这个代码包是用来干什么的
"""这是一个用来定义OpenAI DataShaper包中类型的代码。"""

# 再次导入typing库中的Any和Protocol类型
from typing import Any, Protocol


# 定义一个协议类（Protocol），叫LLMCache
# 这个类描述了一个接口，像字典一样存储和检索数据
class LLMCache(Protocol):
    # 这个方法检查缓存中是否有某个键
    async def has(self, key: str) -> bool:
        """检查缓存是否包含指定的键（key）的值。"""
        # 这里用"..."代表方法的具体实现省略了，实际使用时需要填充代码

    # 这个方法从缓存中获取一个值，如果键不存在则返回None
    async def get(self, key: str) -> Any | None:
        """从缓存中获取键（key）对应的值，可能返回任何类型或None。"""
        # 同样，具体实现省略了

    # 这个方法将一个值写入缓存，还可以附带一些调试信息
    async def set(self, key: str, value: Any, debug_data: dict | None = None) -> None:
        """将一个值和键（key）写入缓存，可选地提供调试数据字典。"""
        # 这里也是方法的占位符，实际使用需要添加代码


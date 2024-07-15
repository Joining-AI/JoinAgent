# 导入两个库，asyncio用于异步编程，time用于获取时间
import asyncio
import time

# 这是微软公司的版权声明
# 根据MIT许可证授权

# 这个文件是用来做限速工具的
"""限速器工具类"""

# 再导入一次asyncio和time，因为之后会用到
import asyncio
import time

# 定义一个名为RateLimiter的类
class RateLimiter:
    """
    原来的策略没有考虑到按分钟限制频率。
    RateLimiter类用来确保CommunityReportsExtractor能按分钟配置来限制速率。
    """

    # 待办事项：使用asyncio实现异步模式的RateLimiter

    # 初始化方法，当创建RateLimiter对象时调用
    def __init__(self, rate: int, per: int):
        # rate：每分钟允许的动作数
        # per：动作的单位时间（通常为1分钟）
        self.rate = rate
        self.per = per
        # 开始时允许的动作数
        self.allowance = rate
        # 记录上一次检查时间
        self.last_check = time.monotonic()

    # 获取令牌的方法，即进行一次动作
    async def acquire(self):
        """从限速器中获取一个令牌，允许执行一次操作"""
        # 获取当前时间
        current = time.monotonic()
        # 计算从上次检查到现在的时间
        elapsed = current - self.last_check
        # 更新最后一次检查的时间
        self.last_check = current
        # 更新允许的动作数
        self.allowance += elapsed * (self.rate / self.per)

        # 如果允许的动作数超过每分钟的最大值，将其设置为最大值
        if self.allowance > self.rate:
            self.allowance = self.rate

        # 如果允许的动作数小于1，说明需要等待
        if self.allowance < 1.0:
            # 计算需要等待的时间
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            # 异步等待
            await asyncio.sleep(sleep_time)
            # 等待后，将允许的动作数清零
            self.allowance = 0.0
        else:
            # 如果允许的动作数大于等于1，可以执行操作并减去一个
            self.allowance -= 1.0


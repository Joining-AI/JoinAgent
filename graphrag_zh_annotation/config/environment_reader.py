# 导入一些Python库，这些库帮助我们处理不同类型的数据和功能
from collections.abc import Callable  # 导入Callable，表示可以调用的对象，比如函数
from contextlib import contextmanager  # 导入contextmanager，用于创建临时上下文管理器
from enum import Enum  # 导入Enum，用于创建枚举类型
from typing import Any, TypeVar  # 导入Any和TypeVar，用于类型注解

# 导入Env库，它帮助我们从环境变量中读取配置信息
from environs import Env

# 这是微软公司的一个版权声明
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 这是一个配置读取工具类的文档字符串
"""A configuration reader utility class."""

# 定义一个类型变量T，可以代表任何类型
T = TypeVar("T")

# 定义两个类型别名
# KeyValue可以是字符串或枚举
KeyValue = str | Enum
# EnvKeySet可以是字符串或字符串列表
EnvKeySet = str | list[str]

# 定义一个函数，名为read_key，接收一个KeyValue类型的参数value
def read_key(value: KeyValue) -> str:
    """这个函数用来读取键值并将其转换为小写字符串"""
    
    # 检查value是否是枚举类型
    if not isinstance(value, str):  # 如果不是字符串
        # 对于枚举类型，返回其值的lowercase形式
        return value.value.lower()
    else:  # 如果是字符串
        # 直接将字符串转换为小写形式并返回
        return value.lower()

# 定义一个名为EnvironmentReader的类，它是一个用于读取配置的工具类
class EnvironmentReader:
    # 这个类有两个属性
    # _env: 保存环境对象
    _env: Env
    # _config_stack: 保存配置的列表（字典）
    _config_stack: list[dict]

    # 初始化方法，当创建EnvironmentReader对象时调用
    def __init__(self, env: Env):
        # 设置环境对象
        self._env = env
        # 初始化配置栈为空列表
        self._config_stack = []

    # 获取环境对象的方法
    def env(self):
        # 返回环境对象
        return self._env

    # 从环境中读取配置值的私有方法
    def _read_env(
        self, env_key: str | list[str], default_value: T, read: Callable[[str, T], T]
    ) -> T | None:
        # 如果env_key是字符串，将其转换为列表
        if isinstance(env_key, str):
            env_key = [env_key]

        # 遍历env_key列表
        for k in env_key:
            # 使用read函数尝试读取配置值，如果返回的不是默认值，则返回该值
            result = read(k.upper(), default_value)
            if result is not default_value:
                return result

        # 如果所有尝试都失败，返回默认值
        return default_value

    # 设置环境变量前缀的方法
    def envvar_prefix(self, prefix: KeyValue):
        # 将前缀转换为大写并添加下划线，然后使用环境对象的prefixed方法处理
        prefix = read_key(prefix)
        prefix = f"{prefix}_".upper()
        return self._env.prefixed(prefix)

    # 创建一个上下文管理器，将值推入配置栈
    def use(self, value: Any | None):
        # 定义一个内部的上下文管理器函数
        @contextmanager
        def config_context():
            # 将值（或空字典）推入配置栈
            self._config_stack.append(value or {})
            try:
                # 执行代码块
                yield
            finally:
                # 结束时从配置栈中弹出最后一个值
                self._config_stack.pop()

        # 返回这个上下文管理器
        return config_context()

    # 获取当前配置段的方法
    def section(self) -> dict:
        # 如果配置栈有内容，返回最后一项；否则返回空字典
        return self._config_stack[-1] if self._config_stack else {}

    # 读取字符串配置值的方法
    def str(
        self,
        key: KeyValue,
        env_key: EnvKeySet | None = None,
        default_value: str | None = None,
    ) -> str | None:
        # 处理键并检查当前配置段是否有该键，如果有则返回其值
        key = read_key(key)
        if self.section and key in self.section:
            return self.section[key]

        # 否则，从环境中读取值，使用_str方法
        return self._read_env(
            env_key or key, default_value, (lambda k, dv: self._env(k, dv))
        )

    # 读取整数配置值的方法
    def int(
        self,
        key: KeyValue,
        env_key: EnvKeySet | None = None,
        default_value: int | None = None,
    ) -> int | None:
        # 类似于str方法，但将值转换为整数
        key = read_key(key)
        if self.section and key in self.section:
            return int(self.section[key])
        return self._read_env(
            env_key or key, default_value, lambda k, dv: self._env.int(k, dv)
        )

    # 读取布尔配置值的方法
    def bool(
        self,
        key: KeyValue,
        env_key: EnvKeySet | None = None,
        default_value: bool | None = None,
    ) -> bool | None:
        # 类似于str方法，但将值转换为布尔值
        key = read_key(key)
        if self.section and key in self.section:
            return bool(self.section[key])

        return self._read_env(
            env_key or key, default_value, lambda k, dv: self._env.bool(k, dv)
        )

    # 读取浮点数配置值的方法
    def float(
        self,
        key: KeyValue,
        env_key: EnvKeySet | None = None,
        default_value: float | None = None,
    ) -> float | None:
        # 类似于str方法，但将值转换为浮点数
        key = read_key(key)
        if self.section and key in self.section:
            return float(self.section[key])
        return self._read_env(
            env_key or key, default_value, lambda k, dv: self._env.float(k, dv)
        )

    # 解析列表配置值的方法
    def list(
        self,
        key: KeyValue,
        env_key: EnvKeySet | None = None,
        default_value: list | None = None,
    ) -> list | None:
        # 类似于str方法，但将值解析为列表
        key = read_key(key)
        result = None
        if self.section and key in self.section:
            result = self.section[key]
            if isinstance(result, list):
                return result

        if result is None:
            result = self.str(key, env_key)
        if result:
            # 分割字符串并返回每个元素去空格后的列表
            return [s.strip() for s in result.split(",")]
        return default_value


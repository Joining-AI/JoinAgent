# 导入logging模块，用于记录程序运行中的信息和错误
import logging

# 导入traceback模块，用于处理程序中的异常信息
import traceback

# 使用dataclasses模块，定义数据类（一种特殊的类，用于简化创建具有默认值的类）
from dataclasses import dataclass

# 导入typing模块的Any类型，表示可以是任何类型的变量
from typing import Any

# 从graphrag.index.typing导入ErrorHandlerFn，这是一个错误处理函数的类型
from graphrag.index.typing import ErrorHandlerFn

# 从graphrag.index.utils导入dict_has_keys_with_types，这是一个检查字典是否包含特定类型键的函数
from graphrag.index.utils import dict_has_keys_with_types

# 从graphrag.llm导入CompletionLLM，这可能是一个完成语言模型的类
from graphrag.llm import CompletionLLM

# 从当前模块的prompts子模块导入COMMUNITY_REPORT_PROMPT，这可能是一个提示字符串
from .prompts import COMMUNITY_REPORT_PROMPT

# 这两行版权信息和许可声明，告诉我们代码的归属和使用的许可协议
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个模块，包含了'CommunityReportsResult'和'CommunityReportsExtractor'两个模型
"""A module containing 'CommunityReportsResult' and 'CommunityReportsExtractor' models."""

# 创建一个日志器，用于记录与这个模块相关的日志信息
log = logging.getLogger(__name__)

# 定义一个数据类，名为CommunityReportsResult
@dataclass
class CommunityReportsResult:
    # 类中的一个属性，'output'，存储的是字符串类型的结果
    output: str
    # 类中的另一个属性，'structured_output'，存储的是一个字典类型的结果
    structured_output: dict

# 定义一个名为CommunityReportsExtractor的类
class CommunityReportsExtractor:
    # 这个类是用来提取社区报告的

    # 类的属性（变量）
    _llm: CompletionLLM  # 用于完成任务的语言模型
    _input_text_key: str  # 输入文本的键，默认是"input_text"
    _extraction_prompt: str  # 提取报告时的提示语句，默认是某个常量
    _output_formatter_prompt: str  # 输出格式化提示，这里没有用到
    _on_error: ErrorHandlerFn  # 错误处理函数，默认不做任何操作
    _max_report_length: int  # 报告的最大长度，默认是1500

    # 初始化方法，当创建这个类的对象时会调用
    def __init__(
        self,
        llm_invoker: CompletionLLM,  # 传入一个语言模型调用器
        input_text_key: str | None = None,  # 可选的输入文本键
        extraction_prompt: str | None = None,  # 可选的提取提示
        on_error: ErrorHandlerFn | None = None,  # 可选的错误处理函数
        max_report_length: int | None = None,  # 可选的最大报告长度
    ):
        # 设置类的属性值
        self._llm = llm_invoker
        self._input_text_key = input_text_key or "input_text"
        self._extraction_prompt = extraction_prompt or COMMUNITY_REPORT_PROMPT
        self._on_error = on_error or (lambda _e, _s, _d: None)
        self._max_report_length = max_report_length or 1500

    # 当这个类的对象被调用时运行的方法
    async def __call__(self, inputs: dict[str, Any]):
        # 初始化输出变量
        output = None

        # 尝试执行以下代码块
        try:
            # 使用语言模型调用器获取报告
            response = (
                await self._llm(
                    # 提供提取提示
                    self._extraction_prompt,
                    json=True,
                    name="create_community_report",
                    # 传入输入文本
                    variables={
                        self._input_text_key: inputs[self._input_text_key]
                    },
                    # 检查返回结果是否有效
                    is_response_valid=lambda x: dict_has_keys_with_types(
                        x,
                        [
                            ("title", str),
                            ("summary", str),
                            ("findings", list),
                            ("rating", float),
                            ("rating_explanation", str),
                        ],
                    ),
                    # 设置模型参数
                    model_parameters={"max_tokens": self._max_report_length},
                )
                or {}
            )
            # 如果有有效响应，则将其转化为json格式
            output = response.json or {}
        # 如果发生错误
        except Exception as e:
            # 记录错误信息
            log.exception("error generating community report")
            # 调用错误处理函数
            self._on_error(e, traceback.format_exc(), None)
            # 设置输出为空字典
            output = {}

        # 从解析后的输出中获取文本形式的报告
        text_output = self._get_text_output(output)

        # 返回结果，包括结构化的输出和文本输出
        return CommunityReportsResult(
            structured_output=output,
            output=text_output,
        )

    # 获取文本输出的方法
    def _get_text_output(self, parsed_output: dict) -> str:
        # 获取标题，如果没有就用"Report"代替
        title = parsed_output.get("title", "Report")
        # 获取摘要，如果没有就用空字符串代替
        summary = parsed_output.get("summary", "")
        # 获取发现项列表
        findings = parsed_output.get("findings", [])

        # 定义一个函数来获取发现项的总结
        def finding_summary(finding: dict):
            if isinstance(finding, str):
                return finding
            return finding.get("summary")

        # 定义一个函数来获取发现项的解释
        def finding_explanation(finding: dict):
            if isinstance(finding, str):
                return ""
            return finding.get("explanation")

        # 将发现项转换成带有标题和解释的文本
        report_sections = "\n\n".join(
            f"## {finding_summary(f)}\n\n{finding_explanation(f)}" for f in findings
        )

        # 组合标题、摘要和发现项的文本
        return f"# {title}\n\n{summary}\n\n{report_sections}"


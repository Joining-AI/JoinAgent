# 导入logging模块，用于记录程序运行中的信息
import logging

# 导入time模块，用于处理时间相关操作
import time

# 使用typing模块的Any类型，表示可以接受任何类型的值
from typing import Any

# 导入tiktoken模块，这个模块可能是用于处理某种特定的令牌或认证
import tiktoken

# 从graphrag库中导入LocalContextBuilder类，用于构建本地上下文
from graphrag.query.context_builder.builders import LocalContextBuilder

# 从graphrag库中导入ConversationHistory类，用于存储对话历史
from graphrag.query.context_builder.conversation_history import ConversationHistory

# 从graphrag库中导入BaseLLM和BaseLLMCallback基类，可能与语言模型有关
from graphrag.query.llm.base import BaseLLM, BaseLLMCallback

# 从graphrag库中导入num_tokens函数，用于计算文本中的令牌数量
from graphrag.query.llm.text_utils import num_tokens

# 从graphrag库中导入BaseQuestionGen基类和QuestionResult类，与问题生成有关
from graphrag.query.question_gen.base import BaseQuestionGen, QuestionResult

# 从graphrag库中导入QUESTION_SYSTEM_PROMPT常量，可能是一个系统提示问题
from graphrag.query.question_gen.system_prompt import QUESTION_SYSTEM_PROMPT

# 这一行是版权声明，表示代码归Microsoft Corporation所有，并遵循MIT许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个名为"Local question generation"的模块，描述了这段代码的主要功能
"""Local question generation."""

# 创建一个日志器，名为__name__（当前模块的名字），用于记录程序运行信息
log = logging.getLogger(__name__)

# 这是一个定义了一个叫做LocalQuestionGen的类，它继承自BaseQuestionGen类
class LocalQuestionGen(BaseQuestionGen):
    # 这个类是用于在全局搜索模式下组织搜索的

    # 当创建一个LocalQuestionGen对象时，会执行这个函数
    def __init__(self,
                 # 这是一个语言模型，用于生成问题
                 llm: BaseLLM,
                 # 这是一个构建本地上下文的工具
                 context_builder: LocalContextBuilder,
                 # 用于编码令牌的工具，可能为空
                 token_encoder: tiktoken.Encoding | None = None,
                 # 系统提示的默认文本
                 system_prompt: str = QUESTION_SYSTEM_PROMPT,
                 # 可选的回调函数列表
                 callbacks: list[BaseLLMCallback] | None = None,
                 # 语言模型的额外参数
                 llm_params: dict[str, Any] | None = None,
                 # 上下文构建器的额外参数
                 context_builder_params: dict[str, Any] | None = None,
             ):
        # 调用基类的初始化方法
        super().__init__(
            llm=llm,
            context_builder=context_builder,
            token_encoder=token_encoder,
            llm_params=llm_params,
            context_builder_params=context_builder_params,
        )
        # 保存系统提示和回调函数
        self.system_prompt = system_prompt
        self.callbacks = callbacks

    # 这个异步函数用于根据历史问题和上下文数据生成一个问题
    async def agenerate(self,
                        question_history: list[str],
                        context_data: str | None,
                        question_count: int,
                        **kwargs,
                    ) -> QuestionResult:
        """
        根据历史问题和上下文数据生成一个问题。
        如果没有提供上下文数据，将使用历史数据生成
        """
        # 记录开始时间
        start_time = time.time()

        # 如果没有历史问题，那么问题文本为空，对话历史也为空
        if len(question_history) == 0:
            question_text = ""
            conversation_history = None
        else:
            # 从历史问题中获取最后一个问题作为当前问题
            question_text = question_history[-1]
            # 构建对话历史
            history = [{"role": "user", "content": query} for query in question_history[:-1]]
            conversation_history = ConversationHistory.from_list(history)

        # 如果没有提供上下文数据，就使用历史数据生成
        if context_data is None:
            context_data, context_records = self.context_builder.build_context(
                query=question_text,
                conversation_history=conversation_history,
                **kwargs,
                **self.context_builder_params,
            )
        else:
            context_records = {"context_data": context_data}

        # 输出信息
        log.info("开始生成问题：%s。上一个问题：%s", start_time, question_text)

        # 创建系统提示
        system_prompt = ""
        try:
            system_prompt = self.system_prompt.format(
                context_data=context_data, question_count=question_count
            )
            # 创建消息列表，包括系统提示和用户问题
            question_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question_text},
            ]

            # 使用语言模型生成回答
            response = await self.llm.agenerate(
                messages=question_messages,
                streaming=True,
                callbacks=self.callbacks,
                **self.llm_params,
            )

            # 返回问题结果，包括回答、上下文数据、完成时间等
            return QuestionResult(
                response=response.split("\n"),
                context_data={
                    "question_context": question_text,
                    **context_records,
                },
                completion_time=time.time() - start_time,
                llm_calls=1,
                prompt_tokens=num_tokens(system_prompt, self.token_encoder),
            )

        # 如果出错，记录异常并返回空回答
        except Exception:
            log.exception("生成问题时出错")
            return QuestionResult(
                response=[],
                context_data=context_records,
                completion_time=time.time() - start_time,
                llm_calls=1,
                prompt_tokens=num_tokens(system_prompt, self.token_encoder),
            )

    # 同样的功能，但不是异步版本
    def generate(self,
                 question_history: list[str],
                 context_data: str | None,
                 question_count: int,
                 **kwargs,
             ) -> QuestionResult:
        """
        根据历史问题和上下文数据生成一个问题。
        如果没有提供上下文数据，将使用历史数据生成
        """
        start_time = time.time()

        # 检查历史问题
        if len(question_history) == 0:
            question_text = ""
            conversation_history = None
        else:
            question_text = question_history[-1]
            history = [{"role": "user", "content": query} for query in question_history[:-1]]
            conversation_history = ConversationHistory.from_list(history)

        # 处理上下文数据
        if context_data is None:
            context_data, context_records = self.context_builder.build_context(
                query=question_text,
                conversation_history=conversation_history,
                **kwargs,
                **self.context_builder_params,
            )
        else:
            context_records = {"context_data": context_data}

        # 输出信息
        log.info("开始生成问题：%s。问题历史：%s", start_time, question_text)

        # 创建系统提示
        system_prompt = ""
        try:
            system_prompt = self.system_prompt.format(
                context_data=context_data, question_count=question_count
            )
            question_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question_text},
            ]

            # 使用语言模型生成回答
            response = self.llm.generate(
                messages=question_messages,
                streaming=True,
                callbacks=self.callbacks,
                **self.llm_params,
            )

            # 返回问题结果，包括回答、上下文数据、完成时间等
            return QuestionResult(
                response=response.split("\n"),
                context_data={
                    "question_context": question_text,
                    **context_records,
                },
                completion_time=time.time() - start_time,
                llm_calls=1,
                prompt_tokens=num_tokens(system_prompt, self.token_encoder),
            )

        # 如果出错，记录异常并返回空回答
        except Exception:
            log.exception("生成问题时出错")
            return QuestionResult(
                response=[],
                context_data=context_records,
                completion_time=time.time() - start_time,
                llm_calls=1,
                prompt_tokens=num_tokens(system_prompt, self.token_encoder),
            )


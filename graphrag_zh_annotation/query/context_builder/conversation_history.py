# 导入数据类模块，用于定义结构化数据
from dataclasses import dataclass
# 导入枚举模块，用于创建 ConversationRole 类型
from enum import Enum
# 导入 pandas 模块，这是一个数据分析库
import pandas as pd
# 导入 tiktoken 模块，这个模块可能用于处理某种特定的令牌或认证
import tiktoken
# 导入自定义的文本工具模块，用于计算令牌数量
from graphrag.query.llm.text_utils import num_tokens

# 版权声明，这是微软公司的代码，遵循 MIT 许可证
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

# 定义一个类，用于存储和管理对话历史
"""Classes for storing and managing conversation history."""

# 导入数据类和枚举模块，用于创建 ConversationRole 类
from dataclasses import dataclass
from enum import Enum

# 导入 pandas 和 tiktoken 模块
import pandas as pd
import tiktoken

# 导入文本工具模块
from graphrag.query.llm.text_utils import num_tokens

# 定义一个枚举类，表示对话中的角色
class ConversationRole(str, Enum):
    # 枚举值：系统、用户和助手
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    # 静态方法，将字符串转换为 ConversationRole 类型
    @staticmethod
    def from_string(value: str) -> "ConversationRole":
        # 根据输入的字符串返回相应的枚举值
        if value == "system":
            return ConversationRole.SYSTEM
        if value == "user":
            return ConversationRole.USER
        if value == "assistant":
            return ConversationRole.ASSISTANT

        # 如果输入的字符串无效，抛出错误
        msg = f"Invalid Role: {value}"
        raise ValueError(msg)

    # 返回枚举值的字符串表示形式
    def __str__(self) -> str:
        return self.value

# 定义一个数据类，用于存储对话中的一次交互（回合）
@dataclass
class ConversationTurn:
    # 属性：角色（ ConversationRole 类型）和内容（字符串）
    role: ConversationRole
    content: str

    # 返回对话回合的字符串表示
    def __str__(self) -> str:
        return f"{self.role}: {self.content}"

# 这里还定义了一个数据类，但没有显示完整的代码，可能还有其他属性或方法
@dataclass

# 定义一个叫做QATurn的类，它用来存储问答对的信息
class QATurn:
    """
    这个类是用来保存问答对的。有一个用户的问题和至少一个助手的答案。
    """

    # 这里定义了一个属性，user_query，它是一个ConversationTurn类型的对象，代表用户的问题
    user_query: ConversationTurn

    # 另一个属性，assistant_answers，它是一个列表，包含多个ConversationTurn类型的答案，或者可能是None
    assistant_answers: list[ConversationTurn] | None = None

    # 定义一个方法，get_answer_text，用于获取助手答案的文本
    def get_answer_text(self) -> str | None:
        """获取助手答案的文本内容，如果有的话。"""
        # 如果assistant_answers有内容，就将所有答案的content连接成一个字符串，并用换行符分隔
        # 如果assistant_answers为空，返回None
        return (
            "\n".join([answer.content for answer in self.assistant_answers])
            if self.assistant_answers
            else None
        )

    # 定义一个方法，__str__，用于打印QATurn对象时显示的字符串形式
    def __str__(self) -> str:
        """返回问答对的字符串表示形式。"""
        # 获取答案的文本
        answers = self.get_answer_text()

        # 如果有答案，返回问题和答案
        # 如果没有答案，只返回问题
        return (
            f"问题：{self.user_query.content}\n答案：{answers}"
            if answers
            else f"问题：{self.user_query.content}"
        )

# 定义一个类，用于存储对话历史记录
class ConversationHistory:
    # 类变量，用于保存对话回合
    turns: list[ConversationTurn]

    # 初始化函数，创建一个空的对话历史对象
    def __init__(self):
        self.turns = []

    # 类方法，从包含对话回合字典的列表创建对话历史
    @classmethod
    def from_list(cls, conversation_turns: list[dict[str, str]]) -> "ConversationHistory":
        # 创建一个新的对话历史对象
        history = cls()
        # 遍历每个对话回合
        for turn in conversation_turns:
            # 从字典中获取角色和内容，如果没有提供角色，默认为用户
            role = ConversationRole.from_string(turn.get("role", ConversationRole.USER))
            content = turn.get("content", "")
            # 将对话回合添加到历史记录中
            history.turns.append(ConversationTurn(role=role, content=content))
        # 返回创建的对话历史对象
        return history

    # 添加一个新的对话回合到历史记录
    def add_turn(self, role: ConversationRole, content: str):
        self.turns.append(ConversationTurn(role=role, content=content))

    # 将对话历史转换为问答回合列表
    def to_qa_turns(self) -> list[QATurn]:
        # 初始化一个空的问答回合列表
        qa_turns = list[QATurn]()
        # 初始化当前问答回合
        current_qa_turn = None
        # 遍历对话历史
        for turn in self.turns:
            # 如果是用户发言，创建或更新问答回合
            if turn.role == ConversationRole.USER:
                if current_qa_turn:
                    qa_turns.append(current_qa_turn)
                current_qa_turn = QATurn(user_query=turn, assistant_answers=[])
            # 如果是助手回答，添加到当前问答回合
            else:
                if current_qa_turn:
                    current_qa_turn.assistant_answers.append(turn)  # 忽略类型检查
        # 添加最后一个问答回合
        if current_qa_turn:
            qa_turns.append(current_qa_turn)
        # 返回问答回合列表
        return qa_turns

    # 获取对话历史中的最后若干个用户发言
    def get_user_turns(self, max_user_turns: int | None = 1) -> list[str]:
        # 初始化一个空的用户发言列表
        user_turns = []
        # 从后往前遍历对话历史
        for turn in self.turns[::-1]:
            # 如果是用户发言，将其内容添加到列表
            if turn.role == ConversationRole.USER:
                user_turns.append(turn.content)
                # 如果达到最大数量，停止添加
                if max_user_turns and len(user_turns) >= max_user_turns:
                    break
        # 返回用户发言列表
        return user_turns

    # 根据参数构建对话历史的上下文数据
    def build_context(
        self,
        token_encoder: tiktoken.Encoding | None = None,
        include_user_turns_only: bool = True,
        max_qa_turns: int | None = 5,
        max_tokens: int = 8000,
        recency_bias: bool = True,
        column_delimiter: str = "|",
        context_name: str = "Conversation History",
    ) -> tuple[str, dict[str, pd.DataFrame]]:
        # 转换为问答回合
        qa_turns = self.to_qa_turns()
        # 只包括用户发言
        if include_user_turns_only:
            qa_turns = [QATurn(user_query=qa_turn.user_query, assistant_answers=None) for qa_turn in qa_turns]
        # 按时间顺序反向排列（最近的在前）
        if recency_bias:
            qa_turns = qa_turns[::-1]
        # 截取最多多少个问答回合
        if max_qa_turns and len(qa_turns) > max_qa_turns:
            qa_turns = qa_turns[:max_qa_turns]

        # 构建上下文文本和数据框
        if len(qa_turns) == 0:
            return ("", {context_name: pd.DataFrame()})
        
        # 添加上下文标题
        header = f"-----{context_name}-----" + "\n"

        # 初始化回合列表和当前数据框
        turn_list = []
        current_context_df = pd.DataFrame()

        # 遍历问答回合
        for turn in qa_turns:
            # 添加用户和助手的发言到回合列表
            turn_list.append({"turn": ConversationRole.USER.__str__(), "content": turn.user_query.content})
            if turn.assistant_answers:
                turn_list.append({"turn": ConversationRole.ASSISTANT.__str__(), "content": turn.get_answer_text()})
            
            # 创建数据框并检查是否超过最大令牌数
            context_df = pd.DataFrame(turn_list)
            context_text = header + context_df.to_csv(sep=column_delimiter, index=False)
            if num_tokens(context_text, token_encoder) > max_tokens:
                break

            current_context_df = context_df

        # 返回最终的上下文文本和数据框
        return (context_text, {context_name.lower(): current_context_df})


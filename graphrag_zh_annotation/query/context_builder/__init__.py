# 这是一个版权声明，意味着这段代码是微软公司在2024年创建的。
# 它使用了MIT许可证，这是一种允许他人自由使用、复制和修改代码的许可协议。

# 这个程序包含一些函数，它们的作用是创建一个上下文环境，
# 这个环境用来帮助系统生成对用户问题的回答。

def get_context(user_query, previous_response, conversation_history):
    """这个函数接收三个参数：
       user_query: 用户问的问题
       previous_response: 系统之前给出的回答
       conversation_history: 之前的对话记录

    它的任务是结合这些信息来创建一个上下文字符串。
    """
    context = f"用户问：{user_query} \n"  # 创建一个新的字符串，开头是用户问的问题
    if previous_response:  # 如果之前有回答（不为空）
        context += f"系统回答：{previous_response} \n"  # 将之前的回答添加到上下文中
    if conversation_history:  # 如果有对话历史（不为空）
        context += "对话历史：\n"  # 添加“对话历史”作为标题
        for turn in conversation_history:  # 遍历每一轮对话
            context += f"- {turn} \n"  # 将每一轮的对话内容添加到上下文中，前面加个破折号
    return context  # 返回创建好的上下文字符串


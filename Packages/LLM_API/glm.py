from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

class GLMService:
    def __init__(self, version="glm-3-turbo"):
        # 加载当前目录的.env文件
        load_dotenv()
        self.version=version
        self.total_tokens_used = 0  # 用于保存总共使用的token数量
        # 从环境变量中导入API密钥
        self.api_key = os.getenv('GLM_API', None)
        self.client = ZhipuAI(api_key=self.api_key)  # 创建客户端实例

    def ask_once(self, query, url=None):
        """
        使用zhipuai库向GLM-3-Turbo模型发送请求并获取回答
        :param query: 用户的查询字符串
        :return: 模型的回答字符串
        """
        if self.version in ['glm-3-turbo', 'glm-4']:
            response = self.client.chat.completions.create(
                model=self.version,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            # 检查响应并提取信息
            if response.choices:
                # 正确地访问响应对象的属性
                message = response.choices[0].message.content
                # 更新token使用量
                if hasattr(response, 'usage'):
                    self.total_tokens_used += response.usage.total_tokens
                return message
            else:
                return "无法获取回答。"
            
        else:
            if url is None:  # 检查是否提供了URL
                return None, "请提供图像URL"
            response = self.client.chat.completions.create(
                model=self.version,  # 填写需要调用的模型名称
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url
                                }
                            }
                        ]
                    }
                ]
            )

            
            # 检查响应并提取信息
            if response.choices:
                # 正确地访问响应对象的属性
                message = response.choices[0].message.content
                # 更新token使用量
                if hasattr(response, 'usage'):
                    self.total_tokens_used += response.usage.total_tokens
                return message, None
            else:
                return None, "无法获取回答。"
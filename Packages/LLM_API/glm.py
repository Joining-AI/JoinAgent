from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv
import base64

class GLMService:
    def __init__(self, version="glm-3-turbo"):
        # 加载当前目录的.env文件
        load_dotenv()
        self.version=version
        self.total_tokens_used = 0  # 用于保存总共使用的token数量
        # 从环境变量中导入API密钥
        self.api_key = os.getenv('GLM_API', None)
        self.client = ZhipuAI(api_key=self.api_key)  # 创建客户端实例

    def ask(self, query):
        """
        使用zhipuai库向GLM-3-Turbo模型发送请求并获取回答
        :param query: 用户的查询字符串
        :return: 模型的回答字符串
        """
        if self.version in ['glm-4v']:
            self.version='glm-4'
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
            

            
    def ask_pic(self, query, image_path):
        """
        使用zhipuai库向GLM模型发送请求并识别图像
        :param query: 用户的查询字符串
        :param image_path: 图像文件路径
        :return: 模型的回答字符串
        """
        # 读取图像文件并进行Base64编码
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = self.client.chat.completions.create(
            model="glm-4v",
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
                                "url": base64_image
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
            return message
        else:
            return "无法获取回答。"
import os
from dotenv import load_dotenv
from openai import OpenAI

class DeepSeekService:
    def __init__(self, version='chat'):
        # 加载当前目录的.env文件
        load_dotenv()

        self.version='deepseek-'+version
        self.client = None
        self.initialized = False
        self.total_tokens_used = 0  # 添加一个成员变量用于保存总共使用的token数量
        # 从环境变量中导入API密钥和基础URL
        api_key = os.getenv('DEEPSEEK_API', None)
        base_url ='https://api.deepseek.com'
        self.init_service(api_key, base_url)

    def init_service(self, api_key: str, base_url: str) -> bool:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.initialized = True
        return True

    def ask_once(self, prompt: str) -> str:
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")
        
        if not self.client:
            raise ValueError("OpenAI 客户端未正确初始化，请检查初始化过程。")
        
        response = self.client.chat.completions.create(
            model=self.version,
            messages=[{"role": "user", "content": prompt}]
        )

        if response:
            total_tokens = response.usage.total_tokens
            self.total_tokens_used += total_tokens  # 更新总共使用的token数量
            #print("本次使用的token数量：", total_tokens)
            return response.choices[0].message.content
        else:
            return ""

import os
import base64
import requests
from dotenv import load_dotenv
from http import HTTPStatus

class HuidaService:
    def __init__(self, model='gpt-4o'):
        # 加载当前目录的.env文件
        load_dotenv()

        self.model = model
        self.api_key = os.getenv('HUIDA_API_KEY', None)
        self.url = 'https://api.huida.app/v1/chat/completions'
        self.initialized = False
        self.input_word_count = 0  # 输入字数
        self.output_word_count = 0  # 输出字数

        if self.api_key:
            self.initialized = True
            print("服务初始化成功")
        else:
            raise ValueError("API密钥未在环境变量中设置")

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def ask_once(self, message, image_path=None, language='中文'):
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = [
            {"role": "system", "content": f"你是一个忠实的助手，请你尊重用户的指令"},
            {"role": "user", "content": message}
        ]

        if image_path:
            base64_image = self.encode_image(image_path)
            messages.append({"role": "user", "content": [
                {"type": "text", "text": message},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]})

        data = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post(self.url, headers=headers, json=data, verify=False)
        if response.status_code == HTTPStatus.OK:
            output_content = response.json()["choices"][0]["message"]['content']
            self.input_word_count = len(message)
            self.output_word_count = len(output_content)
            return output_content
        else:
            return f"请求失败: {response.status_code} - {response.text}"
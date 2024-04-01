import requests
import json
import jwt
import os
import time
import threading
from dotenv import load_dotenv

class SenseService:
    def __init__(self, version='SenseChat',refresh_interval=1700):
        self.version=version
        self.base_url = "https://api.sensenova.cn/v1/llm"
        self.ak = os.getenv("SENSETIME_AK", None)  # 从环境变量获取AK
        self.sk = os.getenv("SENSETIME_SK", None)   # 从环境变量获取SK
        self.authorization = None
        self.refresh_interval = refresh_interval
        self.timer = None
        self.lock = threading.Lock()
        self.refresh_token()
        self.total_tokens_used = 0 

    def generate_jwt_token(self):
        headers = {"alg": "HS256", "typ": "JWT"}
        payload = {"iss": self.ak, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5}
        token = jwt.encode(payload, self.sk, algorithm="HS256", headers=headers)
        return token

    def refresh_token(self):
        with self.lock:
            self.authorization = self.generate_jwt_token()
            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(self.refresh_interval, self.refresh_token)
            self.timer.start()

    def send_get_request(self):
        url = "https://api.sensenova.cn/v1/llm/models"
        headers = {
            "Authorization": "Bearer " +self.authorization,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        return print(response.json())

    def ask_once(self,messages=None, know_ids=None, max_new_tokens=None, n=1, repetition_penalty=1.05, stream=False, temperature=0.8, top_p=0.7, user=None, knowledge_config=None, plugins=None, retry_count=0):
        url = self.base_url+'/chat-completions'
        headers = {"Content-Type": "application/json", "Authorization": "Bearer "+self.authorization}
        payload = {
            "max_new_tokens": max_new_tokens if max_new_tokens is not None else 1024,
            "messages":  [{
                "content": messages,
                "role": "user"
            }],
            "model": self.version,
            "n": n,
            "repetition_penalty": repetition_penalty,
            "stream": stream,
            "temperature": temperature,
            "top_p": top_p,
            'knowledge_config':{},
            'plugins':{}
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        # 提取'message'字段的值
        total_tokens = response_data['data']['usage']['total_tokens']
        self.total_tokens_used += total_tokens  # 更新总共使用的token数量
        message = response_data['data']['choices'][0]['message']
        if response.status_code == 200:
            print("本次使用的token数量：", total_tokens)
            return message
        elif response.status_code == 401:
            if retry_count < 3:  # 允许最多重试3次
                self.refresh_token()  # 刷新token
                return self.send_request(know_ids, max_new_tokens, messages, model, n, repetition_penalty, stream, temperature, top_p, user, knowledge_config, plugins, retry_count + 1)
            else:
                # 超过重试次数，可以返回错误信息或抛出异常
                return {"error": "Authentication failed after 3 retries."}
        else:
            return response.status_code

    def embed(self, input_text=None, model='nova-embedding-stable', retry_count=0):
        url = self.base_url + "/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+self.authorization
        }
        payload = {
            "model": model,
            "input": [input_text]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_data = response.json()
            embedding = {}
            embeddings = response_data.get('embeddings', [])
            if embeddings:
                embedding = embeddings[0].get('embedding', {})
            return embedding
        elif response.status_code == 401:
            if retry_count < 3:
                self.refresh_token()  # 刷新token
                return self.embeddings(model, input_text, retry_count + 1)
            else:
                return {"error": "Authentication failed after 3 retries."}
        else:
            return {"error": f"Request failed with status code {response.status_code}"}


    def __del__(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
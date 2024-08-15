import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import base64
import numpy as np
import concurrent.futures
from tqdm import tqdm

class LLM:
    def __init__(self, version='coder', api_key=None):
        load_dotenv()
        self.version = 'deepseek-' + version
        self.client = None
        self.initialized = False
        self.total_tokens_used = 0

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('DEEPSEEK_API', None)
        
        base_url = 'https://api.deepseek.com'
        self.init_service(self.api_key, base_url)

    def init_service(self, api_key: str, base_url: str) -> bool:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.initialized = True
        return True

    def ask(self, prompt: str) -> str:
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
            self.total_tokens_used += total_tokens
            return response.choices[0].message.content
        else:
            return ""

class MultiLLM:
    def __init__(self, model='deepseek-coder', vision_model='gpt-4o-mini', embed_model='text-embedding-3-large'):
        load_dotenv()
        self.model = model
        self.vision_model = vision_model
        self.embed_model = embed_model
        self.api_key = os.getenv('MULTI_LLM_API', None)
        if not self.api_key:
            raise ValueError("API key not found. Please set the MULTI_LLM_API environment variable.")

    def ask(self, prompt):
        url = "https://api.openai-next.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}, 
                {"role": "user", "content": prompt}
            ]
        }
        
        return self._make_request(url, headers, data, 'ask')

    def look(self, image_path, prompt="What's in this image?"):
        url = "https://api.openai-next.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        base64_image = self._encode_image(image_path)

        payload = {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
        }

        return self._make_request(url, headers, payload, 'look')

    @staticmethod
    def _encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def embed_text(self, input_text):
        url = "https://api.openai-next.com/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)"
        }
        data = {
            "model": self.embed_model,
            "input": input_text
        }
        
        return self._make_request(url, headers, data, 'embed')

    def embed_list(self, texts, num_threads=200):
        def process_text(text):
            embedding = self.embed_text(text)
            return text, embedding

        embeddings = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_text = {executor.submit(process_text, text): text for text in texts}
            for future in tqdm(concurrent.futures.as_completed(future_to_text), total=len(texts), desc="Embedding texts"):
                text = future_to_text[future]
                try:
                    _, embedding = future.result()
                    embeddings[text] = embedding
                except Exception as exc:
                    embeddings[text] = None
                    print(f'Text {text} generated an exception: {exc}')
        
        return embeddings
    
    def partition_by_similarity(self, embeddings_dict, threshold=0.8):
        def cosine_similarity_matrix(matrix):
            norm = np.linalg.norm(matrix, axis=1)
            return np.dot(matrix, matrix.T) / np.outer(norm, norm)

        keys = list(embeddings_dict.keys())
        embeddings = np.array([embeddings_dict[key] for key in keys])

        similarity_matrix = cosine_similarity_matrix(embeddings)
        np.fill_diagonal(similarity_matrix, 0)

        result = {}
        valid_indices = set(range(len(keys)))

        for i in range(len(keys)):
            if i not in valid_indices:
                continue

            similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
            similar_keys = [keys[j] for j in similar_indices if j in valid_indices]

            for idx in similar_indices:
                valid_indices.discard(idx)

            result[keys[i]] = {'Similar_keys': similar_keys}

        return result

    def calculate_similarity(self, text1, text2):
        embedding1 = self.embed_text(text1)
        embedding2 = self.embed_text(text2)

        if embedding1 is None or embedding2 is None:
            return None

        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity

    def _make_request(self, url, headers, data, request_type):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            
            if request_type == 'ask' or request_type == 'look':
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    return response_json['choices'][0]['message']['content']
                else:
                    raise ValueError("No response content found in the API response.")
            elif request_type == 'embed':
                if 'data' in response_json and len(response_json['data']) > 0:
                    return response_json['data'][0]['embedding']
                else:
                    raise ValueError("No embedding found in the API response.")
            else:
                raise ValueError(f"Unknown request type: {request_type}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error occurred during the API request: {e}")

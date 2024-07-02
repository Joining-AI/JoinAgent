import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
import time
from transformers import AutoTokenizer, AutoModel

class Embedder:
    def __init__(self, model_path, batch_size=32, stats_interval=5):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
        self.model.eval()
        self.batch_size = batch_size
        self.stats_interval = stats_interval

    def embed_list(self, elem_list):
        start_time = time.time()
        total_elems = len(elem_list)
        embeddings_dict = {}

        for i in range(0, total_elems, self.batch_size):
            batch_elems = elem_list[i:i+self.batch_size]
            inputs = self.tokenizer(batch_elems, return_tensors="pt", padding=True, truncation=True, max_length=512)
            batches_processed = 0
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).detach().cpu().numpy()

            for elem, embedding in zip(batch_elems, embeddings):
                embeddings_dict[elem] = embedding

            batches_processed += 1
            if batches_processed % self.stats_interval == 0 or (i + self.batch_size) >= total_elems:
                elapsed_time = time.time() - start_time
                elems_processed = min((batches_processed) * self.batch_size, total_elems)
                print(f"已处理 {elems_processed}/{total_elems} 个元素，耗时 {elapsed_time:.2f}秒，速度：{elems_processed / elapsed_time:.2f}个元素/秒")

        return embeddings_dict

    def get_embedding(self, text):
        inputs = self.tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).detach().cpu().numpy()
        return embedding[0]

    def find_most_similar(self, question_str, dict_list, vector_key,query_key,answer_key):
        question_embedding = self.get_embedding(question_str).reshape(1, -1)
        embeddings = np.array([np.array(item[vector_key]) for item in dict_list])
        similarities = cosine_similarity(question_embedding, embeddings)
        max_similarity = np.max(similarities)
        most_similar_idx = np.argmax(similarities)
        most_similar_doc = dict_list[most_similar_idx]
        return most_similar_doc[query_key], most_similar_doc[answer_key]

    @staticmethod
    def step2_contains_digit(string):
        return any(char.isdigit() for char in string)

    def partition_by_similarity(self, data_dict, threshold):
        keys = list(data_dict.keys())
        vectors = [data_dict[key]["嵌入向量"] for key in keys]
        
        # 计算相似度矩阵
        similarity_matrix = cosine_similarity(vectors)

        num_vectors = similarity_matrix.shape[0]
        partition = {}
        visited = set()  # 记录已经分过区的向量索引

        for i in range(num_vectors):
            if i in visited:
                continue
            similar_indices = np.where(similarity_matrix[i] > threshold)[0]
            similar_keys = []
            main_key = keys[i]

            if self.step2_contains_digit(main_key):
                visited.add(i)
                partition[main_key] = {"Similar_keys": []}
                continue

            for j in similar_indices:
                if j == i:
                    continue
                similar_key = keys[j]
                if not self.step2_contains_digit(similar_key):
                    similar_keys.append(similar_key)
                    visited.add(j)
                else:
                    partition[similar_key] = {"Similar_keys": []}
                    visited.add(j)

            partition[main_key] = {"Similar_keys": similar_keys}
            visited.add(i)

        return partition

# coding=utf-8
import time

from loguru import logger

import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self,
                 model_path="./bge-large-en-v1.5") -> None:
        self.model_path = model_path

        self.model = self.__load()
     
    def __load(self):
        logger.debug(f"Start load model = [{self.model_path}]")
        return SentenceTransformer(self.model_path)
    
    def embedding_sentence(self, sentence: str):
        btime = time.time()
        resp = self.model.encode([sentence], normalize_embeddings=True)[0]
        #logger.debug(f"Embedding cost time = [{time.time() - btime}]")
        return [float(_v) for _v in list(resp)]

    def cosine_similary_with_str(self, sentence1: str, sentence2: str):
        vec1 = np.array(self.embedding_sentence(sentence1))
        vec2 = np.array(self.embedding_sentence(sentence2))
        return vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def cosine_similary_with_vec(self, vec1: list, vec2: list):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

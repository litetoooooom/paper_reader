# coding=utf-8
from FlagEmbedding import FlagReranker
from loguru import logger

class PaperRank:
    def __init__(self, model_dir = "./bge-reranker-large") -> None:
        logger.debug(f"Start load model = [{model_dir}]")
        self.reranker = FlagReranker(model_dir, use_fp16=True)

    def rank(self, query: str, informations: list):
        
        cand_list = [[query, info['title']] for info in informations]

        scores = self.reranker.compute_score(cand_list)
        cand_score = [(i, score) for i, score in enumerate(scores)]
        
        return sorted(cand_score, key=lambda x: x[1], reverse=True)

"""
ps = PaperSearch() 
r = ps.rank("large language model", [{"title": "language model"}, {"title": "aaa"}, {"title": "bbb"}, {"title": "ccc"}])
print (r)
"""
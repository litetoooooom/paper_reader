# coding=utf-8
from datetime import datetime, timedelta, date

import arxiv
from loguru import logger


class PaperInterface:
    def __init__(self) -> None:
        self.client = arxiv.Client()
    
    def search(self, query, max_results):
        logger.debug(f"paper interface params: query = {query}, max_results = {max_results}")
        search = arxiv.Search(
            query = query,
            max_results = max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )
        result = list(self.client.results(search))
        logger.debug(f"fetch results length = [{len(result)}]")
        return result
     
    def get_specify_data_paper(self, 
                               paper_date:datetime, 
                               category_name:str, 
                               max_results=200):
        """ 拿到指定类别下，指定日期的数据
        
        args:
            paper_date:  格式 %Y%m%d
            category_name: 指定子类，比如: cs.AI
            max_results: 返回的最大结果数
        """
        tomorrow_date = paper_date + timedelta(days=1)
        return self.get_specify_data_range_paper(paper_date, tomorrow_date, category_name, max_results)
        
    def get_specify_data_range_paper(self, 
                               start_date:datetime, 
                               end_date:datetime, 
                               category_name:str, 
                               max_results=200):
        """ 拿到指定类别下，指定日期范围的数据
        
        args:
            start_date
            end_date:
            category_name: 指定子类，比如: cs.AI
            max_results: 返回的最大结果数
        """
        query = f"cat:{category_name} AND submittedDate:[{start_date.strftime('%Y%m%d')}0000 TO {end_date.strftime('%Y%m%d')}0000]"
        return self.search(query, max_results)
    

"""
pi = PaperInterface()

lastday = date.today() - timedelta(days=1)
r = pi.get_specify_data_paper(lastday, "cs.AI")

for result in r:
    print(f"标题: {result.title}")
    print(f"作者: {', '.join(author.name for author in result.authors)}")
    print(f"摘要: {result.summary}")
    print(f"发布日期: {result.published}")
    print(f"链接: {result.entry_id}\n")
"""
# coding=utf-8

import os
import time
import json
import random
from datetime import datetime, date, timedelta

from loguru import logger

from paper_reader.utils import format_date
from paper_reader.paper_fetch import PaperInterface

class PaperData:
    def __init__(self, cache_path="./cache_data") -> None:
        
        self.cache_path = cache_path
        self._cache = {}  #缓存的数据
    
    def __read_cache_file(self, fname:str):
        """ 读取缓存的文件数据
        """
        res = []
        with open(fname, "r") as fr:
            for line in fr:
                line = line.strip()
                if line:
                    res.append(json.loads(line))
        return res
        
    def refresh_cache_data(self, categories: list):
        """ 刷新文件的缓存数据
        """
        logger.debug("Start refresh cache data...")
        category_names = os.listdir(self.cache_path)
        self._cache = {cname:{} for cname in category_names + categories}
         
        for cname in category_names:
            now_path = os.path.join(self.cache_path, cname)        
            for fname in os.listdir(now_path):
                _temp_name = os.path.join(now_path, fname)
                _temp_data = self.__read_cache_file(_temp_name) 
                self._cache[cname][fname] = _temp_data 

        logger.debug("OK")

    def write_cache_data(self, category_name: str, filename: str, results: list):
        """ 将生成的数据写入到文件

        args:
            category_name: 子类名
            filename: 保存的文件名
            reuslts: 待写入的数据
        """
        dir_path = os.path.join(self.cache_path, category_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        write_fname = os.path.join(dir_path, filename)
        with open(write_fname, "w", encoding="utf-8") as fw:
            for res in results:
                _str = json.dumps(res, ensure_ascii=False)
                fw.write(f"{_str}\n")

        logger.debug(f"Write file, fname = [{write_fname}], done.")
    
    def judge_exists(self, exists_list, single_infor):
        for _cand in exists_list:
            if single_infor["title"] == _cand["title"]:
                return True
        return False
         
    def filter_cache_data(self, 
                          categories: list, 
                          start_date: datetime, 
                          end_date: datetime):
        """ 根据条件对数据进行过滤
        
        args:
            categores:
            start_date:
            end_date
        """
        if len(self._cache) == 0:
            self.refresh_cache_data(categories)
        
        candidate = []
        
        for cate_name in categories:
            if cate_name not in self._cache:
                continue
            for _d_date, _d in self._cache[cate_name].items():
                str2date = datetime.strptime(_d_date, "%Y%m%d").date()
                if start_date <= str2date <= end_date:
                    candidate.extend([_temp for _temp in _d if not self.judge_exists(candidate, _temp)])
        
        return candidate
     
    def load_paper_data(self, 
                        start_date: datetime, 
                        end_date: datetime, 
                        categories: list):
        """ 加载指定类别中，缺失的论文数据

        args:
            start_date: 开始日期
            end_date: 结束日期
            categoris: 论文子类，比如：cs.AI, cs.LG
        """
        logger.debug("Start load paper data...")
        # 刷新已缓存的论文数据
        self.refresh_cache_data(categories)
       
        # 默认最多获取过去30天的数据 
        fetch_date_dict = {}
        for delta in range(1, 31, 1):
            d_date = date.today() - timedelta(days=delta)
            fetch_date_dict[format_date(d_date)] = d_date

        paper_data_call = PaperInterface()
        for cate_name in categories:
            for _f_date_format, _date in fetch_date_dict.items():
                # 判断当前缓存中是否存在指定类别指定日期的数据
                if _f_date_format in self._cache[cate_name]:
                    continue
                
                if _date >= end_date or _date < start_date:
                    continue
                
                paper_result = paper_data_call.get_specify_data_paper(_date, cate_name, max_results=200)
                trans_paper_result = []
                for paper in paper_result:
                    _p = {
                        "title": paper.title,
                        "author": ', '.join(author.name for author in paper.authors),
                        "abstract": paper.summary,
                        "published": paper.published.strftime("%Y-%m-%d"),
                        "categories": paper.categories,
                        "links": paper.entry_id
                    }
                    trans_paper_result.append(_p)
                self.write_cache_data(cate_name, _f_date_format, trans_paper_result)
                # 获取完成后随机睡眠5-10秒，控制请求频率
                time.sleep(random.randint(5, 10))
        # 刷新已缓存的论文数据
        self.refresh_cache_data(categories)
                
                
"""    
paper_d = PaperData()
paper_d.load_paper_data("2024-01-04"["cs.AI"])
"""
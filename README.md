![主页](./images/jiemian.png)

# 论文阅读助手

1. 能自动获取指定类别，指定日期范围的arxiv论文数据
2. 支持embedding的query-title的检索

# TODO 

1. 论文embedding缓存，当前每次重新计算，导致排序的时间很长
2. 添加论文的翻译或者简单总结信息，辅助筛选

# RUN

1. [download ranker model](https://huggingface.co/BAAI/bge-reranker-large), 将下载好的模型放置到项目路径下，也可以自行选择是否使用其他的模型。
2. 创建本地缓存目录 `mkdir cache_data`
3. `pip install -r requirements.txt` 可自定切换国内源
4. `streamlit run app.py`

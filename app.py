# coding=utf-8

import streamlit as st
from datetime import datetime, date, timedelta
from paper_reader.load_data import paper_data_obj

from paper_reader.shared import em_model

def display_paper(paper, score, index):
    st.markdown(f"{index}: {paper['title_translate'].strip()}")
    st.markdown(f"标题：{paper['title']}")
    st.markdown(f"分析: {paper['abstract_summary'].strip()}")

    st.caption(f"作者: {paper['author']}")
    st.caption(f"类别: {paper['categories']}")
    st.caption(f"链接: {paper['links']}")
    st.caption(f"日期: {paper['published']}")
    st.write("---")

def display_search_results(query, start_date, end_date, categories):
    filter_data = paper_data_obj.filter_cache_data(categories, start_date, end_date)
    st.write(f"结果数：{len(filter_data)}")

    st.write(f"正在排序中...")
    query_embedding = em_model.embedding_sentence(query)
    candidate_unsorted_fd_index = [(em_model.cosine_similary_with_vec(query_embedding, _d['title_embedding']), _i) for _i, _d in enumerate(filter_data)]

    count = 1
    for score, index, in sorted(candidate_unsorted_fd_index, key=lambda x: x[0], reverse=True):
        display_paper(filter_data[index], score, count)
        count += 1

def load_paper(start_date: datetime, end_date: datetime, categories: list):
    st.write("正在加载中...")
    paper_data_obj.load_paper_data(start_date, end_date, categories)
    return "已加载完成"

def main():
    st.title('论文阅读助手')

    page = st.session_state.get('page', 'search')

    categories = st.multiselect("选择类别", ['cs.AI', 'cs.CV', 'cs.LG', 'cs.CL', 'cs.SE', 'stat.ML'], ['cs.AI', 'cs.CV', 'cs.LG', 'cs.CL', 'stat.ML'])    
    st.caption('只支持过去一个月的日期选择')
    one_month_ago = date.today() - timedelta(days=30)

    # 默认值，因arxiv更新存在的延迟和时区的问题，尽量在当天下午请求获取昨天的数据
    lastday = date.today() - timedelta(days=1)
    
    with st.form(key='search_form'):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("起始日期", lastday, min_value=one_month_ago, max_value=date.today())
        with col2:
            end_date = st.date_input("结束日期", date.today(), min_value=one_month_ago, max_value=date.today())
        query = st.text_input('输入你的搜索内容')

        coll1, coll2 = st.columns(2)
        with coll1:
            submit_button = st.form_submit_button('搜索')
        with coll2:
            load_button = st.form_submit_button('加载数据')
        
    if submit_button:
        display_search_results(query, start_date, end_date, categories)

    if load_button:
        result = load_paper(start_date, end_date, categories)
        st.write(result)

if __name__ == "__main__":
    main()

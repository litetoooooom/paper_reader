# coding=utf-8

import streamlit as st
from datetime import datetime, date, timedelta

from paper_reader.shared import paper_data, paper_rank

def display_paper(paper):
    st.caption(f"标题：{paper['title']}")
    st.caption(f"作者: {paper['author']}")
    st.caption(f"日期: {paper['published']}")
    st.caption(f"摘要: {paper['abstract']}")
    st.caption(f"类别: {paper['categories']}")
    st.caption(f"链接: {paper['links']}")
    st.write("---")

def display_search_results(query, start_date, end_date, categories):
    st.write(f"显示与 '{query}' 相关的结果")
    filter_data = paper_data.filter_cache_data(categories, start_date, end_date)

    st.write(f"正在排序中...")
    sorted_index = paper_rank.rank(query, filter_data)
    
    for _index, score in sorted_index:
        display_paper(filter_data[_index])

def load_paper(start_date: datetime, end_date: datetime, categories: list):
    st.write("正在加载中...")
    paper_data.load_paper_data(start_date, end_date, categories)
    return "已加载完成"

def main():
    st.title('论文阅读助手')

    page = st.session_state.get('page', 'search')

    categories = st.multiselect("选择类别", ['cs.AI', 'cs.CV', 'cs.LG', 'cs.CL', 'stat.ML'], ['cs.AI', 'cs.CV', 'cs.LG', 'cs.CL', 'stat.ML'])    
    st.caption('只支持过去一个月的日期选择')
    one_month_ago = date.today() - timedelta(days=30)

    # 默认值
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

import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
# from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import datetime
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from openai import OpenAI

# Title of the app
st.title("Solar Tycoon (Jeju Ver. 🏝️)")

starting_message = "제주도 고수들의 비법을 물어보세요. (현재 지원 카테고리: 음식점/카페/디저트)"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        # {"role": "assistant", "content": "Hello, please enter the name of the restaurant you're interested in! 🍽️"})
        {"role": "assistant", "content": starting_message})
else:
    if st.session_state.messages[0]['content'] == "리뷰 분석을 원하시는 제주도 업체명을 입력해주세요!":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.messages = []
        st.session_state.messages.append(
            # {"role": "assistant", "content": "Hello, please enter the name of the restaurant you're interested in! 🍽️"})
            {"role": "assistant", "content": starting_message})



print("2.messages", st.session_state.messages)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) == str:
            st.markdown(message["content"])
        else:
            st.dataframe(message["content"])


def click_button(cat):
    st.session_state.messages.append({"role": "assistant", "content": f"선택하신 카테고리는 다음과 같습니다 : {cat}\n\n"
                                                                      f"해당 카테고리의 고수에게 궁금한 것을 물어보세요!"})
    st.session_state.selected_category = cat
    st.session_state.category_bool = True


if "category_bool" not in st.session_state:
    st.session_state.category_bool = False

if "selected_category" not in st.session_state:
    category_list = ["음식점", "카페", "디저트"]
    with st.chat_message("assistant"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button(category_list[0], key=category_list[0], on_click=click_button, args=[category_list[0]],
                      use_container_width=True)

        with col2:
            st.button(category_list[1], key=category_list[1], on_click=click_button, args=[category_list[1]],
                      use_container_width=True)

        with col3:
            st.button(category_list[2], key=category_list[2], on_click=click_button, args=[category_list[2]],
                      use_container_width=True)

if "review_prepared" not in st.session_state:
    if "restaurant_num" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("리뷰 수집중..."):
                df = get_review(st.session_state.restaurant_num)
            st.markdown("아래와 같이 리뷰 데이터를 수집하였습니다.")
            st.dataframe(df)
            st.markdown("수집된 리뷰에서 궁금하신 점을 물어보세요!")
            st.session_state.messages.append({"role": "assistant", "content": "아래와 같이 리뷰 데이터를 수집하였습니다."})
            st.session_state.messages.append({"role": "assistant", "content": df})
            st.session_state.messages.append({"role": "assistant", "content": "수집된 리뷰에서 궁금하신 점을 물어보세요!"})
            st.session_state.review_df = df
            st.session_state.review_prepared = True


def stream_message(review_df, user_message):
    client = OpenAI(
        api_key="up_xPYsCK4N53bp1LFE6wV4L8MhvAh9J",
        base_url="https://api.upstage.ai/v1/solar"
    )

    stream = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=[
            {
                "role": "system",
                "content": "당신은 리뷰 분석 AI입니다. 당신의 목표는 사용자의 질문에 성심성의껏 답변하는 것입니다."
            },
            {
                "role": "user",
                "content": f"""
                ###로 감싸진 참고 정보를 활용하여, ```로 감싸진 사용자의 질문에 성심성의껏 답변하세요.

                ###
                참고 정보 : {str(review_df['content'].to_list())}
                ###

                ```
                사용자 질문 : {user_message}
                ```
                """
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


# Accept user input
if user_message := st.chat_input("Send Message", disabled=~st.session_state.category_bool):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_message)

    if not "review_prepared" in st.session_state:
        # Perform search and display results
        with st.chat_message("assistant"):
            with st.spinner("업체명 검색중..."):
                restaurants = None
            if restaurants:
                st.markdown("검색 결과는 다음과 같습니다. 해당하는 업체명을 선택해주세요.")
                for num, name, adr in restaurants:
                    st.button(f"{name} - {adr}", key=num, on_click=click_button, args=[name, num])
            else:
                st.markdown("검색 결과가 없습니다.")
    else:
        with st.chat_message("assistant"):
            full_response = st.write_stream(stream_message(st.session_state.review_df, user_message))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
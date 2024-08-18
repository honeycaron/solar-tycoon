from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
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
from dotenv import load_dotenv
import os
import json
import altair as alt

# .env 파일 로드
load_dotenv()

# Title of the app
st.title("Solar Tycoon (Jeju Ver. 🏝️)")

starting_message = "리뷰 분석을 원하시는 제주도 업체명을 입력해주세요!"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        # {"role": "assistant", "content": "Hello, please enter the name of the place you're interested in! 🍽️"})
        {"role": "assistant", "content": starting_message})
else:
    if st.session_state.messages[0]['content'] == "제주도 고수들의 비법을 물어보세요. (현재 지원 카테고리: 음식점/카페/디저트)":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.messages = []
        st.session_state.messages.append(
            # {"role": "assistant", "content": "Hello, please enter the name of the place you're interested in! 🍽️"})
            {"role": "assistant", "content": starting_message})



print("1.messages", st.session_state.messages)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) == str:
            st.markdown(message["content"])
        else:
            st.dataframe(message["content"])


if "rec_button_clicked" not in st.session_state:
    st.session_state.rec_button_clicked = False

def click_button(name, num):
    st.session_state.messages.append({"role": "assistant", "content": f"선택하신 업체명은 다음과 같습니다 : {name}"})
    if "place_name" not in st.session_state:
        st.session_state.place_name = name

    if "place_num" not in st.session_state:
        st.session_state.place_num = num


    st.session_state.messages.append({"role": "assistant", "content": "리뷰를 수집하겠습니다."})


def rec_click_button(user_message):
    st.session_state.rec_button_clicked = True
    st.session_state.rec_question = user_message
    st.session_state.rec_q_list.remove(user_message)

def extract_number_from_pattern(text):
    # Define the regex pattern to match /place/{number}
    pattern = r'/place/(\d+)'

    # Search for the pattern in the given text
    match = re.search(pattern, text)

    # Check if the pattern was found
    if match:
        # Extract and return the number
        return int(match.group(1))
    else:
        # If no match found, return None
        return None


# Function to perform place search
def search_place(place_name):
    base_url = "https://map.naver.com/p/search/"
    search_url = f"{base_url}{'제주도 ' + place_name}"
    options = Options()
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(search_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchIframe"))
    )
    frame = driver.find_element(By.CSS_SELECTOR, "#searchIframe")
    driver.switch_to.frame(frame)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "li"))
    )

    # Extract the required data
    places = []
    li_tags = driver.find_elements(By.TAG_NAME, "li")

    for li in li_tags[:3]:
        place_bluelink = li.find_element(By.CLASS_NAME, 'place_bluelink')
        try:
            name_tag = place_bluelink.find_element(By.TAG_NAME, 'span')
            place_adr = li.find_element(By.CLASS_NAME, 'Pb4bU').text.strip()
        except:
            name_tag = place_bluelink
            place_adr = ""

        place_name = name_tag.text.strip()
        place_bluelink.click()
        time.sleep(0.5)
        current_url = driver.current_url
        print(current_url)
        number = extract_number_from_pattern(current_url)
        if not number:
            name_tag.click()
            time.sleep(0.5)
            current_url = driver.current_url
            print(current_url)
            number = extract_number_from_pattern(current_url)
        places.append((number, place_name, place_adr))
        print((number, place_name, place_adr))
        # break

    driver.close()
    return places


def get_review(place_num):
    search_url = f"https://m.place.naver.com/place/{place_num}/review/visitor?entry=ple&reviewSort=recent"
    options = Options()
    # options.add_argument("--headless")

    # BS4 setting for secondary access
    session = requests.Session()
    headers = {
        "User-Agent": "user value"}

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(search_url)

    driver.implicitly_wait(30)

    # Pagedown
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    try:
        for i in range(5):
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a').click()
            time.sleep(0.4)
    except Exception as e:
        print('finish')

    time.sleep(1)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    reviews = bs.select('li.EjjAW')
    row_list = []
    for r in reviews:
        nickname = r.select_one('div.pui__JiVbY3')
        content = r.select_one('div.pui__vn15t2')
        date = r.select_one('div.pui__QKE5Pr>span.pui__gfuUIT>time')
        visit_cnt = r.select('div.pui__QKE5Pr>span.pui__gfuUIT')[1]

        # exception handling
        nickname = nickname.text if nickname else ''
        content = content.text if content else ''
        date = date.text if date else ''
        visit_cnt = visit_cnt.text if visit_cnt else ''

        time.sleep(0.06)

        # print(nickname, '/', content, '/', date)
        row_list.append([nickname, content, date, visit_cnt])
        time.sleep(0.06)
    raw_df = pd.DataFrame(row_list, columns=['nickname', 'content', 'date', 'visit_cnt'])
    raw_df = raw_df[raw_df['content'].str.len() > 0].reset_index(drop=True)


    return raw_df


def classify_review(review):
    url = "https://serving.app.predibase.com/7ea6d0/deployments/v2/llms/solar-1-mini-chat-240612/generate"

    # Fetch the environment variables
    adapter_id = os.getenv("ADAPTER_ID")
    api_token = os.getenv("PREDIBASE_API_KEY")

    if not adapter_id or not api_token:
        raise ValueError("Environment variables ADAPTER_ID and PREDIBASE_API_TOKEN must be set")

    input_prompt = f"""
    system
    다음은 해당 업체에 대한 소비자의 리뷰입니다. 해당 리뷰를 positive, neutral, negative 중 하나로 분류하세요.
    review
    {review}
    classification
    """

    payload = {
        "inputs": input_prompt,
        "parameters": {
            "adapter_id": adapter_id,
            "adapter_source": "pbase",
            "max_new_tokens": 20,
            "temperature": 0.1
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    try:
        return eval(response.text)["generated_text"]
    except Exception as e:
        raise ValueError("Error in parsing response: " + str(e))


def stream_message(review_df, user_message):
    client = OpenAI(
        api_key=os.getenv('UPSTAGE_API_KEY'),
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
                업체명 : {st.session_state.place_name}
                리뷰 정보 : {str(review_df['content'].to_list())}
                ###

                ```
                사용자 질문 : {user_message}
                ```
                답변하는 언어에 대한 별도의 언급이 없을 경우, 반드시 한국어로 답변해주세요.
                영어에 대한 질문일 경우, 반드시 한국어를 제외한 영어로만 답변해주세요.
                반드시 별도의 포맷(예: json, markdown) 없이 순수한 텍스트로만 답변해주세요.
                """
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def extract_positive_keywords(review_df):
    client = OpenAI(
        api_key=os.getenv('UPSTAGE_API_KEY'),
        base_url="https://api.upstage.ai/v1/solar"
    )

    stream = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=[
            {
                "role": "system",
                "content": "당신은 감성 분석 AI입니다. 당신의 목표는 주어진 리뷰 정보에서 긍정적인 의견을 7개 뽑는 것입니다."
            },
            {
                "role": "user",
                "content": f"""
                ###로 감싸진 참고 정보를 활용하여, ```로 리뷰 정보에서 긍정적인 의견을 7개 추출하고 이를 JSON으로 반환하세요.

                ###
                업체명 : {st.session_state.place_name}
                ###

                ```
                리뷰 정보 : {str(review_df[review_df['sentiment']=='positive']['content'].to_list())}
                ```
                 반드시 별도의 설명없이 'k1', 'k2', 'k3', 'k4','k5', 'k6', 'k7'을 Key값으로 갖는 JSON만 반환하세요.
        
                답변 예시는 다음과 같습니다.
                {{
                  "k1": "커피와 빵이 맛있음",
                  "k2": "바다뷰가 훌륭함",
                  "k3": "베이커리 종류가 다양함",
                  "k4": "직원이 친절함",
                  "k5": "넓은 공간과 편리한 주차",
                  "k6": "포토존과 인테리어가 좋음",
                  "k7": "주변 경치가 멋있음"
                }}
                각 Key별 의견은 반드시 예시와 같이 핵심 키워드 위주로 한 문장 길이로 답변해주세요.
                """
            }
        ],
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content

    if "```json" in full_response:
        full_response = full_response.replace("```json", "")
        full_response = full_response.replace("```", "")

    return full_response


def extract_negative_keywords(review_df):
    client = OpenAI(
        api_key=os.getenv('UPSTAGE_API_KEY'),
        base_url="https://api.upstage.ai/v1/solar"
    )

    stream = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=[
            {
                "role": "system",
                "content": "당신은 감성 분석 AI입니다. 당신의 목표는 주어진 리뷰 정보에서 부정적인 의견을 7개 뽑는 것입니다."
            },
            {
                "role": "user",
                "content": f"""
                ###로 감싸진 참고 정보를 활용하여, ```로 리뷰 정보에서 부정적인 의견을 7개 추출하고 이를 JSON으로 반환하세요.

                ###
                업체명 : {st.session_state.place_name}
                ###

                ```
                리뷰 정보 : {str(review_df[review_df['sentiment'] == 'negative']['content'].to_list())}
                ```
                 반드시 별도의 설명없이 'k1', 'k2', 'k3', 'k4','k5', 'k6', 'k7'을 Key값으로 갖는 JSON만 반환하세요.

                답변 예시는 다음과 같습니다.
                {{
                  "k1": "가격이 비쌈",
                  "k2": "청결 상태가 아쉬움",
                  "k3": "직원 불친절함",
                  "k4": "커피 맛이 일정하지 않음",
                  "k5": "시설 관리가 미흡함",
                  "k6": "주차비가 비쌈",
                  "k7": "혼잡함과 대기 시간이 김"
                }}
                각 Key별 의견은 반드시 예시와 같이 핵심 키워드 위주로 한 문장 길이로 답변해주세요.
                """
            }
        ],
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content

    if "```json" in full_response:
        full_response = full_response.replace("```json", "")
        full_response = full_response.replace("```", "")

    return full_response
def safe_eval(expression):
    while True:
        try:
            result = eval(expression)
            result = eval(result)
            return result
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
def sentiment_color(val):
    if val == 'positive':
        color = 'green'
    elif val == 'negative':
        color = 'red'
    elif val == 'neutral':
        color = 'gray'
    else:
        color = 'white'
    return f'background-color: {color}'

def plot_sentiment_ratio_per_week(df):
    df['date'] = pd.to_datetime(df['date'].apply(lambda x: f'2024.{x[:3]}'), format='%Y.%m.%d')

    df['week'] = df['date'].dt.isocalendar().week

    weekly_sentiment = df.groupby(['week', 'sentiment']).size().reset_index(name='count')

    total_per_week = weekly_sentiment.groupby('week')['count'].transform('sum')
    weekly_sentiment['ratio'] = weekly_sentiment['count'] / total_per_week

    chart = alt.Chart(weekly_sentiment).mark_bar().encode(
        x=alt.X('week:O', title='주차'),
        y=alt.Y('ratio:Q', stack='normalize', title='긍부정 비율'),
        color=alt.Color(
            'sentiment:N',
            title='감성 구분',
            scale=alt.Scale(
                domain=['positive', 'negative', 'neutral'],
                range=['green', 'red', 'gray']
            )
        ),
        tooltip=['week:O', 'sentiment:N', alt.Tooltip('ratio:Q', format='.2%')]
    ).properties(
        title='주별 긍부정 비율',
        width=600,
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

def plot_sentiment_ratio_per_day(df):
    # Convert date to a proper datetime format (assuming the year is 2024)
    df['date'] = pd.to_datetime(df['date'].apply(lambda x: f'2024.{x[:3]}'), format='%Y.%m.%d')

    # Group by date and sentiment to get counts
    daily_sentiment = df.groupby(['date', 'sentiment']).size().reset_index(name='count')

    # Normalize counts to get ratios (proportions)
    total_per_day = daily_sentiment.groupby('date')['count'].transform('sum')
    daily_sentiment['ratio'] = daily_sentiment['count'] / total_per_day

    # Create the Altair chart with custom colors
    chart = alt.Chart(daily_sentiment).mark_bar().encode(
        x=alt.X('date:T', title='날짜'),
        y=alt.Y('ratio:Q', stack='normalize', title='긍부정 비율'),
        color=alt.Color(
            'sentiment:N',
            title='감성 구분',
            scale=alt.Scale(
                domain=['positive', 'negative', 'neutral'],
                range=['green', 'red', 'gray']
            )
        ),
        tooltip=[alt.Tooltip('date:T', title='날짜'), 'sentiment:N', alt.Tooltip('ratio:Q', format='.2%')]
    ).properties(
        title='일별 긍부정 비율',
        width=600,
        height=400
    ).interactive()

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

if "review_prepared" not in st.session_state:
    if "place_num" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("리뷰 수집중..."):
                df = get_review(st.session_state.place_num)
            st.markdown("아래와 같이 리뷰 데이터를 수집하였습니다.")
            st.dataframe(df)
            st.markdown("수집된 리뷰에서 궁금하신 점을 물어보세요!")
            st.session_state.messages.append({"role": "assistant", "content": "아래와 같이 리뷰 데이터를 수집하였습니다."})
            st.session_state.messages.append({"role": "assistant", "content": df})
            st.session_state.messages.append({"role": "assistant", "content": "수집된 리뷰에서 궁금하신 점을 물어보세요!"})
            st.session_state.review_df = df
            st.session_state.review_prepared = True
            st.markdown("아래와 같은 질문들도 가능해요.")
            st.session_state.messages.append({"role": "assistant", "content": "아래와 같은 질문들도 가능해요."})
            rec_q_list = ["긍정적인 리뷰 위주로 요약해주세요.", "외국인을 위한 마케팅 홍보 문구 영어로 작성해주세요.", "감성 분석 보고서 생성해주세요."]
            st.session_state.rec_q_list = rec_q_list
            for q in st.session_state.rec_q_list:
                st.button(q, on_click=rec_click_button, args=[q])


if st.session_state.rec_button_clicked:
    st.session_state.rec_button_clicked = False
    user_message = st.session_state.rec_question
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)
    with st.chat_message("assistant"):
        if "감성" in user_message:
            with st.spinner("감성 분석 보고서 생성 중..."):
                st.session_state.review_df["sentiment"] = [classify_review(x) for x in st.session_state.review_df["content"].to_list()]
                st.markdown(f"{st.session_state.place_name}에 대한 감성 분석 보고서입니다!")
                st.markdown(f"#### 리뷰별 감성 분석 결과 (Solar Mini 파인튜닝 모델 사용)")
                styled_df = st.session_state.review_df[['content', 'sentiment']].style.applymap(sentiment_color, subset=['sentiment'])
                st.dataframe(styled_df)

                st.divider()
                positive_keywords = safe_eval("extract_positive_keywords(st.session_state.review_df)")
                negative_keywords = safe_eval("extract_negative_keywords(st.session_state.review_df)")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 긍정적인 의견 👍")
                    for k, v in positive_keywords.items():
                        st.markdown(f"- {v}")

                with col2:
                    st.markdown("#### 부정적인 의견 👎")
                    for k, v in negative_keywords.items():
                        st.markdown(f"- {v}")
                st.divider()
                plot_sentiment_ratio_per_day(st.session_state.review_df[['sentiment', 'date']])

        else:
            full_response = st.write_stream(stream_message(st.session_state.review_df, user_message))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            for q in st.session_state.rec_q_list:
                st.button(q, on_click=rec_click_button, args=[q])


# Accept user input
if user_message := st.chat_input("Send Message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_message)

    if not "review_prepared" in st.session_state:
        # Perform search and display results
        with st.chat_message("assistant"):
            with st.spinner("업체명 검색중..."):
                places = search_place(user_message)
            if places:
                st.markdown("검색 결과는 다음과 같습니다. 해당하는 업체명을 선택해주세요.")
                for num, name, adr in places:
                    if len(adr) > 0 :
                        button_str = f"{name} - {adr}"
                    else:
                        button_str = name
                    st.button(button_str, key=num, on_click=click_button, args=[name, num])
            else:
                st.markdown("검색 결과가 없습니다.")
    else:
        with st.chat_message("assistant"):
            full_response = st.write_stream(stream_message(st.session_state.review_df, user_message))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            for q in st.session_state.rec_q_list:
                st.button(q, on_click=rec_click_button, args=[q])

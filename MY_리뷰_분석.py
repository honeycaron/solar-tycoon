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
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# Title of the app
st.title("Solar Tycoon (Jeju Ver. 🏝️)")

starting_message = "리뷰 분석을 원하시는 제주도 업체명을 입력해주세요!"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        # {"role": "assistant", "content": "Hello, please enter the name of the restaurant you're interested in! 🍽️"})
        {"role": "assistant", "content": starting_message})
else:
    if st.session_state.messages[0]['content'] == "제주도 고수들의 비법을 물어보세요. (현재 지원 카테고리: 음식점/카페/디저트)":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.messages = []
        st.session_state.messages.append(
            # {"role": "assistant", "content": "Hello, please enter the name of the restaurant you're interested in! 🍽️"})
            {"role": "assistant", "content": starting_message})



print("1.messages", st.session_state.messages)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) == str:
            st.markdown(message["content"])
        else:
            st.dataframe(message["content"])


def click_button(name, num):
    st.session_state.messages.append({"role": "assistant", "content": f"선택하신 업체명은 다음과 같습니다 : {name}"})
    if "restaurant_num" not in st.session_state:
        st.session_state.restaurant_num = num

    st.session_state.messages.append({"role": "assistant", "content": "리뷰를 수집하겠습니다."})


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


# Function to perform restaurant search
def search_restaurant(restaurant_name):
    base_url = "https://map.naver.com/p/search/"
    search_url = f"{base_url}{'제주도 ' + restaurant_name}"
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
    restaurants = []
    li_tags = driver.find_elements(By.TAG_NAME, "li")

    for li in li_tags[:3]:
        place_bluelink = li.find_element(By.CLASS_NAME, 'place_bluelink')
        try:
            name_tag = place_bluelink.find_element(By.TAG_NAME, 'span')
            restaurant_adr = li.find_element(By.CLASS_NAME, 'Pb4bU').text.strip()
        except:
            name_tag = place_bluelink
            restaurant_adr = ""

        restaurant_name = name_tag.text.strip()
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
        restaurants.append((number, restaurant_name, restaurant_adr))
        print((number, restaurant_name, restaurant_adr))
        # break

    driver.close()
    return restaurants


def get_review(restaurant_num):
    search_url = f"https://m.place.naver.com/restaurant/{restaurant_num}/review/visitor?entry=ple&reviewSort=recent"
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
    df = pd.DataFrame(row_list, columns=['nickname', 'content', 'date', 'visit_cnt'])

    return df


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
                restaurants = search_restaurant(user_message)
            if restaurants:
                st.markdown("검색 결과는 다음과 같습니다. 해당하는 업체명을 선택해주세요.")
                for num, name, adr in restaurants:
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
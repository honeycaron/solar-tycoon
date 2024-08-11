import time
from telnetlib import EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from tqdm import tqdm
from time import sleep
import requests
import json
import pandas as pd

# 드라이버 실행
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome( options=options)
driver.get('https://www.google.co.kr/maps')



def review_scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 스크롤을 아래로 내림
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 새로운 리뷰 로딩 대기
        time.sleep(2)  # 로딩 시간 조정

        # 새 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")

        review_dates = driver.find_elements(By.XPATH, '//span[contains(@class, "ODSEW-ShBeI-RgZmSc-date")]')
        for date in review_dates:
            review_date_text = date.text
            if review_date_text == '6달 전':
                print("6달 전 발견")
                break

        # 더 이상 스크롤할 내용이 없을 때 종료
        if new_height == last_height:
            break

        last_height = new_height

def google_reviews(store_list, store_call, gu, count=10):
    query_input = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')

    sleep(3)

    # 리스트 형식으로 저장된 가게 하나씩 검색
    for i in range(len(store_list)):
        count = count
        result_list = []
        store = store_list[i]
        call_num = store_call[i]
        sleep(3)
        query_input.send_keys(gu + " " + store)
        search_btn = driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]/span')
        search_btn.click()
        sleep(2)

        # 가게 번호 확인, 대조
        try:
            first_result = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[6]/button/div/div[2]/div[1]').text
            print(first_result)
            if first_result == call_num:
                print(f"Found matching result: {store}")

        except Exception as e:
            print("음식점 번호가 일치하지 않음")


        #리뷰 버튼 클릭
        review_btn = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
        review_btn.click()

        #정렬 버튼 클릭
        sort_btn = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span/span[2]')
        sort_btn.click()

        #최신순 정렬
        recent_btn = driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
        recent_btn.click()


        # 리뷰 더보기 펼치기
        review_scroll()


        # div태그 스크롤
        sleep(8)
        js_scripts = '''
        let aa = document.getElementsByClassName('section-scrollbox')[0];
        setTimeout(()=>{aa.scroll(0,1000000)}, 1000);
        '''
        driver.execute_script(js_scripts)
        sleep(3)

        # 헤더값 찾기 및 json파일 들고와 리뷰 10개씩 저장하기
        for request in driver.requests:
            if request.response:
                pb = request.url.split('pb=')
                if len(pb) == 2:
                    if pb[1][:6] == '!1m2!1':
                        url_l = request.url.split('!2m2!1i')
                        break


        for number in tqdm(range(count)):
            resp = requests.get((url_l[0] + '!2m2!1i' + '{}' + url_l[1]).format(number))
            review = json.loads(resp.text[5:])
            for user in range(10):
                result_list.append({
                    'ID': review[2][user][0][1],
                    '내용': review[2][user][3],
                    '날짜': review[2][user][1],
                })

        # csv로 저장
        df = pd.DataFrame(result_list)
        df.to_csv('{}.csv'.format(store), encoding='utf-8-sig')

# 사용 예제
df_restNm = pd.read_excel("제주도_restnum_with_adr_pn.xlsx")
store_list = df_restNm['업체명']
store_call = df_restNm['전화번호']

# 함수 실행
google_reviews(store_list, store_call,'제주도', count=5)
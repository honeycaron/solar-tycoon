# Dependency
- python version: ```3.11.8```
- 패키지 : ```requirements.txt``` 파일 참고
    
    ```
    pip install -r requirements.txt
    ```

# AIA

## 함수 목록
- ```login```: 로그인(ID:hello/PW:bye)
- ```home```: 홈페이지 접속
- ```question/{id}/{chat_id}```: 질의
- ```feedback```: 답변에 대한 피드백 저장

## 실행 방법
```
python backend_aia.py
```
- DNS: ```http://127.0.0.1:4000```
- WS: ```ws://127.0.0.1:4000```

# T2S
## 함수 목록
- ```home```: 홈페이지 접속
- ```question/{id}/{chat_id}```: 질의
- ```feedback```: 답변에 대한 피드백 저장

## 실행 방법
```
python backend_t2s.py
```
- DNS: ```http://127.0.0.1:5000```
- WS: ```ws://127.0.0.1:5000```

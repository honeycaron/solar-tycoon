import time
import uuid
from datetime import datetime
import os
import json
import asyncio
import traceback

class AIAEngine:
    def __init__(self, manager, chat_log_dir: str, id: str, chat_id: str, websocket):
        self.manager = manager
        self.chat_log_dir = chat_log_dir
        self.id = id
        self.chat_nm = None
        self.follow_up_question_list = None
        self.chat_id = chat_id
        self.websocket = websocket
        self.message_id = str(uuid.uuid4())
    
    async def message_init(self, question):

        # self.message_id = str(uuid.uuid4())
        self.message_created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        chat_log_path = os.path.join(self.chat_log_dir, f'chat_log_{self.id}_{self.chat_id}.json')

        # 과거 메시지 기록 탐색 후, 채팅명 추출
        if os.path.exists(chat_log_path):
            with open(chat_log_path, 'r', encoding='utf-8') as f:
                response_log = json.load(f)
            chat_nm = response_log['chat_nm']
        
        else:
            chat_nm = ''
            response_log = {
                "id": self.id,
                "chat_id": self.chat_id,
                "chat_nm": chat_nm,
                "chat_content": [],
                "chat_created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        self.chat_nm = chat_nm

        websocket_content = {
            "id": self.id, 
            "chat_id" : self.chat_id,
            "message_id" : self.message_id,
            "chat_nm" : self.chat_nm,
            "response_content" : '',
            "response_type": "system",
            "finished" : "N",
            "wait_message": "메뉴얼 탐색 중입니다", 
        }
        
        await self.websocket.send_json(websocket_content)
        
        if not os.path.exists(chat_log_path):
            await self.get_chat_nm(question)

        return response_log
    
    async def get_chat_nm(self, question):
        time.sleep(1)
        self.chat_nm = question

    async def get_follow_up_questions(self, question):
        time.sleep(1)
        self.follow_up_questions = ["FastAPI 로 Backend 구축하는 방법은?", "소캣을 활용하여 스트리밍 구현하는 방법은?"]

    async def stream_text(self):
        text = ['안녕하','세요 ', '수민님.', ' 잘 ', '부탁드','립니다.','테스트','를 위해','좀 더', ' 내용', '을 늘려 ','보았습', '니다.']

        final_content = ''

        while text:
            t = text.pop(0)

            final_content += t
            
            websocket_content = {
                "id": self.id, 
                "chat_id" : self.chat_id,
                "message_id" : self.message_id,
                "chat_nm" : self.chat_nm,
                "response_content" : t,
                "response_type": "text",
                "finished" : "N",
                "wait_message": "메뉴얼 탐색 중입니다", 
            }

            await self.websocket.send_json(websocket_content)

            time.sleep(0.2)

        response = [
                    {
                        "response_content": final_content,
                        "response_id" : str(uuid.uuid4()),
                        "response_type": "text"
                    }
        ]
        
        return response

    async def stream_links(self):

        response = []

        hyperlinks = ['[참고 링크](https://ko.upstage.ai/global-ai-week-ai-hackathon)']

        for link in hyperlinks:
            websocket_content = {
                    "id": self.id, 
                    "chat_id" : self.chat_id,
                    "message_id" : self.message_id,
                    "chat_nm" : self.chat_nm,
                    "response_content" : link,
                    "response_title": "8",
                    "response_type": "hyperlink",
                    "finished" : "N", # 스트리밍 종료 시 "Y"로 변경
                    "wait_message": "링크 생성 중입니다", 
            }

            await self.websocket.send_json(websocket_content)

            time.sleep(0.1)

            response.append(
                {
                    "response_content": link,
                    "response_id" : str(uuid.uuid4()),
                    "response_type": "link"
                }
            )
        
        return response

    async def stream_images(self):
        response = []

        images = ["https://images.squarespace-cdn.com/content/v1/659384103b38c97cdaf368bd/7e1aa6a4-b7a8-462a-850c-fcffb6ab7f24/Global+AI+Week+AI+Hackathon_card.jpg?format=2500w"]

        for image in images:
            websocket_content = {
                    "id": self.id, 
                    "chat_id" : self.chat_id,
                    "message_id" : self.message_id,
                    "chat_nm" : self.chat_nm,
                    "response_content" : image,
                    "response_type": "image",
                    "finished" : "N", # 스트리밍 종료 시 "Y"로 변경
                    "wait_message": "이미지 생성 중입니다", 
            }

            await self.websocket.send_json(websocket_content)

            time.sleep(0.1)

            response.append(
                {
                    "response_content": image,
                    "response_id" : str(uuid.uuid4()),
                    "response_type": "image"
                }
            )

        return response

    async def stream_follow_up_questions(self, question):

        await self.get_follow_up_questions(question)

        for q in self.follow_up_questions:
            
            websocket_content = {
                "id": self.id, 
                "chat_id" : self.chat_id,
                "message_id" : self.message_id,
                "chat_nm" : self.chat_nm,
                "response_content" : q,
                "response_type": "follow_up_question",
                "finished" : "N", # 스트리밍 종료 시 "Y"로 변경
                "wait_message": "유사 질의문 생성 중입니다", 
            }

            await self.websocket.send_json(websocket_content)

            time.sleep(0.1)
        

    async def message_end(self):
        websocket_content = {
            "id": self.id, 
            "chat_id" : self.chat_id,
            "message_id" : self.message_id,
            "chat_nm" : self.chat_nm,
            "response_content" : "",
            "response_type": "text",
            "finished" : "Y", # 스트리밍 종료 시 "Y"로 변경
            "wait_message": "유사 질의문 생성 중입니다", 
        }
        
        await self.websocket.send_json(websocket_content)

    async def follow_up_question(self, question):
        time.sleep(1)
        follow_up_question = ["FastAPI 로 Backend 구축하는 방법은?", "소캣을 활용하여 스트리밍 구현하는 방법은?"]
        self.follow_up_question_list = follow_up_question

    def chat_nm_maker(self, question):
        time.sleep(1)
        self.chat_nm = question

    async def save_log(self, chat_log_dir, response_log, question, response):
        chat_content = {
                "message_id" : self.message_id,
                "message_created_at" : self.message_created_at,
                "question": question,
                "feedback": None,
                "follow_up_questions": self.follow_up_questions,
                "response" : response
            }

        response_log['chat_content'].append(chat_content)
        response_log['chat_nm'] = self.chat_nm

        with open(os.path.join(chat_log_dir, f'chat_log_{self.id}_{self.chat_id}.json'), 'w', encoding='utf-8') as f:
            json.dump(response_log, f)

    async def question_main(self, question):

        try:
            # 메시지 생성 시작
            response_log = await self.message_init(question)

            # 텍스트 생성
            text_content = await self.stream_text()

            # 하이퍼링크 생성
            links = await self.stream_links()

            # 이미지 링크 생성
            images = await self.stream_images()

            # follow up 질의 생성
            await self.stream_follow_up_questions(question)

            # 대화 기록 저장
            response = text_content + links + images
            await self.save_log(self.chat_log_dir, response_log,  question, response)

        except asyncio.CancelledError:
            await self.websocket.send_json(
                {
                    "errorCodes": ["CANCEL_REQUEST"],
                    "detail":[
                        {
                            "type": "internal",
                            "loc": ["",""],
                            "msg": "User cancelled the request",
                            "input": {}
                        }
                    ]
                }
            )

            await self.message_end()

        except Exception as e:
            print(traceback.format_exc())

        else:
            # 메시지 종료
            await self.message_end()

        
    

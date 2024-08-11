import time
import uuid
from datetime import datetime
import os
import json

class T2SEngine:
    def __init__(self, manager, chat_log_dir: str, id: str, chat_id: str, websocket):
        self.manager = manager
        self.chat_log_dir = chat_log_dir
        self.id = id
        self.chat_id = chat_id
        self.websocket = websocket
    
    async def message_init(self, question):

        self.message_id = str(uuid.uuid4())
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
            "wait_message": "데이터 탐색 중입니다", 
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
        self.follow_up_questions = ["위버스 샵 결재 내역 뽑아줘", "법인 카드 매출 뽑아줘"]

    async def stream_text(self):
        text = ['쿼', '리 ', ' ', '결', '과', '는 ', ' ', '다','음', '과', ' ', '같','습','니','다',
                '```', 'Select ', 'bye ', 'from ', 'dm.', 'hello',
                '```', '', '```', 'Select ', 'kitty ', 'from ', 'dm.', 'cat','```',
                '이','상',' ','연','속','쿼','리', ' ', '예','제','였','습','니','다']

        final_text_content = ''
        final_code_content = ''

        response = []

        type = 'text'

        while text:
            t = text.pop(0)

            if '```' in t:
                if type != 'code':
                    type = 'code'

                    response.append(
                        {
                            "response_content": final_text_content,
                            "response_id" : str(uuid.uuid4()),
                            "response_type": "text"
                        }
                    )

                    final_text_content = ''

                    final_code_content += t
            
                else:
                    final_code_content += t

                    response.append(
                            {
                                "response_content": final_code_content,
                                "response_id" : str(uuid.uuid4()),
                                "response_type": "code"
                            }
                        )

                    final_code_content = ''
                    type = 'text'
                
            else:
                if type == 'text':
                    final_text_content += t
                else:
                    final_code_content += t

            
            websocket_content = {
                "id": self.id, 
                "chat_id" : self.chat_id,
                "message_id" : self.message_id,
                "chat_nm" : self.chat_nm,
                "response_content" : t,
                "response_type": type,
                "finished" : "N",
                "wait_message": "쿼리 생성 중입니다", 
            }

            await self.websocket.send_json(websocket_content)

            time.sleep(0.1)

        if final_text_content != '':
             response.append(
                        {
                            "response_content": final_text_content,
                            "response_id" : str(uuid.uuid4()),
                            "response_type": "text"
                        }
                    )
             
        if final_code_content != '':
             response.append(
                        {
                            "response_content": final_code_content,
                            "response_id" : str(uuid.uuid4()),
                            "response_type": "code"
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

    def save_log(self, chat_log_dir, response_log, question, response):
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
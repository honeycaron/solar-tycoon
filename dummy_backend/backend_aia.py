from fastapi import FastAPI, responses, HTTPException, WebSocket, WebSocketDisconnect, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import os
import pandas as pd
from typing import List
import asyncio

from aia_engine import AIAEngine

chat_log_dir = './chat_log/aia'

os.makedirs(chat_log_dir, exist_ok = True)

app = FastAPI()
router = APIRouter()

active_tasks = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    id: str | None = None
    password: str | None = None

    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate_keys

    # @classmethod
    # def validate_keys(cls, v: Dict[str, Any]):
    #     required_keys = {'id', 'password'}
    #     missing_keys = required_keys - set(v.keys())
    #     if missing_keys:
    #         raise ValueError(f"필수 키 값이 입력되지 않았습니다: {', '.join(missing_keys)}")
    #     return v
    
class Id(BaseModel):
    id: str

class Feedback(BaseModel):
    id: str
    chat_id: str
    message_id: str
    feedback: str

# WebSocket 연결을 관리하는 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # async def broadcast(self, data: str):
    #     for connection in self.active_connections:
    #         await connection.send_json(data)

manager = ConnectionManager()

# # 세션 만료 시간 (1시간)
# SESSION_EXPIRE_TIME = timedelta(hours=1)

# # 세션 정보 저장
# sessions = {}
        
@router.post("/login")
def login(credentials: Credentials):
    try:

        credentials_df = pd.read_csv('credentials.csv')

        if credentials.id == '' or credentials.password == '':
            return responses.JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    'errorCodes': ["ID_REQUIRED", "PASSWORD_REQUIRED"],
                    'detail': [
                        {
                            "type": "missing",
                            "loc": ["body", "id", "passowrd"],
                            "msg": "아이디 혹은 비밀번호를 입력해주세요",
                            "input": {}
                        }
                    ]
                }
            )

        if not credentials.id in credentials_df['id'].tolist():
            return responses.JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    'errorCodes': ["ID_NOT_FOUND"],
                    'detail': [
                        {
                            "type": "not_found",
                            "loc": ["body", "id"],
                            "msg": "아이디를 확인해주세요",
                            "input": {}
                        }
                    ]
                }
            )

        password = credentials_df[credentials_df['id'] == credentials.id]['password'].values[0]

        # 비밀번호 확인
        if credentials.password != password:
            return responses.JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    'errorCodes': ["PASSWORD_MISMATCH"],
                    'detail': [
                        {
                            "type": "mismatch",
                            "loc": ["body", "passowrd"],
                            "msg": "아이디 혹은 비밀번호를 확인해주세요",
                            "input": {}
                        }
                    ]
                }
            )

        # # 세션 생성
        # session_id = str(uuid.uuid4())
        # sessions[session_id] = {
        #     "user_id": credentials.id,
        #     "expire_time": datetime.now() + SESSION_EXPIRE_TIME
        # }

    except HTTPException as httpError:
        raise httpError

    except Exception as e:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'errorCodes': ["INTERNAL_SERVER_ERROR"],
                'detail': [
                    {
                        "type": "internal",
                        "loc": ["", ""],
                        "msg": f"{str(e)}",
                        "input": {}
                    }
                ]
            }
        )
    
    else:
        return responses.JSONResponse(
            content = {
                "status": "success",
                "message": f"{credentials.id} login success",
                # "session_id": session_id
            }
        )

@router.post("/home")
def home(id: Id, 
        #  session_id: str = Header(None)
    ):
    try:
        # # 세션 확인
        # if not session_id or session_id not in sessions or sessions[session_id]["expire_time"] < datetime.now():
        #     raise HTTPException(status_code=401, detail="Unauthorized")

        return responses.JSONResponse(
            content = {
                "id": id.id,
                "favorites" : "N",
                "favorites_list" : [],
                "svc_list": [
                    {
                        "svc_id": "1",
                        "svc_nm": "사내 업무 정보 검색",
                        "svc_dns" : "http://127.0.0.1:4000",
                        "svc_ws" : "ws://127.0.0.1:4000",
                        "backend_svc_id": "aia",
                        "user_type": "카드회사에서 고객의 문의를 상담해주고 있는 Call Center 상담원",
                        "response_style": "bullet point 형식으로 간결하게",
                        "selected": "Y"
                    }, 
                    {
                        "svc_id": "2",
                        "svc_nm": "ERP 데이터 조회",
                        "svc_dns" : "http://127.0.0.1:5000",
                        "svc_ws" : "ws://127.0.0.1:5000",
                        "backend_svc_id": "t2s",
                        "user_type": "지점에서 지계수 데이터를 취합하는 현업 직원",
                        "response_style": "질의에 적합한 SQL 쿼리와 데이터 추출",
                        "selected": "N"
                    }, 
                    {
                        "svc_id": "3",
                        "svc_nm": "이벤트 홍보 문구 및 이미지 생성",
                        "svc_dns" : "http://127.0.0.1:6000",
                        "svc_ws" : "ws://127.0.0.1:6000",
                        "backend_svc_id": "epa",
                        "user_type": "현업 이벤트 기획 담당자",
                        "response_style": "이벤트 컨텐츠 제작 요청 문서 초안 생성",
                        "selected": "N"
                    }
                ]
            }
        )

    except HTTPException as httpError:
        raise httpError
    
    except Exception as e:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'errorCodes': ["INTERNAL_SERVER_ERROR"],
                'detail': [
                    {
                        "type": "internal",
                        "loc": ["", ""],
                        "msg": f"{str(e)}",
                        "input": {}
                    }
                ]
            }
        )

# question
@router.websocket("/question/{id}/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    id: str, 
    chat_id: str
    ):
    
    await manager.connect(websocket)

    try:
        while True:
            aia_engine = AIAEngine(
                manager=manager,
                chat_log_dir=chat_log_dir,
                id=id, 
                chat_id=chat_id,
                websocket=websocket
            )

            query = await websocket.receive_json()

            question = query['question']

            if question != 'terminate':
                task_name = f'{id}_{chat_id}'
                task = asyncio.create_task(aia_engine.question_main(question))
                active_tasks[task_name] = task
            
            elif question == 'terminate':
                task_name = f'{id}_{chat_id}'
                
                if task_name in active_tasks:
                    active_tasks[task_name].cancel()

                    await websocket.send_json(
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

                    # 메시지 종료
                    await aia_engine.message_end()

    except HTTPException as httpError:
        raise httpError
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception as e:
        await websocket.send_json(
            jsonable_encoder(
                {
                    'errorCodes': ["INTERNAL_SERVER_ERROR"],
                    'detail': [
                        {
                            "type": "internal",
                            "loc": ["", ""],
                            "msg": f"{str(e)}",
                            "input": {}
                        }
                    ]
                }
            )
        )

        manager.disconnect(websocket)
    
@router.post("/feedback")
def feedback(feedback: Feedback, 
            #  session_id: str = Header(None)
    ):
    try:
        found = False

        if os.path.exists(os.path.join(chat_log_dir, f'chat_log_{feedback.id}_{feedback.chat_id}.json')):
            with open(os.path.join(chat_log_dir, f'chat_log_{feedback.id}_{feedback.chat_id}.json'), 'r', encoding='utf-8') as f:
                chat_hist = json.load(f)
        
            for i, content in enumerate(chat_hist['chat_content']):
                if content['message_id'] == feedback.message_id:
                    found = True
                    chat_hist['chat_content'][i]['feedback'] = feedback.feedback
                    print(chat_hist['chat_content'][i]['feedback'])

            with open(os.path.join(chat_log_dir, f'chat_log_{feedback.id}_{feedback.chat_id}.json'), 'w', encoding='utf-8') as f:
                json.dump(chat_hist, f)
        
        if not found:
            return responses.JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'errorCodes': ["CHAT_NOT_FOUND"],
                        'detail': [
                            {
                                "type": "not_found",
                                "loc": ["body", "chat_id"],
                                "msg": "사용자의 채팅 기록을 찾을 수 없습니다.",
                                "input": {}
                            }
                        ]
                    }
                )

    except HTTPException as httpError:
        raise httpError
    
    except Exception as e:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'errorCodes': ["INTERNAL_SERVER_ERROR"],
                'detail': [
                    {
                        "type": "internal",
                        "loc": ["", ""],
                        "msg": f"{str(e)}",
                        "input": {}
                    }
                ]
            }
        )
    
    else:
        return responses.JSONResponse(
            content = {
                "status": "success",
                "message": f"{feedback.feedback} feedback log success",
                # "session_id": session_id
            }
        )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_aia:app", host='0.0.0.0', port=4000, reload=True)

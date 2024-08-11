export const functions = {

    /******************************* 메인 페이지 ***********************************/

    'ex_func_needLogin': {
        title: '로그인 페이지로 이동하고 모든 프로세스를 중단',
        process: [
            {
                type: 'page', id: 'move',
                description: '로그인 페이지로 이동',
                inputs: {
                    pageIdOrUrl: 'login',
                    forceRefresh: true,
                }
            },
            { type: 'stop' },
        ]
    },

    'ex_func_serviceChange': {
        title: '서비스 변경',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: true, immediately: true } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_cancelling__', value: true, immediately: true } },
            {
                type: 'websocket', id: 'disconnect',
                description: '현재 연결된 웹소켓 끊기',
                inputs: {
                    url: "__var_websocket__",
                },
            },
            { type: 'delay', inputs: 500 },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_chat_id__', value: null } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_dialogs__', value: [] } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_follow_up__', value: [] } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_reactions__', value: [] } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_processing__', value: false } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: false } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_cancelling__', value: false } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_chat_title__', value: null } },
            {
                type: 'custom', id: 'block_generateRandomId',
                description: '랜덤한 숫자 chat id 생성',
                inputs: {
                    variable: '__var_chat_id__',
                }
            },
            {
                type: 'action', id: 'changeVariable',
                description: '서비스에 맞는 websocket url 설정',
                inputs: {
                    key: '__var_websocket__',
                    value: "(__var_focused__?.svc_ws) + '/question/' + __var_id__ + '/' + __var_chat_id__"
                }
            },
            {
                type: 'websocket', id: 'connect',
                description: '',
                inputs: {
                    url: "__var_websocket__",
                    state: '__var_websocket_state__',
                },
                success: {
                    outputs: {
                        'chat_nm': '__var_chat_title__',
                        'message_id': '__local_message_id__',
                        'response_title': '__local_websocket_msg_title__',
                        'response_type': '__local_websocket_msg_type__',
                        'response_content': '__local_websocket_msg__',
                        'finished': '__local_websocket_finished__',
                        'wait_message': '__var_status__'
                    },
                    action: {
                        type: 'custom', id: 'block_appendDialog',
                        inputs: {
                            id: '__local_message_id__',
                            dialogs: '__var_dialogs__',
                            status: '__var_status__',
                            isHuman: false,
                            title: '__local_websocket_msg_title__',
                            type: '__local_websocket_msg_type__',
                            content: '__local_websocket_msg__',
                            isProcessing: '__var_processing__',
                            finished: '__local_websocket_finished__',
                            followUp: '__var_follow_up__'
                        }
                    },
                },
            },
        ],
    },

    'ex_func_mainPageInit': {
        title: '초기 화면 설정',
        process: [
            {
                type: 'custom', id: 'block_getLocalStorage',
                description: '로컬 저장소에서 사용자 확인',
                inputs: { key: 'userId', variable: '__var_id__' }
            },
            {
                type: 'case',
                description: '사용자가 확인되지 않으면 로그인 페이지로 강제 이동',
                inputs: '!__var_id__',
                success: { type: 'function', id: 'ex_func_needLogin' },
            },
            {
                type: 'api',
                description: 'home API 호출하기',
                inputs: {
                    method: 'post',
                    url: "__var_url__ + '/home'",
                    body: {
                        id: '__var_id__'
                    }
                },
                success: {
                    outputs: {
                        'svc_list': '__var_services__',
                    },
                    action: {
                        type: 'custom', id: 'block_svc_selected',
                        description: 'selected 가 Y 인 값 찾기',
                        inputs: {
                            list: '__var_services__',
                            selected: '__var_focused__',
                        }
                    },
                },
                error: {
                    init: { type: 'custom', id: 'block_buildSnackbar', inputs: { message: '오류 발생' } },
                    custom: {
                        '__ERR_NETWORK': {
                            type: 'custom', id: 'block_buildSnackbar',
                            inputs: {
                                message: '서버에 문제 발생',
                                persist: true,
                                button: 'reload',
                            }
                        },
                        '__ERR_BAD_REQUEST': { type: 'custom', id: 'block_buildSnackbar', inputs: { message: 'Bad Request: 입력 오류' } },
                        // 'TARGET_DATE_REQUIRED': { type: 'custom', id: 'block_buildSnackbar', inputs: { message: 'ERROR: TARGET_DATE_REQUIRED' } },
                    }
                },
            },
            {
                type: 'function', id: 'ex_func_serviceChange',
                description: '웹소켓 연결 및 초기 설정',
                inputs: {
                    __var_id__: '__var_id__',
                    __var_chat_id__: '__var_chat_id__',
                    __var_focused__: '__var_focused__',
                    __var_websocket__: '__var_websocket__',
                    __var_dialogs__: '__var_dialogs__',
                    __var_status__: '__var_status__',
                    __var_processing__: '__var_processing__',
                    __var_cancelling__: '__var_cancelling__',
                    __var_chat_title__: '__var_chat_title__',
                    __var_follow_up__: '__var_follow_up__',
                    __var_reactions__: '__var_reactions__',
                    __var_websocket_state__: '__var_websocket_state__',
                    __var_sending__: '__var_sending__',
                },
            },
        ],
    },

    'ex_func_send': {
        title: '메시지 전송',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__local_message__', value: '__var_message__' } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_message__', value: '', immediately: true } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: true, immediately: true } },
            {
                type: 'custom', id: 'block_appendDialog',
                inputs: {
                    forceNewUser: true,
                    isHuman: true,
                    dialogs: '__var_dialogs__',
                    content: '__local_message__',
                }
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_follow_up__', value: null } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_dialogs__', value: '__var_dialogs__', immediately: true } },
            {
                type: 'websocket', id: 'send',
                description: '질의 보내기',
                inputs: {
                    url: '__var_websocket__',
                    message: {
                        question: '__local_message__'
                    }
                },
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: false } },
        ],
    },

    'ex_func_quickReply': {
        title: '빠른 응답',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: true, immediately: true } },
            {
                type: 'custom', id: 'block_appendDialog',
                inputs: {
                    forceNewUser: true,
                    isHuman: true,
                    dialogs: '__var_dialogs__',
                    content: '__var_message__',
                }
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_follow_up__', value: null } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_dialogs__', value: '__var_dialogs__', immediately: true } },
            {
                type: 'websocket', id: 'send',
                description: '질의 보내기',
                inputs: {
                    url: '__var_websocket__',
                    message: {
                        question: '__var_message__'
                    }
                },
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_sending__', value: false } },
        ],
    },

    'ex_func_reactToMessage': {
        title: '메시지 평가하기',
        process: [
            {
                type: 'api',
                inputs: {
                    method: 'post',
                    url: "(__var_focused__?.svc_dns) + '/feedback'",
                    body: {
                        id: '__var_id__',
                        chat_id: '__var_chat_id__',
                        message_id: '__var_message_id__',
                        feedback: "__var_reaction__ > 0 ? 'positive' : (__var_reaction__ < 0 ? 'negative' : 'none')",
                    }
                },
                success: {
                    // outputs: {},
                    action: {
                        type: 'action', id: 'changeVariable',
                        inputs: {
                            key: '__var_reactions__',
                            value: '({...(__var_reactions__ || {}), [__var_message_id__]: __var_reaction__})'
                        }
                    },
                },
                error: {
                    init: { type: 'custom', id: 'block_buildSnackbar', inputs: { message: '오류 발생' } },
                    custom: {
                        '__ERR_NETWORK': { type: 'custom', id: 'block_buildSnackbar', inputs: {message: '서버에 문제 발생',} },
                        '__ERR_BAD_REQUEST': { type: 'custom', id: 'block_buildSnackbar', inputs: { message: '입력 오류' } },
                    }
                },
            },
        ],
    },

    'ex_func_stop': {
        title: '답장 중단',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_cancelling__', value: true, immediately: true } },
            {
                type: 'websocket', id: 'send',
                description: '정지시키기',
                inputs: {
                    url: '__var_websocket__',
                    message: {
                        question: 'terminate'
                    }
                },
            },
            { type: 'delay', inputs: 1000 },
            {
                type: 'websocket', id: 'clear',
                description: '초기화',
                inputs: {
                    url: '__var_websocket__',
                },
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_cancelling__', value: false } },
        ],
    },

    'ex_func_logout': {
        title: '로그아웃',
        process: [
            { type: 'custom', id: 'block_removeLocalStorage', inputs: { key: 'userId' } },
            {
                type: 'page', id: 'move',
                description: '로그인 페이지로 이동',
                inputs: {
                    pageIdOrUrl: 'login',
                    forceRefresh: true,
                }
            },
        ],
    },





    /******************************* 로그인 페이지 ***********************************/

    'ex_func_loginCheck': {
        title: '로그인 여부 확인',
        process: [
            {
                type: 'custom', id: 'block_getLocalStorage',
                description: '로컬 저장소에서 사용자 확인',
                inputs: { key: 'userId', variable: '__var_username__' }
            },
            {
                type: 'case',
                description: '사용자가 확인되면 메인 페이지로 강제 이동',
                inputs: '__var_username__',
                success: {
                    type: 'page', id: 'move',
                    description: '메인 페이지로 이동',
                    inputs: {
                        pageIdOrUrl: 'main',
                        forceRefresh: true,
                    }
                },
            },
        ],
    },

    'ex_func_login': {
        title: '로그인',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_loading__', value: true, immediately: true } },
            {
                type: 'api',
                description: '로그인 API 호출하기',
                inputs: {
                    method: 'post',
                    url: "__var_url__ + '/login'",
                    body: {
                        id: '__var_username__',
                        password: '__var_password__',
                    }
                },
                success: {
                    // outputs: {},
                    action: {
                        type: 'function', id: 'ex_func_loginSuccess',
                        inputs: {
                            __var_username__: '__var_username__',
                        }
                    },
                },
                error: {
                    init: { type: 'custom', id: 'block_buildSnackbar', inputs: { message: '오류 발생' } },
                    custom: {
                        '__ERR_NETWORK': { type: 'custom', id: 'block_buildSnackbar', inputs: {message: '서버에 문제 발생',} },
                        '__ERR_BAD_REQUEST': { type: 'custom', id: 'block_buildSnackbar', inputs: { message: '입력 오류' } },
                        'ID_REQUIRED': { type: 'action', id: 'changeVariable', inputs: { key: '__var_username_error__', value: '아이디 필수' } },
                        'PASSWORD_REQUIRED': { type: 'action', id: 'changeVariable', inputs: { key: '__var_password_error__', value: '비밀번호 필수' } },
                        'ID_NOT_FOUND': { type: 'action', id: 'changeVariable', inputs: { key: '__var_username_error__', value: '아이디를 찾지 못함' } },
                        'PASSWORD_MISMATCH': { type: 'action', id: 'changeVariable', inputs: { key: '__var_password_error__', value: '비밀번호 불일치' } },
                    }
                },
            },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_loading__', value: false, immediately: true } },
        ],
    },

    'ex_func_loginSuccess': {
        title: '로그인 성공하면 사용자 정보 저장하고 메인 페이지로 이동',
        process: [
            {
                type: 'custom', id: 'block_setLocalStorage',
                description: '로그인한 사용자 아이디를 로컬 저장소에 저장',
                inputs: { key: 'userId', data: '__var_username__' }
            },
            {
                type: 'page', id: 'move',
                description: '메인 페이지로 이동',
                inputs: {
                    pageIdOrUrl: 'main',
                    forceRefresh: true,
                }
            },
        ],
    },

    'ex_func_onLoginFormChange': {
        title: '로그인 입력 변경 시 오류 메시지 숨기기',
        process: [
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_username_error__', value: null } },
            { type: 'action', id: 'changeVariable', inputs: { key: '__var_password_error__', value: null } },
        ],
    },

}
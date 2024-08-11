export const page1 = {
    background: {
        color: "#f9f9f9",
        blur: false,
    },
    colors: {
        'customColor1': {
            name: 'custom color 1'
        }
    },
    theme: {
        default: 'light',
        light: {
            widget: '#ffffff',
            // 'customColor1': '#ffffff',
        },
        dark: {
            // widget: '#ffffff',
        },
    },
    scenarios: {
        default: 'scenario_stable',
        'scenario_test': {
            name: '테스트',
            variables: {
                '__url__': 'http://127.0.0.1:4000',
            },
        },
        'scenario_stable': {
            name: '정식',
            variables: {
                '__url__': 'http://127.0.0.1:4000', // https://aia.gen.ai.shinhancard.com
            },
        },
    },
    variables: {
        '__url__': { name: '/home 을 요청할 초기 링크', description: '', type: 'text', },
        '__current_websocket__': { name: '현재 웹소켓 링크', description: '', type: 'text', },
        '__websocket_state__': { name: '현재 웹소켓 상태', description: '', type: 'text', },
        '__user_id__': { name: '사용자 아이디', description: '', type: 'text', },
        '__focused_service__': { name: '현재 사용중인 서비스', description: '', type: 'any', },
        '__services__': { name: '서비스 목록', description: '', type: 'array', },
        '__chat_id__': { name: '체팅 아이디', description: '', type: 'text', },
        '__chat_title__': { name: '체팅 제목', description: '', type: 'text', },
        '__message__': { name: '입력중인 메시지', description: '', type: 'text', },
        '__message_history__': { name: '대화 기록', description: '', type: 'array', },
        '__ai_status__': { name: '인공지능 상태', description: '인공지능이 어떤 작업을 수행하고 있는지 표시', type: 'text', },
        '__cancelling__': { name: '답변 취소 중', description: '', type: 'bool', },
        '__processing__': { name: '인공지능 작동 여부', description: '인공지능이 사용자의 메시지로 작업을 수행 중인가', type: 'bool', },
        '__sending__': { name: '메시지 전송 중', description: '인공지능이 사용자의 메시지로 작업을 수행 중인가', type: 'bool', },
        '__follow_up_questions__': { name: '빠른 응답', description: '', type: 'array', },
        '__follow_up_question__': { name: '빠른 응답', description: '', type: 'text', },
        '__reactions__': { name: '리액션', description: '', type: 'any', },
        '__reaction__': { name: '방금한 리액션', description: '', type: 'text', },
        '__reaction_msg_id__': { name: '방금 리액션을 한 메시지 아이디', description: '', type: 'text', },
    },
    functions: {
        'function_init': {
            title: '페이지 시작',
                functionId: 'ex_func_mainPageInit',
                functionInputs: {
                    __var_focused__: '__focused_service__',
                    __var_websocket__: '__current_websocket__',
                    __var_id__: '__user_id__',
                    __var_chat_id__: '__chat_id__',
                    __var_chat_title__: '__chat_title__',
                    __var_dialogs__: '__message_history__',
                    __var_status__: '__ai_status__',
                    __var_processing__: '__processing__',
                    __var_sending__: '__sending__',
                    __var_cancelling__: '__cancelling__',
                    __var_follow_up__: '__follow_up_questions__',
                    __var_reactions__: '__reactions__',
                    __var_websocket_state__: '__websocket_state__',
                    __var_url__: '__url__',
                    __var_services__: '__services__',
                }
        },
        'function_serviceChange': {
            title: '서비스 변경',
            functionId: 'ex_func_serviceChange',
            functionInputs: {
                __var_focused__: '__focused_service__',
                __var_websocket__: '__current_websocket__',
                __var_id__: '__user_id__',
                __var_chat_id__: '__chat_id__',
                __var_chat_title__: '__chat_title__',
                __var_dialogs__: '__message_history__',
                __var_status__: '__ai_status__',
                __var_processing__: '__processing__',
                __var_sending__: '__sending__',
                __var_cancelling__: '__cancelling__',
                __var_follow_up__: '__follow_up_questions__',
                __var_reactions__: '__reactions__',
                __var_websocket_state__: '__websocket_state__',
            }
        },
        'function_sendMessage': {
            title: '메시지 전송',
            functionId: 'ex_func_send',
            functionInputs: {
                __var_websocket__: '__current_websocket__',
                __var_message__: '__message__',
                __var_dialogs__: '__message_history__',
                __var_sending__: '__sending__',
                __var_follow_up__: '__follow_up_questions__',
            }
        },
        'function_quickReply': {
            title: '빠른 응답',
            functionId: 'ex_func_quickReply',
            functionInputs: {
                __var_sending__: '__sending__',
                __var_dialogs__: '__message_history__',
                __var_websocket__: '__current_websocket__',
                __var_message__: '__follow_up_question__',
                __var_follow_up__: '__follow_up_questions__',
            }
        },
        'function_reaction': {
            title: '메시지 평가',
            functionId: 'ex_func_reactToMessage',
            functionInputs: {
                __var_focused__: '__focused_service__',
                __var_id__: '__user_id__',
                __var_chat_id__: '__chat_id__',
                __var_reactions__: '__reactions__',
                __var_reaction__: '__reaction__',
                __var_message_id__: '__reaction_msg_id__',
            }
        },
        'function_stopReply': {
            title: '답변 중단',
            functionId: 'ex_func_stop',
            functionInputs: {
                __var_websocket__: '__current_websocket__',
                __var_cancelling__: '__cancelling__',
            }
        },
        'function_logout': {
            title: '로그아웃',
            functionId: 'ex_func_logout',
            functionInputs: {
            }
        },
    },
    events: {
        onStart: 'function_init'
    },
    widgets: {
        'widget_chatGPTStyleSidebar': {
            categoryId: 'chatGPTStyleSidebar',
            inputs: {
                title: '',
                // titleSize: ,
                // tip: '아래 서비스를 눌러서 새 대화를 시작하세요',
                focusedId: '__focused_service__',
                ids: '__services__',
                tabTitles: '__services__?.map(item => item.svc_nm)',
                tabHeight: 72,
                tabSpacing: 2,
                tabFontSize: 18,
                tabTextAlign: 'center',
                // disabled: '__processing__ || __sending__ || __cancelling__',
            },
            colors: {
                // tabBackgrounds: '#424d80',
                tabBackgrounds: '#747480',
            },
            events: {
                tabClick: 'function_serviceChange'
            },
            noShadow: true,
            background: 'transparent',
        },
        'widget_chatGPTStyleChat': {
            categoryId: 'chatGPTStyleChat',
            inputs: {
                title: '__chat_title__',
                dialogs: '__message_history__',
                sending: "__websocket_state__ !== '1' || __sending__",
                stopping: '__cancelling__',
                replying: '__processing__',
                // emptyMessage: '__focused_service__?.svc_nm',
                waitingMessage: '__ai_status__',
                input: '__message__',
                // inputPlaceholder: '여기에 원하는 메시지를 입력하세요...',
                pressEnterToSend: true,
                quickReplies: '__follow_up_questions__',
                quickReply: '__follow_up_question__',
                quickRepliesFill: true,
                connectionState: "__websocket_state__ === '0' ? '연결 중...' : (__websocket_state__ !== '1' ? '연결 재시도 중...' : '')",
                likes: '__reactions__',
                lastLikeReactionId: '__reaction_msg_id__',
                lastLikeReaction: '__reaction__',
            },
            colors: {
                // referenceColor: '#91A8ff',
                referenceColor: '#747480',
            },
            events: {
                // messageTyping: 'function_',
                stop: 'function_stopReply',
                send: 'function_sendMessage',
                quickReply: 'function_quickReply',
                reaction: 'function_reaction',
            },
            noShadow: true,
            // background: 'transparent',
        },
        'widget_logoutButton': {
            categoryId: 'button',
            inputs: {
                // disabled: true,
                // loading: true,
                label: '로그아웃',
                // endIcon: '',
                startIcon: 'logout',
                height: 40,
                minWidth: 120,
                align: 'bottom',
                // radius: 3,
                variant: 'text',
            },
            colors: {
                main: '#ff0000'
            },
            events: {
                click: 'function_logout',
            },
            noShadow: true,
            background: 'transparent',
        },
        'widget_logo': {
            categoryId: 'photo',
            inputs: {
                text: '.',
                url: process.env.PUBLIC_URL + '/ey-logo-sidebar.png',
                // textSize,
            },
            colors: {
            },
            events: {
                // imageClick
            },
            noShadow: true,
            background: 'transparent',
        },
    },
    layout: {
        mode: 'stretch',
        centering: true,
        responsive: [
            {
                cols: 6,
                disableSnap: true,
                layout: {
                    'widget_chatGPTStyleSidebar': { x: 0, y: 0, h: -2 },
                    'widget_chatGPTStyleChat': { x: 3, y: 0, w: -3, h: 0 },
                    'widget_logoutButton': { x: 0.5, y: 1, w: 2},
                    'widget_logo': { x: 0.5, y: 1.5, w: 2},
                    // 'widget_logoutButton': { x: 0, y: 3, w: 3},
                    // 'widget_logo': { x: 0, y: 3, w: 3},
                },
                types: {
                    'widget_chatGPTStyleSidebar': 0,
                    'widget_chatGPTStyleChat': 0,
                    'widget_logoutButton': 0,
                    'widget_logo': 0,
                }
            },
        ],
    }
}
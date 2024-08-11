export const loginPage = {
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
        '__url__': { name: '링크', description: '', type: 'text', },
        '__username__': { name: '사원 번호', description: '', type: 'text', },
        '__password__': { name: '비밀번호', description: '', type: 'text', },
        '__loading__': { name: '처리 중', description: '', type: 'boolean', },
        '__username_error__': { name: '사원 번호 오류 메시지', description: '', type: 'text', },
        '__password_error__': { name: '비밀번호 오류 메시지', description: '', type: 'text', },
    },
    functions: {
        'function_init': {
            title: '페이지 시작',
            functionId: 'ex_func_loginCheck',
            functionInputs: {
                __var_username__: '__username__',
            }
        },
        'function_login': {
            title: '로그인',
            functionId: 'ex_func_login',
            functionInputs: {
                __var_url__: '__url__',
                __var_username__: '__username__',
                __var_password__: '__password__',
                __var_loading__: '__loading__',
                __var_username_error__: '__username_error__',
                __var_password_error__: '__password_error__',
            }
        },
        'function_onChange': {
            title: '입력 변경',
            functionId: 'ex_func_onLoginFormChange',
            functionInputs: {
                __var_username_error__: '__username_error__',
                __var_password_error__: '__password_error__',
            }
        },
    },
    events: {
        onStart: 'function_init'
    },
    widgets: {
        'widget_login': {
            categoryId: 'login',
            inputs: {
                title: '로그인',
                // tip,
                usernameLabel: '사원 번호',
                passwordLabel: '비밀번호',
                confirmLabel: '확인',
                // cancelLabel: '취소',
                username: '__username__',
                password: '__password__',
                usernameError: '__username_error__',
                passwordError: '__password_error__',
                loading: '__loading__',
            },
            colors: {
                // highlightColor: '#ffffff',
                errorColor: '#ff0000',
                // confirmColor: '#85f11e',
                // cancelColor: '#ff0000',
            },
            events: {
                usernameChange: 'function_onChange',
                passwordChange: 'function_onChange',
                confirm: 'function_login',
                // cancel: 'function_',
            },
            noShadow: true,
            background: 'transparent',
        },
        'widget_logo': {
            categoryId: 'photo',
            inputs: {
                text: '.',
                // textSize,
                backgroundSize: 'contain',
                backgroundPosition: 'bottom',
                // url: 'https://www.ey.com/adobe/dynamicmedia/deliver/dm-aid--d415a9f4-f563-4dad-aed7-4024a9fb786a/ey-logo-footer.png?preferwebp=true',
                url: process.env.PUBLIC_URL + '/ey-logo-footer.png',
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
        // mode: 'stretch',
        centering: true,
        responsive: [
            {
                cols: 3,
                layout: {
                    'widget_logo': { x: 1, y: 1, w: 1 },
                    'widget_login': { x: 0, y: 0, h: -1 },
                },
                types: {
                    'widget_login': 0,
                    'widget_logo': 0,
                }
            },
        ],
    }
}
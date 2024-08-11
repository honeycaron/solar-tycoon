export const blocks = ({__move, __overlay, __snackbar, __websocket_assign}) => ({__getValue, __changeValue}) => ({

    block_svc_selected: {
        name: '목록에서 selected 가 Y 인 항목 찾아서 저장',
        execute: ({ list, selected }) => {
            const _list = __getValue(list)
            __changeValue(selected, _list.find(item => item.selected === "Y"))
            // __changeValue(selected, _list.find(item => item.selected === "Y")?.backend_svc_id)
        }
    },

    block_appendDialog: {
        // name: 'set today date if null',
        execute: (
            {
                forceNewUser,
                id,
                dialogs,
                isProcessing,
                isHuman,
                type = 'text',
                title,
                content,
                followUp,
                finished
            }
        ) => {
            __changeValue(isProcessing, __getValue(finished) === 'N', true)

            let parsedDialogs = __getValue(dialogs) || []
            let parsedIsHuman = __getValue(isHuman)
            let parsedTitle = __getValue(title)
            let parsedContent = __getValue(content) || ''
            let parsedType = __getValue(type)

            let lastDialog = parsedDialogs[parsedDialogs.length - 1] || {}
            let lastUser = lastDialog.icon
            let lastMessage = lastDialog.message || []
            let lastContent = lastMessage[lastMessage.length - 1] || {}

            const isSameUser = parsedIsHuman ? (lastUser === 'user') : (lastUser === 'ai')
            const isSameType = parsedType === lastContent.type
            const newContent = { type: parsedType, content: parsedContent }

            if (isSameUser && !__getValue(forceNewUser)) {

                if (parsedType === 'follow_up_question') {
                    __changeValue(followUp, [...(__getValue(followUp) || []), parsedContent])

                } else if (parsedType === 'hyperlink') {
                    if (!lastDialog.references) lastDialog.references = []

                    const num = parseFloat(parsedTitle)
                    if (Number.isNaN(num)) {
                        lastDialog.references = [...lastDialog.references, parsedContent]
                    } else {
                        lastDialog.references[num - 1] = parsedContent
                    }

                } else if (isSameType) {
                    // 현재 content 에 append
                    if (parsedContent) {
                        lastContent.content = (lastContent.content || '').concat(parsedContent)
                    }
                } else {
                    // 새로운 content 추가
                    if (lastContent.content?.length === 0) lastMessage.pop()
                    lastMessage.push(newContent)
                }

            } else {
                // 다르면 새로운 dialog 생성
                parsedDialogs.push({
                    id: __getValue(id),
                    user: isHuman ? '사용자' : '인공지능',
                    icon: isHuman ? 'user' : 'ai',
                    message: parsedContent ? [newContent] : [],
                })
            }

            __changeValue(dialogs, parsedDialogs)
        }
    },

    block_buildSnackbar: {
        name: 'Build Snackbar',
        execute: ({ message, variant, preventDuplicate, autoHideDuration = 3000, persist, button }) => {

            const _parsedMessage = __getValue(message)
            let _buttonComponent

            switch (button) {
                case 'reload':
                    _buttonComponent = (
                        <button
                            style={{
                                background: 'rgba(255,255,255,0.1)',
                                color: 'white',
                                boxShadow: 'none',
                                border: 'none',
                                padding: '8px 12px',
                                cursor: 'pointer',
                            }}
                            onClick={() => window.location.reload()}
                        >
                            Reload
                        </button>
                    )
                    break
            }

            __snackbar(
                _parsedMessage,
                { variant, preventDuplicate, autoHideDuration, persist, action: () => _buttonComponent }
            )
        },
    },

    block_setLocalStorage: {
        name: 'set in local storage',
        execute: ({ key, data }) => {
            localStorage.setItem(__getValue(key), __getValue(data))
        },
    },

    block_getLocalStorage: {
        name: 'get from local storage',
        execute: ({ key, variable }) => {
            const _data = localStorage.getItem(__getValue(key))
            __changeValue(variable, _data)
        },
    },

    block_removeLocalStorage: {
        name: 'remove from local storage',
        execute: ({ key }) => {
            localStorage.removeItem(__getValue(key))
        },
    },

    block_generateRandomId: {
        name: 'generate random id',
        execute: ({ variable }) => {
            const timestamp = Date.now().toString(36)
            const randomNumber = Math.random().toString(36).substring(2, 7)
            const _random = timestamp + '-' + randomNumber
            __changeValue(variable, _random)
        },
    },

    block_console: {
        name: 'Console Log',
        execute: ({ message }) => {
            console.log(__getValue(message))
        },
    },
    
})
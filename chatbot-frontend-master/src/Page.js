import React from "react";
import {useLocation, useNavigate, useParams, useSearchParams} from "react-router-dom";
import {
    HistoryContextProvider,
    PageContextProvider,
    WidgetBoard,
} from "@wizlit/react-widget-board";
import {widgetCategories} from "@wizlit/react-widget";
import {functions} from "./data/functions";
import {blocks} from "./data/blocks";
import {pages} from "./data/pages";
// import {useGlobalData} from "@wizlit/react-component";
import {enqueueSnackbar} from "notistack";
import {pagePrefix} from "./App";

const fetchPageById = async (id) => {
    // const response = await fetch(`/api/posts/${postId}`)
    // const data = await response.json()
    // return data
    return pages[id]
}

const convertStringToNumber = (string) => {
    const number = Number(string)
    if (isNaN(number)) return string
    return number
}

const convertSearchParamsToObject = (searchParams) => {
    const paramsObject = {}

    for (const [key, value] of searchParams) {
        if (paramsObject.hasOwnProperty(key)) paramsObject[key] = searchParams.getAll(key).map(str => convertStringToNumber(str))
        else paramsObject[key] = convertStringToNumber(searchParams.get(key))
    }

    return paramsObject
}

export const Page = (props) => {

    const { id } = useParams()
    const location = useLocation()
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()

    const searchParamsObject = convertSearchParamsToObject(searchParams)

    // const [lastStatus, setLastStatus] = useGlobalData('__last', {})

    const pageComponent = ({key, pageId, page}) => (
        <PageContextProvider
            apiConsole
            // developerMode
            // theme: PropTypes.oneOf(['light', 'dark']),

            categories={widgetCategories}
            sharedFunctions={functions}
            blocks={blocks}
            blockInnerFunctions={{
                __snackbar: enqueueSnackbar
            }}

            bindDefault={{
                key: key,
                pageProperty: page,
                // defaultState
                // scenario: 'scenario_test',
            }}
        >
            <WidgetBoard
                // developerMode
            />
        </PageContextProvider>
    )

    return (
        <HistoryContextProvider
            // developerMode

            location={location}
            pageId={id}
            search={searchParamsObject}

            // defaultData={lastStatus}
            // onChange={setLastStatus}

            fetchPage={fetchPageById}
            navigate={navigate}
            pagePathname={(pageId) => `${pagePrefix}/${pageId}`}
            overlayComponent={pageComponent}
            // loadingComponent
        >
            {pageComponent}
        </HistoryContextProvider>
    )
}
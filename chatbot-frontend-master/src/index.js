import React from 'react';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {createRoot} from "react-dom/client";
import { SnackbarProvider } from 'notistack';
import {BrowserRouter} from "react-router-dom";
// import {GlobalStateProvider} from "@wizlit/react-component";
import {PubSubContextProvider, StateContextProvider, WebSocketContextProvider} from "@wizlit/react-widget-board";

const app = (
    // <GlobalStateProvider>
    <PubSubContextProvider>
        <WebSocketContextProvider
            // developerMode
        >
            <StateContextProvider
                // developerMode
            >
                <SnackbarProvider maxSnack={3}>
                    <BrowserRouter>
                        <App />
                    </BrowserRouter>
                </SnackbarProvider>
            </StateContextProvider>
        </WebSocketContextProvider>
    </PubSubContextProvider>
    // </GlobalStateProvider>
)

const container = document.getElementById('root');
const root = createRoot(container);
root.render(app);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

import React from 'react';
import {Navigate, Route, Routes} from 'react-router-dom';
import {Page} from "./Page";
import {defaultPath} from "./data/pages";

export const pagePrefix = ''

function App() {
  return (
      <Routes>
        <Route path={`${pagePrefix}/:id`} element={<Page />} />
        <Route path="*" element={<Navigate to={`${pagePrefix}${defaultPath}`} replace />} />
      </Routes>
  )
}

export default App
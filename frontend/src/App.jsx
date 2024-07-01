import React from "react";
import "./index.scss";

import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";

import Layout from "./components/Layout";
import ChatPage from "./pages/ChatPage";
import FileUploadPage from "./pages/FileUploadPage";
import Page404 from "./pages/Page404";

const App = () => {

    const router = createBrowserRouter([
        {
            element: <Layout />,
            errorElement: <Page404 />,
            children: [
                {
                    path: "/",
                    element: <ChatPage />,
                },
                {
                    path: "/file-upload",
                    element: <FileUploadPage />,
                },
            ],
        },
    ])

    return (
        <div className="app">
            <RouterProvider router={router} />
        </div>
    )
}

export default App;
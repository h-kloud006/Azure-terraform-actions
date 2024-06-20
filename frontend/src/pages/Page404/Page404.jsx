import React from "react";

import logo from '@Images/logo.png';

function Page404() {
    return (
        <div className="error-page">
            <img src={logo} alt="Logo" className="error-page-logo" />
            <div className="error-page-title">404</div>
            <div className="error-page-text">Page not found.</div>
        </div>
    )
}
export default Page404;
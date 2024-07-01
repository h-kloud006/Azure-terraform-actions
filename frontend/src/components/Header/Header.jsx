import React from 'react';
import './styles.scss';

import { Link, useLocation } from "react-router-dom";

import profilePic from '@Images/profile-pic.svg';
import logo from '@Images/logo.png';

function Header() {
    const location = useLocation();

    function isCurrentPage(path) {
        return location.pathname === path;
    }

    return (
        <header className="header">
            <img src={logo} alt="Logo" className="header-logo"/>
            <div className="header-buttons">
                <Link to={'/file-upload'} className={`header-button ${isCurrentPage('/file-upload') ? 'active' : ''}`}>File Upload</Link>
                <Link to={'/'} className={`header-button ${isCurrentPage('/') ? 'active' : ''}`}>Chat</Link>
            </div>
            <div className="header-user-details">
                <img src={profilePic} alt="Profile Pic" className="header-user-details-pic"/>
                <h5 className="header-user-details-name">John</h5>
            </div>
        </header>
    );
}

export default Header;

import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
    return (
        <header>
            <Link to="/" className="home-button">Home</Link>
            {/* other header content */}
        </header>
    );
}

export default Header;

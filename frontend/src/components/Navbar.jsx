import React from 'react';

export default function Navbar({ setPage }) {
    return (
        <nav className="navbar">
            <button onClick={() => setPage('dashboard')}>Dashboard</button>
            <button onClick={() => setPage('history')}>History</button>
        </nav>
    );
}

import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import HistoryPage from './pages/HistoryPage';

export default function App() {
    const [page, setPage] = useState('dashboard');

    return (
        <div>
            <Navbar setPage={setPage} />
            {page === 'dashboard' && <Dashboard />}
            {page === 'history' && <HistoryPage />}
        </div>
    );
}

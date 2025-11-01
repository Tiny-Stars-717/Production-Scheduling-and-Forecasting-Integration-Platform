import React, { useState, useEffect } from 'react';
import { getHistory, deleteHistory } from '../services/api';
import OrderTable from '../components/OrderTable';

export default function HistoryPage() {
    const [module, setModule] = useState('schedule');
    const [historyData, setHistoryData] = useState([]);

    const fetchHistory = () => {
        getHistory(module).then(res => setHistoryData(res.data.historyList));
    };

    const handleDelete = (recordId) => {
        deleteHistory(module, recordId).then(fetchHistory);
    };

    useEffect(fetchHistory, [module]);

    return (
        <div>
            <h2>History</h2>
            <select value={module} onChange={e => setModule(e.target.value)}>
                <option value="schedule">Schedule</option>
                <option value="forecast">Forecast</option>
                <option value="stock">Stock</option>
            </select>
            <button onClick={fetchHistory}>Refresh</button>
            {historyData.map(record => (
                <div key={record.recordId} style={{border:'1px solid gray', margin:'5px', padding:'5px'}}>
                    <div>Algorithm: {record.algorithm}</div>
                    <div>Timestamp: {record.timestamp}</div>
                    <div>Params: {JSON.stringify(record.params)}</div>
                    <div>Result: {JSON.stringify(record.result)}</div>
                    <button onClick={() => handleDelete(record.recordId)}>Delete</button>
                </div>
            ))}
        </div>
    );
}

import React from 'react'; 

export default function OrderTable({ data }) {
    if (!data || data.length === 0) return <div>No data</div>;

    const headers = Object.keys(data[0]);

    return (
        <table border="1" cellPadding="5">
            <thead>
                <tr>
                    {headers.map(h => <th key={h}>{h}</th>)}
                </tr>
            </thead>
            <tbody>
                {data.map((row, idx) => (
                    <tr key={idx}>
                        {headers.map(h => <td key={h}>{row[h] || ''}</td>)}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

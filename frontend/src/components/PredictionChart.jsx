import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function PredictionChart({ chartData }) {
    if (!chartData) return null;

    const data = {
        labels: chartData.x,
        datasets: [
            {
                label: 'Value',
                data: chartData.y,
                borderColor: 'blue',
                backgroundColor: 'lightblue',
            },
        ],
    };

    return <Line data={data} />;
}

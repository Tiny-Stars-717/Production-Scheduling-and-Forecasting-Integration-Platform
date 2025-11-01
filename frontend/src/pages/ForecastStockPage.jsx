import React, { useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function ForecastStockPage() {
  const [forecastData, setForecastData] = useState([]);
  const [stockData, setStockData] = useState([]);

  const handleForecast = async () => {
    const res = await axios.post("/api/predict/run", { method: "ARIMA" });
    setForecastData(res.data);
  };

  const handleStockOpt = async () => {
    const res = await axios.post("/api/stock/optimize", { method: "PSO" });
    setStockData(res.data);
  };

  return (
    <div className="card">
      <h2>预测与库存优化</h2>
      <button onClick={handleForecast}>执行需求预测</button>
      <button onClick={handleStockOpt}>执行库存优化</button>

      <div className="chart-container">
        <LineChart width={600} height={300} data={forecastData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="forecast" stroke="#8884d8" />
        </LineChart>
      </div>

      <table>
        <thead>
          <tr>{stockData[0] && Object.keys(stockData[0]).map((k) => <th key={k}>{k}</th>)}</tr>
        </thead>
        <tbody>
          {stockData.map((r, i) => (
            <tr key={i}>
              {Object.values(r).map((v, j) => (
                <td key={j}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

import React, { useState } from "react";
import axios from "axios";

export default function SchedulePage() {
  const [useOpt, setUseOpt] = useState(true);
  const [algo, setAlgo] = useState("EDD");
  const [result, setResult] = useState([]);

  const handleSchedule = async () => {
    const res = await axios.post("/api/schedule/run", { useOpt, algo });
    setResult(res.data);
  };

  return (
    <div className="card">
      <h2>排产模块</h2>
      <label>
        <input
          type="checkbox"
          checked={useOpt}
          onChange={() => setUseOpt(!useOpt)}
        />
        使用优化算法
      </label>
      <select value={algo} onChange={(e) => setAlgo(e.target.value)}>
        <option value="EDD">EDD</option>
        <option value="greedy">贪心法</option>
        <option value="batch">批量生产调度</option>
      </select>
      <button onClick={handleSchedule}>执行排产</button>

      <table>
        <thead>
          <tr>{result[0] && Object.keys(result[0]).map((k) => <th key={k}>{k}</th>)}</tr>
        </thead>
        <tbody>
          {result.map((r, i) => (
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

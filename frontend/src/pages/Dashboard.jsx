import React, { useState, useEffect } from 'react';
import OrderTable from '../components/OrderTable';
import PredictionChart from '../components/PredictionChart';
import {
    uploadExcel,
    getLastFilePath,
    readFilePath,
    runSchedule,
    runForecast,
    runStock
} from '../services/api';

export default function Dashboard() {
    const [inputData, setInputData] = useState([]);
    const [scheduleResult, setScheduleResult] = useState([]);
    const [metrics, setMetrics] = useState({});
    const [forecastResult, setForecastResult] = useState([]);
    const [forecastChart, setForecastChart] = useState(null);
    const [stockResult, setStockResult] = useState([]);
    const [stockChart, setStockChart] = useState(null);
    const [algorithm, setAlgorithm] = useState('edd');
    const [forecastAlgo, setForecastAlgo] = useState('arima');
    const [stockAlgo, setStockAlgo] = useState('lp');

    const [loading, setLoading] = useState(false);
    const [log, setLog] = useState('');

    // ✅ 页面加载时自动读取上次使用的文件路径
    useEffect(() => {
        async function loadLastData() {
            try {
                const res = await getLastFilePath();
                if (res.data.filepath) {
                    const r = await readFilePath(res.data.filepath);
                    setInputData(r.data.data || []);
                    setLog('📂 已加载上次使用的数据文件。');
                } else {
                    setLog('ℹ️ 未找到上次文件记录，请上传新文件。');
                }
            } catch (err) {
                console.error('❌ 读取上次文件失败:', err);
                setLog('❌ 无法加载上次文件。');
            }
        }
        loadLastData();
    }, []);

    // ✅ 上传并自动读取 Excel 文件
    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
            setLoading(true);
            const res = await uploadExcel(file);
            if (res.data.status === 'success') {
                setInputData(res.data.data);
                setLog('✅ 文件上传并成功读取。');
            } else {
                setLog('⚠️ 上传失败：' + JSON.stringify(res.data));
            }
        } catch (err) {
            console.error('❌ 上传错误:', err);
            setLog('❌ 上传文件时出错，请检查后端接口。');
        } finally {
            setLoading(false);
        }
    };

    // ✅ 执行排产
    const handleRunSchedule = async () => {
        try {
            setLoading(true);
            setLog(`🚀 正在运行排产算法 [${algorithm}] ...`);
            const res = await runSchedule(algorithm, inputData);
            setScheduleResult(res.data.scheduleResult || []);
            setMetrics(res.data.metrics || {});
            setLog(`✅ 排产完成（算法: ${algorithm}）`);
        } catch (err) {
            console.error('❌ 排产失败:', err);
            setLog('❌ 排产算法运行出错。');
        } finally {
            setLoading(false);
        }
    };

    // ✅ 执行预测
    const handleRunForecast = async () => {
        try {
            setLoading(true);
            setLog(`📈 正在运行预测算法 [${forecastAlgo}] ...`);
            const res = await runForecast(forecastAlgo, inputData);
            setForecastResult(res.data.forecastResult || []);
            setForecastChart(res.data.chartData || null);
            setLog(`✅ 预测完成（算法: ${forecastAlgo}）`);
        } catch (err) {
            console.error('❌ 预测失败:', err);
            setLog('❌ 预测算法运行出错。');
        } finally {
            setLoading(false);
        }
    };

    // ✅ 执行库存优化
    const handleRunStock = async () => {
        try {
            setLoading(true);
            setLog(`📦 正在运行库存优化算法 [${stockAlgo}] ...`);
            const res = await runStock(stockAlgo, forecastResult);
            setStockResult(res.data.stockResult || []);
            setStockChart(res.data.chartData || null);
            setLog(`✅ 库存优化完成（算法: ${stockAlgo}）`);
        } catch (err) {
            console.error('❌ 库存优化失败:', err);
            setLog('❌ 库存优化算法运行出错。');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>📊 智能排产与优化控制台</h1>

            <section style={{ marginTop: '20px' }}>
                <h2>① 数据导入</h2>
                <input
                    type="file"
                    accept=".xlsx, .xls"
                    onChange={handleFileChange}
                    style={{ marginBottom: '10px' }}
                />
                {loading && <div>⏳ 正在处理，请稍候...</div>}
                <OrderTable data={inputData} />
            </section>

            <section style={{ marginTop: '30px' }}>
                <h2>② 排产模块</h2>
                <select value={algorithm} onChange={e => setAlgorithm(e.target.value)}>
                    <option value="edd">EDD</option>
                    <option value="greedy">Greedy</option>
                    <option value="batch">Batch</option>
                </select>
                <button onClick={handleRunSchedule} style={{ marginLeft: '10px' }}>运行排产</button>
                <OrderTable data={scheduleResult} />
                {metrics && Object.keys(metrics).length > 0 && (
                    <div style={{ marginTop: '10px' }}>
                        <strong>性能指标：</strong> {JSON.stringify(metrics)}
                    </div>
                )}
            </section>

            <section style={{ marginTop: '30px' }}>
                <h2>③ 预测模块</h2>
                <select value={forecastAlgo} onChange={e => setForecastAlgo(e.target.value)}>
                    <option value="arima">ARIMA</option>
                    <option value="exp_smooth">指数平滑</option>
                </select>
                <button onClick={handleRunForecast} style={{ marginLeft: '10px' }}>运行预测</button>
                <OrderTable data={forecastResult} />
                <PredictionChart chartData={forecastChart} />
            </section>

            <section style={{ marginTop: '30px' }}>
                <h2>④ 库存优化模块</h2>
                <select value={stockAlgo} onChange={e => setStockAlgo(e.target.value)}>
                    <option value="lp">线性规划</option>
                    <option value="pso">粒子群优化</option>
                </select>
                <button onClick={handleRunStock} style={{ marginLeft: '10px' }}>运行库存优化</button>
                <OrderTable data={stockResult} />
                <PredictionChart chartData={stockChart} />
            </section>

            <section style={{ marginTop: '30px', padding: '10px', background: '#f9f9f9', borderRadius: '8px' }}>
                <h3>系统日志</h3>
                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', color: '#333' }}>
                    {log}
                </pre>
            </section>
        </div>
    );
}

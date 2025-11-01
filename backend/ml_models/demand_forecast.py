import pandas as pd
from datetime import timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
import math
from statsmodels.tsa.stattools import acf
import numpy as np

def preprocess_time_series(input_data):
    """
    数据预处理：兼容 Excel 读取与多种列名
    支持字段：
    - 日期 / 录入日期
    - 需求数量 / 当日需求数量 / 订单数量
    """
    # 判断输入是 DataFrame 还是 list[dict]
    if isinstance(input_data, str):
        # 若传入 Excel 路径
        df = pd.read_excel(input_data)
    else:
        df = pd.DataFrame(input_data)

    # ---- 自动识别日期列 ----
    possible_date_cols = ['录入日期', '日期', 'date', '时间']
    date_col = next((col for col in possible_date_cols if col in df.columns), None)
    if date_col is None:
        raise ValueError("未找到日期列，请包含 '日期' 或 '录入日期'")

    # ---- 自动识别需求列 ----
    possible_demand_cols = ['需求数量', '当日需求数量', '订单数量', '当日订单数']
    demand_col = next((col for col in possible_demand_cols if col in df.columns), None)
    if demand_col is None:
        raise ValueError("未找到需求数量列，请包含 '需求数量' 或 '当日需求数量'")

    # ---- 处理日期和排序 ----
    df['date'] = pd.to_datetime(df[date_col])
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    df.rename(columns={demand_col: '需求数量'}, inplace=True)

    return df


def run_forecast(input_data, algorithm, forecast_days=None, prev_model=None):
    """
    时间序列预测主函数
    -----------------------------------------------------
    input_data: Excel 文件路径 或 list[dict]
    algorithm: 'arima' / 'exp_smooth'
    forecast_days: 预测未来天数（默认 = 样本天数 / 2）
    prev_model: 已训练模型（用于动态更新）
    return: forecast_result, chart_data, new_model
    """
    df = preprocess_time_series(input_data)
    ts = df['需求数量']
    n = len(ts)

    # 动态设定预测天数（样本天数 / 2，向下取整）
    if forecast_days is None:
        forecast_days = max(1, math.floor(n / 2))
    print(f"🔢 样本天数: {n} -> 预测天数: {forecast_days}")

    # 一、ARIMA 模型
    if algorithm == 'arima':
        if prev_model is not None:
            try:
                fit_model = prev_model.append(ts, refit=False)
            except Exception:
                fit_model = prev_model.fit()
        else:
            auto_model = auto_arima(ts, seasonal=False, stepwise=True, suppress_warnings=True)
            best_order = auto_model.order
            model = ARIMA(ts, order=best_order)
            fit_model = model.fit()

        forecast_index = pd.date_range(start=ts.index[-1] + timedelta(days=1),
                                       periods=forecast_days, freq='D')
        forecast = fit_model.forecast(steps=forecast_days)
        forecast_series = pd.Series(forecast, index=forecast_index)

    # 二、指数平滑系列模型
    elif algorithm == 'exp_smooth':
        if prev_model is not None:
            fit_model = prev_model
        else:
            if n <= 20:
                model = Holt(ts)
                fit_model = model.fit()
                model_type = "双指数平滑"
            else:
                # --------------------------
                # 自动判断季节周期（基于ACF）
                # --------------------------
                max_lag = min(30, n // 2)  # 最大滞后期，避免太短或太长
                acf_vals = acf(ts, nlags=max_lag, fft=False)
                # 找到滞后期峰值（忽略滞后0）
                lag_peaks = np.argmax(acf_vals[1:]) + 1
                seasonal_periods = max(2, lag_peaks)  # 至少2
                print(f"🔄 自动判断季节周期: {seasonal_periods}")

                model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=seasonal_periods)
                fit_model = model.fit()
                model_type = f"三指数平滑（周期={seasonal_periods}）"

            print(f"✅ 已选择 {model_type} 模型（样本数: {n}）")

        forecast = fit_model.forecast(forecast_days)
        forecast_index = pd.date_range(start=ts.index[-1] + timedelta(days=1),
                                       periods=forecast_days, freq='D')
        forecast_series = pd.Series(forecast, index=forecast_index)
    else:
        raise ValueError("Unsupported algorithm: 请选择 'arima' 或 'exp_smooth'")

    # 三、统一输出结果
    forecast_result = [
        {"日期": str(d.date()), "预测需求": float(v)} for d, v in forecast_series.items()
    ]
    chart_data = {
        "x": [str(d.date()) for d in ts.index] + [str(d.date()) for d in forecast_series.index],
        "y": [float(v) for v in ts.values] + [float(v) for v in forecast_series.values],  # 转 float
        "分界线": int(len(ts))  # 转 int
    }

    return forecast_result, chart_data, fit_model
import numpy as np
from scipy.optimize import linprog
import random

def run_stock(forecast_data, algorithm):
    """
    智能库存优化算法（线性规划 + 粒子群优化）
    -------------------------------------------------
    参数:
        forecast_data: list[dict]
            格式 [{'日期': '2025-10-24', '预测需求': 100}, ...]
        algorithm: str
            可选 'lp' 或 'pso'
    返回:
        stock_result: list[dict] [{'日期':.., '库存水平':..}, ...]
        chart_data: dict {'x':日期列表, 'y':库存水平}
    -------------------------------------------------
    """

    # 读取需求数据
    demands = np.array([float(d['预测需求']) for d in forecast_data])
    n = len(demands)
    holding_cost = 1.0        # 单位库存持有成本
    shortage_cost = 5.0       # 缺货惩罚成本
    max_stock = max(demands) * 1.5  # 库存上限（经验值）
    daily_supply_limit = max(demands) * 0.8  # 每天最大补货量限制

    #线性规划算法
    if algorithm.lower() == 'lp':
        """
        决策变量:
            x_i = 当日补货量
        约束:
            累积补货量 - 累积需求 >= 0 （不能缺货）
            x_i >= 0, x_i <= daily_supply_limit
        目标:
            最小化 ∑(库存持有成本 + 缺货成本)
        """

        c = np.ones(n) * holding_cost
        A = np.tril(np.ones((n, n))) * -1  # -库存余额 <= -需求累计
        b = -np.cumsum(demands)

        bounds = [(0, daily_supply_limit)] * n

        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if not res.success:
            stock_levels = np.cumsum(demands)
        else:
            deliveries = res.x
            stock_levels = np.cumsum(deliveries - demands)
            stock_levels = np.clip(stock_levels, 0, max_stock)

    # 粒子群优化算法（PSO）
    elif algorithm.lower() == 'pso':
        """
        粒子群用于求解每日补货决策，使得库存总成本最小。
        粒子 = n维补货量向量。
        适应度 = 持有成本 + 缺货惩罚。
        """
        num_particles = 30
        num_iterations = 100
        w, c1, c2 = 0.7, 1.4, 1.4  # 惯性权重与学习因子

        # 初始化
        particles = np.random.uniform(0, daily_supply_limit, (num_particles, n))
        velocities = np.zeros((num_particles, n))
        personal_best = particles.copy()
        global_best = particles[0].copy()

        def fitness(x):
            stock = np.cumsum(x - demands)
            shortage = np.sum(np.abs(stock[stock < 0]))
            holding = np.sum(stock[stock > 0])
            return holding_cost * holding + shortage_cost * shortage

        personal_best_scores = np.array([fitness(p) for p in personal_best])
        global_best = personal_best[np.argmin(personal_best_scores)].copy()
        global_best_score = np.min(personal_best_scores)

        # 迭代更新
        for _ in range(num_iterations):
            for i in range(num_particles):
                r1, r2 = random.random(), random.random()
                velocities[i] = (
                    w * velocities[i]
                    + c1 * r1 * (personal_best[i] - particles[i])
                    + c2 * r2 * (global_best - particles[i])
                )
                particles[i] += velocities[i]
                particles[i] = np.clip(particles[i], 0, daily_supply_limit)

                score = fitness(particles[i])
                if score < personal_best_scores[i]:
                    personal_best[i] = particles[i].copy()
                    personal_best_scores[i] = score

            # 更新全局最优
            best_idx = np.argmin(personal_best_scores)
            if personal_best_scores[best_idx] < global_best_score:
                global_best = personal_best[best_idx].copy()
                global_best_score = personal_best_scores[best_idx]

        deliveries = global_best
        stock_levels = np.cumsum(deliveries - demands)
        stock_levels = np.clip(stock_levels, 0, max_stock)

    else:
        raise ValueError("Unsupported algorithm type. Use 'lp' or 'pso'.")

    # 输出格式（兼容前端）
    stock_result = [
        {"日期": d['日期'], "库存水平": round(float(s), 2)}
        for d, s in zip(forecast_data, stock_levels)
    ]
    chart_data = {
        "x": [d['日期'] for d in forecast_data],
        "y": [round(float(s), 2) for s in stock_levels]
    }

    return stock_result, chart_data

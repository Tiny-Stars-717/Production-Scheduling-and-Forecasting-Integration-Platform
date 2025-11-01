import pandas as pd
from datetime import datetime, timedelta
from copy import deepcopy
from dateutil import parser
import re

def run_schedule_from_excel(input_data, algorithm='edd', batch_size=50, tardiness_weight=1, switch_default=1):
    """
    通用排产调度函数（支持多工序、多机器、顺序加工、批量优化）
    -------------------------------------------------------
    参数:
        input_data: Excel 文件路径 或 list[dict]
        algorithm: 'edd' / 'greedy' / 'batch'
        batch_size: 批量调度时的批大小
        tardiness_weight: 延迟惩罚权重
        switch_default: 默认切换时间（小时）
    返回:
        results: 排产结果表格（list[dict]）
        metrics: 总延迟惩罚、平均延迟惩罚
    """

    #数据读取
    if isinstance(input_data, str):
        df = pd.read_excel(input_data)
    elif isinstance(input_data, list):
        df = pd.DataFrame(input_data)
    else:
        raise ValueError("输入数据格式错误，请传入 Excel 文件路径或 JSON 列表。")

    print(f"📂 读取数据条数: {len(df)}")
    print(f"🧮 数据列: {list(df.columns)}")

    #时间列标准化
    for col in ["到达日期", "最晚交付日期"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    #构建机器集合
    all_machines = set()
    for val in df.get("分配机器", []):
        if pd.notna(val) and str(val).strip() != "":
            all_machines.update([m.strip() for m in str(val).split(",")])
    all_machines = sorted(list(all_machines))
    print("🛠 系统识别机器集合:", all_machines)

    machines_state = {m: {"available_time": 0, "last_product": None} for m in all_machines}
    switch_time = {m: {m2: switch_default for m2 in all_machines if m2 != m} for m in all_machines}

    #构造订单与工序结构
    orders = []
    grouped = df.groupby("订单编号")

    for order_id, group in grouped:
        group = group.sort_values(by="工序编号")
        entry_date = group["到达日期"].iloc[0]
        due_date = group["最晚交付日期"].iloc[0]
        product = str(group["产品型号"].iloc[0])
        quantity = 1  # 暂无“需求数量”，默认1

        operations = []
        for _, row in group.iterrows():
            ops = [m.strip() for m in str(row.get("分配机器", "")).split(",") if m.strip()]
            processing_time = float(row.get("加工时间(h)", 1))
            operations.append({
                "op_no": int(row["工序编号"]),
                "op_id": f"{order_id}_工序{int(row['工序编号'])}",
                "machines": ops if ops else all_machines,
                "processing_time": processing_time
            })

        orders.append({
            "order_id": order_id,
            "product": product,
            "entry_date": entry_date,
            "due_date": due_date,
            "quantity": quantity,
            "operations": operations
        })

    print(f"✅ 构建完成，共 {len(orders)} 个订单。")

    #核心 EDD 调度算法
    def edd_multi_machine(orders, machines_state, switch_time, tardiness_weight):
        schedule = []
        sorted_orders = sorted(orders, key=lambda x: x["due_date"])  # EDD

        for order in sorted_orders:
            prev_finish = 0  # 控制同订单内工序顺序

            for op in order["operations"]:
                best_machine = None
                best_start = None
                best_finish = float("inf")

                for m in op["machines"]:
                    state = machines_state[m]
                    available = state["available_time"]

                    start_time = max(available, prev_finish)
                    finish_time = start_time + op["processing_time"]

                    if finish_time < best_finish:
                        best_finish = finish_time
                        best_machine = m
                        best_start = start_time

                if best_machine is None:
                    raise ValueError(f"工序 {op['op_id']} 没有可用机器！")

                # 更新状态
                machines_state[best_machine]["available_time"] = best_finish
                machines_state[best_machine]["last_product"] = order["product"]
                prev_finish = best_finish

                tardiness = max(0, (best_finish - (order["due_date"] - order["entry_date"]).total_seconds() / 3600))
                penalty = tardiness_weight * tardiness

                schedule.append({
                    "order_id": order["order_id"],
                    "product": order["product"],
                    "op_id": op["op_id"],
                    "machine": best_machine,
                    "processing_time": op["processing_time"],
                    "start_time_dt": order["entry_date"] + timedelta(hours=best_start),
                    "finish_time_dt": order["entry_date"] + timedelta(hours=best_finish),
                    "tardiness": tardiness,
                    "penalty": penalty
                })

        total_penalty = sum(s["penalty"] for s in schedule)
        return schedule, total_penalty

    #Greedy 算法
    def greedy_multi_machine(orders, machines_state, switch_time, tardiness_weight=1):
        """
        全局 SPT 贪心调度算法（考虑工序顺序依赖）
        ---------------------------------------------------------
        原理：
          - 全局贪心：每次从当前可执行的工序池中选加工时间最短的任务
          - 顺序约束：只有前序工序完成后，后续工序才能进入可执行池
        """

        schedule = []
        total_penalty = 0.0

        # 每个订单的当前可执行工序索引
        order_progress = {o["order_id"]: 0 for o in orders}
        order_finish_time = {o["order_id"]: 0.0 for o in orders}

        # 初始可执行工序池（每个订单的第一个工序）
        ready_ops = []
        for order in orders:
            op = order["operations"][0]
            ready_ops.append({
                "order_id": order["order_id"],
                "product": order["product"],
                "entry_date": order["entry_date"],
                "due_date": order["due_date"],
                "op_no": op["op_no"],
                "op_id": op["op_id"],
                "machines": op["machines"],
                "processing_time": op["processing_time"]
            })

        # 循环直到所有工序完成
        while ready_ops:
            # 1️⃣ 选出当前加工时间最短的工序
            ready_ops.sort(key=lambda x: x["processing_time"])
            op = ready_ops.pop(0)

            best_machine = None
            best_start = None
            best_finish = float("inf")

            for m in op["machines"]:
                state = machines_state[m]
                available = state["available_time"]
                last_prod = state["last_product"]

                # 换线时间
                switch_t = 0
                if last_prod and last_prod != op["product"]:
                    switch_t = switch_time.get(m, {}).get(m, 0) or 0

                start_time = max(
                    available + switch_t,
                    order_finish_time[op["order_id"]],
                    0
                )
                finish_time = start_time + op["processing_time"]

                if finish_time < best_finish:
                    best_finish = finish_time
                    best_machine = m
                    best_start = start_time

            # 2️⃣ 更新机器与订单状态
            machines_state[best_machine]["available_time"] = best_finish
            machines_state[best_machine]["last_product"] = op["product"]
            order_finish_time[op["order_id"]] = best_finish

            # 3️⃣ 若该订单还有下一工序，则加入 ready_ops
            order = next(o for o in orders if o["order_id"] == op["order_id"])
            next_index = order_progress[op["order_id"]] + 1
            order_progress[op["order_id"]] = next_index
            if next_index < len(order["operations"]):
                next_op = order["operations"][next_index]
                ready_ops.append({
                    "order_id": order["order_id"],
                    "product": order["product"],
                    "entry_date": order["entry_date"],
                    "due_date": order["due_date"],
                    "op_no": next_op["op_no"],
                    "op_id": next_op["op_id"],
                    "machines": next_op["machines"],
                    "processing_time": next_op["processing_time"]
                })

            # 4️⃣ 计算延迟与惩罚
            due_limit = (op["due_date"] - op["entry_date"]).total_seconds() / 3600
            tardiness = max(0, best_finish - due_limit)
            penalty = tardiness_weight * tardiness
            total_penalty += penalty

            # 5️⃣ 记录结果
            schedule.append({
                "order_id": op["order_id"],
                "product": op["product"],
                "op_id": op["op_id"],
                "machine": best_machine,
                "processing_time": op["processing_time"],
                "start_time_dt": op["entry_date"] + timedelta(hours=best_start),
                "finish_time_dt": op["entry_date"] + timedelta(hours=best_finish),
                "tardiness": round(tardiness, 2),
                "penalty": round(penalty, 2)
            })

        return schedule, total_penalty

    #批量调度优化
    def batch_schedule(orders, machines_state, switch_time, batch_size, tardiness_weight):
        schedule = []
        total_penalty = 0
        # 将订单按到达日期排序，然后分批
        orders_sorted = sorted(orders, key=lambda x: x["entry_date"])
        batched_orders = [orders_sorted[i:i+batch_size] for i in range(0, len(orders_sorted), batch_size)]

        for batch in batched_orders:
            # 每批使用独立机器状态，避免批间干扰
            machines_copy = deepcopy(machines_state)
            s, p = edd_multi_machine(batch, machines_copy, switch_time, tardiness_weight)
            schedule.extend(s)
            total_penalty += p
            # 更新全局机器状态，保证下一批正确衔接
            for m in machines_state:
                machines_state[m]["available_time"] = machines_copy[m]["available_time"]
                machines_state[m]["last_product"] = machines_copy[m]["last_product"]

        return schedule, total_penalty

    #选择算法执行
    machines_state_copy = deepcopy(machines_state)
    if algorithm == 'edd':
        schedule, total_penalty = edd_multi_machine(orders, machines_state_copy, switch_time, tardiness_weight)
    elif algorithm == 'greedy':
        schedule, total_penalty = greedy_multi_machine(orders, machines_state_copy, switch_time, tardiness_weight)
    elif algorithm == 'batch':
        schedule, total_penalty = batch_schedule(orders, machines_state_copy, switch_time, batch_size, tardiness_weight)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    #输出结果
    results = []
    for s in schedule:
        results.append({
            "订单编号": s["order_id"],
            "产品型号": s["product"],
            "工序": s["op_id"],
            "机器": s["machine"],
            "开始时间": s["start_time_dt"].strftime("%Y-%m-%d %H:%M"),
            "完成时间": s["finish_time_dt"].strftime("%Y-%m-%d %H:%M"),
            "延迟(小时)": round(s["tardiness"], 2),
            "延迟惩罚": round(s["penalty"], 2)
        })

    metrics = {
        "总延迟惩罚": round(total_penalty, 2),
        "平均延迟惩罚": round(total_penalty / len(orders), 2) if orders else 0
    }

    return results, metrics

# 兼容旧接口
def run_schedule(input_data=None, algorithm='edd'):
    return run_schedule_from_excel(input_data, algorithm=algorithm)

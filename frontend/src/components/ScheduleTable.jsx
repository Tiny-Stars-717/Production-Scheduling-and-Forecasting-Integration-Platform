import React from "react";

/**
 * 通用排产/预测/库存优化结果表格组件
 * @param {Array} data - 表格数据（数组形式）
 * @param {String} title - 表格标题（例如 "排产结果"）
 */
export default function ScheduleTable({ data = [], title = "排产结果" }) {
  if (!data || data.length === 0) {
    return (
      <div className="p-4 bg-gray-50 rounded-xl shadow-sm text-center text-gray-500">
        暂无数据，请先执行计算。
      </div>
    );
  }

  // 自动获取表头（Object.keys）
  const headers = Object.keys(data[0]);

  // 英文字段转中文映射
  const headerMap = {
    task: "任务",
    start: "开始时间",
    end: "结束时间",
    product: "产品型号",
    demand: "预测需求量",
    day: "日期",
    opt_stock: "优化库存",
    stock: "库存",
    status: "状态",
    machine: "生产线",
  };

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md mt-4">
      <h2 className="text-lg font-semibold text-gray-800 mb-3">
        {title}
      </h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300 rounded-lg">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              {headers.map((key, idx) => (
                <th
                  key={idx}
                  className="px-4 py-2 border border-gray-300 text-center"
                >
                  {headerMap[key] || key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr
                key={i}
                className={`${
                  i % 2 === 0 ? "bg-white" : "bg-gray-50"
                } hover:bg-blue-50 transition`}
              >
                {headers.map((key, j) => (
                  <td
                    key={j}
                    className="px-4 py-2 border border-gray-300 text-center text-sm text-gray-700"
                  >
                    {row[key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

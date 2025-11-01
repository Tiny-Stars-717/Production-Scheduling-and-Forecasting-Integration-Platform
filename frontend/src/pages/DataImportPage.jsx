import React, { useState, useEffect } from "react";
import { uploadExcel, readFilePath } from "../services/api";

export default function DataImportPage() {
  const [tableData, setTableData] = useState([]);
  const [filePath, setFilePath] = useState(localStorage.getItem("lastFilePath") || "");

  // 页面初始化：如果有上次文件路径，则自动读取数据
  useEffect(() => {
    if (filePath) {
      readFilePath(filePath)
        .then(res => {
          if (res.data.status === "success") {
            setTableData(res.data.data);
          } else {
            console.warn("读取文件失败:", res.data.msg);
          }
        })
        .catch(err => console.error("读取文件错误:", err));
    }
  }, [filePath]);

  // 文件选择后自动上传并显示
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const res = await uploadExcel(file);
      if (res.data.status === "success") {
        setTableData(res.data.data);
        localStorage.setItem("lastFilePath", file.name);
        setFilePath(file.name);
      } else {
        alert("文件读取失败: " + res.data.msg);
      }
    } catch (err) {
      console.error("文件上传出错:", err);
      alert("文件上传出错，请查看控制台");
    }
  };

  // 表格单元格修改后自动同步到后端
  const handleCellChange = async (rowIdx, key, value) => {
    const newData = [...tableData];
    newData[rowIdx][key] = value;
    setTableData(newData);

    try {
      // 自动同步整个表格数据到后端
      await uploadExcel(new Blob([JSON.stringify(newData)], { type: "application/json" }));
    } catch (err) {
      console.error("同步数据到后端失败:", err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>数据导入</h2>
      {/* 文件选择后自动读取 */}
      <input type="file" accept=".xlsx,.xls" onChange={handleFileChange} />

      {/* 表格显示 */}
      <table border="1" style={{ marginTop: "10px", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {tableData[0] && Object.keys(tableData[0]).map((key, idx) => (
              <th key={idx}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, rowIdx) => (
            <tr key={rowIdx}>
              {Object.keys(row).map((key, colIdx) => (
                <td key={colIdx}>
                  <input
                    value={row[key]}
                    onChange={(e) => handleCellChange(rowIdx, key, e.target.value)}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

import axios from 'axios';

const baseURL = 'http://localhost:5000/api';

// 数据导入
export const uploadExcel = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${baseURL}/order/upload`, formData);
};

export const readFilePath = (filepath) => {
    return axios.post(`${baseURL}/order/read`, { filepath });
};

export const getLastFilePath = () => {
    return axios.get(`${baseURL}/order/get_path`);
};

// 排产
export const runSchedule = (algorithm, inputData) => {
    return axios.post(`${baseURL}/schedule/run`, { algorithm, inputData })
        .then(res => {
            console.log("🖥 前端收到排产接口返回:", res.data);
            return res;
        });
};


// 生产预测
export const runForecast = (algorithm, inputData) => {
    return axios.post(`${baseURL}/forecast/run`, { algorithm, inputData });
};

// 库存优化
export const runStock = (algorithm, forecastData) => {
    return axios.post(`${baseURL}/stock/run`, { algorithm, forecastData });
};

// 历史查询
export const getHistory = (module) => {
    return axios.get(`${baseURL}/history/${module}`);
};

export const deleteHistory = (module, recordId) => {
    return axios.delete(`${baseURL}/history/${module}`, { data: { recordId } });
};

生产排产与生产预测集成平台
项目简介
本项目是一个学习性项目，旨在构建一个集成的生产排产与生产预测平台。平台的核心功能包括：
生产排产模块：根据订单需求和生产资源进行智能排产。
生产预测模块：通过时间序列分析技术进行生产需求预测。
预留库存优化接口：提供库存优化的扩展接口，方便在后续版本中集成更多优化算法。
该平台采用 Flask 作为后端框架，使用 SQLite 作为数据库，并通过 RESTful API 提供前后端数据交互。项目还涉及机器学习和优化算法的应用，如线性规划（LP）、粒子群优化（PSO）、ARIMA、Holt-Winters 等，具备一定的工业应用价值。
功能模块
1. 生产排产模块
生产排产模块用于根据订单信息进行排产调度，支持以下算法：
EDD（Earliest Due Date）：最早交货期优先调度。
贪心法：根据任务的优先级和资源进行贪心调度。
批量生产调度：根据批次大小对订单进行分组和调度。
2. 生产预测模块
生产预测模块基于历史数据进行生产需求预测，支持以下算法：
ARIMA（AutoRegressive Integrated Moving Average）：用于时间序列预测。
Holt-Winters：适用于季节性波动较大的时间序列数据。
3. 库存优化接口
该平台提供了预留的库存优化接口，用户可以在后续版本中集成不同的库存优化算法，如：
线性规划（LP）：用于库存管理的基本优化。
粒子群优化（PSO）：适用于更复杂的库存优化问题。
4. 数据可视化与历史记录模块
平台提供数据可视化功能，展示生产计划、预测结果以及历史记录，用户可以方便地查看和管理操作历史。需下载安装前端依赖，下载 node_modules。
技术栈
后端：Flask, SQLite
前端：React
机器学习：scikit-learn, statsmodels, pmdarima
优化算法：scipy, numpy
调度算法：自定义实现的调度算法
API文档：Flask-RESTful


Production Scheduling and Forecasting Integration Platform
Project Overview
This project is an educational project aimed at building an integrated platform for production scheduling and forecasting. The core features of the platform include:
Production Scheduling Module: Intelligent scheduling based on order requirements and production resources.
Production Forecasting Module: Forecasting production demands using time series analysis techniques.
Reserved Inventory Optimization Interface: Provides an extension interface for inventory optimization algorithms to be integrated in future versions.
The platform uses Flask for the backend, SQLite for the database, and RESTful APIs for frontend-backend communication. It also integrates machine learning and optimization algorithms such as Linear Programming (LP), Particle Swarm Optimization (PSO), ARIMA, and Holt-Winters, offering industrial application value.
Functional Modules
1. Production Scheduling Module
The production scheduling module schedules orders based on order information, supporting the following algorithms:
EDD (Earliest Due Date): Schedules based on the earliest delivery dates.
Greedy Algorithm: Schedules based on the priority and resources available.
Batch Production Scheduling: Groups orders into batches and schedules them accordingly.
2. Production Forecasting Module
The forecasting module predicts production demand based on historical data, supporting the following algorithms:
ARIMA (AutoRegressive Integrated Moving Average): A time series forecasting method suitable for data without significant seasonality or trend.
Holt-Winters (Exponential Smoothing): Used for time series data with significant seasonal fluctuations. It captures trend, seasonality, and residuals for forecasting.
3. Inventory Optimization Interface
The platform provides a reserved inventory optimization interface, allowing users to integrate different optimization algorithms in future releases, such as:
Linear Programming (LP): A basic inventory management optimization method.
Particle Swarm Optimization (PSO): Used for more complex inventory optimization problems.
4. Data Visualization and History Management
The platform provides data visualization features to display production plans, forecast results, and historical records. Users can easily view and manage operation histories.Install frontend dependencies, including node_modules：npm install
Tech Stack
Backend: Flask, SQLite
Frontend: React
Machine Learning: scikit-learn, statsmodels, pmdarima
Optimization Algorithms: scipy, numpy
Scheduling Algorithms: Custom scheduling algorithms
API Documentation: Flask-RESTful
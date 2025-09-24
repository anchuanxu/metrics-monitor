### 系统说明
这个简单的指标监控系统由以下几个部分组成：
- Web 服务器：使用 Flask 框架构建，提供 HTTP 服务
- 数据处理：使用 Pandas 读取和解析 CSV 文件中的指标数据
- 可视化：使用 Plotly 生成交互式折线图
- Web 界面：使用 Bootstrap 构建响应式网页，展示指标列表和图表
### 使用方法
1. 创建项目目录结构：
```
plaintext
metrics-monitor/
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── metric.html
└── metrics_data/  # 存放CSV文件的目录
```

2. 安装依赖：

```
bash
pip3 install -r requirements.txt
```

3. 将 CSV 文件放入metrics_data目录中

4. 运行应用：
```
bash
python app.py
```
5. 访问系统：打开浏览器，访问 http://服务器IP:5000 即可查看指标监控页面

### 系统功能
1. 自动发现metrics_data目录中的所有 CSV 文件
2. 解析 CSV 文件中的指标数据，按时间排序
3. 在主页显示所有可用的指标名称
4. 点击指标名称可查看该指标的历史趋势折线图
5. 图表支持交互：悬停查看具体数值、缩放、平移等操作
6. 系统会自动处理目录中所有的 CSV 文件，并将相同指标名称的数据整合到一起，生成时间序列的趋势图。如果需要在生产环境中使用，建议使用 Gunicorn 等 WSGI 服务器来运行应用，并适当调整配置以提高性能和安全性。

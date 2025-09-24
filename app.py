import os
import pandas as pd
import plotly.express as px
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
CSV_DIRECTORY = "metrics_data"  # CSV文件存放目录

def extract_time_from_filename(filename):
    """从文件名提取时间（针对result_20250923_203631.csv格式）"""
    try:
        parts = filename.replace(".csv", "").split("_")
        if len(parts) >= 3:
            date_part = parts[1]  # 20250923
            time_part = parts[2]  # 203631
            time_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except:
        pass
    return datetime.now()  # 所有方法失败时使用当前时间

def load_all_metrics():
    metrics = {}
    
    if not os.path.exists(CSV_DIRECTORY):
        print(f"错误：目录 {CSV_DIRECTORY} 不存在")
        return metrics
    
    for filename in os.listdir(CSV_DIRECTORY):
        if not filename.endswith(".csv"):
            continue
            
        file_path = os.path.join(CSV_DIRECTORY, filename)
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 验证CSV格式是否正确
            if "指标名称" not in df.columns or "数值" not in df.columns:
                print(f"{filename} 缺少必要的列（指标名称或数值）")
                continue
            
            # 提取统计时间（第二行数据）
            timestamp = None
            if len(df) >= 1 and df.iloc[0]["指标名称"] == "统计时间":
                try:
                    time_str = df.iloc[0]["数值"]
                    timestamp = pd.to_datetime(time_str)
                except:
                    print(f"{filename} 中的统计时间格式错误，尝试从文件名提取")
                    timestamp = extract_time_from_filename(filename)
            else:
                print(f"{filename} 未找到统计时间，从文件名提取")
                timestamp = extract_time_from_filename(filename)
            
            # 处理指标数据（从第三行开始，即索引1及以后）
            for idx in range(1, len(df)):
                row = df.iloc[idx]
                metric_name = str(row["指标名称"]).strip()
                metric_value = row["数值"]
                
                # 转换数值为数字类型
                try:
                    metric_value = float(metric_value)
                except:
                    print(f"{filename} 中 {metric_name} 的数值 {metric_value} 不是有效数字，已跳过")
                    continue
                
                # 初始化指标列表
                if metric_name not in metrics:
                    metrics[metric_name] = []
                
                # 添加数据点
                metrics[metric_name].append({
                    "value": metric_value,
                    "time": timestamp
                })
                
        except Exception as e:
            print(f"处理 {filename} 时出错：{str(e)}")
            continue
    
    # 按时间排序所有指标数据
    for name in metrics:
        metrics[name].sort(key=lambda x: x["time"])
    
    return metrics

@app.route("/")
def index():
    metrics = load_all_metrics()
    return render_template("index.html", metrics=metrics.keys())

@app.route("/metric/<name>")
def show_metric(name):
    metrics = load_all_metrics()
    if name not in metrics:
        return f"指标 {name} 不存在", 404
    
    # 准备图表数据
    data = metrics[name]
    times = [entry["time"] for entry in data]
    values = [entry["value"] for entry in data]
    
    # 创建折线图
    fig = px.line(
        x=times, 
        y=values, 
        title=f"{name} 趋势变化",
        labels={"x": "时间", "y": "数值"},
        markers=True
    )
    # 美化图表
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#e0e0e0"),
        yaxis=dict(showgrid=True, gridcolor="#e0e0e0"),
        title=dict(font=dict(size=20)),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    graph_html = fig.to_html(full_html=False)
    
    return render_template("metric.html", name=name, graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
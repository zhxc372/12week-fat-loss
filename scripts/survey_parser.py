#!/usr/bin/env python3
"""
12周减脂计划 - 问卷回复解析与数据保存
用法: python3 survey_parser.py "回复的原始文本"
功能: 解析17个字段 → 保存到 data/daily/YYYY-MM-DD.md → 计算趋势 → git commit

返回JSON格式，供AI后续生成方案时使用
"""

import sys
import json
import os
import re
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "daily")
DAILY_DIR = DATA_DIR

FIELDS = [
    ("weight", "体重", "kg"),
    ("avg7", "7日平均", "kg"),
    ("waist", "腰围", "cm"),
    ("sleep", "睡眠质量", ""),
    ("bowel", "排便情况", ""),
    ("night_eat", "夜间进食", ""),
    ("mood", "整体状态", "/10"),
    ("anxiety", "焦虑评分", "/10"),
    ("protein_control", "蛋白范围控制", ""),
    ("binge", "暴食", ""),
    ("training", "训练", ""),
    ("problem", "最大问题", ""),
    ("improve", "改进策略", ""),
    ("gym", "健身房", ""),
    ("swim", "游泳", ""),
    ("dining_out", "外食", ""),
    ("job_task", "求职任务", ""),
]

def parse_reply(text):
    """解析用户的逐行回复"""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    
    # 过滤掉序号前缀（如 "1. 127.8"）
    cleaned = []
    for line in lines:
        # 去掉 "数字." 前缀
        m = re.match(r'^\d+[\.\、\)]\s*(.*)', line)
        if m:
            cleaned.append(m.group(1).strip())
        else:
            cleaned.append(line)
    
    result = {}
    for i, (key, label, unit) in enumerate(FIELDS):
        result[key] = cleaned[i] if i < len(cleaned) else "未填写"
    
    return result

def calc_week_num(start_date, current_date):
    """计算第几周第几天（从start_date算起）"""
    delta = (current_date - start_date).days
    week = delta // 7 + 1
    day = delta % 7 + 1
    return week, day

def get_weight_trend(data_dir, today):
    """读取最近7天数据，计算体重趋势"""
    weights = []
    today_obj = datetime.date.fromisoformat(today)
    
    for i in range(1, 8):
        d = today_obj - datetime.timedelta(days=i)
        filepath = os.path.join(data_dir, f"{d.isoformat()}.md")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            # 提取体重
            m = re.search(r'体重[：:]\s*([\d.]+)\s*kg', content)
            if m:
                weights.append((d.isoformat(), float(m.group(1))))
    
    # 7日平均
    if weights:
        avg7 = sum(w for _, w in weights) / len(weights)
        # 趋势
        if len(weights) >= 2:
            change = weights[-1][1] - weights[0][1]
            trend = "下降" if change < -0.3 else ("上升" if change > 0.3 else "持平")
        else:
            change = 0
            trend = "数据不足"
    else:
        avg7 = None
        change = 0
        trend = "无历史数据"
    
    return {
        "history": weights,
        "avg7": round(avg7, 1) if avg7 else None,
        "change": round(change, 1),
        "trend": trend,
    }

def save_data(data, today_str):
    """保存到 data/daily/YYYY-MM-DD.md"""
    os.makedirs(DAILY_DIR, exist_ok=True)
    
    # 计算周数（默认起始日期2026-05-08，第1天）
    try:
        start = datetime.date(2026, 5, 8)
        today_obj = datetime.date.fromisoformat(today_str)
        week, day = calc_week_num(start, today_obj)
    except:
        week, day = "?", "?"
    
    filepath = os.path.join(DAILY_DIR, f"{today_str}.md")
    
    # 如果文件已存在（已有AI方案），只更新数据部分
    md = f"""# {today_str} | W{week}D{day}

## 上报数据

### 身体数据
- 体重：{data['weight']} kg
- 7日平均：{data['avg7']} kg
- 腰围：{data['waist']}

### 昨日回顾
- 睡眠质量：{data['sleep']}
- 排便：{data['bowel']}
- 夜间进食：{data['night_eat']}
- 整体状态：{data['mood']}/10
- 焦虑：{data['anxiety']}/10
- 蛋白范围控制：{data['protein_control']}
- 暴食：{data['binge']}
- 训练：{data['training']}
- 最大问题：{data['problem']}
- 改进策略：{data['improve']}

### 今日条件
- 健身房：{data['gym']}
- 游泳：{data['swim']}
- 外食：{data['dining_out']}
- 求职任务：{data['job_task']}

## AI当日方案

_待AI生成_
"""
    
    with open(filepath, "w") as f:
        f.write(md)
    
    return filepath

def git_commit(filepath, today_str):
    """自动git commit"""
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=BASE_DIR, capture_output=True, timeout=10
        )
        subprocess.run(
            ["git", "commit", "-m", f"data: {today_str} daily checkin"],
            cwd=BASE_DIR, capture_output=True, timeout=10
        )
        subprocess.run(
            ["git", "push"],
            cwd=BASE_DIR, capture_output=True, timeout=30
        )
        return True
    except Exception as e:
        return f"git error: {e}"

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 survey_parser.py '回复文本'"}, ensure_ascii=False))
        sys.exit(1)
    
    reply_text = sys.argv[1]
    today = datetime.date.today().isoformat()
    
    # 解析
    data = parse_reply(reply_text)
    
    # 体重趋势
    trend = get_weight_trend(DAILY_DIR, today)
    data["trend"] = trend
    
    # 保存
    filepath = save_data(data, today)
    
    # git
    git_result = git_commit(filepath, today)
    
    # 输出JSON供AI使用
    output = {
        "date": today,
        "data": data,
        "saved_to": filepath,
        "git": "ok" if git_result is True else str(git_result),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

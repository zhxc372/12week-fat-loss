#!/usr/bin/env python3
"""
12周减脂计划 - 数据导出为JSON供仪表盘使用
用法: python3 data_export.py
输出: web/data.json（供index.html加载）
"""

import os
import json
import re
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DIR = os.path.join(BASE_DIR, "data", "daily")
WEB_DIR = os.path.join(BASE_DIR, "web")
START_DATE = datetime.date(2026, 5, 8)
END_DATE = START_DATE + datetime.timedelta(weeks=12)

def read_daily(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        content = f.read()
    
    result = {"date": os.path.basename(filepath).replace(".md", "")}
    
    fields = {
        "weight": r'体重[：:]\s*([\d.]+)\s*kg',
        "avg7": r'7日平均[：:]\s*([\d.]+)\s*kg',
        "waist": r'腰围[：:]\s*(\S+)',
        "sleep": r'睡眠质量[：:]\s*(\S+)',
        "bowel": r'排便[：:]\s*(\S+)',
        "night_eat": r'夜间进食[：:]\s*(\S+)',
        "mood": r'整体状态[：:]\s*([\d.]+)',
        "anxiety": r'焦虑[：:]\s*([\d.]+)',
        "protein_control": r'蛋白范围控制[：:]\s*(\S+)',
        "binge": r'暴食[：:]\s*(\S+)',
        "training": r'训练[：:]\s*(\S+)',
        "problem": r'最大问题[：:]\s*(.+)',
        "gym": r'健身房[：:]\s*(\S+)',
        "swim": r'游泳[：:]\s*(\S+)',
    }
    
    for key, pattern in fields.items():
        m = re.search(pattern, content)
        if m:
            val = m.group(1).strip()
            result[key] = float(val) if key in ("weight", "avg7", "mood", "anxiety") else val
    
    return result

def main():
    # 收集所有daily数据
    records = []
    if os.path.exists(DAILY_DIR):
        files = sorted([f for f in os.listdir(DAILY_DIR) if f.endswith(".md") and f != "template.md"])
        for f in files:
            data = read_daily(os.path.join(DAILY_DIR, f))
            if data:
                records.append(data)
    
    # 计算当前周
    today = datetime.date.today()
    week = max(1, (today - START_DATE).days // 7 + 1)
    
    output = {
        "startDate": START_DATE.isoformat(),
        "endDate": END_DATE.isoformat(),
        "currentWeek": week,
        "totalDays": (END_DATE - START_DATE).days,
        "records": records,
        "profile": {
            "targetWeight": 100,
        }
    }
    
    os.makedirs(WEB_DIR, exist_ok=True)
    
    # 写入JSON
    json_path = os.path.join(WEB_DIR, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 注入到HTML（替换placeholder）
    html_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        # 内联JSON到HTML
        json_str = json.dumps(output, ensure_ascii=False)
        html = html.replace("__DATA_PLACEHOLDER__", json_str)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
    
    print(json.dumps({
        "records": len(records),
        "json": json_path,
        "html": html_path,
        "week": week
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
12周减脂计划 - 周复盘数据汇总
用法: python3 weekly_summary.py [week_number]
功能: 读取本周data/daily/数据 → 生成汇总骨架 → 保存到data/weekly/W{N}.md

AI只需要在骨架基础上补充分析和下周建议
"""

import sys
import os
import re
import datetime
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DIR = os.path.join(BASE_DIR, "data", "daily")
WEEKLY_DIR = os.path.join(BASE_DIR, "data", "weekly")
START_DATE = datetime.date(2026, 5, 8)

def get_week_dates(week_num):
    """获取第N周的日期范围"""
    start = START_DATE + datetime.timedelta(weeks=week_num - 1)
    dates = [start + datetime.timedelta(days=d) for d in range(7)]
    return dates

def read_daily(filepath):
    """读取单日数据"""
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, "r") as f:
        content = f.read()
    
    result = {}
    
    # 提取体重
    m = re.search(r'体重[：:]\s*([\d.]+)\s*kg', content)
    if m:
        result["weight"] = float(m.group(1))
    
    m = re.search(r'腰围[：:]\s*(\S+)', content)
    if m:
        result["waist"] = m.group(1)
    
    m = re.search(r'睡眠质量[：:]\s*(\S+)', content)
    if m:
        result["sleep"] = m.group(1)
    
    m = re.search(r'整体状态[：:]\s*([\d.]+)', content)
    if m:
        result["mood"] = float(m.group(1))
    
    m = re.search(r'焦虑[：:]\s*([\d.]+)', content)
    if m:
        result["anxiety"] = float(m.group(1))
    
    m = re.search(r'暴食[：:]\s*(\S+)', content)
    if m:
        result["binge"] = m.group(1)
    
    m = re.search(r'训练[：:]\s*(\S+)', content)
    if m:
        result["training"] = m.group(1)
    
    m = re.search(r'外食[：:]\s*(\S+)', content)
    if m:
        result["dining_out"] = m.group(1)
    
    m = re.search(r'排便[：:]\s*(\S+)', content)
    if m:
        result["bowel"] = m.group(1)
    
    return result

def generate_weekly(week_num):
    """生成周复盘骨架"""
    dates = get_week_dates(week_num)
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    records = []
    weights = []
    moods = []
    anxieties = []
    training_days = 0
    binge_count = 0
    dining_out_count = 0
    sleep_good = 0
    
    for i, d in enumerate(dates):
        filepath = os.path.join(DAILY_DIR, f"{d.isoformat()}.md")
        data = read_daily(filepath)
        
        if data:
            records.append({"date": d.isoformat(), "day": day_names[i], **data})
            if "weight" in data:
                weights.append(data["weight"])
            if "mood" in data:
                moods.append(data["mood"])
            if "anxiety" in data:
                anxieties.append(data["anxiety"])
            if data.get("training") == "完成":
                training_days += 1
            if data.get("binge") == "是":
                binge_count += 1
            if data.get("dining_out") == "有":
                dining_out_count += 1
            if data.get("sleep") in ("好",):
                sleep_good += 1
        else:
            records.append({"date": d.isoformat(), "day": day_names[i], "note": "未打卡"})
    
    # 计算统计
    weight_first = weights[0] if weights else None
    weight_last = weights[-1] if weights else None
    weight_change = round(weight_last - weight_first, 1) if (weight_first and weight_last) else None
    weight_avg = round(sum(weights) / len(weights), 1) if weights else None
    
    avg_mood = round(sum(moods) / len(moods), 1) if moods else None
    avg_anxiety = round(sum(anxieties) / len(anxieties), 1) if anxieties else None
    
    # 生成骨架
    lines = [
        f"# W{week_num:02d} 周复盘",
        f"",
        f"## 本周数据汇总",
        f"",
        f"### 体重",
    ]
    
    for r in records:
        w = r.get("weight", "—")
        lines.append(f"- {r['day']}（{r['date']}）：{w} kg" if isinstance(w, (int, float)) else f"- {r['day']}（{r['date']}）：{r.get('note', '未记录')}")
    
    lines.extend([
        f"",
        f"### 统计",
        f"- 打卡天数：{len([r for r in records if 'weight' in r])}/7",
        f"- 周初体重：{weight_first or '—'} kg",
        f"- 周末体重：{weight_last or '—'} kg",
        f"- 本周变化：{f'{weight_change} kg' if weight_change is not None else '—'}",
        f"- 周平均体重：{weight_avg or '—'} kg",
        f"- 训练完成天数：{training_days}/7",
        f"- 暴食次数：{binge_count}",
        f"- 外食次数：{dining_out_count}",
        f"- 睡眠质量好：{sleep_good}天",
        f"- 平均精神状态：{avg_mood or '—'}/10",
        f"- 平均焦虑：{avg_anxiety or '—'}/10",
        f"",
        f"## AI分析",
        f"",
        f"_待AI补充：_",
        f"",
        f"1. 本周是否合格：",
        f"2. 体重变化评价：",
        f"3. 饮食最大问题：",
        f"4. 训练最大问题：",
        f"5. 下周热量目标：",
        f"6. 下周蛋白/碳水/脂肪目标：",
        f"7. 下周训练安排：",
        f"8. 下周采购清单：",
        f"9. 下周求职任务：",
        f"10. 最重要纠偏动作：",
    ])
    
    return "\n".join(lines), {
        "week": week_num,
        "checkins": len([r for r in records if 'weight' in r]),
        "weight_first": weight_first,
        "weight_last": weight_last,
        "weight_change": weight_change,
        "weight_avg": weight_avg,
        "training_days": training_days,
        "binge_count": binge_count,
        "avg_mood": avg_mood,
        "avg_anxiety": avg_anxiety,
    }

def main():
    week_num = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if not week_num:
        # 自动计算当前周
        today = datetime.date.today()
        delta = (today - START_DATE).days
        week_num = delta // 7 + 1
    
    os.makedirs(WEEKLY_DIR, exist_ok=True)
    
    content, stats = generate_weekly(week_num)
    
    filepath = os.path.join(WEEKLY_DIR, f"W{week_num:02d}.md")
    with open(filepath, "w") as f:
        f.write(content)
    
    # git
    try:
        subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "-m", f"data: W{week_num:02d} weekly summary"], cwd=BASE_DIR, capture_output=True, timeout=10)
        subprocess.run(["git", "push"], cwd=BASE_DIR, capture_output=True, timeout=30)
    except:
        pass
    
    print(json.dumps({"filepath": filepath, "stats": stats}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

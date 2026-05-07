# 12周减脂 - AI工作流规范

> ⚠️ 严格遵守本规范，防止浪费token

---

## 文件读取规则

### ✅ 每次生成方案时读取（共3个文件，约4KB）

| 文件 | 大小 | 内容 |
|------|------|------|
| `docs/diet-rules.md` | ~1.6KB | 饮食目标、食材库、四套菜单、外食规则、防崩指南 |
| `docs/training-system.md` | ~1.4KB | 训练安排、力量A/B（健身房+居家）、禁止动作 |
| `docs/safety-and-cortisol.md` | ~1KB | 状态判断、六条硬规则、安全红线、纠偏规则 |

### ✅ 按需读取（有就读，没有跳过）

| 文件 | 何时读 |
|------|--------|
| `data/daily/YYYY-MM-DD.md`（最近1-2天） | 了解前一天数据 |
| `data/weekly/W{N}.md`（上一周） | 了解上周情况 |
| `data/profile/base.md` | 首次或用户信息有变化时 |

### ❌ 禁止读取（太长，浪费token）

| 文件 | 原因 |
|------|------|
| `docs/plan-full.txt` | 980行原文，已提取到速查版 |
| `docs/cortisol-and-cardio-guide.md` | 已提取到安全速查版 |
| `docs/12周减脂饮食训练执行手册.pdf` | PDF不能直接读 |

---

## 每日工作流（收到问卷回复时）

### Step 1: 调用Python脚本解析保存
```bash
python3 ~/projects/12week-fat-loss/scripts/survey_parser.py '用户的回复文本'
```
脚本会返回JSON：日期、17个字段解析结果、体重趋势、保存路径。

### Step 2: 读取3个速查文件
读取 `diet-rules.md` + `training-system.md` + `safety-and-cortisol.md`。

### Step 3: 生成当日方案
根据解析数据 + 速查规则 + 趋势，生成：

**📋 风险判断**
🟢/🟡/🔴 + 具体原因

**🍽️ 饮食方案**
- 热量/蛋白/碳水/脂肪目标
- 从四套菜单中选一套，根据昨日情况调整
- 如果昨日吃多→轻量修正；昨日吃少→补蛋白碳水

**💪 训练方案**
- 根据健身房/游泳条件选健身房版或居家版
- 根据状态选绿/黄/红级别
- 明确有氧内容+时长+力量动作

**💼 求职任务**
- 具体90-120分钟任务

**⚠️ 纠偏**
- 针对昨日问题给调整

**📌 明日提醒**
- 准备什么食物、训练方向

### Step 4: 更新数据文件
将AI方案追加到 `data/daily/YYYY-MM-DD.md` 的"AI当日方案"部分。

### Step 5: Git提交
```bash
cd ~/projects/12week-fat-loss && git add -A && git commit -m "plan: YYYY-MM-DD daily plan" && git push
```

---

## 周复盘工作流

### 触发条件
- 每周日收到数据后自动触发
- 或用户主动要求

### Step 1: 调用Python脚本汇总
```bash
python3 ~/projects/12week-fat-loss/scripts/weekly_summary.py
```
自动读取本周所有daily数据，生成骨架到 `data/weekly/W{N}.md`。

### Step 2: 读取3个速查文件（同上）

### Step 3: 补充分析
在骨架基础上填写10项分析内容：
1. 本周是否合格
2. 体重变化评价
3. 饮食最大问题
4. 训练最大问题
5-10. 下周目标和计划

### Step 4: Git提交

---

## 月度总结工作流

每月第4周复盘完成后触发。读取本月4个W{N}.md，生成 `data/monthly/M{N}.md`。

## 12周最终复盘

第12周复盘完成后，读取所有周复盘 + 月度总结，生成最终报告。

---

## 安全第一

任何时候用户数据中出现以下信号，**优先提醒就医**，不在方案中安排训练：
- 呕吐、腹泻
- 酮体阳性
- 胸痛、晕厥、严重气短
- 明显脱水
- 持续腹痛

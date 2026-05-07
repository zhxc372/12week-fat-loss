# 12周减脂计划

张小厨的12周强执行减脂项目。

## 计划文档

- [12周执行手册（完整版）](docs/plan-full.txt) — 饮食、训练、外食规则、采购清单、风险红线
- [皮质醇与有氧优化指南](docs/cortisol-and-cardio-guide.md) — 有氧强度分层、训练调整规则、六条硬规则

## 打卡模板

复制对应模板，填好数据发给AI即可获得当日方案。

| 模板 | 用途 | 频率 |
|------|------|------|
| [每日打卡](checkin-templates/每日打卡.md) | 标准每日数据上报 + 获取当日方案 | 每天 |
| [快速日报](checkin-templates/快速日报.md) | 简版上报，快速获取调整 | 时间紧时 |
| [完整日报](checkin-templates/完整日报.md) | 含所有项目的完整上报 | 需要详细方案时 |
| [每周复盘](checkin-templates/每周复盘.md) | 本周数据复盘 + 下周计划 | 每周日 |
| [医生上下文](checkin-templates/医生上下文.md) | 医疗安全上下文（首次使用时填写） | 一次性 |

## 数据记录

AI会自动保存每日上报数据，用于每日复盘、每周复盘、月度总结和最终复盘。

- `data/daily/` — 每日数据
- `data/weekly/` — 周复盘
- `data/monthly/` — 月度总结
- `data/profile/` — 基础信息

## 项目结构

```
12week-fat-loss/
├── docs/                    # 计划文档
│   ├── plan-full.txt        # 12周执行手册
│   └── cortisol-and-cardio-guide.md
├── checkin-templates/       # 打卡模板（复制填好发给AI）
├── data/                    # 数据记录（AI自动维护）
└── README.md
```

## 安全底线

- 不生酮、不断食、不脱水
- 每日碳水 ≥ 100g
- 不自行调整处方药
- 出现呕吐/腹泻/酮体阳性/胸痛/晕厥/严重气短 → 立即就医

"""
河东区城建谋划项目精准谋划分析
生成时间: 2026-03-12
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# 读取项目数据
df = pd.read_excel('真实项目2/河东区城建谋划项目分类汇总0226.xlsx')

# 分析结果
analysis_result = {
    "分析时间": datetime.now().isoformat(),
    "项目总数": len(df),
    "总投资": {
        "总计(万元)": df['总投资(万元)'].sum(),
        "拟申请政策资金(万元)": df['拟申请政策资金(万元)'].sum()
    },
    "项目分类统计": df['项目分类'].value_counts().to_dict(),
    "资金领域统计": df['申报资金领域'].value_counts().to_dict(),
    "项目阶段统计": df['项目阶段'].value_counts().to_dict(),
    "重点项目识别": [],
    "资金匹配建议": [],
    "风险提示": []
}

# 识别重点项目（投资额大、政策资金占比高）
for idx, row in df.iterrows():
    total = row['总投资(万元)']
    policy = row['拟申请政策资金(万元)']
    if pd.notna(total) and pd.notna(policy) and total > 0:
        ratio = policy / total
        if total >= 10000 or ratio >= 0.7:
            analysis_result["重点项目识别"].append({
                "项目名称": row['项目名称'],
                "总投资(万元)": total,
                "政策资金(万元)": policy,
                "资金占比": f"{ratio:.1%}",
                "申报领域": row['申报资金领域']
            })

# 资金匹配建议
funding_suggestions = {
    "中央预算内投资-城市更新": {
        "适用项目": "城市更新类项目",
        "申报要点": "需符合城市更新示范工作要求，重点支持老旧小区改造、基础设施提升",
        "资金比例": "一般不超过总投资的70%"
    },
    "超长期特别国债-城市地下管网": {
        "适用项目": "地下管网改造项目",
        "申报要点": "需纳入城市地下管网改造规划，重点支持雨污分流、老旧管网更新",
        "资金比例": "一般不超过总投资的60%"
    },
    "超长期特别国债-住宅老旧电梯更新": {
        "适用项目": "老旧电梯更新改造",
        "申报要点": "电梯使用年限超过15年，需提供安全评估报告",
        "资金比例": "一般不超过总投资的55%"
    }
}

analysis_result["资金匹配建议"] = funding_suggestions

# 风险提示
risks = []
for idx, row in df.iterrows():
    if row['项目代码'] == '暂无':
        risks.append(f"项目 '{row['项目名称'][:20]}...' 缺少项目代码，影响立项审批")
    
    total = row['总投资(万元)']
    policy = row['拟申请政策资金(万元)']
    if pd.notna(total) and pd.notna(policy) and total > 0:
        ratio = policy / total
        if ratio > 0.7:
            risks.append(f"项目 '{row['项目名称'][:20]}...' 政策资金占比{ratio:.0%}过高，需配套资金保障")

analysis_result["风险提示"] = risks

# 保存分析结果
output_dir = Path("outputs/河东区城建谋划项目分析")
output_dir.mkdir(parents=True, exist_ok=True)

with open(output_dir / "分析结果.json", 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)

print(json.dumps(analysis_result, ensure_ascii=False, indent=2))

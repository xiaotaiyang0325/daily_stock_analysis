#!/usr/bin/env python3
"""
股票分析报告汇总脚本
每天 14:30 检查 GitHub 仓库的最新报告，汇总成大白话发给王大博儿
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
REPO_PATH = "/Users/wangdabo/projects/daily_stock_analysis"
STOCK_NAMES = {
    "000034": "神州数码",
    "000977": "浪潮信息", 
    "002261": "拓维信息",
    "688808": "联讯仪器",
    "688041": "海光信息",
    "688256": "寒武纪",
    "603019": "中科曙光"
}

def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or REPO_PATH,
            capture_output=True, 
            text=True,
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(f"命令执行失败: {cmd}, 错误: {e}")
        return None

def get_latest_report():
    """获取最新的报告文件"""
    reports_dir = Path(REPO_PATH) / "reports"
    if not reports_dir.exists():
        return None
    
    # 查找今天的报告
    today = datetime.now().strftime("%Y%m%d")
    report_files = list(reports_dir.glob(f"*{today}*.md"))
    
    if not report_files:
        # 查找最新的报告
        report_files = sorted(reports_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    return report_files[0] if report_files else None

def read_report(report_path):
    """读取报告内容"""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取报告失败: {e}")
        return None

def summarize_report(report_content):
    """将报告汇总成大白话"""
    if not report_content:
        return "今天没有生成报告，可能是非交易日。"
    
    # 这里我会根据实际报告内容来写汇总逻辑
    # 暂时返回一个示例格式
    summary = """📊 今日股票分析汇总

【一句话结论】
今天整体市场情况...

【个股简况】
• 神州数码(000034): ...
• 浪潮信息(000977): ...
• 拓维信息(002261): ...
• 联讯仪器(688808): ...
• 海光信息(688041): ...
• 寒武纪(688256): ...
• 中科曙光(603019): ...

【关键信号】
• 哪只涨停了？
• 哪只资金流入最多？

【操作建议】
基于你的模拟盘，建议...

---
详细报告已保存到仓库，可随时查看。
"""
    return summary

def send_to_user(message):
    """发送消息给王大博儿"""
    # 这里我会调用 send_message 工具
    print(f"[发送给用户]\n{message}")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("📊 股票分析报告汇总")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 拉取最新代码
    print("\n1️⃣ 拉取最新报告...")
    result = run_command("git pull origin main")
    if result:
        print(f"✅ 已更新: {result}")
    else:
        print("⚠️ 拉取失败，使用本地报告")
    
    # 2. 获取最新报告
    print("\n2️⃣ 查找最新报告...")
    latest_report = get_latest_report()
    if not latest_report:
        print("❌ 没有找到报告")
        send_to_user("今天没有生成股票分析报告，可能是非交易日或分析任务未运行。")
        return
    
    print(f"✅ 找到报告: {latest_report.name}")
    
    # 3. 读取报告内容
    print("\n3️⃣ 读取报告内容...")
    report_content = read_report(latest_report)
    if not report_content:
        print("❌ 读取报告失败")
        return
    
    print(f"✅ 报告长度: {len(report_content)} 字符")
    
    # 4. 汇总成大白话
    print("\n4️⃣ 生成大白话汇总...")
    summary = summarize_report(report_content)
    
    # 5. 发送给用户
    print("\n5️⃣ 发送给王大博儿...")
    if send_to_user(summary):
        print("✅ 发送成功")
    else:
        print("❌ 发送失败")
    
    print("\n" + "=" * 50)
    print("✨ 完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()

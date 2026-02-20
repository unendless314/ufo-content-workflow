#!/usr/bin/env python3
"""
UFO Content Workflow - Todo List Generator
生成選題待辦清單，方便 AI 與人類查看工作狀態

Usage:
    python scripts/todo.py [command] [options]

Commands:
    list [status]     - 列出選題（可指定狀態: todo, researching, drafted, published）
    next              - 顯示下一個建議執行的選題（優先級 + 狀態）
    stats             - 顯示統計資訊
    research          - 列出需要進行研究的選題
    draft             - 列出需要撰寫草稿的選題
    overdue           - 列出逾期未完成的選題
"""

import yaml
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 設定檔案路徑（scripts/todo.py -> 專案根目錄）
TOPICS_FILE = Path(__file__).parent.parent / "topics.yaml"


def load_topics() -> dict:
    """載入 topics.yaml"""
    with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_priority_weight(priority: str) -> int:
    """將優先級轉換為排序權重（數字越小越優先）"""
    weights = {'p0': 0, 'p1': 1, 'p2': 2}
    return weights.get(priority, 99)


def format_topic_line(topic: dict, show_status: bool = True) -> str:
    """格式化單個選題為一行摘要"""
    id_ = topic['id']
    title = topic['title'][:35] + '...' if len(topic['title']) > 35 else topic['title']
    priority = topic['priority'].upper()
    status = topic['status']
    
    # 狀態圖示
    icons = {
        'todo': '⬜',
        'researching': '🔍',
        'drafted': '📝',
        'published': '✅',
        'archived': '📦'
    }
    icon = icons.get(status, '⬜')
    
    if show_status:
        return f"{icon} [{id_}] [{priority}] {title} ({status})"
    return f"[{id_}] [{priority}] {title}"


def cmd_list(args: list):
    """列出選題清單"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 過濾條件
    filter_status = args[0] if args else None
    filter_priority = None
    
    # 解析參數（如: --priority=p0）
    for arg in args:
        if arg.startswith('--priority='):
            filter_priority = arg.split('=')[1]
    
    # 過濾與排序
    filtered = topics
    if filter_status:
        filtered = [t for t in filtered if t['status'] == filter_status]
    if filter_priority:
        filtered = [t for t in filtered if t['priority'] == filter_priority]
    
    # 按優先級、狀態排序
    filtered.sort(key=lambda x: (get_priority_weight(x['priority']), x['id']))
    
    if not filtered:
        print("📭 沒有符合條件的選題")
        return
    
    # 分組顯示
    current_priority = None
    for topic in filtered:
        if topic['priority'] != current_priority:
            current_priority = topic['priority']
            priority_name = {'p0': '🚨 P0 - 立即執行', 'p1': '🔥 P1 - 高優先', 'p2': '📌 P2 - 待規劃'}.get(current_priority, current_priority)
            print(f"\n{priority_name}")
            print("-" * 60)
        
        print(format_topic_line(topic))
    
    print(f"\n共 {len(filtered)} 個選題")


def cmd_next(args: list):
    """顯示下一個建議執行的選題"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 尋找第一個可執行的選題
    # 排序：P0 > P1 > P2，todo > researching > drafted
    status_order = {'todo': 0, 'researching': 1, 'drafted': 2, 'published': 3, 'archived': 4}
    
    candidates = [t for t in topics if t['status'] not in ['published', 'archived']]
    candidates.sort(key=lambda x: (get_priority_weight(x['priority']), status_order.get(x['status'], 99)))
    
    if not candidates:
        print("🎉 所有選題都已完成或發布！")
        return
    
    topic = candidates[0]
    
    print("=" * 60)
    print(f"🎯 下一個建議執行：{topic['id'].upper()}")
    print("=" * 60)
    print(f"\n標題：{topic['title']}")
    print(f"優先級：{topic['priority'].upper()}")
    print(f"狀態：{topic['status']}")
    print(f"類型：{topic['type']}")
    print(f"平台：{', '.join(topic['platforms']) if topic['platforms'] else '未定'}")
    print(f"\n研究問題：")
    for i, q in enumerate(topic.get('research_questions', []), 1):
        print(f"  {i}. {q}")
    print(f"\n備註：{topic.get('notes', '無')}")
    
    # 建議動作
    print("\n" + "-" * 60)
    if topic['status'] == 'todo' and not topic.get('research_completed'):
        print("💡 建議動作：使用 Deep Research Skill 生成研究提示詞")
    elif topic['status'] == 'researching':
        print("💡 建議動作：完成研究報告後，更新 research_completed: true")
    elif topic['status'] == 'drafted':
        print("💡 建議動作：製作資產（縮圖、字幕），準備發布")


def cmd_stats(args: list):
    """顯示統計資訊"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 各狀態數量
    status_counts = {}
    priority_counts = {}
    type_counts = {}
    
    for t in topics:
        status_counts[t['status']] = status_counts.get(t['status'], 0) + 1
        priority_counts[t['priority']] = priority_counts.get(t['priority'], 0) + 1
        type_counts[t['type']] = type_counts.get(t['type'], 0) + 1
    
    print("=" * 60)
    print("📊 選題統計總覽")
    print("=" * 60)
    
    print(f"\n總選題數：{len(topics)}")
    
    print("\n【依狀態】")
    status_names = {
        'todo': '⬜ 待開始',
        'researching': '🔍 研究中',
        'drafted': '📝 草稿完成',
        'published': '✅ 已發布',
        'archived': '📦 已封存',
        'completed': '✨ 已完成'
    }
    for status, name in status_names.items():
        count = status_counts.get(status, 0)
        if count > 0:
            bar = '█' * count
            print(f"  {name}: {bar} ({count})")
    
    print("\n【依優先級】")
    for p in ['p0', 'p1', 'p2']:
        count = priority_counts.get(p, 0)
        name = {'p0': '🚨 P0', 'p1': '🔥 P1', 'p2': '📌 P2'}[p]
        print(f"  {name}: {count} 個選題")
    
    print("\n【依類型】")
    for type_name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {type_name}: {count}")


def cmd_research(args: list):
    """列出需要進行研究的選題"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 需要研究的：todo 且 research_completed 為 false
    need_research = [
        t for t in topics 
        if t['status'] in ['todo', 'researching'] and not t.get('research_completed', False)
    ]
    need_research.sort(key=lambda x: get_priority_weight(x['priority']))
    
    if not need_research:
        print("🔬 所有進行中的選題都已完成研究階段")
        return
    
    print("=" * 60)
    print("🔬 需要進行研究的選題")
    print("=" * 60)
    
    for topic in need_research:
        print(f"\n[{topic['id']}] [{topic['priority'].upper()}] {topic['title']}")
        print(f"狀態：{topic['status']}")
        print("研究問題：")
        for i, q in enumerate(topic.get('research_questions', [])[:3], 1):
            # 截斷過長的問題
            display_q = q[:60] + '...' if len(q) > 60 else q
            print(f"  {i}. {display_q}")
        if len(topic.get('research_questions', [])) > 3:
            print(f"  ... 還有 {len(topic['research_questions']) - 3} 個問題")


def cmd_draft(args: list):
    """列出需要撰寫草稿的選題"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 需要撰寫草稿：研究完成但 draft_completed 為 false
    need_draft = [
        t for t in topics 
        if t.get('research_completed', False) and not t.get('draft_completed', False)
    ]
    need_draft.sort(key=lambda x: get_priority_weight(x['priority']))
    
    if not need_draft:
        print("📝 所有已完成研究的選題都已撰寫草稿（或沒有已完成研究的選題）")
        return
    
    print("=" * 60)
    print("📝 研究完成，等待撰寫草稿的選題")
    print("=" * 60)
    
    for topic in need_draft:
        print(f"\n[{topic['id']}] [{topic['priority'].upper()}] {topic['title']}")
        print(f"平台：{', '.join(topic['platforms']) if topic['platforms'] else '未定'}")
        print(f"建議：針對各平台撰寫適配的內容草稿")


def cmd_overdue(args: list):
    """列出逾期未完成的選題（P0 超過 2 週、P1 超過 1 個月未更新）"""
    data = load_topics()
    topics = data.get('topics', [])
    
    # 這裡簡化處理：顯示 P0 中長時間處於非完成狀態的選題
    overdue = [
        t for t in topics 
        if t['priority'] == 'p0' and t['status'] not in ['published', 'archived', 'completed']
    ]
    
    if not overdue:
        print("✅ 沒有逾期的 P0 選題")
        return
    
    print("=" * 60)
    print("🚨 需要關注的 P0 選題（高優先但未完成）")
    print("=" * 60)
    
    for topic in overdue:
        print(f"\n[{topic['id']}] {topic['title']}")
        print(f"狀態：{topic['status']}")
        print(f"備註：{topic.get('notes', '無')}")


def main():
    """主程式入口"""
    args = sys.argv[1:]
    command = args[0] if args else 'list'
    command_args = args[1:]
    
    commands = {
        'list': cmd_list,
        'next': cmd_next,
        'stats': cmd_stats,
        'research': cmd_research,
        'draft': cmd_draft,
        'overdue': cmd_overdue,
        'help': lambda x: print(__doc__)
    }
    
    if command in commands:
        try:
            commands[command](command_args)
        except Exception as e:
            print(f"❌ 執行錯誤：{e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"❌ 未知命令：{command}", file=sys.stderr)
        print(f"可用命令：{', '.join(commands.keys())}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

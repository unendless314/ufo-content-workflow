#!/usr/bin/env python3
"""
Fringe Research Prompt Finalizer
將 AI 生成的草稿提示詞轉換為標準模板格式。
"""

import re
import sys
from pathlib import Path


def get_template_content():
    template_path = Path(__file__).parent.parent / "references" / "template-detailed.md"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    print(f"錯誤: 找不到模板文件 '{template_path}'")
    sys.exit(1)


def extract_fields(draft):
    """從草稿提取可變更字段"""
    data = {}
    
    # 主題名稱
    lines = draft.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('═', '─')):
            topic = re.sub(r'\s+深度研究$', '', line)
            topic = re.sub(r'^#\s*', '', topic)
            data['topic'] = topic.strip()
            break
    
    # 核心問題
    m = re.search(r'\*\*核心問題：\*\*\s*(.+?)(?=\n\n|\n\*\*|$)', draft, re.DOTALL)
    if m:
        data['core_question'] = m.group(1).strip()
    
    # 邊界條件
    bc_match = re.search(r'\*\*邊界條件：\*\*\s*\n(.*?)(?=\n##|\n---|$)', draft, re.DOTALL)
    if bc_match:
        content = bc_match.group(1)
        
        m = re.search(r'[\-\*]\s+時間範圍：(.+?)(?=\n[\-\*]|\n\n|$)', content)
        if m:
            data['time_range'] = m.group(1).strip()
        
        m = re.search(r'[\-\*]\s+地理範圍：(.+?)(?=\n[\-\*]|\n\n|$)', content)
        if m:
            data['geo_range'] = m.group(1).strip()
        
        m = re.search(r'[\-\*]\s+關鍵術語：(.+?)(?=\n[\-\*]|\n\n|$)', content, re.DOTALL)
        if m:
            data['key_terms'] = m.group(1).strip()
    
    # 阻力檔案
    res_match = re.search(r'\*\*阻力檔案：\*\*\s*\n(.*?)(?=\n\*\*邊界|$)', draft, re.DOTALL)
    if res_match:
        content = res_match.group(1)
        
        m = re.search(r'[\-\*]\s+主要阻力來源：(.+?)(?=\n[\-\*]|\n\n|$)', content)
        if m:
            data['resistance_primary'] = m.group(1).strip()
        
        m = re.search(r'[\-\*]\s+次要阻力：(.+?)(?=\n[\-\*]|\n\n|$)', content)
        if m:
            data['resistance_secondary'] = m.group(1).strip()
    
    return data


def apply_to_template(template, data):
    """將字段應用到模板"""
    result = template
    
    # 主題名稱
    if 'topic' in data:
        result = result.replace('# [主題名稱] 深度研究', f'# {data["topic"]} 深度研究')
    
    # 核心問題
    if 'core_question' in data:
        result = result.replace(
            '**核心問題：** [根據用戶需求生成的具體研究問題]',
            f'**核心問題：** {data["core_question"]}'
        )
    
    # 邊界條件
    if 'time_range' in data:
        result = result.replace(
            '- 時間範圍：[開始] 至 [結束]',
            f'- 時間範圍：{data["time_range"]}'
        )
    
    if 'geo_range' in data:
        result = result.replace(
            '- 地理範圍：[區域]',
            f'- 地理範圍：{data["geo_range"]}'
        )
    
    if 'key_terms' in data:
        result = result.replace(
            '- 關鍵術語：[術語列表]',
            f'- 關鍵術語：{data["key_terms"]}'
        )
    
    # 阻力檔案
    if 'resistance_primary' in data:
        result = result.replace(
            '- 主要阻力來源：[根據主題識別，如：保密機制 / 典範衝突 / 污名化]',
            f'- 主要阻力來源：{data["resistance_primary"]}'
        )
    
    if 'resistance_secondary' in data:
        result = result.replace(
            '- 次要阻力：[如：學術污名化、媒體框架]',
            f'- 次要阻力：{data["resistance_secondary"]}'
        )
    
    return result


def main():
    if len(sys.argv) != 3:
        print("用法: python finalize_prompt.py <草稿文件> <輸出文件>")
        sys.exit(1)
    
    draft_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    if not draft_path.exists():
        print(f"錯誤: 找不到草稿文件 '{draft_path}'")
        sys.exit(1)
    
    try:
        template = get_template_content()
        draft = draft_path.read_text(encoding="utf-8")
        
        data = extract_fields(draft)
        
        print("ℹ️  從草稿提取的字段:")
        for key, value in data.items():
            preview = value[:60] + "..." if len(value) > 60 else value
            print(f"   - {key}: {preview}")
        
        final = apply_to_template(template, data)
        output_path.write_text(final, encoding="utf-8")
        
        print(f"\n✅ 定稿已生成: {output_path}")
        
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

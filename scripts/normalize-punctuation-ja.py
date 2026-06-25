#!/usr/bin/env python3
"""
日译汉标点规范化脚本 (ja-zh)
功能：将日文中译后的标点转为中文全角，机械归一化。
用法：python3 normalize-punctuation-ja.py "文件.md"
"""
import re
import sys


def is_cjk(c: str) -> bool:
    """判断字符是否为 CJK 字符（含中文/日文汉字/假名/韩文）"""
    if not c:
        return False
    o = ord(c)
    return (
        (0x3400 <= o <= 0x9FFF)   # CJK Unified Ideographs Extension A + basic
        or (0x3000 <= o <= 0x303F)  # CJK Symbols and Punctuation
        or (0xFF00 <= o <= 0xFFEF)  # Halfwidth and Fullwidth Forms
        or (0x3040 <= o <= 0x309F)  # Hiragana
        or (0x30A0 <= o <= 0x30FF)  # Katakana
        or (0x4E00 <= o <= 0x9FFF)  # CJK Unified Ideographs (redundant but safe)
        or (0xF900 <= o <= 0xFAFF)  # CJK Compatibility Ideographs
    )


def is_japanese_kana(c: str) -> bool:
    """判断是否为假名字符"""
    if not c:
        return False
    o = ord(c)
    return (0x3040 <= o <= 0x309F) or (0x30A0 <= o <= 0x30FF)


# ---- 替换映射 ----

# 日文标点 → 中文标点
JP_TO_CN_PUNCT = {
    # 読点（日文逗号）→ 中文逗号
    '、': '，',
    # 句号保留，但日文句号有时在半角位置，先统一
    # '。' stays '。'
}

# 半角标点 → 全角（仅当紧邻 CJK 字符时）
HALF_TO_FULL = {
    ',': '，',
    ';': '；',
    ':': '：',
    '?': '？',
    '!': '！',
    '(': '（',
    ')': '）',
}

# 日文引号 → 中文引号
# 「」→ ""  『』→ ''
JP_QUOTE_MAP = {
    '「': '"',
    '」': '"',
    '『': ''',
    '』': ''',
}

# 日文波浪线 → 中文浪纹
JP_WAVE = {
    '〜': '～',
}

# Markdown 链接模式
LINK_PATTERN = re.compile(r'\[[^\]]*\]\([^)]*\)')


def should_skip_line(line: str) -> bool:
    """判断是否应跳过该行（不做任何标点转换）"""
    stripped = line.strip()
    if stripped == '':
        return True
    if line.lstrip().startswith('>'):
        return True  # blockquote（日文原文）不碰
    if stripped.startswith('```') or stripped.endswith('```'):
        return True  # 代码块边界
    if stripped == '---':
        return True
    return False


def is_inside_code_block(lines: list, idx: int) -> bool:
    """检查行是否在代码块内"""
    in_block = False
    for i in range(idx + 1):
        stripped = lines[i].strip()
        if stripped.startswith('```'):
            in_block = not in_block
    return in_block


def fix_line(line: str) -> str:
    """对单行进行标点规范化"""
    # 1. 保存 Markdown 链接
    store = []
    line = LINK_PATTERN.sub(
        lambda m: (store.append(m.group(0)) or '\x00%d\x00' % (len(store) - 1)),
        line
    )

    chars = list(line)
    n = len(chars)

    # 2. 日文特有标点转换（読点 → 逗号）
    for i, c in enumerate(chars):
        if c in JP_TO_CN_PUNCT:
            chars[i] = JP_TO_CN_PUNCT[c]

    # 3. 日文引号 → 中文引号
    for i, c in enumerate(chars):
        if c in JP_QUOTE_MAP:
            chars[i] = JP_QUOTE_MAP[c]

    # 4. 日文波浪线 → 中文浪纹
    for i, c in enumerate(chars):
        if c in JP_WAVE:
            chars[i] = JP_WAVE[c]

    # 5. 半角标点 → 全角（仅当紧邻 CJK 字符时）
    #    前一个字符或后一个字符是 CJK 才转
    for i, c in enumerate(chars):
        if c in HALF_TO_FULL:
            prev_cjk = is_cjk(chars[i - 1]) if i > 0 else False
            next_cjk = is_cjk(chars[i + 1]) if i + 1 < n else False
            if prev_cjk or next_cjk:
                chars[i] = HALF_TO_FULL[c]

    # 6. 恢复 Markdown 链接
    line = ''.join(chars)
    line = re.sub(
        r'\x00(\d+)\x00',
        lambda m: store[int(m.group(1))],
        line
    )

    return line


def count_residual_issues(line: str) -> int:
    """统计行中的残留问题数"""
    # 排除 Markdown 链接
    cleaned = LINK_PATTERN.sub('', line)
    count = 0

    # 检查残留的日文読点
    count += cleaned.count('、')

    # 检查紧邻 CJK 的半角标点
    for i, c in enumerate(cleaned):
        if c in HALF_TO_FULL:
            prev_cjk = is_cjk(cleaned[i - 1]) if i > 0 else False
            next_cjk = is_cjk(cleaned[i + 1]) if i + 1 < len(cleaned) else False
            if prev_cjk or next_cjk:
                count += 1

    # 检查残留的日文引号
    for q in '「」『』':
        count += cleaned.count(q)

    # 检查残留的日文波浪线
    count += cleaned.count('〜')

    return count


def main():
    if len(sys.argv) < 2:
        print("用法: python3 normalize-punctuation-ja.py <文件.md>")
        sys.exit(1)

    src = sys.argv[1]

    try:
        with open(src, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {src}")
        sys.exit(1)

    # 判断每行是否在代码块内
    code_block_flags = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_block = not in_block
        code_block_flags.append(in_block)

    fixed_lines = []
    for i, line in enumerate(lines):
        if should_skip_line(line) or code_block_flags[i]:
            fixed_lines.append(line)
        else:
            fixed_lines.append(fix_line(line))

    # 写回文件
    with open(src, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))

    # 自检报告
    total_residual = 0
    for i, line in enumerate(fixed_lines):
        if not should_skip_line(line) and not code_block_flags[i]:
            r = count_residual_issues(line)
            if r > 0:
                print(f"  行 {i + 1}: {r} 处残留 → {line[:80]}...")
            total_residual += r

    if total_residual == 0:
        print(f"✓ 标点规范化完成，残留: 0")
    else:
        print(f"⚠ 标点规范化完成，残留: {total_residual}（请手动检查以上行）")

    return total_residual


if __name__ == '__main__':
    sys.exit(main())

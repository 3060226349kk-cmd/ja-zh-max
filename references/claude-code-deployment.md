# Claude Code 部署指南

将 `ja-zh-translation-polish` 部署到 Claude Code 的两种方案。

## 首选方案：JUNCTION 单源架构（推荐）

**原理**：在 `~/.agents/skills/` 下维护一个 canonical 副本，Hermes 和 Claude Code 两侧均通过 Windows 目录 Junction 指向它。任一侧修改即时同步，无需重复部署。

### 架构

```
~/.agents/skills/ja-zh-translation-polish/   ← 唯一真源
    ├── SKILL.md          ← 使用 $HOME/.agents/... 绝对路径（跨平台通用）
    ├── references/
    └── scripts/

Hermes:  ~/AppData/Local/hermes/skills/ja-zh-translation-polish  →  JUNCTION  ┐
Claude:  ~/.claude/skills/ja-zh-translation-polish                →  JUNCTION  ┘
```

### 部署命令（Windows，cmd 管理员或普通用户）

```bash
# 1. 创建 canonical 目录（若不存在）
CANONICAL="$HOME/.agents/skills/ja-zh-translation-polish"
mkdir -p "$CANONICAL/references" "$CANONICAL/scripts"

# 2. 从 Hermes 侧复制全部内容到 canonical
cp -r "$HOME/AppData/Local/hermes/skills/ja-zh-translation-polish/"* "$CANONICAL/"

# 3. 修正 SKILL.md 中的脚本路径为跨平台绝对路径
#    $SKILL_DIR/scripts/...  →  $HOME/.agents/skills/ja-zh-translation-polish/scripts/...
#    ~/AppData/Local/hermes/... → ~/.agents/skills/ja-zh-translation-polish/...

# 4. 删除两侧旧目录，创建 Junction
rm -rf "$HOME/AppData/Local/hermes/skills/ja-zh-translation-polish"
rm -rf "$HOME/.claude/skills/ja-zh-translation-polish"
cmd //c "mklink /J C:\\Users\\$USERNAME\\AppData\\Local\\hermes\\skills\\ja-zh-translation-polish C:\\Users\\$USERNAME\\.agents\\skills\\ja-zh-translation-polish"
cmd //c "mklink /J C:\\Users\\$USERNAME\\.claude\\skills\\ja-zh-translation-polish C:\\Users\\$USERNAME\\.agents\\skills\\ja-zh-translation-polish"
```

### SKILL.md 跨平台路径策略

YAML frontmatter **保留**（Claude Code 无视不报错，Hermes 需要它加载 skill）。
脚本路径全部改用 `$HOME/.agents/skills/<name>/scripts/...` 而非 `$SKILL_DIR/...`：

```bash
# 旧（仅 Hermes 可用）：
python3 "$SKILL_DIR/scripts/normalize-punctuation-ja.py" "..."

# 新（Hermes + Claude Code 通用）：
python3 "$HOME/.agents/skills/ja-zh-translation-polish/scripts/normalize-punctuation-ja.py" "..."
```

### ⚠ Windows Junction 创建陷阱

| 命令 | 现象 | 原因 |
|------|------|------|
| `ln -s`（git-bash） | **静默复制为实体目录**，不报错 | git-bash 的 `ln -s` 在 Windows 上权限不足时回退为 `cp -r` |
| `mklink /D`（cmd） | "没有足够的权限执行此操作" | 目录符号链接需要管理员权限 |
| `mklink /J`（cmd） | ✅ 正常工作 | 目录 Junction 不需要管理员权限（NTFS 原生支持） |

**验证 Junction 是否生效**：
```bash
# 在任一侧写入文件，另一侧应立即可见
echo "test" > "$HOME/AppData/Local/hermes/skills/ja-zh-translation-polish/.probe"
cat "$HOME/.claude/skills/ja-zh-translation-polish/.probe"  # 应输出 test
rm "$HOME/AppData/Local/hermes/skills/ja-zh-translation-polish/.probe"

# cmd 确认 Junction 类型
cmd //c "dir C:\\Users\\$USERNAME\\AppData\\Local\\hermes\\skills\\ | findstr ja-zh"
# 应输出：<JUNCTION>     ja-zh-translation-polish [C:\Users\...\.agents\skills\ja-zh-translation-polish]
```

## 备选方案：独立副本 + 手动适配

**适用场景**：无法使用 Junction 的平台（如非 NTFS 文件系统），或需要两侧 SKILL.md 有实质性差异时。

### 目标结构

```
~/.claude/skills/ja-zh-translation-polish/
├── SKILL.md                          ← 去 YAML frontmatter，加 Claude 使用说明
├── references/                       ← 全部 .md 原样复制（含本文件自身）
│   ├── japanese-translationese-symptoms.md
│   ├── japanese-techniques.md
│   ├── japanese-text-analysis.md
│   ├── wasei-kango-traps.md
│   ├── revision-methodology.md
│   ├── libertine-vocabulary-ja.md
│   ├── textbook-extraction-workflow.md
│   └── claude-code-deployment.md      ← 本文件
└── scripts/
    ├── normalize-punctuation-ja.py    ← 路径引用修正：$SKILL_DIR → 相对路径
    └── bilingual-to-pdf.py            ← 同上，且 Hermes 显式路径改为 Claude 路径
```

## 部署命令（Windows git-bash）

```bash
HERMES_SKILL="$HOME/AppData/Local/hermes/skills/ja-zh-translation-polish"
CLAUDE_SKILL="$HOME/.claude/skills/ja-zh-translation-polish"

# 建目录
mkdir -p "$CLAUDE_SKILL/references" "$CLAUDE_SKILL/scripts"

# 复制参考文件和脚本（原样）
cp "$HERMES_SKILL/references/"*.md "$CLAUDE_SKILL/references/"
cp "$HERMES_SKILL/scripts/"*.py "$CLAUDE_SKILL/scripts/"

# SKILL.md 需要手动处理：去 YAML frontmatter，修正脚本路径
```

## SKILL.md 适配要点

1. **去 Hermes YAML frontmatter**（`---` 到 `---` 之间的内容）
2. **顶部加 Claude Code 使用说明**（版本号按实际 Hermes `SKILL.md` YAML frontmatter 的 `version` 字段填写）：
   ```markdown
   # 日译汉翻译润色 v{version}
   > **Claude Code 适配版** · 源: Hermes `ja-zh-translation-polish`
   > **用法**: 对话中说「加载日译汉技能」，或直接引用本文件路径（`~/.claude/skills/ja-zh-translation-polish/SKILL.md`）。翻译完成后，运行 `scripts/normalize-punctuation-ja.py` 做标点规范化。
   ```
3. **修正脚本路径**（两处都要改）：`python3 "$SKILL_DIR/scripts/bilingual-to-pdf.py"` → `python3 "scripts/bilingual-to-pdf.py"`，`python3 "$SKILL_DIR/scripts/normalize-punctuation-ja.py"` → `python3 "scripts/normalize-punctuation-ja.py"`；此外显式路径示例 `~/AppData/Local/hermes/skills/…` → `~/.claude/skills/…`
4. 参考文件保持原样（纯 Markdown，无需修改）

## ⚠ 常见陷阱：原样复制未适配

**问题**：直接用 `cp` 复制 SKILL.md 而不做上述三步适配，导致 Claude Code 版：
- 保留了 Hermes YAML frontmatter（多余但无害）
- `$SKILL_DIR` 变量在 Claude Code 中不解析，脚本调用失败
- 无 Claude Code 专用使用说明，用户不知道如何加载

**验证**（部署后跑一遍）：
```bash
# 确认无 YAML frontmatter（首行不应是 ---）
head -1 ~/.claude/skills/ja-zh-translation-polish/SKILL.md

# 确认无残留 $SKILL_DIR
grep -c '\$SKILL_DIR' ~/.claude/skills/ja-zh-translation-polish/SKILL.md
# 输出应为 0
```

## Claude Code 中的使用

**一次性加载**（对话中）：
```
请读取 ~/.claude/skills/ja-zh-translation-polish/SKILL.md 并按其中方法论翻译以下日文：……
```

**持久化**（写入 CLAUDE.md）：
```markdown
所有日译汉任务，请先读取并遵循 ~/.claude/skills/ja-zh-translation-polish/SKILL.md 的完整方法论。
翻译完成后，运行 scripts/normalize-punctuation-ja.py 做标点规范化。
```

## 与 Hermes 版的差异

| 项目 | Hermes | Claude Code |
|------|--------|-------------|
| 发现机制 | `skill_view()` 自动加载 | 需用户显式引用文件路径 |
| 参考文件 | `skill_view(file_path=)` 懒加载 | 需手动在对话中指定读取 |
| 版本号 | YAML `version` 字段 | Markdown 标题（需手动同步） |
| 脚本路径 | `$SKILL_DIR/scripts/` | `scripts/`（相对） |

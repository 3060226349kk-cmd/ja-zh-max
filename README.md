# ja-zh-max — 日汉翻译打磨 Hermes Agent Skill

把日文译成地道中文，产出日中对照译文，彻底摆脱「翻訳調」。

[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-Skill-blueviolet)](https://hermes-agent.nousresearch.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.3.0-blue)](SKILL.md)

---

## 这是什么？

**ja-zh-max** 是 [Hermes Agent](https://hermes-agent.nousresearch.com) 的一个翻译技能（Skill），专门用于 **日文 → 中文** 翻译与润色。

核心方法论基于高宁《日汉翻译教程》的系统理论，配合 7 阶段翻译工作流，解决日译汉中最常见的三大问题：

1. **同形汉字的陷阱** —「検討する」≠「检讨」、「手紙」≠「手纸」
2. **SOV → SVO 的语序重构** — 日语谓语在句末，中文在中间
3. **暧昧文化的语法化** — 日语的「～と思われる」「～かもしれない」不等于中文的「似乎」「或许」

## 功能

- ✅ 日文 → 中文翻译，去翻译腔
- ✅ 自动产出日中对照译文（Markdown + HTML 双格式）
- ✅ 按文本类型调节归化尺度（小说/论文/新闻/商务）
- ✅ 参考文件系统：和製漢語陷阱、日语技法、修订方法论
- ✅ 内置标点规范脚本

## 安装

### 方式 1：从 GitHub 安装（推荐）

```bash
# 进入你的 Hermes skills 目录
cd ~/AppData/Local/hermes/skills/

# 克隆仓库
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git ja-zh-max
```

### 方式 2：手动复制

将 `SKILL.md` 及 `references/`、`scripts/` 复制到 Hermes skills 目录下即可。

## 使用

在 Hermes 中直接提出翻译请求即可自动触发：

```
把这段日文翻成中文：
...

翻一下这段日文，去翻译腔：
...

帮我润色这段译文：
...
```

更详细的用法见 [SKILL.md](SKILL.md)。

## 文件结构

```
ja-zh-max/
├── SKILL.md                           # 主技能文件
├── README.md                          # 本文件
├── LICENSE                            # MIT 许可
├── .gitignore
├── references/
│   ├── claude-code-deployment.md       # Claude Code 部署指南
│   ├── japanese-techniques.md          # 日语翻译技法
│   ├── japanese-text-analysis.md       # 日语文本分析
│   ├── japanese-translationese-symptoms.md  # 日语翻译腔症状
│   ├── libertine-vocabulary-ja.md      # 日语风流词汇
│   ├── revision-methodology.md         # 修订方法论
│   ├── textbook-extraction-workflow.md # 教材提取工作流
│   └── wasei-kango-traps.md           # 和製漢語陷阱
└── scripts/
    ├── bilingual-to-pdf.py             # 对照→PDF 生成
    └── normalize-punctuation-ja.py     # 日语标点规范化
```

## 许可

MIT License — 详见 [LICENSE](LICENSE)。

---

### 关联项目

- [en-zh-translation-polish](https://github.com/3060226349kk-cmd/en-zh-translation-polish) — 英汉翻译打磨
- [humanizer](https://github.com/3060226349kk-cmd/humanizer) — 文本人声化

---

# ja-zh-max — Japanese→Chinese Translation Polish Skill for Hermes Agent

Translate Japanese into idiomatic Chinese with bilingual parallel output. Eliminates "translationese" (翻訳調) once and for all.

## What is this?

A dedicated [Hermes Agent](https://hermes-agent.nousresearch.com) skill for **Japanese→Chinese translation and polishing**. Built on Gao Ning's *Japanese-Chinese Translation Course* theoretical framework with a 7-stage translation workflow.

### Features

- ✅ Natural Chinese output — no translationese
- ✅ Bilingual parallel Markdown + HTML output
- ✅ Adjustable domestication register (fiction/academic/news/business)
- ✅ Reference system: wasei-kango traps, Japanese techniques, revision methodology
- ✅ Built-in punctuation normalization scripts

## Installation

```bash
cd ~/AppData/Local/hermes/skills/
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git ja-zh-max
```

## Usage

Just ask Hermes:

```
Translate this Japanese to Chinese:
...

Polish this translation, remove the translationese:
...
```

## License

MIT — see [LICENSE](LICENSE).

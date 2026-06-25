# jp-zh-max — 日译汉翻译润色 Claude Code Skill（Ultra 增强版）

日文→中文翻译打磨，产出日中对照译文。基于高宁《日汉翻译教程》20 个蒸馏技能。

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.2.0)](SKILL.md)

## 这是什么？

**jp-zh-max** 是 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的翻译技能，专门用于 **日文 → 中文** 翻译与润色。

Ultra 增强版：在 jp-zh 的 9 阶段工作流基础上，集成了高宁《日汉翻译教程》（上海外语教育出版社，2008）经 book2skill 蒸馏的 **20 个技能**，覆盖：

- 同形汉字词陷阱（「検討する」≠「检讨」）
- 汉语译词选择与动词虚化
- SOV → SVO 语序重构
- 连体修饰链拆解
- 暧昧文化语法化的消除（「～と思われる」「～かもしれない」）
- 汉译被动句的隐形回避
- 专业术语体系构建

## 安装

### 方式 1：克隆到 Claude Code skills 目录

```bash
# 进入 Claude Code skills 目录
cd ~/.claude/skills/

# 克隆仓库
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git jp-zh-max

# 确保子目录引用有效
# （如果使用 jp-zh 的共用 references/scripts，需手动创建 symlink）
```

### 方式 2：手动复制

将 `SKILL.md`、`ultra/`、`references/`、`scripts/` 复制到 `~/.claude/skills/` 下即可。

## 使用

在 Claude Code 中提出翻译请求：

```
日译中：
（你的日文原文）
```

或者直接打开日文文件翻译：

```
把这个文件翻译成中文
```

详见 [SKILL.md](SKILL.md)。

## 文件结构

```
jp-zh-max/
├── SKILL.md                                # 主技能文件（v3.2.0）
├── README.md                               # 本文件
├── LICENSE                                 # MIT License
├── .gitignore
├── ultra/
│   └── SKILL_MAP.md                        # Ultra 增强技能映射表
├── references/
│   ├── claude-code-deployment.md           # Claude Code 部署
│   ├── japanese-techniques.md              # 日语翻译技法
│   ├── japanese-text-analysis.md           # 日语文本分析
│   ├── japanese-translationese-symptoms.md # 日语翻译腔症状
│   ├── libertine-vocabulary-ja.md          # 日语风流词汇
│   ├── output-formats.md                   # 输出格式规范
│   ├── project-init.md                     # 项目初始化
│   ├── revision-methodology.md             # 修订方法论
│   ├── textbook-extraction-workflow.md     # 教材提取工作流
│   └── wasei-kango-traps.md               # 和製漢語陷阱
└── scripts/
    ├── bilingual-to-pdf.py                 # 对照→PDF 生成
    ├── normalize-punctuation-ja.py         # 日语标点规范化
    └── strip-version-markers.py            # 版本标记清理
```

## 许可

MIT License — 详见 [LICENSE](LICENSE)。

---

# jp-zh-max — Japanese→Chinese Translation Polish (Ultra) for Claude Code

Translate Japanese into idiomatic Chinese with bilingual parallel output. Ultra-enhanced with 20 distilled skills from Gao Ning's *Japanese-Chinese Translation Course*.

## Install

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git jp-zh-max
```

## Usage

Ask Claude Code:

```
Translate this Japanese to Chinese:
...

Polish this translation:
...
```

## License

MIT

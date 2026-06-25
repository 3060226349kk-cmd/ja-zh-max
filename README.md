# jp-zh-max — 日译汉翻译润色 Claude Code Skill

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.2.0)](SKILL.md)

> 日文→中文翻译与润色。9 阶段工作流 + 高宁《日汉翻译教程》20 个蒸馏技能 + 4 层校验链。
> 专为 Claude Code 设计，输出日中对照译文。
>
> 📊 [完整工作流流程图（含校验链）](ultra/WORKFLOW.md)

---

## 目录

- [这是什么？](#这是什么)
- [方法论基石](#方法论基石)
- [工作流管线](#工作流管线)
- [校验链](#校验链)
- [快速安装](#快速安装)
- [快速使用](#快速使用)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [致谢](#致谢)
- [许可](#许可)

---

## 这是什么？

**jp-zh-max** 是 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的翻译 skill，将日文译为地道中文并产出日中对译。集成了高宁《日汉翻译教程》（上海外语教育出版社，2008）经 book2skill 蒸馏的 **20 个翻译技能**。

### 日译汉三大核心差异

日译汉与英译汉有三重根本不同，jp-zh-max 的设计围绕这三者展开：

1. **同形汉字词的虚假安全感**——日文大量使用汉字，译者会下意识直接搬运：「検討する」→「检讨」（应为「讨论/研究」）、「手紙」→「手纸」（应为「信」）。高宁称之为「陷阱，会给译文留下隐患或重创」。
2. **SOV → SVO 的语序鸿沟**——日语谓语在句末、修饰语全部前置；中文谓语在中间、定语不能无限堆叠。长连体修饰链是日译中最常见的结构难点。
3. **暧昧文化的语法化**——日语通过「～と思われる」「～かもしれない」「～ようだ」等将不确定性语法化；中文虽也有委婉表达，但密度远低于日语。直译会造成「似乎」「或许」「被认为」泛滥。

---

## 方法论基石

本 skill 的方法论根基是高宁《日汉翻译教程》（上海外语教育出版社，2008），经 book2skill 管线蒸馏为可执行的 20 个技能。核心理论框架如下。

### 三大统领原则

> **「译对」优先于「译好」**——先求准确，再求优美（第 18 页）
>
> **「日语选义，汉语选词」**——词义最终由语境决定，不由辞典决定（第 61 页）
>
> **修改由大到小层层推进**——篇章 → 句子 → 词汇，理解问题重于修辞问题（第 425 页）

### 20 个蒸馏技能覆盖

四组方法论：

| 分组 | 技能 | 应用阶段 |
|------|------|---------|
| **翻译意识与语境**（6 技能） | 翻译意识、反孤句原则、语境适切原则、大众语境/个人语境、辞书活用与词义、理性把握/感性把握 | 预读取 + 阶段 0-2 |
| **结构与句法**（4 技能） | 缩扩句法、后推法、审美制约机制、宏观到微观/宏观把握微观 | 阶段 1-3 |
| **选词与润色**（6 技能） | 同义句多译案选择、同源译文比较、译文修改分层框架、回译训练法、修辞翻译教学、修辞意识发展 | 阶段 3-7 |
| **文体与类型**（4 技能） | 文体与翻译、译得好回归译得对、理解是技巧之母、专业术语体系构建 | 阶段 0-5 |

详见 [`ultra/SKILL_MAP.md`](ultra/SKILL_MAP.md) 查看每个技能与工作流阶段的精确映射关系。

---

## 工作流管线

jp-zh-max 的工作流由 **9 个阶段** 组成，其中 6 个阶段引入了高宁方法论的具体技能。各阶段概述如下（具体门禁条件与脚本路径见 [SKILL.md](SKILL.md)）。

### 预备阶段

| 阶段 | 名称 | 职责 |
|------|------|------|
| **-1** | 项目目录初始化 | 创建 `source/` 目录、文件归位、格式提取 |
| **-0.5** | 方法论预读取批 | 一次性读取 14 个方法论 SKILL.md，建立全流程方法论地基 |

### 核心翻译管线（阶段 0→6）

| 阶段 | 名称 | 职责 |
|------|------|------|
| **0** | 文本分析 | 定归化档位（偏硬/偏中/偏软）、text-profile、文体三层分析、语境分析；应用翻译意识、反孤句原则、文体与翻译框架 |
| **1** | 理解与脱壳 | 脱离日文语言外壳、语义还原、连体修饰链解析；软文本逐句标注翻译自由度边界（审美制约机制） |
| **2** | 初译 | 汉语选词、SOV → SVO 重构、敬语降维、和製漢語两步法；应用辞书活用与词义、理性把握与感性把握 |
| **3** | 润色诊断 | 翻译腔清除（8 类症状）、多译案选择、语域对齐；关键句执行发散→收敛→选优 |
| **4** | 音韵打磨 | 朗读校准、双音节/四字结构、节奏重组（软文本放开，硬文本点到为止） |
| **5** | 质检 | 14 项自检、原文对照修正；应用同源译文比较、译文修改分层框架（四层）、回译训练法 |
| **6** | 标点规范化 | 机械执行 `normalize-punctuation-ja.py`，日文标点→中文全角 |

### 交付（阶段 8）

| 步骤 | 职责 |
|------|------|
| **8A** | 最终清理：剥夺版本标记、删除 text-profile、添加译者署名（`strip-version-markers.py`） |
| **8B** | 派生交付物：日中对照 MD/HTML/EPUB/MOBI |

### 超长文本并行翻译

当单篇翻译量超过 5,000 字时，按章节/幕次切割为独立子任务并行翻译。流程：

- **阶段 A**：子代理并行翻译（各执行阶段 0-6），每段标 `[v3·Q✓]`
- **阶段 B**：集成合并、格式清理、日文标点规范化
- **阶段 C**：整书校验链（全局术语统一 + 语感连续 + AI 模式污染检测）
- **阶段 D**：交付物生成

---

## 校验链

翻译文本落盘后、交付物生成前，必须经过以下 **4 步校验**。任一步发现问题 → 回到对应阶段修复 → 重走校验链。**不可跳过任一步骤。**

```
阶段 6（标点规范化）
       ↓
① scribe:prose-reviewer       — AI 腔 / 翻译腔 / 语感漂移
       ↓
② verification-before-completion — 交付物完整性 + 日中配对
       ↓
③ humanizer                   — 四维验证（Fidelity / Naturalness / Grammar / AI Patterns）
                                 + 强制对抗式自审
       ↓
④ humanizer-zh                — 中文 AI 痕迹终审（24 条规则）
       ↓
阶段 8（交付）
```

### 步骤 1：scribe:prose-reviewer

审查中文译文的 AI 写作腔、翻译腔残留、禁用短语、语感漂移、结构单调。**参考意见**——所建议的修改由 humanizer（步骤 3）拥有最终裁量权。

### 步骤 2：verification-before-completion

全交付物完整性检查：MD/HTML 是否齐全、标点残留是否为 0、日中配对是否完整、原文件是否在 `source/` 内。确认「humanizer 尚未执行」等运行状态。

软文本（自由度 ≥ 4）在此步后插入修辞技能：修辞翻译教学 + 修辞意识发展。

### 步骤 3：humanizer

将中文译文按段落切割为 chunk（每块 3-5 段），对每个 chunk 执行四维验证：

- **Fidelity**（忠实度：逐句对照源文，检查语义等价/否定/情态/专名）
- **Naturalness**（自然度：翻译腔/语感/语域）
- **Grammar**（语法错字：搭配/标点/一致）
- **AI Patterns**（AI 痕迹：29 种模式）

通过后执行**强制对抗式自审**——对全部已通过的 chunk 重新逐句审查，防止系统性盲区遗漏。

humanizer 对 prose-reviewer 的建议拥有**最终裁量权**：批准、拒绝、或发现其遗漏的问题。

### 步骤 4：humanizer-zh

仅处理中文译文行（过滤日文 blockquote），按 chunk 逐块过 **24 条中文 AI 痕迹规则**（四大类 × 6 条：内容模式 / 语言语法 / 风格模式 / 交流填充）。检测并修复 AI 高频词汇、破折号滥用、三段式排比、否定式排比、系动词回避、虚假范围、填充短语、通用积极结论等。

**职责边界**：humanizer 负责「译得对」（Fidelity + Naturalness + Grammar），humanizer-zh 负责「读起来像人写的」（中文 AI 痕迹清除）。两者各司其职。

### 自动修正规则

校验链四步中发现的任何错误或问题，**默认自动修正**并直接写入对照 MD 文件，不等待逐条批准。修正后的 MD 是阶段 8 派生 HTML/EPUB/MOBI 的唯一输入源。

---

## 快速安装

### 方式 1：克隆到 Claude Code skills 目录（推荐）

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git jp-zh-max
```

克隆完成后，`references/`、`scripts/`、`ultra/` 子目录自动就位，工作流脚本路径自洽。

### 方式 2：手动复制

将仓库内以下内容完整复制到 `~/.claude/skills/jp-zh-max/`：

```
SKILL.md
references/
scripts/
ultra/
```

**注意**：工作流脚本（`normalize-punctuation-ja.py`、`strip-version-markers.py`）和 `ultra/` 方法论文件通过相对路径引用。手动复制必须保持目录结构完整，否则阶段 6 标点规范化与阶段 8A 最终清理的脚本执行会失败。

### 环境要求

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（推荐最新版本）
- Python 3.8+（运行 `scripts/` 下辅助脚本）
- Pandoc（可选，EPUB/MOBI/PDF 输出）

---

## 快速使用

在 Claude Code 中提出翻译请求：

```
日译中：
（你的日文原文）
```

或从文件翻译：

```
把这个文件翻译成中文
```

Claude Code 将自动触发 jp-zh-max skill，执行完整工作流管线。首次使用会自动加载方法论预读取批（阶段 -0.5），建立方法论地基。

---

## 项目结构

```
jp-zh-max/
├── SKILL.md                       # 运行时指令：完整工作流、准入/准出门禁、脚本路径
├── README.md                      # 本文件
├── LICENSE                        # MIT
├── .gitignore
├── references/                    # 方法论文档（翻译技巧、陷阱清单、文本分析框架）
│   ├── claude-code-deployment.md      # Claude Code 部署说明
│   ├── japanese-techniques.md         # 日译汉技巧库（词性转换、增减词、分句合句等）
│   ├── japanese-text-analysis.md      # 日文文本分析框架
│   ├── japanese-translationese-symptoms.md  # 翻译腔 8 类症状清单
│   ├── libertine-vocabulary-ja.md      # 性/身体直白内容语域对等词汇表
│   ├── output-formats.md              # 派生交付物（HTML/EPUB/MOBI/PDF）生成脚本
│   ├── project-init.md                # 阶段 -1 项目目录初始化详细步骤
│   ├── revision-methodology.md        # 译文修改方法论（高宁三层修改）
│   ├── textbook-extraction-workflow.md # 教材/书籍文本提取工作流
│   └── wasei-kango-traps.md           # 和製漢語陷阱清单（同形异义词对照表）
├── scripts/                       # 工作流辅助脚本
│   ├── normalize-punctuation-ja.py    # 阶段 6：日文标点→中文全角（机械执行）
│   ├── strip-version-markers.py       # 阶段 8A：剥夺版本标记 + 清理 + 译者署名
│   └── bilingual-to-pdf.py            # 日中对照 MD → PDF（按需）
└── ultra/                         # 方法论组件（高宁 20 技能的文件映射与流程图）
    ├── SKILL_MAP.md                   # 20 个技能与工作流阶段映射表（含跳过规则速查）
    └── WORKFLOW.md                    # 翻译工作流流程图（Mermaid，含校验链）
```

---

## 贡献指南

**维护者：** [Lilipuut](https://github.com/3060226349kk-cmd) — 项目创建者，负责核心工作流设计与方法论集成。

本 skill 欢迎贡献。以下指引帮助您理解项目结构并有效参与。

### 开发环境准备

1. 安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. 克隆本仓库到 `~/.claude/skills/jp-zh-max/`

### 贡献流程

1. **开 issue**：在 [Issues](https://github.com/3060226349kk-cmd/ja-zh-max/issues) 描述改动目标，确保与其他贡献者不冲突
2. **Fork + Branch**：从 `master` 创建 feature branch（如 `fix/wasei-kango-typo`、`feat/new-reference`）
3. **改动范围**：
   - `SKILL.md`：工作流阶段的门禁条件、脚本路径、方法论引用
   - `references/*.md`：翻译技巧、陷阱清单的增补或修正
   - `scripts/*.py`：辅助脚本的功能扩展或 bug 修复
   - `ultra/*.md`：方法论映射表或工作流流程图的更新
   - `README.md`：中文版 + 英文版同时更新（精确对称原则）
4. **提交**：commit message 以前置标签开头，如 `[SKILL]` `[REF]` `[SCRIPT]` `[ULTRA]` `[DOC]`
5. **PR**：关联 issue，描述改动内容与验证方式

### 代码规范

- SKILL.md：保留 YAML frontmatter（`name` / `description` / `version` / `allowed-tools`），工作流阶段标注准入/准出门禁
- references/*.md：每条技巧以有编号的列表条目呈现，引用原文出处（高宁原书页码）
- scripts/*.py：兼容 Python 3.8+，不接受外部依赖；文件路径通过 `$SKILL_DIR` 环境变量或相对路径解析
- 跨平台注意：脚本路径在 Windows（git-bash）和 macOS/Linux 下均需可运行
- 新增方法论文档需在 `SKILL_MAP.md` 中注册其阶段映射

### 发布流程

1. 版本号更新：`SKILL.md` 的 YAML `version` 字段 + README badge 链接
2. CHANGELOG（可选）记录每次版本的主要变更
3. 合并到 `master` 后即通过 `git clone` 可获取最新版本

---

## 致谢

**项目作者：** [Lilipuut](https://github.com/3060226349kk-cmd) — jp-zh-max 整体架构设计、方法论集成与实现。

本 skill 的基本框架源自 [en-zh-translation-polish](https://github.com/3060226349kk-cmd/en-zh-translation-polish)（英汉翻译打磨），在其 7 阶段工作流基础上扩展为日汉翻译专用版。感谢原技能的架构设计。

书中 20 个翻译技能的蒸馏提取通过 [cangjie-skill](https://github.com/3060226349kk-cmd/cangjie-skill) 的 book2skill 管线完成。

特别鸣谢 **高宁** 教授——《日汉翻译教程》（上海外语教育出版社，2008）为整套方法论提供了系统理论基石。本书的翻译意识论、语境分析框架、文体三层分析、缩扩句法与后推法等核心概念，构成了本 skill 每个阶段的学理支撑。

校验链中的 `verification-before-completion` 步骤来自 [Superpowers](https://github.com/3060226349kk-cmd/superpowers) 技能集、`scribe:prose-reviewer` 来自 [scribe](https://github.com/3060226349kk-cmd/scribe)、`humanizer` 与 `humanizer-zh` 为独立校验管线。感谢各技能的开放架构。

## 许可

MIT License — 详见 [LICENSE](LICENSE)。

---

---

# jp-zh-max — Japanese→Chinese Translation Polish for Claude Code

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.2.0)](SKILL.md)

> Japanese→Chinese translation and polish. 9-stage workflow + 20 distilled skills from Gao Ning's *Japanese-Chinese Translation Course* + 4-step validation pipeline.
> Designed for Claude Code, outputs bilingual parallel text.
>
> 📊 [Full workflow diagram (with validation chain)](ultra/WORKFLOW.md)

---

## Table of Contents

- [What Is This?](#what-is-this)
- [Theoretical Foundation](#theoretical-foundation)
- [Workflow Pipeline](#workflow-pipeline)
- [Validation Pipeline](#validation-pipeline)
- [Quick Install](#quick-install)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## What Is This?

**jp-zh-max** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) translation skill that renders Japanese into idiomatic Chinese with bilingual parallel output. It integrates **20 distilled skills** from Gao Ning's *Japanese-Chinese Translation Course* (上海外语教育出版社, 2008) via the book2skill pipeline.

### Three Fundamental Japanese→Chinese Challenges

jp-zh-max is designed around three challenges that distinguish Japanese→Chinese translation from English→Chinese:

1. **False Safety of Kanji Look-alikes**—Japanese uses kanji extensively, creating a strong temptation to carry the surface form directly into Chinese: 「検討する」→ "review/study" (not "conduct a self-criticism"), 「手紙」→ "letter" (not "toilet paper"). Gao Ning calls these "traps that leave hidden damage in the translation."
2. **SOV → SVO Structural Gap**—Japanese predicates land at the end of the sentence with all modifiers front-loaded; Chinese predicates sit in the middle with strict modifier length limits. Long attributive chains are the single most common structural difficulty.
3. **Grammaticalized Ambiguity**—Japanese grammaticalizes uncertainty through 「～と思われる」「～かもしれない」「～ようだ」; Chinese has far lower density of hedging. Literal translation produces an unnatural proliferation of "seems," "perhaps," and "it is thought that."

---

## Theoretical Foundation

The skill's methodology is rooted in Gao Ning's *Japanese-Chinese Translation Course* (上海外语教育出版社, 2008), distilled into 20 executable skills via the book2skill pipeline.

### Three Governing Principles

> **"Getting it right comes before making it sound good"**—accuracy first, elegance second (p. 18)
>
> **"Interpret in Japanese, choose words in Chinese"**—meaning is determined by context, not by dictionary (p. 61)
>
> **"Revision proceeds from large to small"**—text → sentence → word; comprehension problems outweigh rhetoric problems (p. 425)

### 20 Distilled Skills

Four groups:

| Group | Skills | Applied In |
|-------|--------|-----------|
| **Translation awareness & context** (6) | Translation consciousness, anti-isolated-sentence principle, contextual appropriateness, mass vs personal context, dictionary use & word meaning, rational vs intuitive grasp | Preload + Phases 0-2 |
| **Structure & syntax** (4) | Contraction-expansion syntax, backward-propagation method, aesthetic constraint mechanism, macro-to-micro path | Phases 1-3 |
| **Word choice & polish** (6) | Multi-translation selection, comparative analysis, layered revision framework, back-translation training, rhetorical translation teaching, rhetorical awareness development | Phases 3-7 |
| **Style & genre** (4) | Style & translation, "good" recedes to "correct," comprehension as mother of technique, terminology system building | Phases 0-5 |

See [`ultra/SKILL_MAP.md`](ultra/SKILL_MAP.md) for the complete mapping between each skill and its workflow phase.

---

## Workflow Pipeline

jp-zh-max's workflow comprises **9 phases**, 6 of which incorporate specific skills from Gao Ning's methodology. The following is a structural overview; gate conditions and script paths are documented in [SKILL.md](SKILL.md).

### Preparation Phases

| Phase | Name | Responsibility |
|-------|------|---------------|
| **-1** | Project directory init | Create `source/`, move files, extract formats |
| **-0.5** | Methodology preload batch | Read 14 methodology SKILL.md files in one pass to establish a full-pipeline foundation |

### Core Translation Pipeline (Phases 0→6)

| Phase | Name | Responsibility |
|-------|------|---------------|
| **0** | Text analysis | Set domestication level (hard/mid/soft), write text-profile, three-layer style analysis, context analysis; apply translation consciousness, anti-isolated-sentence, style & translation frameworks |
| **1** | Comprehension & deverbalization | Strip Japanese surface forms, semantic还原, parse long attributive chains; annotate per-sentence freedom boundary for soft texts (aesthetic constraint mechanism) |
| **2** | First draft | Chinese word selection, SOV → SVO restructuring, keigo降维, two-step wasei-kango handling; apply dictionary use & word meaning + rational vs intuitive grasp |
| **3** | Polish diagnosis | Translationese cleanup (8 symptom classes), multi-translation selection, register alignment; divergence → convergence → selection for key sentences |
| **4** | Prosody polish | Read-aloud calibration, disyllabic/tetrasyllabic rhythm, pace restructuring (soft texts only) |
| **5** | Quality check | 14-item self-check, source-target comparison; apply comparative translation analysis + layered revision framework (4 layers) + back-translation training |
| **6** | Punctuation normalization | Mechanical: `normalize-punctuation-ja.py`, Japanese→Chinese fullwidth conversion |

### Delivery (Phase 8)

| Step | Responsibility |
|------|---------------|
| **8A** | Final cleanup: strip version markers, delete text-profile, add translator credit (`strip-version-markers.py`) |
| **8B** | Generate deliverables: bilingual MD/HTML/EPUB/MOBI |

### Parallel Translation for Long Texts

When single-pass translation exceeds 5,000 characters, the text is split by chapter/section into independent sub-tasks:

- **Phase A**: Parallel sub-agent translation (each executes Phases 0-6), tagged `[v3·Q✓]`
- **Phase B**: Merge, format cleanup, Japanese punctuation normalization
- **Phase C**: Full-text validation chain (global terminology consistency, prosodic continuity, AI pattern contamination detection)
- **Phase D**: Deliverable generation

---

## Validation Pipeline

After the translation is written to disk and before deliverables are generated, the following **4-step chain** must execute in order. Any failure → return to the relevant phase → re-run the chain. **No step may be skipped.**

```
Phase 6 (Punctuation Normalization)
       ↓
① scribe:prose-reviewer            — AI-isms / translationese / prosodic drift
       ↓
② verification-before-completion   — deliverable integrity + bilingual alignment
       ↓
③ humanizer                        — 4-dimension validation (Fidelity / Naturalness /
                                       Grammar / AI Patterns)
                                     + forced adversarial self-review
       ↓
④ humanizer-zh                     — Chinese AI-trace final review (24 rules)
       ↓
Phase 8 (Delivery)
```

### Step 1: scribe:prose-reviewer

Audits the Chinese translation for AI writing patterns, residual translationese, banned phrases, register drift, and structural monotony. **Advisory**—proposed edits are subject to final approval by humanizer (Step 3).

### Step 2: verification-before-completion

Full deliverable integrity check: MD/HTML completeness, punctuation residual (must be 0), bilingual segment alignment, source file presence in `source/`. Confirms operational state ("humanizer not yet executed," etc.).

For soft texts (freedom ≥ 4), inserts rhetorical skills after this step: rhetorical translation teaching + rhetorical awareness development.

### Step 3: humanizer

Splits the Chinese translation into chunks (3-5 paragraphs each) and runs 4-dimension validation on each:

- **Fidelity**: sentence-by-sentence source comparison (semantic equivalence, negation, modality, proper nouns)
- **Naturalness**: translationese, prosodic feel, register fit
- **Grammar**: collocation, punctuation, agreement
- **AI Patterns**: 29 AI writing pattern rules

After all chunks pass, executes **forced adversarial self-review**—re-examines every already-passed chunk from scratch to catch systematic blind spots.

humanizer has **final authority** over prose-reviewer's suggestions: approve, reject, or detect issues prose-reviewer missed.

### Step 4: humanizer-zh

Processes only Chinese translation lines (filters Japanese blockquote lines). Runs each chunk against **24 Chinese AI-trace rules** (4 categories × 6: content patterns / language grammar / style patterns / conversational fillers). Detects and fixes: AI high-frequency vocabulary, em-dash overuse, three-part parallelism, negative parallelism, copula avoidance, false scope, filler phrases, generic positive conclusions, etc.

**Role boundary**: humanizer ensures "correctness" (Fidelity + Naturalness + Grammar); humanizer-zh ensures "reads like human writing" (Chinese AI trace removal). The two are complementary and non-substitutable.

### Auto-fix Rules

Any error or issue discovered during the 4-step chain is **auto-fixed by default** and written directly into the bilingual MD file. No per-item approval is required. The corrected MD is the sole input source for Phase 8 deliverable generation (HTML/EPUB/MOBI).

---

## Quick Install

### Method 1: Clone to Claude Code skills directory (recommended)

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/ja-zh-max.git jp-zh-max
```

After cloning, all subdirectories (`references/`, `scripts/`, `ultra/`) are in place with self-consistent script paths.

### Method 2: Manual copy

Copy the following to `~/.claude/skills/jp-zh-max/`:

```
SKILL.md
references/
scripts/
ultra/
```

**Note**: Workflow scripts (`normalize-punctuation-ja.py`, `strip-version-markers.py`) and `ultra/` methodology files rely on relative path resolution. Manual copy must preserve the full directory structure, otherwise Phase 6 normalization and Phase 8A cleanup scripts will fail.

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (latest version recommended)
- Python 3.8+ (for `scripts/` helper scripts)
- Pandoc (optional, for EPUB/MOBI/PDF output)

---

## Quick Start

In Claude Code, make a translation request:

```
Translate this Japanese to Chinese:
(your Japanese text here)
```

Or translate from a file:

```
Translate this file to Chinese
```

Claude Code will automatically invoke the jp-zh-max skill and execute the full workflow pipeline. On first run, the methodology preload batch (Phase -0.5) loads automatically to establish the full-pipeline foundation.

---

## Project Structure

```
jp-zh-max/
├── SKILL.md                       # Runtime instructions: full workflow, gate conditions, script paths
├── README.md                      # This file
├── LICENSE                        # MIT
├── .gitignore
├── references/                    # Methodology documents (techniques, trap lists, text analysis)
│   ├── claude-code-deployment.md      # Claude Code deployment notes
│   ├── japanese-techniques.md         # Japanese→Chinese technique inventory
│   ├── japanese-text-analysis.md      # Japanese text analysis framework
│   ├── japanese-translationese-symptoms.md  # 8-class translationese symptom list
│   ├── libertine-vocabulary-ja.md      # Register-matched vocabulary for explicit content
│   ├── output-formats.md              # Deliverable generation scripts (HTML/EPUB/MOBI/PDF)
│   ├── project-init.md                # Phase -1 project init detailed steps
│   ├── revision-methodology.md        # Gao Ning's 3-layer revision methodology
│   ├── textbook-extraction-workflow.md # Textbook/book text extraction workflow
│   └── wasei-kango-traps.md           # Kanji lookalike trap list with cross-reference table
├── scripts/                       # Workflow helper scripts
│   ├── normalize-punctuation-ja.py    # Phase 6: Japanese→Chinese fullwidth conversion
│   ├── strip-version-markers.py       # Phase 8A: strip markers + cleanup + translator credit
│   └── bilingual-to-pdf.py            # Bilingual MD → PDF (on demand)
└── ultra/                         # Methodology components (Gao Ning 20-skill file mapping & diagram)
    ├── SKILL_MAP.md                   # 20-skill to workflow-phase mapping table (with skip rules)
    └── WORKFLOW.md                    # Translation workflow diagram (Mermaid, with validation chain)
```

---

## Contributing

**Maintainer:** [Lilipuut](https://github.com/3060226349kk-cmd) — project creator, responsible for core workflow design and methodology integration.

Contributions are welcome. The following guidelines explain the project structure and how to participate effectively.

### Setting Up a Development Environment

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Clone this repository to `~/.claude/skills/jp-zh-max/`

### Contribution Workflow

1. **Open an issue**: Describe the proposed change in [Issues](https://github.com/3060226349kk-cmd/ja-zh-max/issues) to avoid conflicting work
2. **Fork + Branch**: Create a feature branch from `master` (e.g. `fix/wasei-kango-typo`, `feat/new-reference`)
3. **Scope of changes**:
   - `SKILL.md`: phase gate conditions, script paths, methodology references
   - `references/*.md`: additions or corrections to technique inventories and trap lists
   - `scripts/*.py`: feature extensions or bug fixes
   - `ultra/*.md`: skill mapping table or workflow diagram updates
   - `README.md`: update Chinese and English versions simultaneously (precise symmetry)
4. **Commit**: prefix with scope tag (e.g. `[SKILL]`, `[REF]`, `[SCRIPT]`, `[ULTRA]`, `[DOC]`)
5. **PR**: link the issue, describe the change and verification method

### Code Conventions

- SKILL.md: preserve YAML frontmatter (`name`, `description`, `version`, `allowed-tools`); annotate phase gate conditions (entry/exit criteria)
- references/*.md: numbered list entries with source attribution (Gao Ning page numbers)
- scripts/*.py: Python 3.8+ compatible, zero external dependencies; resolve file paths via `$SKILL_DIR` env var or relative paths
- Cross-platform: scripts must run on Windows (git-bash), macOS, and Linux
- New methodology documents must register their phase mapping in `SKILL_MAP.md`

### Release Process

1. Bump version in `SKILL.md` YAML `version` field + README badge link
2. (Optional) Maintain a CHANGELOG for notable changes per release
3. Merge to `master`—the latest version is then available via `git clone`

---

## Acknowledgements

**Author:** [Lilipuut](https://github.com/3060226349kk-cmd) — overall architecture design, methodology integration, and implementation of jp-zh-max.

The skill's base framework derives from [en-zh-translation-polish](https://github.com/3060226349kk-cmd/en-zh-translation-polish), an English→Chinese translation polish skill. The original 7-stage workflow was expanded into a Japanese→Chinese specific edition.

Distillation of the 20 textbook skills was performed via the book2skill pipeline in [cangjie-skill](https://github.com/3060226349kk-cmd/cangjie-skill).

Special thanks to **Prof. Gao Ning**—his *Japanese-Chinese Translation Course* (上海外语教育出版社, 2008) provides the systematic theoretical foundation for this skill's methodology. The book's translation consciousness theory, context analysis framework, three-layer style analysis, contraction-expansion syntax, and backward-propagation method constitute the scholarly backbone of every phase in this skill.

The validation pipeline's `verification-before-completion` step is powered by [Superpowers](https://github.com/3060226349kk-cmd/superpowers), `scribe:prose-reviewer` by [scribe](https://github.com/3060226349kk-cmd/scribe), and `humanizer`/`humanizer-zh` by their respective validation skills. Thanks to each project's open architecture.

## License

MIT License — see [LICENSE](LICENSE).

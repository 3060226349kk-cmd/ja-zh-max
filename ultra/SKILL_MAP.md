# jp-zh-max Ultra 技能映射表

> 快速查阅：每个 jp-zh 阶段对应的 ultra 技能及执行方式。
> 完整设计见 `docs/superpowers/specs/2026-06-25-jp-zh-ultra-integration-design.md`
> 📊 翻译工作流流程图见 [`WORKFLOW.md`](WORKFLOW.md)（含校验链）

## 预读取批（P0）—— 阶段 -1 之后执行

一次性 Read 以下文件，建立方法论地基（不 invoke Skill）：

| # | 文件 | Read 路径 |
|---|------|-----------|
| 1 | INDEX | `jp-zh-ultra/INDEX.md` |
| 2 | 翻译意识 | `jp-zh-ultra/翻译意识/SKILL.md` |
| 3 | 反孤句原则 | `jp-zh-ultra/反孤句原则/SKILL.md` |
| 4 | 审美制约机制 | `jp-zh-ultra/审美制约机制/SKILL.md` |
| 5 | 宏观到微观路径 | `jp-zh-ultra/宏观到微观路径/SKILL.md` |
| 6 | 宏观把握微观把握 | `jp-zh-ultra/宏观把握微观把握/SKILL.md` |
| 7 | 理解是技巧之母 | `jp-zh-ultra/理解是技巧之母/SKILL.md` |
| 8 | 译得好回归译得对 | `jp-zh-ultra/译得好回归译得对/SKILL.md` |
| 9 | 语境适切原则 | `jp-zh-ultra/语境适切原则/SKILL.md` |
| 10 | 大众语境个人语境 | `jp-zh-ultra/大众语境个人语境/SKILL.md` |
| 11 | 辞书活用与词义 | `jp-zh-ultra/辞书活用与词义/SKILL.md` |
| 12 | 理性把握感性把握 | `jp-zh-ultra/理性把握感性把握/SKILL.md` |
| 13 | 缩扩句法 | `jp-zh-ultra/缩扩句法/SKILL.md` |
| 14 | 后推法 | `jp-zh-ultra/后推法/SKILL.md` |

## 阶段级 Invoke

| 阶段 | 技能 | Invoke 参数 | 触发条件 |
|------|------|------------|---------|
| 0 | 翻译意识 | `Skill("jp-zh-ultra/翻译意识")` | 始终 |
| 0 | 反孤句原则 | `Skill("jp-zh-ultra/反孤句原则")` | 始终 |
| 0 | 文体与翻译 | `Skill("jp-zh-ultra/文体与翻译")` | 始终 |
| 1 | 审美制约机制 | `Skill("jp-zh-ultra/审美制约机制")` | 软文本（自由度≥4）执行；硬文本跳过 |
| 2 | 辞书活用与词义 | `Skill("jp-zh-ultra/辞书活用与词义")` | 始终 |
| 2 | 理性把握感性把握 | `Skill("jp-zh-ultra/理性把握感性把握")` | 始终 |
| 3 | 同义句多译案选择 | `Skill("jp-zh-ultra/同义句多译案选择")` | 仅对 [v2·W] / [v2·S] 标记句执行 |
| 5 | 同源译文比较 | `Skill("jp-zh-ultra/同源译文比较")` | 关键段落 2-3 处 |
| 5 | 译文修改分层框架 | `Skill("jp-zh-ultra/译文修改分层框架")` | 始终 |
| 5 | 回译训练法 | `Skill("jp-zh-ultra/回译训练法")` | 关键段落 3-5 处 |
| 7 | 修辞翻译教学 | `Skill("jp-zh-ultra/修辞翻译教学")` | 软文本（自由度≥4）；硬文本跳过 |
| 7 | 修辞意识发展 | `Skill("jp-zh-ultra/修辞意识发展")` | 同上（配对 invoke） |

## 跳过规则速查

| 场景 | 跳过哪些 |
|------|---------|
| 硬文本（自由度 1-3） | 审美制约机制 invoke + 修辞双技能 invoke |
| 聊天小段翻译（不落盘） | 全部 ultra 接入（预读取 + invoke） |
| 用户要求快速出稿 | 全部 ultra 接入 |
| 短篇（< 2,000 字） | P0 预读取仅保留 INDEX.md + 6 个核心框架（#1-6） |

## ultra 技能依赖关系速查

```
翻译意识 ← 反孤句原则, 审美制约机制, 宏观到微观, 宏观把握微观, 理解是技巧之母, 译得好回归译得对
语境适切原则 ← 反孤句原则, 大众语境个人语境
辞书活用与词义 === 理性把握感性把握     (composes-with)
缩扩句法 === 后推法                     (composes-with)
同义句多译案选择 === 同源译文比较       (composes-with)
文体与翻译 === 回译训练法               (composes-with)
修辞翻译教学 === 修辞意识发展           (composes-with)
译文修改分层框架 ← 宏观到微观, 宏观把握微观
```

---
name: warm-paper-html-template
description: 暖纸质感 HTML 设计系统 V3 — 双语翻译对照/长文阅读/电子书风格；含进度条、侧边 TOC、封面区、双语对排版、深色模式、打印优化
metadata:
  node_type: memory
  type: reference
  originSessionId: 4eee29d3-02ac-44b8-b9f3-9df67cce6d43
---

# 暖纸质感 HTML 模板 V3（默认输出风格）

当前版本基于家畜人ヤプー V3.html 验证。适用于 en-zh-max 和 jp-zh-max 两套翻译技能的 HTML 输出。

## 设计特征

- 暖米白底色 `#faf8f5`，深灰正文 `#1e1e1e`
- 宋体系列：`Source Han Serif SC` / `Noto Serif CJK SC` / `STSong`
- 标题字体：`Public Sans` / `Noto Sans SC`
- 段落首行缩进两字、两端对齐（书本式排版）
- 深色模式完整适配
- 引用块：左侧驼色边框 + 浅米背景
- 注脚块：accent 色左边框

## 交互组件

1. **固定进度条**（顶部 3px，随滚动填充）
2. **侧边 TOC 面板**（左上 ☰ 按钮，滑入式，点击链接/外侧自动关闭）

## CSS 体系

### CSS 变量（完整原版）

```css
:root {
  --bg: #faf8f5;
  --text: #1e1e1e;
  --text-secondary: #555;
  --text-tertiary: #999;
  --border: #d8d0c8;
  --accent: #7a5c3a;
  --accent-light: #b8956a;
  --blockquote-bg: #f5f0ea;
  --blockquote-border: #c4b5a5;
  --note-bg: #f3eee7;
  --sep-color: #bbb;
  --link: #7a5c3a;
  --toc-bg: #f7f3ed;
  --toc-hover: #eee8df;
  --chapter-title-color: #4a3f35;
  --dropcap-color: #7a5c3a;
  --progress-bar: #d4c5b5;
  --progress-fill: #7a5c3a;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1c1a18;  --text: #d0d0d0;  --text-secondary: #aaa;
    --text-tertiary: #777;  --border: #444;
    --accent: #c9a84c;  --accent-light: #dbbb6a;
    --blockquote-bg: #252320;  --blockquote-border: #6a5d4e;
    --note-bg: #22201d;  --sep-color: #555;  --link: #c9a84c;
    --toc-bg: #242220;  --toc-hover: #33302b;
    --chapter-title-color: #c0b8ab;  --dropcap-color: #c9a84c;
    --progress-bar: #444;  --progress-fill: #c9a84c;
  }
}
```

### @page 打印

```css
@page { size: A4; margin: 20mm 18mm; }
```

### body 基础

```css
body {
  font-family: 'Source Han Serif SC', 'Noto Serif CJK SC', 'STSong', 'SimSun',
               'Noto Serif SC', 'Noto Sans SC', serif;
  font-size: 17px;
  line-height: 1.9;
  max-width: 860px;
  margin: 0 auto;
  padding: 0 28px 80px;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}
```

## 组件模板

### 封面区

```html
<div class="cover">
  <h1>书名</h1>
  <p class="sub">外语标题</p>
  <p class="desc" style="margin-top:30px;font-size:16px;font-weight:500;color:var(--text-secondary);">第X章　章名</p>
  <p class="desc" style="font-size:14px;color:var(--text-tertiary);">外语章名</p>
  <p class="credit">作者 ｜ 译者：Lilipuut + Claude</p>
</div>
```

CSS：
```css
.cover { text-align: center; padding: 80px 0 50px; position: relative; }
.cover::after {
  content: ''; display: block; width: 60px; height: 2px;
  background: var(--accent); margin: 30px auto 0;
}
.cover h1 {
  font-family: 'Public Sans', 'Noto Sans SC', -apple-system, sans-serif;
  font-size: 30px; font-weight: 700; letter-spacing: 4px;
  color: var(--chapter-title-color); margin: 0 0 6px;
}
.cover .sub {
  font-family: 'Public Sans', 'Noto Sans SC', -apple-system, sans-serif;
  font-size: 15px; font-weight: 300; color: var(--text-secondary);
  letter-spacing: 3px;
}
.cover .desc { font-size: 14px; color: var(--text-tertiary); line-height: 1.8; }
.cover .credit { font-size: 13px; color: var(--text-tertiary); margin-top: 16px; }
```

### 章标题

```html
<h1 class="chapter-title" id="chX">第X章　章名</h1>
```

CSS：
```css
h1.chapter-title {
  font-family: 'Public Sans', 'Noto Sans SC', -apple-system, sans-serif;
  font-size: 24px; font-weight: 600; text-align: center;
  margin: 50px 0 30px; padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
  color: var(--chapter-title-color); letter-spacing: 3px;
}
h1.chapter-title::after {
  content: ''; display: block; width: 40px; height: 2px;
  background: var(--accent); margin: 16px auto 0;
}
```

### 双语对（核心组件）

```html
<div class="pair">
  <blockquote>
    <p>原文（blockquote 内）</p>
  </blockquote>
  <div class="cn">
    中文译文，首行缩进两字。
  </div>
</div>
```

CSS：
```css
.pair { margin: 1em 0; page-break-inside: avoid; break-inside: avoid; }
.pair blockquote {
  font-family: 'Source Han Serif SC', 'Noto Serif CJK SC', 'STSong', 'SimSun', serif;
  font-size: 14.5px; line-height: 1.8;
  color: var(--text-secondary);
  border-left: 3px solid var(--blockquote-border);
  background: var(--blockquote-bg);
  padding: 0.4em 0.8em 0.4em 1.2em; margin: 0;
  border-radius: 0 4px 4px 0;
}
.pair blockquote p { margin: 0.25em 0; text-indent: 0; }
.pair blockquote sup, .pair .cn sup {
  font-size: 0.7rem; font-family: 'JetBrains Mono', 'Fira Code', monospace;
}
.pair .cn {
  font-family: 'Source Han Serif SC', 'Noto Serif CJK SC', 'STSong', 'SimSun', serif;
  font-size: 16px; line-height: 2; color: var(--text);
  padding-left: 0.8rem; margin: 0.2em 0;
  text-indent: 2em; text-align: justify;
}
```

### 注脚块

```html
<div class="notes">
  <p>[1] 注脚内容</p>
  <p>[2] 注脚内容</p>
</div>
```

CSS：
```css
.notes {
  padding: 0.6em 1.2em; margin: 0.8em 0 0.8em 1.5em;
  background: var(--note-bg);
  border-left: 2px solid var(--accent);
  border-radius: 0 4px 4px 0;
  font-size: 13px; line-height: 1.8; color: var(--text-secondary);
  page-break-inside: avoid; break-inside: avoid;
}
.notes p { margin: 0.2em 0; }
```

### 进度条

```html
<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>
```

CSS：
```css
.progress-container {
  position: fixed; top: 0; left: 0; right: 0;
  height: 3px; background: var(--progress-bar); z-index: 1000;
}
.progress-bar {
  height: 100%; width: 0%; background: var(--progress-fill);
  transition: width 0.2s ease;
}
```

### TOC 侧边面板

```html
<button class="toc-toggle" id="tocToggle" title="目录">☰</button>
<nav class="toc-panel" id="tocPanel">
  <h2>目录</h2>
  <a class="toc-chapter" href="#ch3">第三章　罗马：基础</a>
  <a class="toc-section" href="#p1">节标题</a>
</nav>
```

CSS（完整见原版，关键部分）：
```css
.toc-panel {
  position: fixed; top: 0; left: -320px;
  width: 300px; height: 100vh;
  background: var(--toc-bg);
  border-right: 1px solid var(--border);
  z-index: 999; overflow-y: auto;
  transition: left 0.3s ease;
  padding: 60px 16px 24px;
}
.toc-panel.open { left: 0; }
.toc-panel a.toc-chapter { font-weight: 600; margin-top: 4px; }
.toc-panel a.toc-section { padding-left: 24px; font-size: 13px; }
```

### JS 交互（三步）

```javascript
// 1. 滚动进度条
window.addEventListener('scroll', function() {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  document.getElementById('progressBar').style.width = progress + '%';
});

// 2. TOC 展开/收起
document.getElementById('tocToggle').addEventListener('click', function() {
  document.getElementById('tocPanel').classList.toggle('open');
});

// 3. TOC 链接点击关闭
document.querySelectorAll('.toc-panel a').forEach(function(link) {
  link.addEventListener('click', function() {
    document.getElementById('tocPanel').classList.remove('open');
  });
});

// 4. 点击外侧关闭
document.addEventListener('click', function(e) {
  const panel = document.getElementById('tocPanel');
  const toggle = document.getElementById('tocToggle');
  if (panel.classList.contains('open') && !panel.contains(e.target) && !toggle.contains(e.target)) {
    panel.classList.remove('open');
  }
});
```

### 分隔符

```css
.sep { text-align: center; color: var(--sep-color); font-size: 16px; margin: 1.5em 0; letter-spacing: 1em; }
```

```html
<div class="sep">· · ·</div>
```

### 译者署名

```html
<p style="text-align:center;color:var(--text-tertiary);font-size:13px;">译者：Lilipuut + Claude</p>
```

### @media print 降级

```css
@media print {
  body { background: white !important; padding: 0; max-width: none;
    -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .progress-container, .toc-toggle, .toc-panel { display: none !important; }
  .pair blockquote { background: #f7f5f0 !important; }
  .notes { background: #f8f5f0 !important; }
}
```

## 完整页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>标题</title>
<style>
/* === 完整 CSS 体系（复制上方全部） === */
</style>
</head>
<body>

<div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>

<button class="toc-toggle" id="tocToggle" title="目录">☰</button>
<nav class="toc-panel" id="tocPanel">
  <h2>目录</h2>
  <!-- TOC 条目 -->
</nav>

<div class="cover">
  <h1>书名</h1>
  <p class="sub">外语标题</p>
  <p class="credit">译者：Lilipuut + Claude</p>
</div>

<h1 class="chapter-title" id="ch1">第一章</h1>

<div class="pair">
  <blockquote><p>原文</p></blockquote>
  <div class="cn">译文</div>
</div>

<div class="sep">· · ·</div>
<p style="text-align:center;color:var(--text-tertiary);font-size:13px;">译者：Lilipuut + Claude</p>

<script>
/* === 完整 JS 交互（复制上方） === */
</script>
</body>
</html>
```

## 适用场景

- **翻​译文档**（英译中/日译中双语对照）的 HTML 输出
- 长文/书籍的 HTML 阅读版
- PDF 输出的样式蓝本

## 与其他设计系统的关系

本模板为 **翻译/小说类** 默认设计系统。`quiz-html-design-system.md`（CEU Academic Navy 海军蓝系）保留为试卷/测验类场景备选。

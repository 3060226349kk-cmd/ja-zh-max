# 阶段 -1：项目目录初始化（日→中）

> 仅在翻译整本书籍/文件时执行。聊天小段翻译跳过。

## 准入 / 准出

- ⚠ **准入：** 用户已提供待翻译内容（文件路径或直接文本）。无输入 = 退回用户索取。
- ✅ **准出：** `source/` 目录存在、原始文件已移入、提取产物已生成、归位验证三项断言全部通过。

## 步骤 1：创建项目目录与子目录

```python
import os, shutil

src_dir = r'C:\Users\<用户名>\Downloads'   # ← 替换为实际下载路径
book_name = '《项目书籍名称》'           # ← 替换为实际书名
project_dir = os.path.join(src_dir, book_name)
source_dir = os.path.join(project_dir, 'source')
bilingual_dir = os.path.join(project_dir, 'bilingual')

os.makedirs(source_dir, exist_ok=True)
os.makedirs(bilingual_dir, exist_ok=True)
```

## 步骤 2：将原始电子书移入 source/

```python
original_file = os.path.join(src_dir, '原书名.epub')   # ← 替换为实际文件名
target_path = os.path.join(source_dir, os.path.basename(original_file))
shutil.move(original_file, target_path)
print(f'原始ファイルを移動しました: {target_path}')
```

> ⚠ **必须用 `shutil.move`（移动），不是 `shutil.copy`（复制）。**

## 步骤 3：从 source/ 内的文件提取文本

```python
import subprocess

epub_path = os.path.join(source_dir, '原书名.epub')
md_path = os.path.join(source_dir, '原书名.md')
pandoc = r'C:\pandoc-3.9\pandoc.exe'
subprocess.run([pandoc, epub_path, '-t', 'markdown', '--wrap=none', '-o', md_path], check=True)
print(f'Markdown に変換しました: {md_path}')
```

其他格式的提取命令：

| 格式 | 工具 | 命令要点 |
|------|------|---------|
| `.epub` | Pandoc | `-t markdown --wrap=none`，保留标题层级 |
| `.docx` / `.html` / `.md` | Pandoc | 同上 |
| `.azw3` | Calibre `ebook-convert` | `D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe` |
| `.mobi` | Python `mobi` 模块 | 输出 Markdown，保留标题层级 |
| `.pdf` | PyMuPDF (`fitz`) 或 `marker-pdf` OCR | 详见 `references/textbook-extraction-workflow.md` |

## 步骤 4：归位验证 ★ 落盘前必检

```python
root_files = os.listdir(src_dir)
source_files = os.listdir(source_dir)

# 检查 1：原始电子书在 source/ 内
orig_name = os.path.basename(original_file)
assert orig_name in source_files, \
    f'❌ 原始ファイルが source/ に移動されていません：{orig_name}'

# 检查 2：根层级无同名残留
residual = [f for f in root_files if f == orig_name]
assert len(residual) == 0, f'❌ 原始ファイルがルート階層に残留しています：{residual}'

# 检查 3：提取产物无散落
extracted = [f for f in root_files
             if f.endswith(('.txt', '.md', '.html'))
             and book_name[1:-1] in f]
assert len(extracted) == 0, f'❌ 抽出ファイルがルート階層に散在しています：{extracted}'

print('✅ ファイル帰位検証通過')
```

## 完成后的目标目录结构

```
源文件所在ディレクトリ（例：Downloads）/
  └── 《プロジェクト書籍名》/
      ├── source/                          ← 元の電子書籍 + 抽出テキスト
      │   ├── 元の書籍.epub
      │   ├── 原書名.md
      │   └── ...
      ├── bilingual/                       ← サブエージェントの生出力
      ├── 《書籍名》 翻译(日中对照).md
      ├── 《書籍名》 翻译(日中对照).html
      ├── 《書籍名》 翻译(全中文).md       （オプション）
      ├── 《書籍名》 译文.epub
      └── 《書籍名》 译文.mobi
```

- フォルダ名は中国語書名
- **いかなるファイルもルート階層に散在させない**
- **並行翻訳時**：delegate_task に正しい `project_dir` パスを渡すこと

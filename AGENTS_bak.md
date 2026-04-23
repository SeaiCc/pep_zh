# PEP 补全计划 - 项目架构

# 项目根目录
path:\\to\\your\\project

## 概述
本项目用于下载、转换和翻译 Python PEP (Python Enhancement Proposal) 文档为本地 Markdown 格式。

## 目录结构

```
.
├── pep_html/      # 原始 HTML 格式的 PEP 文档（下载源）
├── pep_en/        # 转换后的英文 Markdown 文档
├── pep_zh/        # 中文翻译的 Markdown 文档（待完成）
├── pep_en_bak/    # 英文文档备份
├── list.md        # PEP 编号列表（共 89 个 PEP，已去重排序）
├── link.md        # PEP 官方链接列表
├── list_bak.md    # PEP 列表备份
├── convert_pep.py # HTML 到 Markdown 转换脚本
└── translate_pep.py # 翻译脚本（未完整实现）
```

## 主要脚本

### convert_pep.py
HTML 到 Markdown 转换器。

**输入**: `pep_html/pep_*.html` 文件
**输出**: `pep_en/PEP {num}.md` 文件

**用法**:
```bash
python convert_pep.py
```

**功能**:
- 提取 PEP 标题和元数据（Author, Status, Type 等）
- 转换为 Markdown 格式（标题、列表、代码块、引用等）
- 清理 HTML 特殊字符和多余空白

### translate_pep.py
翻译脚本（未完整实现，仅读取文件示例）。

**注意**: 当前版本仅读取文件并打印内容，翻译功能待实现。

## PEP 来源
所有 PEP 文档来自官方站点：https://peps.python.org/

## 运行要求
- Python 3.x
- 已下载并存放于 `pep_html/` 的 PEP HTML 文件

## 翻译工作流程

### 翻译 PEP 文件

翻译 PEP 文档时，请遵循以下流程：

1. **读取源文件**: 从 `pep_en/PEP_XXXX.md` 读取英文内容
2. **翻译**: 使用 LLM 自带能力翻译成中文（不调用外部 API）
3. **保存**: 输出到 `pep_zh/PEP_XXXX.md`，保持相同文件名格式

### 翻译注意事项

- 保持 Markdown 格式（标题、列表、代码块、引用等）
- 保留元数据字段名（如 `Author`、`Status`、`Type` 等），仅翻译值
- 保留代码示例、链接、PEP 引用编号（如 PEP 8、PEP 20）
- 技术术语可使用英文或通用中文译名
- 保持原文的章节结构和层次

### 示例命令流程

```
1. 读取：pep_en/PEP_0001.md
2. 翻译为中文
3. 保存：pep_zh/PEP_0001.md
```

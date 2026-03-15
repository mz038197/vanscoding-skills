# Vanscoding Skills Repository

一個包含多個 AI 技能的綜合技能庫，組織成不同的分類以便於管理和使用。

[English](#english-version) | [中文](#中文版本)

---

## 中文版本

### 簡介

**Vanscoding Skills** 是一個專業的 AI 技能庫，為文檔處理和生產力工具集成提供完整的支援。這個 monorepo 包含了多個精心設計的技能模組，可以獨立安裝和使用。

### 專案架構

```
vanscoding-skills/
│
├── README.md                   # 專案說明（此檔案）
├── LICENSE                     # 專案授權條款
│
├── Documents/                  # 文檔處理技能分類
│   ├── word/                   # Word 文檔處理
│   │   ├── SKILL.md
│   │   ├── scripts/            # 輔助腳本
│   │   ├── ooxml/              # OOXML 標準定義
│   │   └── LICENSE.txt
│   │
│   ├── pdf/                    # PDF 檔案操作
│   │   ├── SKILL.md
│   │   ├── forms.md            # 表單填充指南
│   │   ├── reference.md        # 進階參考
│   │   ├── scripts/            # PDF 處理工具
│   │   └── LICENSE.txt
│   │
│   ├── pptx/                   # PowerPoint 簡報
│   │   ├── SKILL.md
│   │   ├── scripts/            # 投影片操作
│   │   ├── ooxml/              # OOXML 架構
│   │   └── LICENSE.txt
│   │
│   ├── xlsx/                   # Excel 試算表
│   │   ├── SKILL.md
│   │   ├── recalc.py           # 公式重新計算
│   │   └── LICENSE.txt
│   │
│   ├── google-sheets/          # Google 試算表
│   │   ├── SKILL.md
│   │   └── scripts/
│   │
│   └── agent-soul-crafter/     # AI 代理人格設計
│       ├── SKILL.md
│       └── _meta.json
│
└── Productivity/               # 生產力工具整合分類
    ├── google-email/           # Gmail 電子郵件管理
    │   ├── SKILL.md
    │   └── scripts/            # OAuth、附件處理
    │
    └── google-calendar/        # Google 日曆整合
        ├── SKILL.md
        └── scripts/
```

### 技能概覽

#### 📄 文檔處理（Documents）

| 技能 | 描述 | 功能 |
|------|------|------|
| **word** | Word 文檔處理 | 建立、編輯、追蹤變更、評論、格式化 |
| **pdf** | PDF 檔案操作 | 表單填充、文字提取、圖像轉換、欄位檢查 |
| **pptx** | PowerPoint 簡報 | 投影片操作、OOXML 處理、HTML 轉換 |
| **xlsx** | Excel 試算表 | 公式、格式、資料分析、重新計算 |
| **google-sheets** | Google 試算表 | 試算表整合、資料管理 |
| **agent-soul-crafter** | AI 代理人格 | 設計 AI 代理的個性和行為 |

#### 🚀 生產力工具（Productivity）

| 技能 | 描述 | 功能 |
|------|------|------|
| **google-email** | Gmail 電子郵件 | OAuth 認證、附件下載、訊息管理 |
| **google-calendar** | Google 日曆 | 日曆操作、行程管理 |

### 使用方式

#### 安裝特定技能

每個技能都可以獨立使用。選擇你需要的技能資料夾位置：

```bash
# 例如：安裝 Word 文檔處理技能
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/word
```

#### 技能檔案結構

每個技能都包含：

- **SKILL.md** - 技能定義和使用指南
- **scripts/** - 相關的輔助程式和工具
- **LICENSE.txt** - 授權條款（如適用）
- **參考文件** - 詳細的技術文件

### 技能特性

✨ **完整的文檔支援**
- 支援所有主要辦公文檔格式（Word、PDF、PowerPoint、Excel）
- 包含 OOXML 標準定義和驗証工具

🔧 **豐富的工具集**
- Python 腳本用於自動化任務
- JavaScript 工具用於前端處理
- 完整的 API 參考

☁️ **雲端整合**
- Google 套件集成（Gmail、Google 日曆、Google 試算表）
- OAuth 認證支援

📚 **詳細文件**
- 每個技能都有完整的 SKILL.md 說明
- 進階參考和範例代碼
- 使用指南和最佳實踐

### 授權

本專案遵循 Anthropic 的授權條款。詳見 [LICENSE](./LICENSE) 檔案。

個別技能可能有其特定的授權條款，請查看各技能資料夾內的 LICENSE.txt 檔案。

### 專案優勢

✅ **集中管理** - 所有技能在一個倉庫中，易於維護  
✅ **清晰分類** - 按用途分為文檔處理和生產力工具  
✅ **獨立安裝** - 只安裝你需要的技能  
✅ **版本控制** - 完整的 Git 歷史和標籤支援  
✅ **教育友好** - 適合教室和學習環境使用  

### 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個專案！

### 聯絡方式

有任何問題或建議，請通過 GitHub Issues 聯絡我們。

---

## English Version

### Introduction

**Vanscoding Skills** is a comprehensive AI skill library providing complete support for document processing and productivity tool integration. This monorepo contains multiple carefully designed skill modules that can be installed and used independently.

### Project Structure

The repository is organized into two main categories:

- **Documents/** - Document processing skills (Word, PDF, PowerPoint, Excel, Google Sheets)
- **Productivity/** - Productivity tool integration (Gmail, Google Calendar)

Each skill is self-contained with its own SKILL.md, scripts, and documentation.

### Available Skills

#### 📄 Document Processing

- **word** - Word document processing with change tracking and comments
- **pdf** - PDF manipulation including form filling and text extraction
- **pptx** - PowerPoint presentation handling with OOXML support
- **xlsx** - Excel spreadsheet with formulas and data analysis
- **google-sheets** - Google Sheets integration
- **agent-soul-crafter** - AI agent personality design

#### 🚀 Productivity Tools

- **google-email** - Gmail integration with OAuth and attachment handling
- **google-calendar** - Google Calendar management

### Installation

Install a specific skill from the repository:

```bash
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/word
```

### License

This project follows Anthropic's licensing terms. See the [LICENSE](./LICENSE) file for details.

Individual skills may have their own license terms. Check the LICENSE.txt file in each skill's folder.

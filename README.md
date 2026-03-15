# Vanscoding Skills Repository

一個包含多個 AI 技能的綜合技能庫，組織成不同的分類以便於管理和使用。

[English](#english-version) | [中文](#中文版本)

---

## 中文版本

### 簡介

**Vanscoding Skills** 是一個專業的 AI 技能庫，為文檔處理和生產力工具集成提供完整的支援。這個 monorepo 包含了多個精心設計的技能模組，可以獨立安裝和使用。

### 專案架構

```
vanscoding-skills/                     # Monorepo 根目錄
│
├── README.md                          # 專案說明（此檔案）
├── LICENSE                            # MIT 授權條款
├── CONTRIBUTING.md                    # 貢獻指南
├── .gitignore                         # Git 忽略規則
│
├── Documents/                         # 📄 文檔處理技能分類
│   │
│   ├── word/                          # Word 文檔處理技能
│   │   ├── SKILL.md                  # 技能定義和使用指南
│   │   ├── LICENSE.txt               # Anthropic 授權條款
│   │   ├── docx-js.md                # JavaScript DOCX 文件
│   │   ├── ooxml.md                  # OOXML 參考文件
│   │   ├── scripts/                  # Python 輔助腳本
│   │   │   ├── __init__.py
│   │   │   ├── document.py           # 文檔操作函式
│   │   │   ├── utilities.py          # 工具函式
│   │   │   └── templates/            # XML 模板
│   │   └── ooxml/                    # OOXML 標準定義和驗証
│   │       ├── schemas/              # XSD 架構檔案
│   │       │   ├── ISO-IEC29500-4_2016/
│   │       │   ├── ecma/fouth-edition/
│   │       │   ├── microsoft/
│   │       │   └── mce/
│   │       └── scripts/              # OOXML 工具腳本
│   │
│   ├── pdf/                           # PDF 檔案操作技能
│   │   ├── SKILL.md                  # 技能定義和使用指南
│   │   ├── LICENSE.txt               # 授權條款
│   │   ├── forms.md                  # 表單填充完整指南
│   │   ├── reference.md              # 進階功能參考
│   │   └── scripts/                  # Python PDF 工具
│   │       ├── extract_form_field_info.py
│   │       ├── check_fillable_fields.py
│   │       ├── fill_fillable_fields.py
│   │       ├── convert_pdf_to_images.py
│   │       └── 其他工具...
│   │
│   ├── pptx/                          # PowerPoint 簡報技能
│   │   ├── SKILL.md                  # 技能定義和使用指南
│   │   ├── LICENSE.txt               # 授權條款
│   │   ├── html2pptx.md              # HTML 轉 PPTX 指南
│   │   ├── ooxml.md                  # OOXML 參考文件
│   │   ├── scripts/                  # Python 和 JavaScript 工具
│   │   │   ├── thumbnail.py
│   │   │   ├── replace.py
│   │   │   ├── rearrange.py
│   │   │   ├── inventory.py
│   │   │   └── html2pptx.js
│   │   └── ooxml/                    # OOXML 標準和驗証工具
│   │
│   ├── xlsx/                          # Excel 試算表技能
│   │   ├── SKILL.md                  # 技能定義和使用指南
│   │   ├── LICENSE.txt               # 授權條款
│   │   └── recalc.py                 # 公式重新計算工具
│   │
│   ├── google-sheets/                 # Google 試算表整合技能
│   │   ├── SKILL.md                  # 技能定義和使用指南
│   │   └── scripts/
│   │       └── cli.py                # Google Sheets CLI 工具
│   │
│   └── agent-soul-crafter/            # AI 代理人格設計技能
│       ├── SKILL.md                  # 技能定義和使用指南
│       └── _meta.json                # 元資料
│
└── Productivity/                      # 🚀 生產力工具整合分類
    │
    ├── google-email/                  # Gmail 電子郵件管理技能
    │   ├── SKILL.md                  # 技能定義和使用指南
    │   └── scripts/
    │       ├── oauth_cli.py           # OAuth 認証工具
    │       ├── list_messages.py       # 列出郵件訊息
    │       ├── download_attachments.py # 下載附件
    │       └── send_test.py           # 發送測試郵件
    │
    └── google-calendar/               # Google 日曆整合技能
        ├── SKILL.md                  # 技能定義和使用指南
        └── scripts/
            └── oauth_cli.py           # OAuth 認証工具
```

#### 架構說明

**目錄分類邏輯：**
- **Documents/** - 文檔和檔案處理相關的 6 個技能模組
- **Productivity/** - 雲端工具和生產力軟體的 2 個技能模組

**每個技能的標準結構：**
- `SKILL.md` - 必要檔案，包含技能定義、使用指南和範例
- `scripts/` - 實用工具和輔助程式
- `LICENSE.txt` - 授權條款（如適用）
- 其他文件 - 參考資料、指南、架構定義等

**共計：**
- 8 個可獨立安裝的技能模組
- 141 個檔案（涵蓋腳本、文件、架構定義）
- 54,644+ 行程式碼和文件

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

#### 🚀 快速開始

1. **查看可用技能**
   
   瀏覽 [Documents](./Documents/) 和 [Productivity](./Productivity/) 資料夾，查看所有可用的技能。

2. **安裝特定技能**
   
   每個技能都可以獨立使用。選擇你需要的技能，使用該技能資料夾的完整 GitHub URL：

3. **查看技能說明**
   
   安裝後，閱讀技能中的 `SKILL.md` 檔案以了解使用方式。

#### 📦 完整安裝命令

**文檔處理技能：**

```bash
# Word 文檔處理
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/word

# PDF 檔案操作
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/pdf

# PowerPoint 簡報
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/pptx

# Excel 試算表
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/xlsx

# Google 試算表
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/google-sheets

# AI 代理人格設計
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/agent-soul-crafter
```

**生產力工具技能：**

```bash
# Gmail 電子郵件管理
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Productivity/google-email

# Google 日曆整合
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Productivity/google-calendar
```

#### 技能檔案結構

每個技能都包含：

- **SKILL.md** - 技能定義和使用指南
- **scripts/** - 相關的輔助程式和工具
- **LICENSE.txt** - 授權條款（如適用）
- **參考文件** - 詳細的技術文件（如 reference.md、forms.md 等）

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

歡迎提交 Issue 和 Pull Request 來改進這個專案！詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

### 常見問題（FAQ）

**Q: 我可以同時安裝多個技能嗎？**

A: 可以！每個技能都是獨立的，你可以根據需要安裝多個技能。它們不會互相衝突。

**Q: 這些技能需要付費嗎？**

A: 不需要。所有技能都是基於開源或 Anthropic 授權的材料，可以免費使用。具體授權詳見各技能資料夾內的 LICENSE.txt。

**Q: 如何更新已安裝的技能？**

A: 技能的更新通常需要重新安裝。建議定期檢查本倉庫的更新。

**Q: Word 和 PDF 技能支援哪些功能？**

A: 
- **Word** 技能支援：建立、編輯、追蹤變更、評論、格式化、OOXML 處理
- **PDF** 技能支援：表單填充、文字提取、圖像轉換、欄位檢查、元資料提取

**Q: Google 工具技能需要認証嗎？**

A: 需要。Google 相關技能需要 OAuth 認証。每個技能的 scripts/ 資料夾中都有 `oauth_cli.py` 工具來處理認証流程。

**Q: 技能文件在哪裡找？**

A: 每個技能都有：
- `SKILL.md` - 基本使用指南
- `reference.md` 或類似的檔案 - 進階參考
- `forms.md` 或類似的檔案 - 特定功能的詳細指南

**Q: 如何報告錯誤或提出功能建議？**

A: 請在本倉庫開啟 Issue。我們歡迎所有的反饋和建議！

### 進階用法

#### 在本地開發技能

如果你想修改或擴展某個技能：

1. Fork 本倉庫
2. 在你的 fork 中修改技能
3. 在本地測試
4. 提交 Pull Request

#### 技能目錄結構最佳實踐

建立新技能時，遵循以下結構：

```
your-skill/
├── SKILL.md                # 必要：技能定義
├── LICENSE.txt             # 授權條款
├── README.md              # 可選：額外說明
├── scripts/               # Python/JavaScript 工具
│   ├── __init__.py
│   └── tool.py
└── docs/                  # 可選：詳細文件
    ├── reference.md
    ├── examples.md
    └── api.md
```

#### 版本控制和標籤

本倉庫使用語義化版本控制。主要版本標籤用於課堂版本：

```bash
git tag v1.0.0  # 第一個穩定版本
git tag v2.0.0  # 重大更新
```

### 聯絡方式

有任何問題或建議，請通過以下方式聯絡我們：

- 📧 GitHub Issues - 報告錯誤或提出功能建議
- 💬 GitHub Discussions - 一般性問題和討論
- 📝 Pull Requests - 提交改進

---

## English Version

### Introduction

**Vanscoding Skills** is a comprehensive AI skill library providing complete support for document processing and productivity tool integration. This monorepo contains multiple carefully designed skill modules that can be installed and used independently.

### Project Structure

The repository is organized into two main categories:

- **Documents/** - Document processing skills (6 modules)
  - word: Word document processing
  - pdf: PDF file manipulation
  - pptx: PowerPoint presentations
  - xlsx: Excel spreadsheets
  - google-sheets: Google Sheets integration
  - agent-soul-crafter: AI agent personality design

- **Productivity/** - Productivity tool integration (2 modules)
  - google-email: Gmail management
  - google-calendar: Google Calendar integration

Each skill is self-contained with its own SKILL.md, scripts, and documentation.

### Available Skills

#### 📄 Document Processing

| Skill | Description | Features |
|-------|-------------|----------|
| **word** | Word document processing | Create, edit, track changes, comments, formatting |
| **pdf** | PDF file manipulation | Form filling, text extraction, image conversion |
| **pptx** | PowerPoint presentations | Slide operations, OOXML processing, HTML conversion |
| **xlsx** | Excel spreadsheets | Formulas, formatting, data analysis |
| **google-sheets** | Google Sheets integration | Spreadsheet management, data handling |
| **agent-soul-crafter** | AI agent personality | Design agent personality and behavior |

#### 🚀 Productivity Tools

| Skill | Description | Features |
|-------|-------------|----------|
| **google-email** | Gmail management | OAuth authentication, attachment handling, message management |
| **google-calendar** | Google Calendar integration | Calendar operations, schedule management |

### Installation

Install a specific skill from the repository using its GitHub URL:

```bash
# Example: Install Word document processing skill
npx skills add https://github.com/mz038197/vanscoding-skills/tree/main/Documents/word

# Install all document processing skills:
# pdf, pptx, xlsx, google-sheets, agent-soul-crafter

# Install all productivity tools:
# google-email, google-calendar
```

### License

This project follows Anthropic's licensing terms. See the [LICENSE](./LICENSE) file for details.

Individual skills may have their own license terms. Check the LICENSE.txt file in each skill's folder.

### Key Features

✨ **Complete Document Support**
- Support for all major office document formats (Word, PDF, PowerPoint, Excel)
- Includes OOXML standard definitions and validation tools

🔧 **Rich Toolset**
- Python scripts for automation tasks
- JavaScript tools for frontend processing
- Complete API references

☁️ **Cloud Integration**
- Google Suite integration (Gmail, Google Calendar, Google Sheets)
- OAuth authentication support

📚 **Detailed Documentation**
- Each skill has comprehensive SKILL.md documentation
- Advanced references and code examples
- Usage guides and best practices

### Project Advantages

✅ **Centralized Management** - All skills in one repository for easy maintenance  
✅ **Clear Organization** - Categorized by document processing and productivity tools  
✅ **Independent Installation** - Install only the skills you need  
✅ **Version Control** - Complete Git history and tag support  
✅ **Education-Friendly** - Suitable for classroom and learning environments  

### Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Frequently Asked Questions

**Q: Can I install multiple skills?**

A: Yes! Each skill is independent and can be installed without conflicts.

**Q: Are these skills free?**

A: Yes! All skills are based on open-source or Anthropic-licensed materials and are free to use.

**Q: How do I update installed skills?**

A: Check this repository regularly for updates and reinstall skills as needed.

**Q: Do Google tools require authentication?**

A: Yes. Google-related skills require OAuth authentication. Each skill includes an oauth_cli.py tool in its scripts/ folder.

### Contact

For questions or suggestions, please:

- 📧 Open an Issue - Report bugs or request features
- 💬 Start a Discussion - General questions and discussions
- 📝 Submit a Pull Request - Contribute improvements

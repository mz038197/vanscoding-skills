# Vanscoding Skills Repository

一個包含多個 AI 技能的綜合技能庫，組織成不同的分類以便於管理和使用。

[English](#english-version) | [中文](#中文版本)

---

## 中文版本

### 簡介

**Vanscoding Skills** 是一個專業的 AI 技能庫，涵蓋文檔處理、Microsoft MarkItDown 轉 Markdown、Obsidian 整合、進階技能工程化、瀏覽器與網頁自動化（含 Webwright code-as-action、Playwright CLI）、網路搜尋與查證（Felo CLI）、媒體創作、電腦視覺與人臉辨識、教學課務流程（含凡思 PEAS 陪練／教練／VTuber MVP 陪練／Workshop Bridge **WG-13～22**）、Agent 設定引導、開發與 Git 工作流程、Nanobot 整合、Readmoo 階段一匯出與生產力工具。本 monorepo 包含 30 個可獨立安裝的技能模組。

### 專案架構

```
vanscoding-skills/                     # Monorepo 根目錄
│
├── README.md                          # 專案說明（此檔案）
├── LICENSE                            # MIT 授權條款
├── CONTRIBUTING.md                    # 貢獻指南
├── .gitignore                         # Git 忽略規則
│
├── Documents/                         # 📄 文檔與 Agent 引導技能
│   ├── word/                          # Word 文檔處理
│   ├── pdf/                           # PDF 檔案操作
│   ├── pptx/                          # PowerPoint 簡報
│   ├── xlsx/                          # Excel 試算表
│   ├── google-sheets/                 # Google 試算表整合
│   ├── markitdown-guide/              # Microsoft MarkItDown（多格式轉 Markdown）
│   ├── agent-soul-crafter/            # SOUL.md 人格設計引導
│   ├── agents-md-guide/               # AGENTS.md 建構引導
│   ├── user-md-guide/                 # USER.md 建構引導
│   ├── obsidian-cli/                  # Obsidian vault 讀寫與自動化（obsidian CLI）
│   ├── skill-creator/                 # Skill 建立基礎指南（init／package／驗證腳本）
│   └── skill-creator-advanced/        # Skill 建立進階：evals、benchmark 與打包迭代
│
├── Browser/                           # 🌐 瀏覽器與網頁自動化
│   ├── browser-use/                   # Browser Use Cloud SDK（操作瀏覽器、爬取、自動化）
│   ├── chrome-devtools/               # Chrome DevTools MCP（除錯、自動化、效能與網路）
│   ├── webwright/                     # Webwright code-as-action（本機 Playwright、截圖與 action log 驗證）
│   └── playwright-cli/
│       └── playwright-cli/            # Playwright CLI（快照、互動、測試）
│
├── Developer/                         # 🛠️ 開發與 Git 工作流程
│   ├── git-pr-description/            # 依 branch 差異產生 PR Title／Description
│   └── git-smart-commit/              # 依邏輯拆分 conventional commit
│
├── Media/                             # 🎵 媒體與創作
│   └── ace-music/                     # ACE Music AI 音樂生成
│
├── Vision/                            # 👁️ 電腦視覺與人臉
│   └── facenet-cli/                   # facenet-pytorch CLI（`fnet`：embedding、比對、JSON）
│
├── Search/                            # 🔍 搜尋與資訊檢索
│   └── felo-cli/                      # Felo CLI／API（`@willh/felo-cli --json`、FELO_API_KEY）
│
├── Teacher/                           # 📚 教學與課務
│   ├── orangeapple-class-report/      # 橘子蘋果課後學習表現報告流程
│   ├── peas-example-coach/            # 凡思陪練（清單、思考格、PEAS 開場、理解評估摘要）
│   ├── peas-challenge-coach/          # 凡思教練（challenges、六欄 prompt、程式＋理解驗收）
│   ├── peas-vtuber-coach/             # 凡思 VTuber 陪練（Agent Studio PNGtuber 四狀態 GIF + TTS MVP）
│   └── peas-workshop-advanced-coach/  # 凡思 Workshop Bridge 教練（WG-13～22 路由、bridge 卡、WG-22 拆檔）
│
├── nanobot/                           # 🤖 Nanobot 整合
│   └── setup-line-channel/            # LINE Messaging API channel 設定
│
└── Productivity/                      # 🚀 生產力工具整合
    ├── google-email/                  # Gmail 電子郵件管理
    ├── google-calendar/               # Google 日曆整合
    └── readmoo-capture/               # Readmoo 網頁版階段一截圖匯出（Playwright）
```

#### 架構說明

**目錄分類邏輯：**

- **Documents/** - 文檔處理、Agent 設定引導、MarkItDown、Obsidian 與 skill 工程（12 個技能）
- **Browser/** - 瀏覽器操作與網頁自動化（4 個技能）
- **Developer/** - 開發與 Git 工作流程（2 個技能）
- **Media/** - 媒體生成與創作（1 個技能）
- **Vision/** - 電腦視覺與人臉辨識（1 個技能）
- **Search/** - 搜尋、查證與即時資訊（1 個技能）
- **Teacher/** - 教學與課務流程（5 個技能）
- **nanobot/** - Nanobot 專案相關整合（1 個技能）
- **Productivity/** - 雲端工具與生產力（3 個技能）

**每個技能的標準結構：**

- `SKILL.md` - 必要檔案，包含技能定義、使用指南和範例
- `scripts/` - 實用工具和輔助程式（如適用）
- `LICENSE.txt` - 授權條款（如適用）
- 其他文件 - 參考資料、指南、架構定義等

**共計：** 30 個可獨立安裝的技能模組

### 技能概覽

#### 📄 文檔與 Agent 引導（Documents）


| 技能                         | 描述            | 功能                                                                                                 |
| -------------------------- | ------------- | -------------------------------------------------------------------------------------------------- |
| **word**                   | Word 文檔處理     | 建立、編輯、追蹤變更、評論、格式化                                                                                  |
| **pdf**                    | PDF 檔案操作      | 表單填充、文字提取、圖像轉換、欄位檢查                                                                                |
| **pptx**                   | PowerPoint 簡報 | 投影片操作、OOXML 處理、HTML 轉換                                                                             |
| **xlsx**                   | Excel 試算表     | 公式、格式、資料分析、重新計算                                                                                    |
| **google-sheets**          | Google 試算表    | 試算表整合、資料管理                                                                                         |
| **markitdown-guide**       | MarkItDown 指南 | microsoft/markitdown：多格式轉 Markdown、CLI／API、外掛與 Office／圖像流程                                         |
| **agent-soul-crafter**     | AI 代理人格       | 設計 AI 代理的個性和行為                                                                                     |
| **agents-md-guide**        | AGENTS.md 引導  | 階段式建構 AGENTS.md（核心、記憶、心跳）                                                                          |
| **user-md-guide**          | USER.md 引導    | 建構給 agent 用的個人設定檔（人本＋結構化）                                                                          |
| **obsidian-cli**           | Obsidian CLI  | 讀寫 vault、搜尋、任務、搬移／更名、斷鏈與孤立筆記                                                                       |
| **skill-creator**          | Skill 建立指南    | SKILL.md 結構、scripts／references／assets、漸進式揭露；`init_skill.py`、`package_skill.py`、`quick_validate.py` |
| **skill-creator-advanced** | 進階 Skill 建立   | 命名、邊界、evals、benchmark、驗證與打包迭代流程（可與 skill-creator 搭配）                                               |


#### 🌐 瀏覽器與網頁自動化（Browser）


| 技能                  | 描述                  | 功能                                         |
| ------------------- | ------------------- | ------------------------------------------ |
| **browser-use**     | Browser Use         | 操作瀏覽器、爬取網頁、網頁自動化（Cloud / Open Source）      |
| **chrome-devtools** | Chrome DevTools MCP | 透過 MCP 除錯網頁、自動化互動、分析效能、檢視網路請求              |
| **webwright**       | Webwright           | code-as-action：本機 Playwright 逐步執行、`final_runs/run_<id>/` 截圖與 action log、CP 自我驗證 |
| **playwright-cli**  | Playwright CLI      | `playwright-cli` 指令：開啟頁面、快照、點擊輸入、測試與 trace |


#### 🛠️ 開發與 Git 工作流程（Developer）


| 技能                     | 描述    | 功能                                              |
| ---------------------- | ----- | ----------------------------------------------- |
| **git-pr-description** | PR 描述 | 依目前 branch 與目標 branch 差異產生 PR Title／Description |
| **git-smart-commit**   | 智慧提交  | 將變更依邏輯分群，產出多筆 conventional commit               |


#### 🎵 媒體與創作（Media）


| 技能            | 描述        | 功能                           |
| ------------- | --------- | ---------------------------- |
| **ace-music** | ACE Music | AI 音樂生成（歌詞、風格、cover、repaint） |


#### 👁️ 電腦視覺與人臉（Vision）


| 技能              | 描述                  | 功能                                                        |
| --------------- | ------------------- | --------------------------------------------------------- |
| **facenet-cli** | facenet CLI（`fnet`） | facenet-pytorch 命令列：人臉 embedding、建庫、1:1／1:N 比對、可選 JSON 輸出 |


#### 🔍 搜尋與資訊檢索（Search）


| 技能 | 描述 | 功能 |
|------|------|------|
| **felo-cli** | Felo 搜尋 | 搜尋／查證／即時資訊：優先 `npx -y @willh/felo-cli --json`、SDK 或 `FELO_API_KEY` + OpenAPI |


#### 📚 教學與課務（Teacher）


| 技能                           | 描述       | 功能                                                                                                                                                          |
| ---------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **orangeapple-class-report** | 橘子蘋果課堂報告 | 梯次名單、逐字稿修復、測驗成績、家長三明治回饋報告（Chrome DevTools + Obsidian）                                                                                                       |
| **peas-example-coach**       | 凡思陪練     | 依 `example-learning-checklist.md` **必做**條目陪練；開場 `PEAS · 凡思陪練` 品牌畫面、進度 M／N、思考格；落檔 `session-records/peas-example-log.md`；**理解評估摘要**（五軸 + Sigmoid 總分，選修另列挑戰加分） |
| **peas-challenge-coach**     | 凡思挑戰教練   | 陪練後依 `challenges.md` 逐題釐清規格、對齊條列、六欄提示詞交 coding agent；**程式行為驗收**後**理解驗收**（`uv run`）；落檔 `session-records/peas-challenge-log.md`；評分格式與陪練對齊                     |
| **peas-vtuber-coach**        | 凡思 VTuber 陪練 | Agent Studio 右欄 **PNGtuber MVP**（idle／thinking／talking 四狀態 GIF + 模板內建 TTS）；依 `references/step-scripts.md` 一次一步、完成句前進；生圖用 ChatGPT／Gemini 網頁；Prompt A 改 `studio_shell/agent_panel.py` |
| **peas-workshop-advanced-coach** | 凡思 Workshop Bridge 教練 | **WG-13～22** 路由／狀態機：依 `references/bridge/` 逐關卡 handoff；WG-13～21 可選直接實作或引導釐清；**WG-22** 契約優先拆檔 `agent_core.py` + `main.py` |


#### 🤖 Nanobot 整合（nanobot）


| 技能                     | 描述           | 功能                                                        |
| ---------------------- | ------------ | --------------------------------------------------------- |
| **setup-line-channel** | LINE Channel | 為 nanobot 新增 LINE Messaging API、Webhook、Cloudflare Tunnel |


#### 🚀 生產力工具（Productivity）


| 技能                  | 描述         | 功能                                                                            |
| ------------------- | ---------- | ----------------------------------------------------------------------------- |
| **google-email**    | Gmail 電子郵件 | OAuth 認證、附件下載、訊息管理                                                            |
| **google-calendar** | Google 日曆  | 日曆操作、行程管理                                                                     |
| **readmoo-capture** | Readmoo 匯出 | Readmoo 階段一 viewport 截圖、`readmoo-auth.json`、同捆 `readmoo_capture_snapshots.py` |


### 使用方式

#### 🚀 快速開始

1. **查看可用技能**
  瀏覽 [Documents](./Documents/)、[Browser](./Browser/)、[Developer](./Developer/)、[Media](./Media/)、[Vision](./Vision/)、[Search](./Search/)、[Teacher](./Teacher/)、[nanobot](./nanobot/)、[Productivity](./Productivity/) 資料夾，查看所有可用的技能。
2. **安裝特定技能**
  每個技能都可以獨立使用。選擇你需要的技能後，以 `owner/repo/倉庫內路徑` 安裝，例如 `mz038197/vanscoding-skills/Documents/word`。
3. **查看技能說明**
  安裝後，閱讀技能中的 `SKILL.md` 檔案以了解使用方式。

#### 📦 安裝命令範例

**文檔與 Agent 引導（Documents）：**

```bash
npx skills add mz038197/vanscoding-skills/Documents/word
npx skills add mz038197/vanscoding-skills/Documents/pdf
npx skills add mz038197/vanscoding-skills/Documents/pptx
npx skills add mz038197/vanscoding-skills/Documents/xlsx
npx skills add mz038197/vanscoding-skills/Documents/google-sheets
npx skills add mz038197/vanscoding-skills/Documents/markitdown-guide
npx skills add mz038197/vanscoding-skills/Documents/agent-soul-crafter
npx skills add mz038197/vanscoding-skills/Documents/agents-md-guide
npx skills add mz038197/vanscoding-skills/Documents/user-md-guide
npx skills add mz038197/vanscoding-skills/Documents/obsidian-cli
npx skills add mz038197/vanscoding-skills/Documents/skill-creator
npx skills add mz038197/vanscoding-skills/Documents/skill-creator-advanced
```

**瀏覽器與網頁自動化（Browser）：**

```bash
npx skills add mz038197/vanscoding-skills/Browser/browser-use
npx skills add mz038197/vanscoding-skills/Browser/chrome-devtools
npx skills add mz038197/vanscoding-skills/Browser/webwright
npx skills add mz038197/vanscoding-skills/Browser/playwright-cli/playwright-cli
```

**開發與 Git 工作流程（Developer）：**

```bash
npx skills add mz038197/vanscoding-skills/Developer/git-pr-description
npx skills add mz038197/vanscoding-skills/Developer/git-smart-commit
```

**媒體與創作（Media）：**

```bash
npx skills add mz038197/vanscoding-skills/Media/ace-music
```

**電腦視覺與人臉（Vision）：**

```bash
npx skills add mz038197/vanscoding-skills/Vision/facenet-cli
```

**搜尋與資訊檢索（Search）：**

```bash
npx skills add mz038197/vanscoding-skills/Search/felo-cli
```

**教學與課務（Teacher）：**

```bash
npx skills add mz038197/vanscoding-skills/Teacher/orangeapple-class-report
npx skills add mz038197/vanscoding-skills/Teacher/peas-example-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-challenge-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-vtuber-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-workshop-advanced-coach
```

**Nanobot 整合：**

```bash
npx skills add mz038197/vanscoding-skills/nanobot/setup-line-channel
```

**生產力工具（Productivity）：**

```bash
npx skills add mz038197/vanscoding-skills/Productivity/google-email
npx skills add mz038197/vanscoding-skills/Productivity/google-calendar
npx skills add mz038197/vanscoding-skills/Productivity/readmoo-capture
```

#### 技能檔案結構

每個技能都包含：

- **SKILL.md** - 技能定義和使用指南
- **scripts/** - 相關的輔助程式和工具
- **LICENSE.txt** - 授權條款（如適用）
- **參考文件** - 詳細的技術文件（如 reference.md、forms.md 等）

### 技能特性

✨ **文檔與 Agent 設定**

- 支援主要辦公文檔格式（Word、PDF、PowerPoint、Excel）與 OOXML
- MarkItDown 指南：PDF／Office／圖像／音訊等轉 Markdown，供 LLM 管線使用
- AGENTS.md / USER.md 建構引導，讓 agent 更懂工作區與使用者
- Obsidian CLI：直接操作 vault 與筆記自動化
- Skill Creator：基礎建立流程與 init／package／驗證腳本
- Skill Creator Advanced：可測、可迭代、可打包的進階 skill 工程流程

🌐 **瀏覽器與網頁**

- Browser Use 雲端或開源模式：操作瀏覽器、爬取、自動化
- Chrome DevTools MCP：除錯、自動化互動、效能與網路分析
- Webwright：本機 Playwright code-as-action、`plan.md` 與 `final_runs/` 工作區契約、截圖證據驗證
- Playwright CLI：終端機驅動瀏覽器、快照與 E2E 測試流程

🛠️ **開發與 Git**

- PR 描述產生、依邏輯拆分 conventional commit

🎵 **媒體與創作**

- ACE Music：AI 音樂生成（歌詞、風格、cover、repaint）

👁️ **電腦視覺與人臉**

- facenet-cli（`fnet`）：人臉 embedding、建庫、比對、可選 JSON 輸出

🔍 **搜尋與資訊**

- felo-cli：搜尋、查證、即時資訊（CLI `--json`、SDK、`FELO_API_KEY`）

📚 **教學與課務**

- 橘子蘋果課後報告：梯次、逐字稿、測驗成績到家長回饋的一條龍流程
- **凡思 PEAS 教學技能**：`peas-example-coach` → `peas-challenge-coach` → `peas-workshop-advanced-coach`（**WG-13～22** Workshop Bridge）；陪練／挑戰共用 `session-records/` 與理解評估摘要（五軸 + Sigmoid）
- 凡思陪練：清單必做進度、不暴露後台、一次一問、思考格落檔
- 凡思挑戰教練：對齊條列 → Persona～Example 六欄完整提示詞 → coding agent 改 `main.py` → 雙段驗收後落實作紀錄
- 凡思 VTuber 陪練：Agent Studio 右欄 PNGtuber 四狀態 GIF MVP；`step-scripts.md` 劇本、一次一步、完成句前進；生圖 ChatGPT／Gemini、Prompt A／B 交 coding agent
- 凡思 Workshop Bridge 教練：掃描 `wg_milestone_checklist.md` 決定 `next_wg`，依 `references/bridge/` 單卡 handoff；WG-22 走契約優先拆檔流程

🤖 **Nanobot 整合**

- LINE Messaging API channel、Webhook、Cloudflare Tunnel

🔧 **豐富的工具集**

- Python / JavaScript 腳本、完整 API 參考

☁️ **雲端整合**

- Google 套件（Gmail、日曆、試算表）、OAuth 認證
- Readmoo 網頁讀者階段一截圖匯出（與 Playwright／uv 工作流程對齊）

📚 **詳細文件**

- 每個技能都有 SKILL.md、進階參考與使用指南

### 授權

本專案遵循 Anthropic 的授權條款。詳見 [LICENSE](./LICENSE) 檔案。

個別技能可能有其特定的授權條款，請查看各技能資料夾內的 LICENSE.txt 檔案。

### 專案優勢

✅ **集中管理** - 所有技能在一個倉庫中，易於維護  
✅ **清晰分類** - 按用途分為文檔／Agent／Obsidian／skill 工程、瀏覽器、開發與 Git、媒體、電腦視覺、搜尋、教學課務、nanobot、生產力工具  
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

**Q: PEAS 教學技能（example／challenge／vtuber／workshop）如何搭配？**

A: 建議依序：**陪練**（`peas-example-coach`）→ **挑戰教練**（`peas-challenge-coach`）→ **Workshop Bridge 教練**（`peas-workshop-advanced-coach`，**WG-13～22**）。前兩者共用 `session-records/` 與五軸 + Sigmoid 評分；Workshop Bridge 以 `wg_milestone_checklist.md` 掃描進度、路由至 `references/bridge/` 單一關卡 handoff，WG-22 另走契約優先拆檔（`agent_core.py` + `main.py`）。**VTuber 陪練**（`peas-vtuber-coach`）可獨立使用：需已有 Agent Studio（`studio_shell/`），逐步完成右欄 PNGtuber GIF + TTS MVP，與 checklist／challenge 流程無硬性先後。

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

**Vanscoding Skills** is a comprehensive AI skill library for document processing, Microsoft MarkItDown-to-Markdown workflows, Obsidian integration, advanced skill engineering, browser automation (including Webwright code-as-action and Playwright CLI), web search and fact-finding (Felo CLI), media creation, computer vision and face recognition, teaching workflows (including Fansi PEAS coaches, VTuber MVP coaching, and Workshop Bridge WG-13–22), agent configuration guides, development and Git workflows, Nanobot integration, Readmoo stage-1 export workflows, and productivity tools. This monorepo contains 30 skill modules that can be installed and used independently.

### Project Structure

The repository is organized into nine categories:

- **Documents/** - Documents, agent guides, MarkItDown, Obsidian, and skill engineering (12 modules)
  - word, pdf, pptx, xlsx, google-sheets, markitdown-guide, agent-soul-crafter, agents-md-guide, user-md-guide, obsidian-cli, skill-creator, skill-creator-advanced
- **Browser/** - Browser and web automation (4 modules)
  - browser-use: Browser Use Cloud SDK for browser control, scraping, automation
  - chrome-devtools: Chrome DevTools MCP for debugging, automation, performance, and network inspection
  - webwright: Local Playwright code-as-action — `plan.md`, `final_runs/run_<id>/`, screenshots, action logs, CP self-verify
  - playwright-cli (under `Browser/playwright-cli/playwright-cli/`): Terminal-driven Playwright CLI — snapshots, interaction, tests
- **Developer/** - Development and Git workflows (2 modules)
  - git-pr-description: Generate PR title and description from branch diffs
  - git-smart-commit: Split changes into logical conventional commits
- **Media/** - Media and creation (1 module)
  - ace-music: ACE Music AI music generation
- **Vision/** - Computer vision and face recognition (1 module)
  - facenet-cli: facenet-pytorch CLI (`fnet`) for embeddings, face DB, 1:1 / 1:N matching, optional JSON
- **Search/** - Search, lookup, and current information (1 module)
  - felo-cli: Prefer `@willh/felo-cli --json`, SDK, or `FELO_API_KEY` + Felo OpenAPI for search and fact-finding
- **Teacher/** - Teaching and class operations (5 modules)
  - orangeapple-class-report: Orange Apple post-class parent report workflow (Chrome DevTools + Obsidian)
  - peas-example-coach: Fansi checklist coaching — required items only, PEAS splash, thinking grid, `session-records/`, Understanding Assessment Summary (five axes + Sigmoid)
  - peas-challenge-coach: Fansi challenge coach after checklist — `challenges.md`, aligned specs, six-column prompts, program then understanding acceptance (`uv run`), shared scoring format
  - peas-vtuber-coach: Fansi VTuber MVP coach — Agent Studio right-panel PNGtuber (idle/thinking/talking GIF + built-in TTS); step-scripts, one step at a time, ChatGPT/Gemini for assets, Prompt A/B via coding agent
  - peas-workshop-advanced-coach: Fansi Workshop Bridge coach — WG-13–22 router/state machine via `references/bridge/` cards; WG-22 contract-first split of `agent_core.py` + `main.py`
- **nanobot/** - Nanobot integration (1 module)
  - setup-line-channel: LINE Messaging API channel, webhook, Cloudflare Tunnel
- **Productivity/** - Productivity tools (3 modules)
  - google-email, google-calendar, readmoo-capture (Readmoo stage-1 viewport capture via Playwright / bundled script)

Each skill is self-contained with its own SKILL.md, scripts (where applicable), and documentation.

### Available Skills

#### 📄 Documents


| Skill                      | Description               | Features                                                                                                                      |
| -------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **word**                   | Word document processing  | Create, edit, track changes, comments, formatting                                                                             |
| **pdf**                    | PDF file manipulation     | Form filling, text extraction, image conversion                                                                               |
| **pptx**                   | PowerPoint presentations  | Slide operations, OOXML processing, HTML conversion                                                                           |
| **xlsx**                   | Excel spreadsheets        | Formulas, formatting, data analysis                                                                                           |
| **google-sheets**          | Google Sheets integration | Spreadsheet management, data handling                                                                                         |
| **markitdown-guide**       | MarkItDown guide          | microsoft/markitdown: convert many formats to Markdown; CLI / API, plugins, PPTX images                                       |
| **agent-soul-crafter**     | AI agent personality      | Design agent personality and behavior                                                                                         |
| **agents-md-guide**        | AGENTS.md guide           | Stage-based AGENTS.md construction                                                                                            |
| **user-md-guide**          | USER.md guide             | Build personal profile for agents                                                                                             |
| **obsidian-cli**           | Obsidian CLI              | Read/write vault, search, tasks, move/rename, broken links and orphans                                                        |
| **skill-creator**          | Skill creation guide      | SKILL.md anatomy, scripts/references/assets, progressive disclosure; `init_skill.py`, `package_skill.py`, `quick_validate.py` |
| **skill-creator-advanced** | Advanced skill authoring  | Naming, boundaries, evals, benchmarks, validation, packaging (pairs with skill-creator)                                       |


#### 🌐 Browser


| Skill               | Description         | Features                                                                                  |
| ------------------- | ------------------- | ----------------------------------------------------------------------------------------- |
| **browser-use**     | Browser Use         | Browser control, web scraping, automation (Cloud / Open Source)                           |
| **chrome-devtools** | Chrome DevTools MCP | Debug pages, automate interactions, analyze performance, inspect network requests via MCP |
| **webwright**       | Webwright           | Code-as-action local Playwright — `final_runs/run_<id>/` screenshots, action logs, CP self-verify |
| **playwright-cli**  | Playwright CLI      | `playwright-cli` commands: open pages, snapshots, clicks/types, tests and tracing         |


#### 🛠️ Developer


| Skill                  | Description    | Features                                                              |
| ---------------------- | -------------- | --------------------------------------------------------------------- |
| **git-pr-description** | PR description | Generate PR title and description from current vs target branch diffs |
| **git-smart-commit**   | Smart commits  | Group changes and produce multiple conventional commits               |


#### 🎵 Media


| Skill         | Description | Features                                            |
| ------------- | ----------- | --------------------------------------------------- |
| **ace-music** | ACE Music   | AI music generation (lyrics, style, cover, repaint) |


#### 👁️ Vision


| Skill           | Description          | Features                                                                                       |
| --------------- | -------------------- | ---------------------------------------------------------------------------------------------- |
| **facenet-cli** | facenet CLI (`fnet`) | Face embeddings, face DB, 1:1 / 1:N matching via facenet-pytorch; optional JSON for automation |


#### 🔍 Search


| Skill | Description | Features |
|-------|-------------|----------|
| **felo-cli** | Felo search | Search, lookup, current facts — prefer `npx -y @willh/felo-cli --json`, SDK, or `FELO_API_KEY` + OpenAPI |


#### 📚 Teacher


| Skill                        | Description               | Features                                                                                                                                                                                                               |
| ---------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **orangeapple-class-report** | Orange Apple class report | Rosters, transcript cleanup, quiz scores, sandwich-style parent feedback                                                                                                                                               |
| **peas-example-coach**       | Fansi checklist coach     | Required items from `example-learning-checklist.md`; PEAS splash; M/N progress; thinking grid → `session-records/peas-example-log.md`; Understanding Assessment Summary (five axes + Sigmoid; optional items as bonus) |
| **peas-challenge-coach**     | Fansi challenge coach     | After checklist: `challenges.md` per challenge — spec alignment, six-column prompt for coding agent; program acceptance then understanding acceptance; logs/scores under `session-records/`                            |
| **peas-vtuber-coach**        | Fansi VTuber coach        | Agent Studio right-panel **PNGtuber MVP** — four-state GIF (idle/thinking/talking) + built-in TTS; `references/step-scripts.md`, one step at a time; ChatGPT/Gemini for assets; Prompt A updates `studio_shell/agent_panel.py` |
| **peas-workshop-advanced-coach** | Fansi Workshop Bridge coach | **WG-13–22** — progress scan via `wg_milestone_checklist.md`, route to one `references/bridge/` card; WG-22 contract-first split of `agent_core.py` + `main.py` |


#### 🤖 Nanobot


| Skill                  | Description  | Features                                                   |
| ---------------------- | ------------ | ---------------------------------------------------------- |
| **setup-line-channel** | LINE Channel | LINE Messaging API, webhook, Cloudflare Tunnel for nanobot |


#### 🚀 Productivity Tools


| Skill               | Description                 | Features                                                                                  |
| ------------------- | --------------------------- | ----------------------------------------------------------------------------------------- |
| **google-email**    | Gmail management            | OAuth authentication, attachment handling, message management                             |
| **google-calendar** | Google Calendar integration | Calendar operations, schedule management                                                  |
| **readmoo-capture** | Readmoo export              | Stage-1 viewport screenshots, `readmoo-auth.json`, bundled `readmoo_capture_snapshots.py` |


### Installation

Install a skill with `owner/repo/path` (example: `mz038197/vanscoding-skills/Documents/word`):

```bash
# Documents
npx skills add mz038197/vanscoding-skills/Documents/word
npx skills add mz038197/vanscoding-skills/Documents/pdf
npx skills add mz038197/vanscoding-skills/Documents/pptx
npx skills add mz038197/vanscoding-skills/Documents/xlsx
npx skills add mz038197/vanscoding-skills/Documents/google-sheets
npx skills add mz038197/vanscoding-skills/Documents/markitdown-guide
npx skills add mz038197/vanscoding-skills/Documents/agent-soul-crafter
npx skills add mz038197/vanscoding-skills/Documents/agents-md-guide
npx skills add mz038197/vanscoding-skills/Documents/user-md-guide
npx skills add mz038197/vanscoding-skills/Documents/obsidian-cli
npx skills add mz038197/vanscoding-skills/Documents/skill-creator
npx skills add mz038197/vanscoding-skills/Documents/skill-creator-advanced

# Browser
npx skills add mz038197/vanscoding-skills/Browser/browser-use
npx skills add mz038197/vanscoding-skills/Browser/chrome-devtools
npx skills add mz038197/vanscoding-skills/Browser/webwright
npx skills add mz038197/vanscoding-skills/Browser/playwright-cli/playwright-cli

# Developer
npx skills add mz038197/vanscoding-skills/Developer/git-pr-description
npx skills add mz038197/vanscoding-skills/Developer/git-smart-commit

# Media
npx skills add mz038197/vanscoding-skills/Media/ace-music

# Vision
npx skills add mz038197/vanscoding-skills/Vision/facenet-cli

# Search
npx skills add mz038197/vanscoding-skills/Search/felo-cli

# Teacher
npx skills add mz038197/vanscoding-skills/Teacher/orangeapple-class-report
npx skills add mz038197/vanscoding-skills/Teacher/peas-example-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-challenge-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-vtuber-coach
npx skills add mz038197/vanscoding-skills/Teacher/peas-workshop-advanced-coach

# Nanobot
npx skills add mz038197/vanscoding-skills/nanobot/setup-line-channel

# Productivity
npx skills add mz038197/vanscoding-skills/Productivity/google-email
npx skills add mz038197/vanscoding-skills/Productivity/google-calendar
npx skills add mz038197/vanscoding-skills/Productivity/readmoo-capture
```

### License

This project follows Anthropic's licensing terms. See the [LICENSE](./LICENSE) file for details.

Individual skills may have their own license terms. Check the LICENSE.txt file in each skill's folder.

### Key Features

✨ **Documents & Agent Guides** - Office formats (Word, PDF, PowerPoint, Excel), OOXML; MarkItDown guide for LLM-ready Markdown; AGENTS.md / USER.md construction guides; Obsidian CLI; skill-creator (core workflow + scripts) and skill-creator-advanced (evals, benchmarks, packaging)  
🌐 **Browser & Web** - Browser Use for browser control, scraping, automation (Cloud / Open Source); Chrome DevTools MCP; Webwright code-as-action with screenshot evidence; Playwright CLI for snapshots, interaction, and tests  
🛠️ **Developer & Git** - PR description generation, logical conventional commit splits  
🎵 **Media & Creation** - ACE Music for AI music generation  
👁️ **Vision** - facenet-cli (`fnet`) for face embeddings, matching, optional JSON output  
🔍 **Search** - felo-cli for web search, lookup, and current information (CLI, SDK, API)  
📚 **Teacher** - Orange Apple reports; **Fansi PEAS teaching skills** (example → challenge → Workshop Bridge `peas-workshop-advanced-coach` for WG-13–22) with shared `session-records/` and aligned scoring where applicable; **VTuber MVP coach** (`peas-vtuber-coach`) for Agent Studio PNGtuber GIF + TTS workflow  
🤖 **Nanobot** - LINE Messaging API channel, webhook, Cloudflare Tunnel  
🔧 **Rich Toolset** - Python / JavaScript scripts, API references  
☁️ **Cloud Integration** - Google (Gmail, Calendar, Sheets), OAuth; Readmoo web reader stage-1 capture workflow  
📚 **Documentation** - SKILL.md per skill, references, usage guides  

### Project Advantages

✅ **Centralized Management** - All skills in one repository  
✅ **Clear Organization** - Documents, Browser, Developer, Media, Vision, Search, Teacher, nanobot, Productivity  
✅ **Independent Installation** - Install only the skills you need  
✅ **Version Control** - Git history and tag support  
✅ **Education-Friendly** - Suitable for classroom and learning  

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

**Q: How do the PEAS teaching skills (example / challenge / vtuber / workshop) fit together?**

A: Use them in order: **example coach** → **challenge coach** → **Workshop Bridge coach** (`peas-workshop-advanced-coach`, **WG-13–22**). Example and challenge coaches share `session-records/` and five-axis + Sigmoid scoring; Workshop Bridge scans progress, routes to one bridge card under `references/bridge/`, and uses a contract-first split flow for WG-22. **VTuber coach** (`peas-vtuber-coach`) stands alone: requires an existing Agent Studio project (`studio_shell/`) and walks through the right-panel PNGtuber GIF + TTS MVP step by step — no strict prerequisite to the checklist/challenge flow.

### Contact

For questions or suggestions, please:

- 📧 Open an Issue - Report bugs or request features
- 💬 Start a Discussion - General questions and discussions
- 📝 Submit a Pull Request - Contribute improvements


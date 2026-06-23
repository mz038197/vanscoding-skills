# peas-capstone-report

Agent Studio 專題報告陪練 skill — 引導學生產出 `report/專題報告.{md,pptx,docx}` 與 `report/assets/專題海報.png`。

## 老師端（vanscoding-skills 維護者）

在 repo 根目錄：

```powershell
.\scripts\sync-skill-to-agents.ps1 -SourcePath Teacher/peas-capstone-report
```

## 學生端（課堂安裝）

### 方式 A：Git 子路徑

1. Clone 或 sparse checkout `Teacher/peas-capstone-report/` 資料夾。
2. 整份複製到：

```text
%USERPROFILE%\.cursor\skills\peas-capstone-report\
```

3. 重開 Cursor 或新開 Agent 對話，說「用 peas-capstone-report 帶我寫專題報告」。

### 方式 B：Zip

1. 老師 zip `peas-capstone-report` 資料夾內容（含 `SKILL.md`、`references/`、`assets/`、`scripts/`）。
2. 解壓到 `%USERPROFILE%\.cursor\skills\peas-capstone-report\`。
3. 同上觸發 skill。

## 學生專案前置

- 已安裝 Agent Studio（專案根有 `studio_shell/`）。
- `~/.peas-agent/config.json` 已設定學校發放的 `api_key`（報告內**不要**寫 key 或 Router 位址）。
- Step 7 需 **vcr-imagegen** skill（`%USERPROFILE%\.cursor\skills\vcr-imagegen\`）與 `VSROUTER_API_KEY`；無 key 時依 `references/poster-fallback.md` 用 ChatGPT／Gemini 網頁後備。

## 產出位置

在**專題專案根目錄**建立 `report/`，完成後應有：

- `專題報告.md`、`專題報告.pptx`、`專題報告.docx`
- `project-architecture.mmd`
- `assets/server-topology.png`、`project-architecture.png`、`demo-*.png`
- `assets/專題海報.png`（Step 7，直式 2:3 展覽海報）

## 腳本依賴（Agent 代跑時）

```bash
# mmdc（Node）
npx -y @mermaid-js/mermaid-cli ...

# Python（課堂環境擇一安裝）
uv pip install python-pptx python-docx
```

Step 7 海報：vcr-imagegen `generate-image.ps1`（見 `references/poster-prompt-template.md`）。

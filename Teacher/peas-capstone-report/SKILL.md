---
name: peas-capstone-report
description: 逐步引導 Agent Studio 專題學生完成可繳交報告（專題介紹、左欄↔右欄互動、成果／創新／技術由學生主筆；Agent 代勞架構 Mermaid、全班相同 server 拓撲圖、MD／PPT／Word）。每則回覆前必讀 references/step-scripts.md 當前 step_id；Step 1–3 學生口述、對齊條列後才落檔；Step 6 必產專題報告.docx 且嵌入全部 PNG。觸發：專題報告、capstone、Agent Studio 架構圖、server 配置圖。
version: "1.0.0"
updated: "2026-06-21"
---

# 專題報告陪練（peas-capstone-report）

## 何時使用

- 馬公高中 Agent Studio + peas-agent-core 專題，要產出 **Markdown + PPTX + DOCX** 報告。
- 使用者說「專題報告」「capstone」「架構圖」「server 配置圖」「peas-capstone-report」等。
- **前置**：專案已有 `studio_shell/`；`~/.peas-agent/config.json` 已指向學校 Router（**報告內不寫 Router IP／URL**）。

## 核心原則

- **劇本在 `references/step-scripts.md`**：話術、對齊條列、組裝指令都在該檔；本檔只寫執行協定。
- **學生主筆 A 段（Step 1–3）**：專題介紹、左欄↔右欄互動、成果／創新／技術 — 學生用**自己的話**回答；Agent **整理成條列**並請學生確認後才寫入 `report/`。
- **Agent 代勞 B 段（Step 0、4–6）**：preflight、複製 server 圖、撰寫 `project-architecture.mmd`、mmdc 產 PNG、收 demo 截圖、產 MD／PPT／DOCX。
- **禁止**：改 `studio_shell/pages/` 程式、維運 Ollama Router、在報告中貼 api_key 或 Router 位址。

## 執行協定（每則回覆前必做）

1. **確認 `current_step`**：`1` | `2` | `3` | `3c` | `0` | `4` | `4b` | `5` | `6`。首次觸發 → `1`。學生回覆匹配當步 `completion_phrases` 後才進下一 `step_id`（順序見 step-scripts 末尾速查表）。
2. **讀取** `references/step-scripts.md` **該 step_id 整段**（含 `學生可見模板`、`if_stuck`、`agent_must_not`）。
3. **Step 1–3**：一次只問一題；學生答完再追問或進下一步；**不得**代寫長篇，只整理條列。
4. **Step 3c**：輸出完整對齊條列，學生說「確認」後才進 Step 0。
5. **Step 4–6**：可動手寫檔、跑腳本；完成前依 `references/verification.md` 檢查（含 **docx 須嵌入圖片**、demo 張數 ≥ 自訂頁數）。
6. **禁止**：同一則兩個待辦；未確認對齊條列就產 MD；交付無圖 docx。

## 產出契約（學生專案 `report/`）

```text
report/
├── 專題報告.md
├── 專題報告.pptx
├── 專題報告.docx          ← 必須含嵌入 PNG
├── project-architecture.mmd
├── .capstone-progress.md
└── assets/
    ├── server-topology.png
    ├── project-architecture.png
    └── demo-*.png         ← 每自訂頁至少 1 張
```

## 參考檔索引

| 檔案 | 用途 |
|------|------|
| `references/step-scripts.md` | **主檔**；每則必讀當步 |
| `references/student-voice-worksheet.md` | Step 1–3 引導問題與條列範例 |
| `references/studio-patterns.md` | 左欄↔右欄組裝規則 + 已核准 Mermaid 範例 |
| `references/server-topology.md` | 全班相同 server 圖說明（無 IP） |
| `references/mermaid-to-png-guide.md` | mmdc 失敗時 ChatGPT／Gemini 後備 |
| `references/screenshot-guide.md` | demo 截圖規範 |
| `references/report-template.md` | `專題報告.md` 章節骨架 |
| `references/ppt-slide-map.md` | MD → 投影片對照 |
| `references/docx-fallback.md` | docx 腳本失敗後備 |
| `references/verification.md` | Step 6 交件前檢查 |

## 腳本（B 段 Agent 執行）

| 腳本 | 用途 |
|------|------|
| `scripts/render_project_diagram.py` | `.mmd` → PNG（npx mmdc） |
| `scripts/build_capstone_ppt.py` | MD → pptx |
| `scripts/build_capstone_docx.py` | MD + assets → docx（**須嵌圖**） |

路徑：在**學生專案根目錄**執行，以 skill 內腳本絕對路徑或複製到專案後執行；`--report-dir report` 為預設。

## 圖片三類

| 圖 | 來源 |
|----|------|
| Server | 複製 skill `assets/server-topology.png` → `report/assets/` |
| 個人架構 | 學生專案 `report/project-architecture.mmd` + mmdc |
| Demo | 學生 `Win+Shift+S` 截自訂頁 → `demo-01.png` … |

**個人架構 Mermaid**：節點用平易近人中文（點餐頁、AI 大腦…）；**禁止**以 `format_extra_context`、`pages/4_*.py` 作節點主文字。

## 觸發後第一則

讀 step-scripts **§ Step 1**，**只**輸出 Step 1 學生可見模板。

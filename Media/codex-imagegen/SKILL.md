---
name: codex-imagegen
version: "1.0.0"
updated: "2026-06-21"
description: Use when the user asks to generate images, illustrations, covers, posters, teaching visuals, social graphics, or course assets as files in the project; mentions Codex CLI, imagegen, or terminal-based image generation; or needs PNG/JPEG output under paths like assets/generated.
disable-model-invocation: false
---

# Codex CLI 圖片生成

## 定位

| 層 | 路徑 | 角色 |
|----|------|------|
| **官方 imagegen** | `~/.codex/skills/.system/imagegen/` | Codex Agent 內建生圖規則（`$imagegen` 時自動載入） |
| **本 skill** | `~/.cursor/skills/codex-imagegen/` | Cursor 批次／固定路徑的**薄包裝**：只呼叫同捆腳本 |

生圖仍走官方內建 `image_gen` 工具（**Codex login 訂閱額度**）。**不**使用 `image_gen.py` Platform API（需 `OPENAI_API_KEY`，另計費）。

互動式單張、可手動存檔：可直接用 **Codex Desktop** + 官方 skill，不必經本 skill。

## 核心原則

需要產出**專案內實際 PNG 檔**時，agent **只呼叫**：

`$env:USERPROFILE\.cursor\skills\codex-imagegen\scripts\generate-image.ps1`

不要手動組 `codex exec`；路徑檢查、Codex 呼叫、交檔與驗證都由腳本負責。

## 何時使用

- 要落地圖檔（非僅 prompt 文案）
- 固定輸出如 `assets/generated/...`
- 批次、StyleFile、manifest 管線

**不要用**：只要構想；或使用者指定 DALL·E／SD 等且堅持不用 Codex。

## 前置條件

```powershell
npm install -g @openai/codex
codex --version
codex login
```

## 標準流程

1. 決定 `-OutputPath`（預設 `assets/generated/image.png`，相對專案根）
2. 中文或長 prompt → UTF-8 檔 + `-PromptFile`；長 style → `-StyleFile`
3. 執行腳本；結束碼 0 且檔案存在
4. 回報路徑與 prompt 摘要；失敗則說明原因（登入、額度、重試）

```powershell
$gen = Join-Path $env:USERPROFILE '.cursor/skills/codex-imagegen/scripts/generate-image.ps1'

# 中文／批次：PromptFile + StyleFile（推薦）
& $gen `
  -PromptFile ".cursor/tmp/codex-imagegen-prompt.txt" `
  -StyleFile "styles/08_白底塗鴉教學風.md" `
  -OutputPath "assets/generated/example.png" `
  -AspectRatio "16:9" `
  -Cwd (Get-Location).Path
```

工作目錄已是專案根可省略 `-Cwd`。驗參數用 `-DryRun`。

**Prompt 檔**：用 UTF-8 無 BOM（勿用可能帶 BOM 的 `Set-Content -Encoding UTF8` 寫中文檔，除非確認無 BOM）。

## 參數速查

| 參數 | 說明 |
|------|------|
| `-ImagePrompt` | 與 `-PromptFile` 二擇一 |
| `-PromptFile` | UTF-8 prompt 檔；中文優先 |
| `-OutputPath` | 預設 `assets/generated/image.png` |
| `-Cwd` | Codex `--cd`；預設目前目錄 |
| `-AspectRatio` | 如 `16:9`、`1:1` |
| `-Style` / `-StyleFile` | 風格關鍵字或風格檔 |
| `-DryRun` | 只印 prompt，不呼叫 codex |

## 腳本交檔邏輯（無需額外參數）

內建 `$imagegen` **沒有 destination 參數**；預設先存 `~/.codex/generated_images/`。腳本在 `codex exec` 後依序：

1. 目標路徑有**本次新寫入**且 ≥ 100KB → 接受
2. 否則從 **session log** 解 `image_generation_call.result` base64 → 寫入目標（exec 模式常需此步）
3. 否則才從 `generated_images/{sessionId}/` 複製**本次 session 新檔**
4. **拒絕**修改時間過舊的 cache（例如隔日仍指向 6/12 舊圖）

Prompt 中的 `Save the image to …` 是給 Codex Agent 的指示，**不能**當成工具保證路徑。

## 常見問題

| 狀況 | 處理 |
|------|------|
| 找不到 codex | 安裝並 `codex login` |
| stale / 缺檔 | 重試；確認訂閱額度；腳本會嘗試 session log 解圖 |
| 同一張舊圖 | Agent 誤複製 cache；腳本應拒絕；若仍發生請回報 |
| Platform API | 僅在使用者**明確要求** `image_gen.py` 時才用 |

## 參考

- 官方：`~/.codex/skills/.system/imagegen/SKILL.md`
- 舊教學（部分已過時，僅背景）：`G:\我的雲端硬碟\Obsidian\Agent\raw\inbox\Cursor + Codex CLI 圖片生成.md`

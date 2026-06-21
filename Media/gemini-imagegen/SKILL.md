---
name: gemini-imagegen
version: "1.0.0"
updated: "2026-06-21"
description: Use when the user asks to generate images, illustrations, covers, posters, teaching visuals, or course assets via Gemini CLI; mentions gemini CLI, terminal image generation with Google Gemini, or PNG/JPEG under paths like assets/generated with Gemini.
disable-model-invocation: false
---

# Gemini CLI 圖片生成

## 核心原則

需要產生實際圖片檔時，agent **只呼叫同捆 PowerShell 腳本**：

`$env:USERPROFILE\.cursor\skills\gemini-imagegen\scripts\generate-image.ps1`

不要手動拼 `gemini -p ...` 的完整參數列；安裝檢查、工作目錄、`--approval-mode` 與輸出路徑驗證都由腳本處理。

### 「產圖」在本 skill 的定義（請與使用者預期對齊）

- **要**：**Gemini／Google 的原生影像生成**（模型回傳的影像／IMAGE 類輸出）或 **官方第一方生圖 MCP**（例如帳號已設定的 Imagen 等）所產生的像素，再寫入指定路徑。
- **不要**：讓 CLI 代理 **寫程式或呼叫繪圖套件「手畫」** 圖檔（例如 Python + Pillow／matplotlib、Node canvas、ImageMagick 合成、手刻極小 PNG 等）。那類輸出不算「用 Gemini 原生生圖」，與本 skill 目標相反。

Gemini CLI 預設常是一般「寫程式代理」；若未指定 **支援影像輸出的模型**（見下）或未接 **生圖 MCP**，很容易退回寫碼畫圖。請**強烈建議**在帳號可用時加上 `-Model`，並以 [Gemini API 模型總覽](https://ai.google.dev/gemini-api/docs/models) 與 [Image generation 指南](https://ai.google.dev/gemini-api/docs/image-generation) 的現行字串為準。

### 官方「原生生圖」模型 id（查核自 Google 文件）

| 行銷名稱 | Model code（`-Model` 帶這個） | 說明 |
|----------|-------------------------------|------|
| Nano Banana（2.5 Flash Image） | `gemini-2.5-flash-image` | [模型頁](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)；文件列穩定版為此字串；已廢止舊 preview：`gemini-2.5-flash-image-preview`。 |
| Nano Banana 2（3.1 Flash Image Preview） | `gemini-3.1-flash-image-preview` | [模型頁](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image-preview)；[Image generation](https://ai.google.dev/gemini-api/docs/image-generation) 範例程式即用此 id。 |
| Nano Banana Pro（3 Pro Image Preview） | `gemini-3-pro-image-preview` | [模型頁](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)。 |

若上述 id 在 CLI 仍回 **`ModelNotFoundError` / 404**，代表目前 **API 金鑰／專案／帳單／區域或方案** 未開到該模型端點，與字串拼錯無關。請到 [Google AI Studio](https://aistudio.google.com/) 的模型選單確認帳號可選的影像模型，或查 Cloud 專案是否啟用 **Generative Language API** 與付費／配額限制。

## 何時使用

- 使用者要**用 Gemini CLI 產出實際圖檔**（不是只要文字描述）。
- 關鍵詞：Gemini CLI 產圖、`gemini -p`、headless、與 codex-imagegen 類似的「終端機生圖」但指定 Google Gemini。

**不要**用此 skill：不要落地檔案、只要構想；或使用者指定 Codex／DALL·E／本地 SD 等其他工具且堅持不用 Gemini CLI。

## 前置條件（使用者環境）

若尚未就緒，請提示使用者在本機執行：

- `npm install -g @google/gemini-cli`
- `gemini --version`
- 依 [Gemini CLI 認證說明](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) 完成登入或設定 `GEMINI_API_KEY`（以官方文件為準）。

## 標準流程

1. 決定輸出路徑。未指定時用 `assets/generated/image.png`（相對於專案根目錄／`-Cwd`）。
2. 執行同捆腳本。英文或純 ASCII 可直接用 `-ImagePrompt`：

```powershell
$gen = Join-Path $env:USERPROFILE '.cursor/skills/gemini-imagegen/scripts/generate-image.ps1'
& $gen `
  -ImagePrompt "a bright Scratch course cover for elementary students" `
  -OutputPath "assets/generated/scratch-cover.png" `
  -AspectRatio "16:9" `
  -Style "bright, friendly" `
  -Model "gemini-3.1-flash-image-preview"
```

3. 中文 prompt 優先寫成 UTF-8 檔案，再用 `-PromptFile`：

```powershell
$promptPath = Join-Path (Get-Location) '.cursor/tmp/gemini-imagegen-prompt.txt'
New-Item -ItemType Directory -Force -Path (Split-Path $promptPath -Parent) | Out-Null
Set-Content -LiteralPath $promptPath -Encoding UTF8 -Value "一張 Scratch 課程封面圖，適合國小學生"

$gen = Join-Path $env:USERPROFILE '.cursor/skills/gemini-imagegen/scripts/generate-image.ps1'
& $gen `
  -PromptFile $promptPath `
  -OutputPath "assets/generated/scratch-cover.png" `
  -AspectRatio "16:9" `
  -Style "明亮、友善" `
  -Model "gemini-3.1-flash-image-preview"
```

4. **強烈建議**：加上 `-Model`，使用你帳號已開通、且官方文件標示**支援影像輸出／原生生圖**的模型 id；留空則使用 CLI 預設模型，常見後果是代理改寫程式畫圖（違反本 skill 目標）。
5. 若 agent 已在專案根目錄工作，可省略 `-Cwd`。僅檢查參數時可加 `-DryRun`。
6. 確認終端機結束碼為 0，且輸出檔存在。
7. 回覆使用者：圖片路徑、prompt 摘要；失敗時轉述錯誤並提示安裝、認證、模型名稱或重試。

## 參數速查

| 參數 | 說明 |
|------|------|
| `-ImagePrompt` | 必填（若未給 `-PromptFile`）。圖片需求；亦可用第一個位置參數。 |
| `-PromptFile` | 選填。UTF-8 文字檔；中文 prompt 建議用此。 |
| `-OutputPath` | 選填。預設 `assets/generated/image.png`。 |
| `-Cwd` | 選填。專案根（Gemini 工作區），預設為目前目錄。 |
| `-AspectRatio` | 選填。例如 `16:9`、`1:1`。 |
| `-Style` | 選填。風格關鍵字。 |
| `-Model` | **強烈建議填寫**。`-m`／`--model`；帳號可用時宜為官方影像／原生生圖模型（請查最新模型表）。留空則不傳 `-m`，易與「原生生圖」預期不符。 |
| `-ApprovalMode` | 選填。預設 `yolo`（自動核准工具）。可改 `auto_edit` 等（須為 CLI 支援值）。 |
| `-DryRun` | 選填。只列出將送出的提示與參數，不呼叫 `gemini`。 |

## 行為說明（與 Codex imagegen 的差異）

- Gemini CLI 使用 headless：`-p`／`--prompt`，並搭配 `--approval-mode`（預設 `yolo`）讓寫檔等工具在非互動環境可執行；**不要**同時傳 `-y` 與 `--approval-mode`（CLI 會拒絕）。
- **與 Codex `$imagegen` 不同**：Codex 內建 imagegen 捷徑；Gemini CLI 則是代理＋模型／工具能力。腳本會用英文硬性約束「只接受原生生圖或官方生圖 MCP」，但**無法**在技術上攔截代理執行 Python；若仍出現寫碼畫圖，請改 `-Model`、檢查 MCP，或改走 [Gemini API 影像生成](https://ai.google.dev/gemini-api/docs/image-generation) 等非代理路徑。

## 常見問題

- **找不到 gemini**：安裝全域套件並確認 PATH。
- **認證失敗**：依官方文件完成 OAuth 或 API key；錯誤碼如 `ModelNotFoundError` 時檢查 `-Model` 是否為你帳號可用 id。
- **檔案未產生**：檢查輸出路徑是否在 `-Cwd` 底下、換新路徑重試；檢視 CLI 輸出是否被沙箱或政策擋下。
- **Windows 出現 `AttachConsole failed` 等 node-pty 訊息**：常見於子程序記錄；以**結束碼與輸出檔是否存在**為準。

## 其他資源

- Headless 模式：[Headless Mode | gemini-cli](https://google-gemini.github.io/gemini-cli/docs/cli/headless.html)

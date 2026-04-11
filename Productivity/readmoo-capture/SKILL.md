---
name: readmoo-capture
description: Guides agents through Readmoo web reader export from onboarding through stage-1 viewport screenshots only. Agents must first check for readmoo-auth.json in the project root; if present, prefer running capture first and only fall back to playwright-cli login plus state-save when missing or when capture indicates expired state (signin). Before capture, ensure project root has uv deps (uv init if no pyproject.toml, then uv add playwright pillow, uv sync, playwright install chromium). Uses skill-bundled scripts/readmoo_capture_snapshots.py via uv run from ~/.cursor/skills/readmoo-capture/scripts/ (Windows: %USERPROFILE%\.cursor\skills\readmoo-capture\scripts\readmoo_capture_snapshots.py). Triggers: Readmoo 匯出、階段一、截圖、readmoo_capture_snapshots、readmoo-auth.json、manifest.json before OCR.
---

# Readmoo 階段一：從流程說明到截圖腳本完成

本 skill 對齊 wiki《Readmoo 網頁版匯出（Playwright）》中 **人工起點 → 儲存 storage state → 純截圖腳本跑完並驗證** 的範圍。**不含** OCR（`readmoo_ocr_pages.py`）與組章（`readmoo_assemble_markdown.py`）；若使用者要全管線，先讀同一 wiki 的後半段。

## 權威來源

- Wiki（完整細節、話術、禁止事項）：`G:\我的雲端硬碟\Obsidian\Agent\wiki\Readmoo-網頁版匯出-Playwright流程.md`
- **階段一截圖腳本**與本 skill **同捆**，固定路徑：
  - 相對於 skill 目錄：`scripts/readmoo_capture_snapshots.py`
  - Windows 範例：`%USERPROFILE%\.cursor\skills\readmoo-capture\scripts\readmoo_capture_snapshots.py`
- **`readmoo-auth.json`**：預設放在**專案根目錄**（與 wiki／`state-save` 慣例一致）。Agent **進入流程時先檢查**該路徑是否存在且為一般檔案；**有則優先**走「直接截圖」嘗試，**無或截圖判定過期**再走 `playwright-cli` 登入與 `state-save`。
- **playwright-cli**（`open`／`state-save`）：在**同一專案根目錄**（workspace 根）執行。
- **執行截圖腳本**：仍在該專案根目錄下用 **`uv run`** 呼叫 **skill 內腳本的絕對路徑**（見關卡 4）。**不要**改用專案根目錄的 `readmoo_capture_snapshots.py` 或其他複本，以免與本 skill／`manifest.json` 的 `capture_script` 欄位約定不一致。
- **專案尚無 uv 環境時**：Agent 應在專案根**先**依 **關卡 3** 完成 `uv init`（僅當無 `pyproject.toml`）與 `uv add playwright pillow`，再 `uv sync` 與安裝 Chromium；**不要**在未確認依賴前就跳去關卡 4。

## Agent 行為原則（本階段）

1. **先說明階段目標**，再給指令；不要一次混談 OCR／分章。
2. **一次只推進一個關卡**；下一關前確認產物存在。
3. **進入後第一步**：在**專案根目錄**（已 `cd` workspace 根）檢查 **`readmoo-auth.json` 是否存在**。  
   - **存在**：向使用者簡短說明「先沿用既有登入狀態嘗試截圖；若失敗再請你登入重存」→ 確認依賴後**優先執行截圖腳本**（關卡 4）。  
   - **不存在**：進入 **關卡 1–2**（`open` → 登入與第一頁 → `state-save`），再截圖。
4. **過期／無效判定**：截圖腳本若因仍停在登入頁而結束（stderr 提示 `signin`、或程序退出碼 **2**），**視為** `readmoo-auth.json` 已過期或不適用 → **不要**重複盲跑；改引導使用者走 **關卡 1–2** 重新製作 `readmoo-auth.json`，再執行關卡 4。
5. **絕不**代替使用者決定「第一頁」：**僅在**需重新 `state-save` 時（B 路徑），必須由使用者在 `playwright-cli` 開出的視窗內手動翻到起點頁。若走 A 路徑（沿用既有 json），起點為**當初存 state 時**的頁面；若要改起點，必須重走 B 路徑並在存檔前翻到新起點。
6. 在 B 路徑中，於使用者明確回覆「已登入且已到第一頁」且瀏覽器仍開著之前，**不要**執行 `state-save`。
7. Python 依賴與腳本執行：**優先** 在專案根用 uv（見關卡 3：`uv init` → `uv add` → `uv sync` → `uv run …`）；與 wiki 一致。使用者若堅持以全域 `python` 執行可配合，但 Agent 預設仍走 uv。
8. `readmoo-auth.json` 含 cookie／儲存狀態，**勿提交 git**；若專案尚未忽略，提醒列入 `.gitignore`。

## 階段閘門檢查清單

| 關卡 | 進入條件 | 產物／狀態 |
|------|-----------|------------|
| 0 說明對齊 | 使用者要開始 Readmoo 匯出 | 使用者理解：優先沿用 `readmoo-auth.json`；必要時才登入重存；階段一只截圖 |
| 0a 檢查 auth | 已 `cd` 專案根 | 確認 `readmoo-auth.json` 有／無；決定走 A 或 B 路徑（見下） |
| 0b uv 專案就緒 | 將執行關卡 4 前 | 專案根有 `pyproject.toml` 且已納入 `playwright`、`pillow`（見關卡 3）；否則先 `uv init`／`uv add`／`uv sync` |
| A 直接截圖 | **有** `readmoo-auth.json`；依賴已就緒；已對齊 `--max-pages` | 執行關卡 4；成功則產物齊；若 signin／exit 2 → 轉 B |
| B1 開閱讀器 | **無** auth 或 A 失敗；有 mooreader 網址 | 可見 headed 視窗 |
| B2 登入與第一頁 | 使用者完成 | 網址為 mooreader、可見內文、**非** signin；視窗勿關 |
| B3 state-save | 上列皆真 | `readmoo-auth.json` 寫入專案根 |
| 4 截圖腳本 | `readmoo-auth.json` 存在；已確認 `--max-pages` | `readmoo_<ID>/assets/*.png`、`manifest.json`、`run.log` |

**路徑摘要**：`0a` → `0b`（必要時）→ 若有 auth → **A → 4**；若無 auth 或 A 判定過期 → **B1 → B2 → B3 → 4**（關卡 4 前仍須滿足 `0b`）。

## 關卡 1：開啟閱讀器（playwright-cli，僅 B 路徑）

在**專案根目錄**開終端機，執行（將書籍 ID 換成實際數字）：

```powershell
playwright-cli open --headed --persistent "https://new-read.readmoo.com/mooreader/你的書籍ID"
```

**Agent 應提示使用者**：只用這個視窗登入；翻到要當**起點**的第一頁；完成後回覆「已登入並到第一頁」。**必須** `--headed`（避免看不到視窗）；**建議** `--persistent` 以利與後續 `state-save` 一致。

若使用者看不到視窗：Alt+Tab、第二螢幕、確認有 `--headed`。

## 關卡 2：儲存 storage state（僅 B 路徑）

**同一專案目錄**，瀏覽器仍為 playwright-cli 開啟且已完成登入與第一頁定位：

```powershell
cd <專案根目錄>
playwright-cli state-save readmoo-auth.json
```

完成後 agent **必須確認**檔案存在；若不存在，**停止**，不要跑截圖腳本。

**重點**：state 必須來自 **playwright-cli 這個 Chromium**，不是一般 Chrome 手動匯出。

## 關卡 3：依賴（僅首次、環境變更，或專案尚無 `pyproject.toml`）

**Agent 進入流程時**：在專案根檢查是否存在 `pyproject.toml`，且依賴是否已含 **playwright**、**pillow**（截圖腳本與末頁指紋所需）。未就緒則依序完成下列步驟，**再**進關卡 4。

### 3a 專案根尚無 `pyproject.toml`

在**專案根目錄**初始化並加入依賴（非互動；目錄已非空時仍可執行）：

```powershell
cd <專案根目錄>
uv init --no-readme
uv add "playwright>=1.49.0" "pillow>=11.0.0"
```

若使用者已手動建立空專案、僅缺依賴，可略過 `uv init`，直接 **3b**。

### 3b 已有 `pyproject.toml` 但尚未加入 playwright／pillow

```powershell
cd <專案根目錄>
uv add "playwright>=1.49.0" "pillow>=11.0.0"
```

### 3c 同步與瀏覽器二進位

```powershell
cd <專案根目錄>
uv sync
uv run playwright install chromium
```

完成後以 `uv run python -c "import playwright; import PIL"` 快速自檢（無錯誤即可）。

## 關卡 4：純截圖腳本（階段一）

**進入前再次確認**：專案根目錄有 `readmoo-auth.json`；與使用者對齊本次 `--max-pages`（主要停止條件）。  
若剛從 A 路徑失敗轉入 B 路徑，須在 **B3 完成後**再執行本關。

**建議（有視窗，方便觀察翻頁）**：在**已通過關卡 3 的專案根目錄**（通常即 **Cursor workspace 根**）執行；腳本本體在 **skill 目錄**。

```powershell
$CAP = Join-Path $env:USERPROFILE '.cursor\skills\readmoo-capture\scripts\readmoo_capture_snapshots.py'
cd <專案根目錄>
uv run $CAP --storage-state readmoo-auth.json --url "https://new-read.readmoo.com/mooreader/你的書籍ID" --max-pages 120
```

（`$CAP` 可改為你機器上該 skill 的實際絕對路徑；重點是 **`uv run` 的目標檔必須是 skill 內的 `scripts/readmoo_capture_snapshots.py`**。）

**可選參數**（與腳本一致）：

- `--out-dir`：輸出根目錄。未指定時，預設為**目前工作目錄**（`Path.cwd()`）下的 `readmoo_exports`；在 Cursor 內建終端若已 `cd` 到專案根，即等同 **workspace 根目錄**（對應 `_default_out_root()`）。若要寫入 wiki 的 raw，請自行傳 `--out-dir "G:\我的雲端硬碟\Obsidian\Agent\raw\readmoo_exports"`。
- `--headless`：無頭模式（`launch(headless=True)`）。`--pause-ms`（預設 900）、`--same-streak`（預設 1）**有無 headless 都會生效**：前者控制每步等待；後者用於翻頁後 viewport 指紋連續相同達該次數則視為末頁。
- **停止條件**（腳本已移除依章節停止）：主要為 **`--max-pages`**；另可因 **`--same-streak`** 判定末頁而提前結束。

### 執行後常見結束原因

- 達 `--max-pages`
- 末頁偵測（連續翻頁畫面指紋不變達 `--same-streak`）
- 網址仍含 `signin` → **state 無效或過期**，應回到關卡 1–2 重做，**不要**硬跑 OCR

## 完成驗證（階段一「完成」的定義）

在輸出目錄下檢查（預設為 **workspace（目前工作目錄）** 下 `readmoo_exports/readmoo_<書籍ID>/`，有傳 `--out-dir` 則依該路徑）：

- `assets/` 內有預期數量的 `p*.png`
- `manifest.json` 存在
- `run.log` 存在（若腳本有寫入）

Agent 應向使用者簡報：張數、是否有 manifest、停止原因（max-pages／末頁／錯誤）。

### 僅有舊截圖、沒有 manifest

**不要**直接進 OCR。先：

```powershell
uv run readmoo_backfill_manifest.py --book-dir <readmoo_書籍目錄>
```

## 本階段應避免（對齊 wiki 第八節之精簡版）

- 專案根**明明已有** `readmoo-auth.json`，仍一律從頭逼使用者登入（應先嘗試 A 路徑）
- signin／exit 2 後仍反覆執行截圖而不引導重存 state
- 在 B 路徑中，使用者未確認登入與第一頁就執行 `state-save`
- Agent 自行假設「現在就是第一頁」
- 把截圖、OCR、分章同一則訊息講完
- 缺 `manifest.json` 仍帶使用者跑 `readmoo_ocr_pages.py`

## 話術骨架（僅到階段一結束）

**若已有 `readmoo-auth.json`（A 路徑）**

1. 「專案裡已有 `readmoo-auth.json`，我先沿用這份登入狀態跑階段一截圖；若登入已過期，再請你依流程重新登入並存檔。」
2. 「這次要抓幾頁？我會用 `--max-pages` 設定。」
3. （若失敗）「狀態可能過期了。請依下面步驟用 `playwright-cli` 登入、翻到你要的起點頁，再 `state-save`，我們再跑一次截圖。」

**若沒有 auth 或 A 失敗後（B 路徑）**

1. 「請在 `playwright-cli` 開出的視窗登入，並翻到你要當起點的第一頁。完成後告訴我。」
2. 「接下來在同一專案目錄執行 `playwright-cli state-save readmoo-auth.json`。」
3. 「然後我只跑階段一截圖，不做 OCR。這次要抓幾頁？我會用 `--max-pages` 設定。」
4. 「跑完後我會確認 `assets/` 與 `manifest.json`。」

## 後續（本 skill 不展開執行）

- 階段二：`uv run readmoo_ocr_pages.py --book-dir <readmoo_書籍目錄>`
- 階段三：`uv run readmoo_assemble_markdown.py --book-dir <readmoo_書籍目錄>`

細節與 OCR 引擎選擇見 wiki 第四、五節。

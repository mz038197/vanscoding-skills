---
name: agents-md-guide
description: >-
  引導初次使用者建立自己的 AGENTS.md，採階段式引導（先核心、再記憶、再心跳），
  產出單一檔案即可從第一天用到進階。當使用者要建立 AGENTS.md、撰寫 agent 指令、或問「怎麼寫 AGENTS.md」時使用此 skill。
---

# AGENTS.md 建構引導 — 給工作區的 Agent 指令

本 skill 協助初次使用者建立 **AGENTS.md**，讓 Cursor、nanobot 或其他 agent 知道「自己是誰、怎麼開機、怎麼用記憶與心跳」。採用**階段式**與**條件式**設計：同一份 AGENTS.md 在還沒有 `memory/` 或 `HEARTBEAT.md` 時也能正常運作；之後建立這些檔案後不必改 AGENTS.md 就會生效。

## 何時使用本引導

- 第一次要為工作區或 agent 建立 AGENTS.md
- 想合併多份 AGENTS.md（例如 nanobot 版與通用模板版）並統一格式
- 不確定記憶、心跳在「初期還沒有」時該怎麼寫——本引導用條件式描述處理

## AGENTS.md 是什麼

`AGENTS.md` 是給 **agent 讀的工作區指令**：身份與開機流程、記憶與心跳規則、對外行為、群組禮節、工具與平台格式等。本引導產出的內容同時適用 Cursor 系工具與 nanobot；記憶與心跳段落以「若存在則…」撰寫，故從第一天到之後擴充都能用同一份檔案。

## 設計原則（引導時向對方說明）

1. **一份檔案從頭用到尾**：不產出「簡易版 / 完整版」兩份，避免分裂。
2. **條件式描述**：凡依賴「記憶目錄、MEMORY.md、HEARTBEAT.md、cron」的段落，一律寫成「若存在則…」「當環境支援時…」，沒有就跳過，不報錯。
3. **階段式擴充**：先完成核心（身份、原則、Red Lines、群組、工具），再依需要加入記憶與心跳的說明與實際建立目錄/檔案。

---

## 撰寫流程（依序進行）

### 步驟 1：確認檔案位置與標題

- **路徑**：工作區根目錄的 `AGENTS.md`，或環境約定位置（例如 `~/.nanobot/workspace/AGENTS.md`）。
- **標題**：建議 `# AGENTS.md — Your Workspace` 或 `# Agent Instructions`，與既有慣例一致即可。

先詢問：「這份 AGENTS.md 會放在哪個專案或目錄？標題想用英文還是中文？」

---

### 步驟 2：產出「核心」區塊（必做，不依賴記憶/心跳）

核心區塊包含以下內容，**不需要**事先建立 `memory/` 或 `HEARTBEAT.md`：

- **身份與開機**：若存在則讀 `SOUL.md`、`USER.md`；若存在 `BOOTSTRAP.md` 則依其執行後刪除。Session 開始時若存在 `memory/` 則讀取今日與昨日的 `memory/YYYY-MM-DD.md`（若存在）；若為**主 session**（直接與人類對話）且存在 `MEMORY.md` 則讀取。一律寫成「若存在則…」，沒有就跳過。
- **基本原則**：簡潔、準確、友善；呼叫工具前簡短說明意圖，不預測結果；時態精準（執行前「I will run X」、收到結果後「X returned Y」）；在得到工具結果前不宣稱成功；請求模糊時先問清楚。
- **Red Lines**：不外洩私人資料；不經詢問不執行破壞性指令；優先 `trash` 而非 `rm`；有疑慮時先問。
- **對外 vs 對內**：讀檔、探索、搜尋、在工作區內可自由做；發信、發文、對外發送等先問。
- **群組**：在群組中你是參與者而非人類的代言人。何時該回（被點名、能加值、糾正重要錯誤等）、何時應沉默（閒聊、已有人回答、避免刷存在感）；避免同一則訊息回多次（triple-tap）。若平台支援表情反應（Discord、Slack），可適度使用表情符號，一次一則。
- **工具與平台**：Skills 與 `TOOLS.md`（若存在）；若適用，可註明平台格式（例如 Discord 不用 markdown 表格、多連結用 `<>`；WhatsApp 不用標題、用粗體或大寫強調）。若有語音敘事需求可註明（例如 ElevenLabs TTS）。

產出時直接使用「若存在則…」的寫法，讓 agent 在沒有這些檔案時也不會出錯。

---

### 步驟 3：產出「記憶」區塊（選做，條件式）

向對方說明：「記憶機制可以之後再加。現在先寫進 AGENTS.md 也無妨，因為是條件式——沒有 `memory/` 或 `MEMORY.md` 時 agent 會自動跳過。」

- **每日筆記**：若工作區存在 `memory/`，則 session 開始時讀取 `memory/今天.md`、`memory/昨天.md`（若存在）。
- **長期記憶**：若存在 `MEMORY.md` 且為**主 session**，則讀取並可更新；在群組或共用 session **不**載入 MEMORY.md（隱私）。
- **寫下來才記得住**：若使用記憶，重要事項寫入 `memory/YYYY-MM-DD.md` 或 `MEMORY.md`，不依賴「心裡記住」。

若對方**現在**就要啟用記憶，引導建立 `memory/` 目錄與 `MEMORY.md`（可為空），並說明之後可在 heartbeat 或手動時把每日檔精煉進 MEMORY.md。

---

### 步驟 4：產出「心跳」區塊（選做，條件式）

向對方說明：「心跳需要環境支援（例如 nanobot 每 30 分鐘輪詢）。若你的環境還沒有，這段先寫進 AGENTS.md 也沒關係——收到 heartbeat 且存在 `HEARTBEAT.md` 時才執行。」

- **觸發條件**：若收到 heartbeat 輪詢訊息**且**工作區存在 `HEARTBEAT.md`，則讀取並依其指示執行；若無需執行則回覆 `HEARTBEAT_OK`。
- **管理方式**：若環境允許，可用檔案工具對 `HEARTBEAT.md` 新增、刪除或改寫任務（例如 `edit_file` / `write_file`）；週期性任務寫入 HEARTBEAT.md，而非僅建一次性 cron。
- **Heartbeat vs Cron**：精準時間、一次性提醒、要直接發送到頻道時用 **cron**（若環境支援，例如 `nanobot cron add`）；可批次、可略為延遲、需對話脈絡的週期檢查用 **heartbeat**。

若對方**現在**就有 heartbeat 環境，引導建立 `HEARTBEAT.md`（可為空或簡短清單），並可選建立 `memory/heartbeat-state.json` 記錄上次檢查時間。

---

### 步驟 5：產出「提醒／Cron」區塊（選做，依環境）

若環境支援 cron（例如 nanobot），可加入一節說明：

- 當使用者要求「在指定時間提醒」時，使用環境提供的 cron 指令（例如 `nanobot cron add --name "reminder" --message "..." --at "YYYY-MM-DDTHH:MM:SS" --deliver --to "USER_ID" --channel "CHANNEL"`），並從當前 session 取得 USER_ID 與 CHANNEL。
- **不要**只把提醒寫進 MEMORY.md——那樣不會觸發實際通知。

若環境不支援 cron，此節可省略或註明「當你日後有 cron 時可加入此節」。

---

### 步驟 6：收尾與檢查

1. **存檔**：確認 `AGENTS.md` 在約定路徑、副檔名為 `.md`。
2. **結構**：至少具備核心區塊；記憶與心跳為條件式，可與核心並存。
3. **用語**：與專案或 USER.md、SOUL.md 一致；標題層級統一（例如 `##` 大節、`###` 小節）。
4. **長度**：若過長可將重複或範例移至 `reference.md`，SKILL 內保留「見 AGENTS_TEMPLATE.md」即可。

---

## 完整模板

引導時可依步驟逐段產出，或讓對方直接從本 skill 的 **AGENTS_TEMPLATE.md** 複製後再依環境刪減/改寫。模板已採用條件式描述，從第一天即可使用。

- 完整合併版（含 YAML frontmatter、核心、記憶、心跳、cron）見同目錄下 **[AGENTS_TEMPLATE.md](AGENTS_TEMPLATE.md)**。
- 若對方使用 nanobot，請保留 cron 一節並依實際指令調整；若純 Cursor 且無 heartbeat，可刪除 cron 與 heartbeat 段落，僅留核心與記憶（仍為條件式）。

---

## 引導時可問的關鍵問題

1. 「這份 AGENTS.md 會放在哪個專案或目錄？標題想用英文還是中文？」
2. 「你現在有沒有 SOUL.md / USER.md？若沒有，要不要先做身份與偏好（可參考 USER.md 引導）？」
3. 「你會不會用到長期記憶？若會，我們可以現在建 `memory/` 和 `MEMORY.md`；若還不確定，先寫條件式段落即可。」
4. 「你的環境有沒有 heartbeat 或 cron（例如 nanobot）？若有，我們加上對應段落並建立 HEARTBEAT.md 或說明 cron 用法。」
5. 「有沒有 Red Lines 或對外行為要特別寫明（例如不代發文、不刪檔先問）？」

依回答產出對應區塊，並建議貼到約定路徑後再微調。

---

## 總結檢查清單

完成後可協助對方確認：

- [ ] 檔案名為 `AGENTS.md`，位於約定目錄
- [ ] 至少具備核心區塊（身份、原則、Red Lines、對外、群組、工具）
- [ ] 記憶與心跳皆為「若存在則…」，沒有 memory/ 或 HEARTBEAT.md 時不會報錯
- [ ] 若有 cron 環境，已加入提醒一節並註明勿只寫 MEMORY.md
- [ ] 標題層級與用語一致，方便日後維護

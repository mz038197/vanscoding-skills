---
name: google-sheets
description: 使用 Google Sheets API / gspread 讀寫 Google 試算表（支援讀取範圍、更新、附加列、清除等基本操作）。
metadata: {"nanobot":{"emoji":"📊","requires":{"bins":["python3"]},"pip":["gspread","google-auth"]}}
---

# Google Sheets Skill

此 Skill 用來讓 agent 與 Google Sheets（試算表）互動：讀取範圍、更新儲存格、附加列、清除範圍等。

- 適用情境：需要在自動化流程或教案中保存學生分數、記錄、讀取教案內容，或用試算表作為簡易資料庫時。
- 不適用：需要人為授權的情境（若使用服務帳號，無法代表使用者存取私人試算表）。

重要：使用前請先完成下列先決條件。

先決條件

1. 在 Google Cloud Console 啟用 Google Sheets API（以及必要時的 Drive API）。
2. 建議使用「服務帳號（Service Account）」進行機器人存取：
   - 建立服務帳號並產生 JSON 金鑰檔（service-account.json）。
   - 將目標試算表分享給服務帳號的 email（例如: my-svc@...iam.gserviceaccount.com）。
3. 安裝 Python 套件（若使用 gspread 範例）：
   - pip install gspread google-auth
4. 設定環境變數（其中一種方式）：
   - GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   或
   - 把 service-account JSON 內容放到 GOOGLE_SA_JSON 環境變數（可在容器或 CI 中使用）。
5. 取得試算表 ID（Spreadsheet ID）或完整 URL，Skill 的範例會用 SHEET_ID 環境變數。

檔案放置與執行位置建議

- Skill 的程式碼應放在專案的 skills 目錄中：
  - 建議路徑（此 repo）： D:\Work\Python\nanobot\nanobot\skills\google-sheets
  - CLI 腳本： D:\Work\Python\nanobot\nanobot\skills\google-sheets\scripts\cli.py
  - Skill 說明檔： D:\Work\Python\nanobot\nanobot\skills\google-sheets\SKILL.md
- 執行時常把 credentials（金鑰）放在 agent 的 workspace：
  - 例如： C:\Users\mz038\.nanobot\workspace\credentials.json
  - 或在環境變數 GOOGLE_APPLICATION_CREDENTIALS 指向金鑰檔路徑
- 原則：程式碼放在 repository 的 skills 目錄，敏感金鑰放在 workspace 或受控的環境變數中（不要放在公開 repo）。

CLI (已建立)

- 檔案： skills/google-sheets/scripts/cli.py
- 支援指令： read, write, append, clear
- 範例：
  - 讀取: python cli.py --sheet-id SHEETID read --range A1:C3
  - 寫入單格: python cli.py --sheet-id SHEETID write --range A1 --value Hello
  - 附加列: python cli.py --sheet-id SHEETID append --row "a,b,c"
  - 清除: python cli.py --sheet-id SHEETID clear --range A1
- 參數與環境變數：
  - --creds: 指定 service account json 檔路徑（可選）
  - --sheet-id: 試算表 ID（或設定 SHEET_ID 環境變數）
  - --worksheet: 工作表名稱（預設：工作表1）

實作細節

- 使用 gspread 與 google.oauth2.service_account.Credentials 進行驗證與存取。
- 支援兩種取得憑證方式：
  1. GOOGLE_APPLICATION_CREDENTIALS 指向 JSON 檔案
  2. 若在 workspace，預設會嘗試讀取 C:\Users\<user>\.nanobot\workspace\credentials.json
- CLI 的錯誤會回傳到 stdout/stderr，方便 agent 或使用者檢查。

安全性和授權注意事項

- 將 service account 金鑰妥善保存，不要將金鑰放到公開 repo。若需要版本控制，可在私有 repo 或使用 Secret Manager。
- 若需代表使用者存取私人試算表，請使用 OAuth2 流程並妥善保存 refresh token（本 Skill 預設使用服務帳號）。

部署與 CI

- 在 CI 或 container 中：
  - 將 service account JSON 透過 CI Secret 注入到環境變數（GOOGLE_APPLICATION_CREDENTIALS 或 GOOGLE_SA_JSON）。
  - 安裝依賴： pip install -r requirements.txt（或 pip install gspread google-auth）。
- 若要在 agent 裡被呼叫：可用 exec 工具執行該 CLI，或直接 import skills/google-sheets/cli.py 中的函式。

常見錯誤及對應

- "FileNotFoundError: 找不到 service account 金鑰檔" — 確認 GOOGLE_APPLICATION_CREDENTIALS 或 workspace 的 credentials.json 路徑
- "insufficient permissions" — 確認 Sheets API 已啟用，且試算表已分享給服務帳號
- JSON 格式錯誤 — 若用環境變數，確保是完整 JSON 字串

後續擴充（建議）

- 提供更完整的高階 wrapper（set_cell, get_cell, find_row, batch_update）
- 加入單元測試與 CI 範例
- 增加 OAuth2 flow 的選項（代表使用者授權）

---
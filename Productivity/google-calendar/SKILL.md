---
name: google-calendar
description: 使用 Google Calendar API 管理行事曆事件（建立、讀取、更新、刪除、列出、設定提醒等）。
metadata: {"nanobot":{"emoji":"📅","requires":{"bins":["python3"]},"pip":["google-api-python-client","google-auth","google-auth-oauthlib"]}}
---

# Google Calendar Skill

此 Skill 用於讓 agent 或自動化腳本操作 Google Calendar：新增/修改/刪除事件、查詢事件、設定提醒與日曆共享等。

適用情境

- 自動化建立會議、同步行程至團隊日曆
- 從外部系統產生事件（如表單回覆、任務系統）
- 建立提醒或排程例行工作

先決條件

1. 啟用 Google Calendar API（Google Cloud Console）。
2. 選擇驗證方式：
   - Service Account（適合服務型資源或已在 Google Workspace 設定 domain-wide delegation）：需將目標日曆分享給 service account 或啟用代表使用者授權。
   - OAuth2 用戶授權（適合代表使用者存取私人日曆）：需建立 OAuth client ID 並完成授權流程取得 token.json。
3. 安裝相依套件：
   - pip install google-api-python-client google-auth google-auth-oauthlib

授權與憑證（簡要說明）

優先推薦：OAuth2（使用者授權）

- 為什麼優先：對於需要在使用者個人日曆建立事件（包含邀請參與者並寄送邀請郵件）的情境，OAuth2（Installed App / Desktop）是最直接且安全的方式。OAuth2 會以使用者身分建立/邀請事件，並可避免 service account 對邀請參與者的限制。

- 簡易流程（建議步驟）：
  1. 在 Google Cloud Console 建立 OAuth 2.0 Client ID（應用類型：Desktop app 或 Other）。
  2. 下載 client_secret.json 並放到工作目錄： C:/Users/<user>/.nanobot/workspace/client_secret.json
  3. 在 repo 或 workspace 建立一個簡單的 CLI（範例：oauth_cli.py）。
  4. 在本機執行： python oauth_cli.py authorize （或印出授權 URL 在另一台有瀏覽器的機器開啟），完成授權後會產生 token.json。
  5. token.json 檔案建議放置： C:/Users/<user>/.nanobot/workspace/token.json（並加入 .gitignore）。
  6. 之後 CLI 用 token.json 建立事件（sendUpdates='all'）即可發送邀請給參與者。

- 建議 scope： https://www.googleapis.com/auth/calendar.events

備援選擇：Service Account（適合後端/系統日曆）

- 優點：適合後端/無人值守的工作流程（如批次建立事件、將系統產生的行程寫入共用日曆）。
- 限制：service account 無法以一般使用者身分直接邀請外部參與者（除非在 Workspace 設定 domain-wide delegation）。若要讓 service account 存取某個私人/個人日曆，需由該日曆的擁有者把日曆分享給 service account 的 client_email。
- 金鑰檔建議放置： C:/Users/<user>/.nanobot/workspace/credentials.json，或透過環境變數 GOOGLE_APPLICATION_CREDENTIALS 指定。


建議檔案結構（repo）

- D:\Work\Python\nanobot\nanobot\skills\google-calendar\
  - SKILL.md  <-- 本檔
  - metadata.yaml 或 SKILL.yaml（若需）
  - scripts/  <-- 放可執行的 CLI 與 helper scripts
    - cli.py
    - helpers.py
  - samples/  <-- 範例輸出或測試檔

使用範例（CLI/腳本）

- oauth_cli.py（已提供範例腳本，位於 skills/google-calendar/scripts/oauth_cli.py）：
  - 授權（會開啟本機瀏覽器）：
    - python scripts/oauth_cli.py authorize
  - 或印出授權 URL（在無瀏覽器環境或要在其他機器完成授權時使用）：
    - python scripts/oauth_cli.py auth_url
    - 在有瀏覽器的機器開啟連結，完成授權並取得 code
    - 回到執行環境後使用： python scripts/oauth_cli.py finish --code <AUTH_CODE>
  - 建立事件（會使用 token.json，並向與會者發出邀請）：
    - python scripts/oauth_cli.py create --calendar primary --start 2026-03-05T10:00:00+08:00 --end 2026-03-05T11:00:00+08:00 --summary "會議" --attendees "a@example.com,b@example.com" --location "會議室"
  - 列出事件：
    - python scripts/oauth_cli.py list --calendar primary --time-min 2026-03-05T00:00:00+08:00 --time-max 2026-03-06T00:00:00+08:00

- 備援：若使用 service account 的 CLI（例如 scripts/cli_service.py），請確保 credentials.json 放置於 workspace 並以 GOOGLE_APPLICATION_CREDENTIALS 指定或程式讀取該檔。

範例檔案路徑（workspace）：
- C:/Users/<user>/.nanobot/workspace/
  - client_secret.json  <-- OAuth client
  - token.json          <-- 授權後的使用者憑證
  - credentials.json    <-- （備援）Service account 金鑰

備註：在使用 oauth_cli.py 時，請先安裝相依套件：
  pip install google-api-python-client google-auth google-auth-oauthlib

建議使用的 OAuth 範圍（Scopes）

- 最常用： https://www.googleapis.com/auth/calendar.events （建立/修改/刪除活動）
- 讀取事件： https://www.googleapis.com/auth/calendar.events.readonly
- 完整存取（包含日曆設定）： https://www.googleapis.com/auth/calendar

實作注意事項

- 時區處理：事件時間要包含時區或以 RFC3339 格式（例如 2026-03-05T10:00:00+08:00）。
- 誤刪風險：刪除/更新操作請在腳本加入確認或 soft-delete 機制（例如先標記再真正刪除）。
- 權限與分享：若使用 service account，請把日曆分享給 service account 的 email，或使用 domain-wide delegation。
- 日配額：長時間大量建立事件時注意 API quota，建議批次與節流。

安全與隱私

- 不要將 client_secret.json 或 service account 金鑰放在公開 repo。使用 CI 時，透過 Secret 管理注入。
- 限制權限範圍（scopes）以降低風險。
- 審查 scripts 中的外部依賴，避免任意命令執行（尤其當 Skill 可能被外部上傳時）。

在 agent/CI 中的部署建議

- 在 container 或 CI 裡透過環境變數注入金鑰路徑或 JSON 內容。
- 安裝相依： pip install -r requirements.txt
- 若需要互動式 OAuth：在本地或有瀏覽器的環境完成授權後把 token.json 上傳到執行環境（或透過安全流程交換 token）。
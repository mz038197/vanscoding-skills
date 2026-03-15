---
name: google-email
description: 使用 Gmail API 讀取、搜尋、傳送及管理郵件（支援草稿、標籤、附件、搜尋查詢與推播通知）。
metadata: {"nanobot":{"emoji":"✉️","requires":{"bins":["python3"]},"pip":["google-api-python-client","google-auth","google-auth-oauthlib","google-auth-httplib2"]}}
---

# Google Email (Gmail) Skill

此 Skill 讓 agent 或自動化腳本以程式化方式操作 Gmail：列出/搜尋郵件、讀取郵件內容（含附件）、傳送郵件／草稿、修改標籤、設定推播通知等。

設想情境

- 自動將特定主題或寄件者的郵件整理至指定標籤
- 定期匯出某種通知信到試算表或文件
- 由 agent 代為傳送/草稿郵件（如提醒、報表）
- 篩選垃圾郵件或產生摘要供人檢閱

不適用情境

- 無法繞過 Gmail 的使用者授權（必須使用合適的 OAuth 或授權設置）。
- 若需以服務帳號直接存取個人 Gmail（非 Workspace 域下的委派），可能會受限。

先決條件

1. 在 Google Cloud Console 啟用 Gmail API（Gmail API）。
2. 選擇驗證方式：
   - OAuth2（推薦，代表使用者）：適合需要代表使用者操作其個人信箱的情境。需要 client_secret.json 並執行授權流程取得 token.json。
   - 服務帳號（Service Account）與域委派（Domain-wide Delegation）：僅在 Google Workspace 管理員允許時可用，適合企業統一管理信箱帳號（需管理員設定）。
3. 設定必要的 OAuth scopes（依功能最小授權）：
   - 讀取郵件： https://www.googleapis.com/auth/gmail.readonly
   - 傳送郵件： https://www.googleapis.com/auth/gmail.send
   - 完整存取（讀寫）： https://www.googleapis.com/auth/gmail.modify
   - 管理草稿： https://www.googleapis.com/auth/gmail.compose
   - 推播/訂閱： https://www.googleapis.com/auth/gmail.metadata

快速開始（給新 agent 的友善引導）

1. 讀本檔（SKILL.md）與範例程式，確認你要做的功能與對應 scope。
2. 把 OAuth client 憑證放到 workspace（預設位置）：
   - C:/Users/<user>/.nanobot/workspace/client_secret.json
3. 若使用 OAuth2，執行授權流程：
   - 有 CLI 範例： oauth_cli.py auth_url（取得授權連結）或 oauth_cli.py authorize（嘗試在執行環境開啟瀏覽器）。
   - 使用者完成授權後會產生 code，或 oauth_cli.py 會儲存 token.json（預設：C:/Users/<user>/.nanobot/workspace/token.json）。
4. 建立並測試簡單讀取腳本（範例在 skills 下應包含 scripts/）：
   - 列出未讀郵件、搜尋特定寄件者或主題、下載附件、或傳送測試郵件。
5. 在實作時務必：使用最小必要 scope、妥善保護憑證與 token.json，並在 log 中避免輸出敏感內容（信件全文、附件）。

常見 API 與功能說明

- 列出郵件： users.messages.list (q=搜尋字串, labelIds= 等)
- 取得郵件內容： users.messages.get (format=raw|full|metadata)
- 傳送郵件： users.messages.send（需先把 MIME 以 base64url 編碼）
- 建立/傳送草稿： users.drafts.create / users.drafts.send
- 修改標籤： users.messages.modify（addLabelIds / removeLabelIds）
- 批次修改： users.messages.batchModify
- 推播通知（watch）： users.watch（需設定 Pub/Sub）
- 下載附件： users.messages.attachments.get

注意事項與實作要點

- 分頁：list 可能回傳大量結果，請用 nextPageToken 分頁抓取。
- 編碼：郵件的原始內容常在 base64url，處理時請正確解碼，且處理 multipart MIME。
- 附件：attachments.get 回傳的是 base64 字串，需解碼後存檔。檔名與檔案類型需信賴來源確認安全性。
- 發信：構造 MIME 時請注意 header（From、To、Subject、Content-Type），並對中文主旨/內文做正確編碼（RFC 2047 / UTF-8）。
- 權限最小化：僅請求執行所需 scope，避免使用廣域 scope 如 gmail.readwrite 若只需傳送請使用 gmail.send。
- 隱私/合規：郵件為高度敏感資料。任何擷取、儲存或轉發都要先獲得使用者同意，並遵守隱私政策/法規。

範例程式片段（Python, 使用 google-api-python-client）

- 初始化 service（假設 token.json 已存在）：

  from google.oauth2.credentials import Credentials
  from googleapiclient.discovery import build
  creds = Credentials.from_authorized_user_file('C:/Users/.../workspace/token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
  service = build('gmail', 'v1', credentials=creds)

- 簡單搜尋並列出信件 ID：

  res = service.users().messages().list(userId='me', q='subject:APCS', maxResults=50).execute()
  msgs = res.get('messages', [])
  for m in msgs:
      print(m['id'])

- 取得郵件內容（raw）並解碼：

  msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
  import base64, email
  raw = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
  mime = email.message_from_bytes(raw)

- 傳送郵件（簡易示例）：

  from email.mime.text import MIMEText
  import base64
  message = MIMEText('測試內容', 'plain', 'utf-8')
  message['to'] = 'someone@example.com'
  message['from'] = 'me@example.com'
  message['subject'] = '測試'
  raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
  res = service.users().messages().send(userId='me', body={'raw': raw}).execute()

運作與錯誤處理建議

- 憑證/授權錯誤：捕捉 401/403，提示重新授權或檢查 token.json 與 client_secret.json 路徑。
- API 配額/速率限制：遇到 429 或 5xx，使用退避機制（exponential backoff）重試。
- 網路/格式錯誤：對解析 MIME、base64 解碼加入錯誤處理以避免崩潰。

如何寫入記憶（給 agent 開發者）

- 如果 agent 後續需要記住使用者偏好（例如常用搜尋字串、要標記的標籤 ID），把這類「偏好」與「設定」寫入 long-term memory（memory/MEMORY.md）而非寫入含敏感郵件內容的記憶。
- 千萬不要把郵件內容或附件寫入長期記憶檔（PII）。

部署建議

- 常見檔案位置（workspace 預設）：
  - client_secret.json（OAuth client）
  - token.json（OAuth token，授權後產生）
- 建議在 skills/google-email 下放 scripts/ 範例：auth_url、authorize、list_messages、get_message、send_message、download_attachment。請參考 google-calendar skills 的 oauth_cli.py 結構以維持一致。

安全提醒

- token.json 與 client_secret.json 含敏感資訊，請勿上傳到公開 repository。
- 傳送郵件前，確認收件者與內文不包含機密資料，或已經經過使用者明確同意。

FAQ（短問答）

- Q: 我可以用 Service Account 存取個人 Gmail 嗎？
  A: 不行（除非透過 Workspace 的 domain-wide delegation 並由管理員授權）。

- Q: 我該用哪個 scope？
  A: 儘量用最小必要權限。例如只需傳送則用 gmail.send；只需搜尋與讀取 metadata 則考慮 gmail.metadata 或 gmail.readonly。

- Q: 如何處理大量郵件？
  A: 使用分頁 (nextPageToken)，批次操作 batchModify，並實作退避重試。


若你要，我可為此 Skill 補上範例 scripts（oauth_cli.py、list_messages.py、send_test.py、download_attachments.py），並把它們放到 workspace 的 skills/google-email/scripts/。請告訴我你需要哪些範例。
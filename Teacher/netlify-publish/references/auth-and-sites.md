# Auth 與站台

步驟 2 才讀。目標：後續 `netlify deploy` 能靜默跑完，不必互動選單。

## Ticket login（未登入時的預設）

學生只負責在**自己的瀏覽器**登入／授權。建站、上傳、拿 URL 都由 agent 做。

Agent 的手停在 CLI 與「打開預設瀏覽器」：開票、用系統打開 `url`、等學生回覆後再 `--check`。登入頁上的帳號、密碼、OAuth、驗證碼一律由學生自己打。

先前課堂事故是 agent 代填或重試登入，觸發鎖帳。`--check` 只問這張票通過了沒，不是登入嘗試，不會走同一條鎖帳路徑。用 `Start-Process` 打開授權頁也不算代登入：只開分頁，不填表。

**完成**：`netlify login --check <ticket_id> --json` 的 `status` 是 `authorized`。

1. 開一張票（`--request` 的字串會出現在授權頁，寫課堂／專案名即可）：

```powershell
netlify login --request "Publish this site" --json
```

JSON 會有 `url`、`ticket_id`、`check_command`。立刻用本機預設瀏覽器打開 `url`：

```powershell
Start-Process <url>
```

告訴使用者：瀏覽器應已打開授權頁；沒帳號就在那頁註冊，有帳號就登入，再允許 Netlify CLI。不要請他複製網址。`Start-Process` 失敗時，再把 `url` 放進對話當後備。

這一輪到此暫停，等使用者回「點好了」或等他在瀏覽器完成。不要為了等授權而連續 `--check` 空轉十分鐘。

2. 使用者回覆後立刻：

```powershell
netlify login --check <ticket_id> --json
```

| `status` | 動作 |
|---|---|
| `pending` | 告訴他授權頁可能還開著，點允許後再說一聲；不要自己狂輪詢 |
| `authorized` | token 已寫進本機 Netlify CLI config，進下一步 |
| `denied` | 停下，請使用者重開一張票 |

登入卡住時，請學生自己在那個分頁處理（忘記密碼、換帳號、過驗證）。Agent 不代填、不重試、不用 Chrome DevTools／瀏覽器 MCP 操作 `app.netlify.com` 的登入或授權頁。對話裡出現密碼或驗證碼：告訴學生改在瀏覽器輸入，不要接收、不要代送。

3. 確認：

```powershell
netlify status --json
```

看得到 user 就繼續建站／deploy。

無旗標的 `netlify login` 會在 agent 的非互動 shell 裡自己開瀏覽器再空等，課堂上不要用。

Token 寫在使用者本機的 Netlify CLI config（Windows：`%APPDATA%\netlify\Config\config.json`）。不要把檔案內容貼進對話。

## 已有 token（備用）

CI 或使用者已經有 personal access token 時，設 `NETLIFY_AUTH_TOKEN` 即可，不必再走 ticket login。

```powershell
if ($env:NETLIFY_AUTH_TOKEN) { "token set" } else { "token missing" }
```

只印有無，不印值。單次指令可加 `--auth $env:NETLIFY_AUTH_TOKEN`。

## 已有站台

這個資料夾已有 `.netlify/state.json`，或使用者／上次回報已給 site ID：之後每個 `deploy` 加 `--site <id-or-name>`，不要 `sites:create`。同一份作業再發佈必須蓋同一條 URL。

第一次成功後立刻綁定，讓下次還找得到：

```powershell
netlify link --id <site-id>
```

這會寫 `.netlify/state.json`。若專案有 git，把 `.netlify` 加進 `.gitignore`。

已登入、這個資料夾卻沒有 link：先 `netlify sites:list --json`，名稱對得上再 link，對不上再新建。

## 新建站台

登入之後、還沒有站台時，agent 直接建，不必再問。先列 team：

```powershell
netlify teams:list --json
```

一個 team 就用它的 slug。多個就問使用者。然後：

```powershell
netlify sites:create --name <slug> --account-slug <team-slug> --json
```

`<slug>` 從資料夾名來，小寫字母、數字、連字號。課堂上很多人會用同一個作業名：被占用就在後面加短後綴再試，不要死重試同一個，也不要用學生真實姓名當後綴。從 JSON 取出 site id，立刻 `netlify link --id`，後續 `--site` 帶它。

`sites:create` 要驗證 email：停下，請學生去收件匣完成驗證再發佈。

也可在第一次 deploy 同時建：

```powershell
netlify deploy --site-name <slug> --team <team-slug> --dir=<artifact> --prod --json
```

## Anonymous（丟一次網址）

沒有帳號、只要暫時可開的 URL，而且使用者同意用完即丟：

```powershell
netlify deploy --dir=<artifact> --allow-anonymous --json
```

站台一小時內要有人認領，否則刪除。課堂要留著改、要同一條 URL 更新：走 ticket login + 具名站台，不要走這條。

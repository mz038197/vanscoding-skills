# Troubleshooting

Deploy 失敗才讀。把 CLI 原文錯誤、log URL、site id 一起回給使用者。修的是 artifact 或參數，然後重跑同一條 `deploy`。

## 指令卡住、出現選單

缺 `--dir`、`--site`／link、或 token，CLI 會問人。補齊旗標再跑。不要在 agent session 裡回答互動提示。

## netlify / npx 找不到

連 `npx` 都沒有就是沒裝 Node：停下，請使用者裝 Node.js LTS，開新終端機再來。不要改去操作 Netlify 登入頁來繞過。本機有舊版 `netlify` 也不改用它，一律 `npx --yes netlify-cli`。

## Not logged in

走 ticket login：`netlify login --request "..." --json`，`Start-Process` 打開 `url`，再 `netlify login --check <ticket_id> --json` 直到 `authorized`。見 [auth-and-sites.md](auth-and-sites.md)。不要改跑無旗標的 `netlify login`。CI 才改設 `NETLIFY_AUTH_TOKEN`。

## No site linked

加 `--site <id-or-name>`，或先 `netlify link --id`，或 `--site-name` + `--team` 新建。見 [auth-and-sites.md](auth-and-sites.md)。

## 開網站是 Netlify 404

`--dir` 根目錄沒有 `index.html`。補一份（複製首頁檔，不要改原檔名）再 `--prod`。其他 HTML 仍可用 `/檔名.html` 打開，但 `/` 只認 `index.html`。

## Publish directory not found / 開起來是原始碼

`--dir` 指錯層。先在本機確認 artifact 裡有入口檔，再把 `--dir` 對準那層。建置失敗時停在建置錯誤，不要改 `--dir` 去蓋過壞掉的 build。

## 網站重整路由 404

SPA 缺 `_redirects`。在 artifact 根加：

```
/*    /index.html   200
```

再 `--prod` 傳一次。

## Secrets scanning 擋住

若掃到的是真密鑰：從要上傳的檔案拿掉，輪替該密鑰，再發。不要關 scanner。若是假陽性，用 `SECRETS_SCAN_OMIT_KEYS` / `SECRETS_SCAN_OMIT_PATHS` 收窄，不要設 `SECRETS_SCAN_ENABLED=false`。

## 手動 prod 被 Git push 蓋掉

站台若接了 Git CD，下一次 production branch 的 push 會取代這次 CLI prod。要這次手傳留下去：請使用者在 Netlify UI Deploys 鎖定該 deploy。長期仍應改走 Git CD（本 skill 不做那條）。

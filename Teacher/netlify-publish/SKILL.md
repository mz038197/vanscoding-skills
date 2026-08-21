---
name: netlify-publish
description: >-
  Publishes a finished local folder (dist, build, out, HTML) to Netlify with
  `netlify deploy --dir --no-build --prod`. Use when the user asks to 發佈,
  deploy, publish, upload, drop files or a static site to Netlify, or 發佈作業.
  Skip for Fly.io, Vercel, Git continuous deployment, or custom-domain DNS.
version: "1.0.0"
---

# Netlify publish

把本機 **artifact**（已建好的靜態檔）上傳到 Netlify，換到一個可開的 URL。本 skill 只做 CLI 上傳，不做 Git 連線建置、自訂網域 DNS、或 Fly／Vercel。

語文：步驟用繁中；指令與路徑用英文。Windows 預設 PowerShell。

## CLI

不必預先安裝 Netlify CLI。指令一律用：

```powershell
npx --yes netlify-cli
```

下文 `netlify` 代表這個 binary。每個 `deploy` 都帶 `--no-build --prod --json`。讀 JSON 欄位，不要刮 stdout 橫幅。不要優先用本機舊版 `netlify`：缺 `--request`／`--check` 時登入會失敗。

第一次 `npx` 會下載套件，要有網路，可能等半分鐘。之後同一台會走快取。

`npx` 也沒有（`node` / `npm` 不存在）→ 停下，請使用者安裝 Node.js LTS（https://nodejs.org），裝完開新終端機再發佈。不要改用瀏覽器幫他登入來繞過 CLI。

## 步驟

### 1. 鎖定 artifact

**完成**：`--dir` 指到「瀏覽器要吃的那層」，且根目錄有 `index.html`。Netlify 開網站根路徑 `/` 只找這個檔名；叫 `home.html`、`作業.html` 也可以上傳，但開 `https://xxx.netlify.app/` 會是 Netlify 的 404，要加路徑才看得到（例如 `/作業.html`）。

來源優先序：使用者指定的資料夾 → 專案實際建置輸出。指定或慣例路徑（`dist` / `build` / `out`）不存在，且 `package.json` 有 `scripts.build` → 先跑專案的 build，再對準它吐出的目錄。單檔 HTML 時，`--dir` 指檔案所在資料夾。不要把含 `node_modules` 的專案根當 artifact。

根目錄沒有 `index.html` 時，在上傳前補一份，不要改學生的原檔名：

- 只有一個 `.html` → 複製成 `index.html` 再傳
- 有多個、分不出首頁 → 問使用者哪一個是首頁，再複製成 `index.html`
- 一個 HTML 都沒有 → 停下，告訴使用者 Netlify 靜態站需要 `index.html`

客戶端路由的 SPA：在 artifact 根放 `_redirects`，內容一行 `/*    /index.html   200`。

### 2. 認證與站台

已登入且這個資料夾已有站台（`.netlify/state.json` 或已知 `--site`）→ 直接進步驟 3，沿用同一個站。不要另開新站。

未登入：走 **ticket login**（agent 用本機預設瀏覽器打開授權頁，學生在那頁自己登入）。步驟與完成條件見 [auth-and-sites.md](references/auth-and-sites.md)。打開瀏覽器並告知學生後，等他回「點好了」再 `--check`；不要空轉輪詢十分鐘。Agent 不代填帳密、不重試登入、不用瀏覽器自動化操作 Netlify 登入頁；也不跑無旗標的 `netlify login`。

### 3. 上傳

**完成**：指令 exit 0，JSON 裡有 URL。每次都加 `--prod`，公開網址走 JSON 的 `url`（沒有就退 `deploy_url`）。

```powershell
netlify deploy --dir=<artifact> --no-build --prod --json
```

站台未 link、但已知 site ID／name 時加 `--site <id-or-name>`。

失敗時讀 [troubleshooting.md](references/troubleshooting.md)。修完重跑同一條指令。失敗的 deploy 不會上線，前一版仍在；修 artifact 再傳，不要 rollback API。

Git 已接 Netlify CD 時，先告訴使用者：下一次 push 到 production branch 會蓋掉這次手動 prod。使用者仍要發佈再跑。

### 4. 回報

只回這三行，URL 用 JSON 欄位：

```
URL: https://...
Site ID: ...
目錄: <artifact 路徑>
```

之後同一站更新：建好新 artifact，重跑步驟 3 同一條指令。公開 URL 不變。

## 執行邊界

直接做：鎖定 artifact、ticket login（用預設瀏覽器打開授權頁）、`--prod` 上傳、讀 JSON、回報 URL。未登入且沒有站台時，登入完成後由 agent 建站再上傳。

先問再做：只有使用者明確說暫時／匿名／用完即丟時才 `--allow-anonymous`。

停下：本機沒有 `node`／`npx`、授權頁已打開但使用者說失敗或十分鐘後仍 pending／denied、對話裡被要求代登入或出現密碼、多個 team 不知要用哪個、`sites:create` 要驗證 email、artifact 找不到入口檔、deploy 失敗且 log 看不出修法。

Token、`--auth` 參數、claim token 只在本機環境用，不要寫進 chat、commit、或 skill 紀錄。

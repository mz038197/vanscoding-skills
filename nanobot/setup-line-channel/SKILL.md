---
name: add-line-channel
description: 為 nanobot 專案新增 LINE Messaging API channel。使用 aiohttp webhook server 接收訊息，httpx 回覆訊息，Cloudflare Tunnel 暴露公網端點。當用戶想整合 LINE Bot、設定 LINE Webhook、或詢問 nanobot LINE channel 相關問題時使用此 skill。
---

# 為 nanobot 新增 LINE Channel

## 架構概覽

```
LINE App → LINE Server → Cloudflare Tunnel → localhost:8080 (aiohttp)
                                                     ↓
                                               MessageBus
                                                     ↓
                                              AgentLoop → LINE Push API → LINE App
```

## 需要改動的檔案

| 檔案 | 類型 |
|------|------|
| `nanobot/config/schema.py` | 新增 `LineConfig` + 加入 `ChannelsConfig` |
| `nanobot/channels/line.py` | 全新建立 |
| `nanobot/channels/manager.py` | 加入 LINE 初始化區塊 |
| `pyproject.toml` | 新增 `aiohttp` 依賴 |
| `~/.nanobot/config.json` | 新增 line 設定區塊 |

---

## Step 1：`nanobot/config/schema.py`

在 `QQConfig` 之後、`MatrixConfig` 之前插入：

```python
class LineConfig(Base):
    """LINE Messaging API channel configuration (webhook mode)."""

    enabled: bool = False
    channel_secret: str = ""
    channel_access_token: str = ""
    webhook_path: str = "/line/webhook"
    webhook_port: int = 8080
    allow_from: list[str] = Field(default_factory=list)
```

在 `ChannelsConfig` 末尾加入：

```python
line: LineConfig = Field(default_factory=LineConfig)
```

## Step 2：`nanobot/channels/line.py`（新增）

關鍵實作點：
- `start()`：用 `aiohttp` 啟動 HTTP server，監聽 `webhook_port`
- `stop()`：呼叫 `runner.cleanup()` 乾淨關閉
- `send()`：用 `httpx` POST 到 `https://api.line.me/v2/bot/message/push`
- `_verify_signature()`：HMAC-SHA256 驗簽，使用 `channel_secret`
- `_handle_webhook()`：解析 LINE events，拒絕無效簽名（回傳 403）
- `_process_event()`：只處理 `type=message` + `message.type=text`，群組用 `groupId` 當 `chat_id`

```python
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
```

## Step 3：`nanobot/channels/manager.py`

在 Matrix channel 區塊之後、`self._validate_allow_from()` 之前加入：

```python
# LINE channel
if self.config.channels.line.enabled:
    try:
        from nanobot.channels.line import LineChannel
        self.channels["line"] = LineChannel(
            self.config.channels.line,
            self.bus,
        )
        logger.info("LINE channel enabled")
    except ImportError as e:
        logger.warning("LINE channel not available: {}", e)
```

## Step 4：`pyproject.toml`

在 `dependencies` 末尾加入：

```toml
"aiohttp>=3.10.0,<4.0.0",
```

安裝：

```powershell
.venv\Scripts\pip install aiohttp
```

## Step 5：`~/.nanobot/config.json`

在 `channels` 的 `qq` 區塊後加入：

```json
"line": {
  "enabled": false,
  "channelSecret": "",
  "channelAccessToken": "",
  "webhookPath": "/line/webhook",
  "webhookPort": 8080,
  "allowFrom": []
}
```

---

## LINE Developers Console 設定

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立或選擇 **Messaging API** Channel
3. 取得以下兩個值填入 `config.json`：
   - **Channel Secret** → Basic settings 頁面
   - **Channel Access Token** → Messaging API 頁面（點 Issue 產生）
4. 啟用 Webhook：`Use webhook` → **Enabled**

---

## Cloudflare Tunnel 設定

### 安裝

```powershell
winget install Cloudflare.cloudflared
```

### 臨時使用（開發/測試）

```powershell
cloudflared tunnel --url http://localhost:8080
```

輸出的 URL 格式：`https://xxx-xxx.trycloudflare.com`

填入 LINE Webhook URL：
```
https://xxx-xxx.trycloudflare.com/line/webhook
```

> ⚠️ 每次重啟 cloudflared URL 會改變，須重新設定 LINE Console

### 長期使用（生產環境）

```powershell
# 1. 需要先登入 Cloudflare 帳號
cloudflared tunnel login

# 2. 建立命名 tunnel
cloudflared tunnel create nanobot-line

# 3. 建立 ~/.cloudflared/config.yml
# tunnel: <tunnel-id>
# credentials-file: ~/.cloudflared/<tunnel-id>.json
# ingress:
#   - hostname: line.yourdomain.com
#     service: http://localhost:8080
#   - service: http_status:404

# 4. 設定 DNS
cloudflared tunnel route dns nanobot-line line.yourdomain.com

# 5. 啟動
cloudflared tunnel run nanobot-line
```

---

## 啟動驗證

啟動 nanobot，確認以下兩行出現：

```
[green]✓[/green] Channels enabled: line
LINE webhook listening on port 8080 at path /line/webhook
```

在 LINE Developers Console 點「Verify」，應回傳 200 OK。

---

## 常見錯誤排查

| 錯誤 | 原因 | 解決方法 |
|------|------|---------|
| `502 Bad Gateway` | nanobot 未啟動，或 webhook server 未監聽 8080 | 確認 `enabled: true` 且 nanobot 已啟動 |
| `empty allowFrom (denies all)` | `allowFrom` 為空陣列 | 改為 `["*"]`（允許所有人）或填入特定 userId |
| `403 Invalid signature` | `channelSecret` 錯誤 | 從 LINE Console Basic settings 重新複製 |
| `aiohttp ImportError` | 套件未安裝 | `pip install aiohttp` |

### `allowFrom` 設定規則

```json
"allowFrom": ["*"]                    // 允許所有人
"allowFrom": ["U1234567890abcdef"]    // 只允許特定 userId
```

取得用戶 `userId`：啟動後傳訊息給 bot，nanobot log 會顯示 `sender_id: U...`

---

## 注意事項

- LINE channel 為 webhook 模式（需公網可達），與 Telegram/DingTalk/Feishu 的長輪詢/Stream 模式不同
- `allowFrom` 不可留空，否則 nanobot 啟動時會報錯並終止
- 群組訊息用 `groupId` 作為 `chat_id`；個人訊息用 `userId`
- 目前僅支援純文字訊息（`message.type=text`）；圖片、貼圖等類型會被忽略

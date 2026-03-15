---
name: browser-use
description: 當使用者需要操作瀏覽器、爬取網頁或網頁自動化時，使用 Browser Use Cloud SDK 撰寫並執行腳本
---
# Browser Use — 讓agent代為操作瀏覽器

當使用者要求**操作瀏覽器**、**爬取網頁**、**從網站取得資料**、**網頁自動化**，或類似「幫我去 OOO 網站做 XXX」時，你應該：

1. **使用 Browser Use Cloud SDK** 撰寫腳本（Python 優先，或 TypeScript）
2. **在終端機執行**該腳本
3. **將執行結果**（`result.output` 或結構化資料）回報給使用者

## API Key 選擇（二選一）

| 模式 | 需要的 Key | 說明 |
|------|------------|------|
| **Cloud** | `BROWSER_USE_API_KEY` | 用他們的雲端瀏覽器與模型，不能改用 OpenAI Key。 |
| **Open Source** | `OPENAI_API_KEY`（或 Anthropic / Google） | 本機跑瀏覽器，LLM 用 OpenAI / Claude / Gemini，**可用你現有的 OpenAI Key**。 |

- 若使用者**已有 OpenAI Key、不想再申請 Browser Use Key**，請用 **Open Source** 寫法（見下方「Open Source：用 OpenAI Key」）。
- 若使用者未特別指定，可預設用 Cloud（需 `BROWSER_USE_API_KEY`），或依專案已有環境變數決定。

## 前置條件

- **Cloud**：`pip install browser-use-sdk`，設定 `BROWSER_USE_API_KEY`。取得：https://cloud.browser-use.com/settings?tab=api-keys
- **Open Source**：`pip install browser-use uv`，執行 `uvx browser-use install` 安裝 Chromium；設定 `OPENAI_API_KEY`（或 `ANTHROPIC_API_KEY` / `GOOGLE_API_KEY`），不需 BROWSER_USE_API_KEY。

## 執行環境（venv）

- **請在 venv 內執行**：`pip install` 與執行腳本時，應使用專案的虛擬環境，避免污染全域 Python、也減少與其他專案套件衝突。
- **若專案已有 venv**：先啟動 venv 再執行指令。
  - Windows：`.\venv\Scripts\activate`，或直接用 `.\venv\Scripts\python script.py`。
  - macOS / Linux：`source venv/bin/activate`，或 `venv/bin/python script.py`。
- **若尚無 venv**：在專案目錄執行 `python -m venv venv` 建立，再啟動 venv 後安裝依賴（`pip install browser-use-sdk` 或 `pip install browser-use uv`）並執行腳本。

## 撰寫腳本時使用以下 API

### 新專案請用 v3 API

**Python (v3)：**
```python
import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse
from pydantic import BaseModel  # 若要結構化輸出

async def main():
    client = AsyncBrowserUse()
    # 自然語言任務，回傳在 result.output
    result = await client.run("使用者的自然語言指令，例如：取得 Hacker News 前 5 則標題")
    print(result.output)
    # 可選：結構化輸出
    # result = await client.run("...", output_schema=YourPydanticModel)

asyncio.run(main())
```

**常用 run() 參數 (v3)：**
- `output_schema`: Pydantic 模型 → 回傳型別化資料
- `session_id`: 沿用同一瀏覽器 session
- `keep_alive=True`: 任務結束後保留 session 以便後續指令
- `proxy_country_code`: 如 `"us"`, `"de"` 住宅代理
- `profile_id`: 已登入的瀏覽器設定檔
- `max_cost_usd`: 成本上限（美金）

**Session 多步驟範例：**
```python
session = await client.sessions.create(proxy_country_code="us")
r1 = await client.run("先登入 example.com", session_id=str(session.id), keep_alive=True)
r2 = await client.run("再點設定頁", session_id=str(session.id))
await client.sessions.stop(str(session.id))
```

### v2 API（若專案已用 v2）

```python
from browser_use_sdk import AsyncBrowserUse
# client = AsyncBrowserUse(); result = await client.run("...")
```

### Open Source：用 OpenAI Key（不需 BROWSER_USE_API_KEY）

使用者若想用 **OPENAI_API_KEY**（或 Anthropic、Google），改用開源套件 `browser-use`，本機跑瀏覽器、LLM 用 OpenAI：

```python
import asyncio
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env 的 OPENAI_API_KEY

async def main():
    llm = ChatOpenAI(model="gpt-4.1-mini")  # 或 gpt-4o 等
    agent = Agent(
        task="使用者的自然語言指令，例如：取得 Hacker News 前 5 則標題",
        llm=llm,
    )
    result = await agent.run()
    print(result)  # 或依回傳格式處理

asyncio.run(main())
```

- 安裝：`pip install browser-use uv`，再執行 `uvx browser-use install`（安裝 Chromium）。
- 環境變數：`.env` 或系統設定 `OPENAI_API_KEY`。亦可改用 `ChatAnthropic` + `ANTHROPIC_API_KEY`、`ChatGoogle` + `GOOGLE_API_KEY`。
- 參考：https://docs.browser-use.com/open-source/quickstart

## 執行流程

1. 確認或建立可執行腳本的環境：若有專案目錄則在該目錄的 **venv** 內操作；若無則先 `python -m venv venv` 並啟動（見上方「執行環境（venv）」）。
2. 在 venv 內若未安裝 `browser-use-sdk`（Cloud）或 `browser-use`（Open Source），先執行對應的 `pip install ...`。
3. 撰寫符合使用者需求的腳本（將使用者的描述轉成 `client.run("...")` 的任務文字）。
4. 在終端機用 **venv 的 Python** 執行腳本（例如啟動 venv 後 `python script.py`，或 Windows 下 `.\venv\Scripts\python script.py`），並擷取輸出。
5. 將 `result.output` 或結構化結果整理後回覆給使用者。

## 錯誤處理

- **Cloud**：若 `BROWSER_USE_API_KEY` 未設定，提醒使用者到 cloud.browser-use.com 取得並設定。
- **Open Source**：若用 OpenAI，需設定 `OPENAI_API_KEY`；其他 LLM 用對應的 Key。
- 逾時或 API 錯誤：Cloud v3 可捕獲 `TimeoutError` 與 `BrowserUseError`（`from browser_use_sdk.v3 import BrowserUseError`）。

## 參考文件

- Cloud SDK：https://docs.browser-use.com/cloud/coding-agent-quickstart  
- Cloud 完整文件：https://docs.browser-use.com/cloud/llms-full.txt  
- Open Source（用 OpenAI Key）：https://docs.browser-use.com/open-source/quickstart  

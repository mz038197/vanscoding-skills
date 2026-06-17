# Playwright 模式（Windows / 繁中版）

探索與 final 腳本**一律**用 `write_file` 寫 `.py`，再以 Shell / `exec` 執行。**禁止** Windows heredoc（`python - <<'PY'`）。

## 瀏覽器引擎

- **預設**：Chromium — `playwright.chromium.launch(headless=True)`
- **Fallback**：若出現 `ERR_HTTP2_PROTOCOL_ERROR` 或 TLS/H2 指紋阻擋，改 Firefox — `playwright.firefox.launch(headless=True)`，並執行 `playwright install firefox`

在腳本開頭可讀 `browser_engine.txt`（由 Setup 寫入）決定引擎：

```python
ENGINE = Path(os.environ.get("WORKSPACE_DIR", ".")).joinpath("browser_engine.txt")
engine = ENGINE.read_text(encoding="utf-8").strip() if ENGINE.is_file() else "chromium"
launch = playwright.chromium if engine == "chromium" else playwright.firefox
browser = await launch.launch(headless=True)
```

## 探索腳本骨架（本機 headless）

將下列內容寫入 `WORKSPACE_DIR/explore_1.py` 後執行：

```python
import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright

WORKSPACE = Path(os.environ.get("WORKSPACE_DIR", "."))
SCREENSHOTS = WORKSPACE / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()

        await page.goto("<START_URL>", wait_until="domcontentloaded")
        await page.screenshot(path=str(SCREENSHOTS / "explore_1_start.png"))

        print("URL:", page.url)
        print("TITLE:", await page.title())
        snapshot = await page.locator("body").aria_snapshot()
        print("ARIA:", snapshot)

        await browser.close()

asyncio.run(main())
```

執行（擇一）：

```powershell
$env:WORKSPACE_DIR = "outputs/<task_id>"
uv run python outputs/<task_id>/explore_1.py
```

規則：

- **一律** `viewport={"width": 1280, "height": 1800}`。
- **禁止** `page.screenshot(full_page=True)`。
- 每次 Playwright 執行為全新 session：從起始 URL 導航，在程式中重建 filter 狀態。

## 以 role + name 定位元素

```python
await page.get_by_role("button", name="Filters").click()
await asyncio.sleep(1)

panel = page.get_by_role("button", name="Filters").first.locator("..")
print(await panel.aria_snapshot())

await page.get_by_role("checkbox", name="BMW").check()
await asyncio.sleep(1)
```

drawer/dropdown 關閉後若選取狀態不可見，驗證截圖前須重開。

## 優先互動填表，少用 deep-link URL

參數化搜尋（地點、日期、filter）應**在頁面上操作控件**，而非把參數硬塞進 URL query。Deep link 易因 locale/A/B 測試失效。

互動填表要點：

- 用 `get_by_role` / `aria-label`，避免脆弱 CSS class。
- 輸入後等 suggestion listbox，再點選符合的選項。
- 日期區間等同 modal 內多欄位：modal **只開一次**，用 `Tab` 在欄位間移動。
- 填完點明確 submit，不要依賴 auto-submit。
- 擷取結果前重新讀表單狀態，assert 每個 CP。

## Final 腳本 instrumentation

`final_runs/run_<id>/final_script.py` 必須：

- 寫入 `final_runs/run_<id>/screenshots/final_execution_<step>_<action>.png`
- 每次執行前清空並追加 `final_runs/run_<id>/final_script_log.txt`
- 結尾將最終資料寫入 log

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

RUN_DIR = Path(__file__).parent
SCREENSHOTS = RUN_DIR / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)
LOG = RUN_DIR / "final_script_log.txt"
LOG.write_text("")

def log(step: int, msg: str) -> None:
    line = f"step {step} action: {msg}\n"
    LOG.open("a", encoding="utf-8").write(line)
    print(line, end="")

async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()

        await page.goto("<START_URL>", wait_until="domcontentloaded")
        await page.screenshot(path=str(SCREENSHOTS / "final_execution_1_open_start_page.png"))
        log(1, "open start page")

        final_value = "<price / code / winner>"
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"\nFINAL_RESPONSE: {final_value}\n")

        await browser.close()

asyncio.run(main())
```

## 檢查指令（Windows）

```powershell
Get-ChildItem -Recurse final_runs/run_<id>
Get-Content final_runs/run_<id>/final_script_log.txt
```

視覺檢查：**Cursor** 用 `Read` 讀 PNG；**peas-agent** 若無 vision，以 log + ARIA 為主，並在 `plan.md` 註明。

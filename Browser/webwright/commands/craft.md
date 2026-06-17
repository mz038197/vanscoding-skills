---
description: 將 Webwright 網頁任務參數化為可重用的 CLI 工具（final_script.py + argparse）。
argument-hint: <含具體數值的網頁任務描述>
---

你是 Webwright agent，處於 **CLI 工具模式**。請先讀 `SKILL.md` 與 `reference/cli_tool_mode.md`，完成 **Setup** 後，將下列任務參數化，使 `final_script.py` 日後可用不同參數重跑：

$ARGUMENTS

步驟：

1. **Identify parameters** — 找出使用者可能變更的條件；網站固定項（起始 URL、selector 策略）保持 hard-code。
2. **Write `plan.md`** — 含 `# Parameters` 表格與 `# Critical Points`；預設值須使 `python final_script.py` 無參數時重現原任務。
3. **Author `final_script.py`** — 在 `final_runs/run_<id>/`：
   - 一個可重用函式 + Google 風格 `Args:` docstring + `argparse`
   - import 時無 side effect
   - 第一行 log：`step 0 params: name=value ...`
   - headless Chromium（必要時 Firefox），viewport 1280×1800，禁止 `full_page=True`
4. **無參數重現任務** — `uv run python final_runs/run_<id>/final_script.py`
5. **Import 安全 smoke test** — 另開 process import 模組，確認不啟動瀏覽器。
6. **Self-verify** — 對照 `plan.md` 每個 CP；失敗則修正並在 `run_<id+1>/` 重跑。
7. **Show `--help`** — 執行 `--help` 並向使用者說明如何帶不同參數重跑。

完整契約見 `reference/cli_tool_mode.md`；Playwright 骨架見 `reference/playwright_patterns.md`。

---
description: 以 Webwright 一次性模式完成網頁任務（Playwright 腳本 + 截圖驗證）。
argument-hint: <自然語言網頁任務描述>
---

你是 Webwright agent。請以 code-as-action 方式完成下列網頁任務：在本機 Playwright 逐步執行，將截圖與 action log 存入 `final_runs/run_<id>/`，並驗證結果。

任務：

$ARGUMENTS

請先讀同 skill 目錄下的 `SKILL.md`，並完成 **Setup**（playwright 套件 + Chromium）。再依標準流程：

1. 選定 `WORKSPACE_DIR`，撰寫 `plan.md` 與關鍵點清單。
2. 用 scratch `.py` 探索（Windows：write_file + exec，禁止 heredoc）。
3. 在新 `final_runs/run_<id>/` 撰寫並執行 instrumented `final_script.py`（viewport 1280×1800，headless Chromium，禁止 `full_page=True`）。
4. 對照截圖與 `final_script_log.txt` 自我驗證；失敗則在 `run_<id+1>/` 重跑。
5. 向使用者報告最終資料。

詳見 `reference/playwright_patterns.md` 與 `reference/workflow.md`。**不要**使用 CLI 工具模式。

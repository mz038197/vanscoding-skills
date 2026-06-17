# 工作流程（繁中版）

Webwright 六步迴圈的詳細說明，適用 Cursor 與 peas-agent-core。原版 `image_qa` / `self_reflection` 改由 host agent 自行驗證；**不需要**額外 LLM API key。

任務開始前先完成 `SKILL.md` 的 **Setup**（`playwright` 套件 + Chromium；必要時 Firefox fallback）。

## 1. Plan

將任務拆成關鍵點（CP），寫入 `WORKSPACE_DIR/plan.md`：

```markdown
# Task
<使用者任務原文>

# Critical Points
- [ ] CP1: <約束 / filter / sort / 選取 / 必要資料>
- [ ] CP2: ...
```

CP 規則：

- 每個 CP 可獨立驗證。
- 數值、日期、數量、單位須精確。
- 排序類 CP 須對應網站實際控件。
- 若任務要求最終資料，單獨列一個 CP。

## 2. Explore

目標：找到穩定 selector、確認 filter 控件存在、規劃每個 CP 的證據來源。

- 在 `WORKSPACE_DIR/` 執行 scratch `.py`（見 `playwright_patterns.md`）。
- 探索截圖放在 `WORKSPACE_DIR/screenshots/`（與 `final_runs/` 分開）。
- 每步印 URL、title、`aria_snapshot()`。
- Cursor 可讀 PNG；peas-agent 優先 ARIA + log。
- filter 看似不存在時，先展開 drawer/accordion/行動版 filter 再判斷。
- 搜尋框不能代替專用 filter 控件。

## 3. Author `final_script.py`

建立新 `final_runs/run_<id>/`，依 `playwright_patterns.md` instrument：

- viewport 1280×1800，headless 本機 **Chromium**（必要時 Firefox），禁止 `full_page`
- 每個 CP 一張 `final_execution_<step>_<action>.png`
- 每個約束相關互動一行 `step <n> action: ...` log
- 最終資料寫入 `final_script_log.txt`

## 4. Execute

執行一次。若 crash，在同一 run 修正重跑；若截圖與修正後流程不符，刪除不一致截圖以保持乾淨執行紀錄。

## 5. Self-verify

對 `plan.md` 每個 CP：

1. 指出對應截圖和/或 log 行。
2. Cursor：讀 PNG 確認；peas-agent：優先 log + ARIA。
3. 證據須**明確**：filter chip 可見、日期精確、sort 來自網站控件、submit 已執行、最終資料可讀。
4. 僅在證據充分時勾選 CP。

失敗則診斷具體原因，修正 `final_script.py`，在 `run_<id+1>/` 重跑。若為 Chromium 指紋問題，依 Setup 切換 Firefox。

空結果集可接受，前提是 filter 已正確套用且有證據。

## 6. Done

僅當以下**全部**成立時結束：

1. `plan.md` 列出所有 CP。
2. `final_runs/run_<id>/final_script.py` 乾淨跑完，產出 log 與所有 CP 截圖。
3. 每個 CP 已勾選並引用證據。
4. 最終資料已告知使用者且存在於 `final_script_log.txt`。
5. 目錄與 log 內容符合預期。

任一不成立則繼續 diagnose → fix → 新 `run_<id+1>/`。
